"""Task 12 runner: khôi phục nhu cầu bằng DLinear với mã gốc của tác giả (frn-50k-baseline @ 8af694a).

Kế thừa nguyên runner Task 9 (đã chạy được trên Colab 12,7 GB RAM): mô hình, `mimic_missing`,
`set_seed`, `_imputation` (fit/predict, chặn âm np.where(imputation > 0, imputation, 0)) và
`evaluation_decoupling` dùng nguyên mã tác giả. Viết lại để tiết kiệm RAM, giữ nguyên công thức:
  - load_data, evaluation_mnar: như Task 9 (đọc train.parquet local, X float32, norm_val (n, 1, 6)).
  - _demand_recovery (chỉ chạy khi --missing_rate 0): đọc train.parquet local thay vì Hugging Face,
    chỉ thay lát giờ 6..21 tại đúng các giờ hết hàng bằng giá trị khôi phục, giữ nguyên 8 giờ đêm
    ([0:6], [22:24]) và các giờ quan sát được, cộng đủ 24 giờ thành sale_amount_pred; giữ nguyên
    hours_sale và sale_amount gốc trong Parquet xuất ra (19 cột gốc + sale_amount_pred).
Với --verify_equivalence (chỉ dùng cho tập nhỏ), script so bản viết lại với bản gốc của tác giả
trên cùng dữ liệu, cùng seed và dừng nếu kết quả khác nhau.
"""
import argparse, contextlib, gc, io, json, os, sys, time

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

ap = argparse.ArgumentParser()
ap.add_argument('--author_exp', required=True, help='.../frn-50k-baseline/latent_demand_recovery/exp')
ap.add_argument('--data_path', required=True, help='train.parquet')
ap.add_argument('--work_dir', required=True, help='thư mục chạy (checkpoint, imputation .npy)')
ap.add_argument('--model', default='DLinear')
ap.add_argument('--missing_rate', type=float, default=0.3)
ap.add_argument('--seed', type=int, default=1024)
ap.add_argument('--epochs', type=int, default=5)
ap.add_argument('--batch_size', type=int, default=128)
ap.add_argument('--pairs', type=int, default=0, help='0 = toàn bộ; >0 = chỉ lấy N cặp đầu (chạy thử)')
ap.add_argument('--saving_path', default=None, help='thư mục lưu checkpoint (mặc định work_dir/save)')
ap.add_argument('--resume_ckpt', default=None,
                help='file .pypots đã huấn luyện: bỏ qua fit, nạp checkpoint rồi predict + evaluation_mnar')
ap.add_argument('--out_parquet', default=None,
                help='nơi ghi demand parquet khi missing_rate = 0 (mặc định work_dir/demand/demand.parquet)')
ap.add_argument('--verify_equivalence', action='store_true',
                help='so bản gốc và bản viết lại của load_data/evaluation_mnar (chỉ dùng cho tập nhỏ)')
args = ap.parse_args()
args.work_dir = os.path.abspath(args.work_dir)
args.saving_path = os.path.abspath(args.saving_path) if args.saving_path else None
args.resume_ckpt = os.path.abspath(args.resume_ckpt) if args.resume_ckpt else None
args.out_parquet = os.path.abspath(args.out_parquet) if args.out_parquet else None


def ram_gb():
    try:
        import psutil
        return psutil.Process().memory_info().rss / 1024 ** 3
    except Exception:
        return float('nan')


SCALAR = ['store_id', 'product_id', 'dt', 'sale_amount', 'discount', 'holiday_flag',
          'precpt', 'avg_temperature', 'stock_hour6_22_cnt']
LISTS = ['hours_sale', 'hours_stock_status']


def read_train(path, n_pairs):
    """Đọc train, sắp xếp theo (store_id, product_id, dt) như mã tác giả."""
    df = pq.read_table(path, columns=SCALAR).to_pandas()
    mats = {}
    for col in LISTS:
        arr = pq.read_table(path, columns=[col]).column(col).combine_chunks()
        lens = pc.list_value_length(arr).to_numpy(zero_copy_only=False)
        if not (lens == 24).all():
            raise ValueError(f'{col}: có dòng không đủ 24 giờ')
        mats[col] = arr.flatten().to_numpy(zero_copy_only=False).reshape(-1, 24)
        del arr
    order = np.lexsort((pd.to_datetime(df['dt']).to_numpy(),
                        df['product_id'].to_numpy(), df['store_id'].to_numpy()))
    df = df.iloc[order].reset_index(drop=True)
    for col in LISTS:
        mats[col] = mats[col][order]
    rows = order                              # vị trí dòng trong file gốc, theo thứ tự đã sắp xếp
    if n_pairs > 0:
        key = df['store_id'].astype(np.int64) * 1_000_000 + df['product_id'].astype(np.int64)
        keep = key.isin(pd.unique(key)[:n_pairs]).to_numpy()
        df = df[keep].reset_index(drop=True)
        for col in LISTS:
            mats[col] = mats[col][keep]
        rows = rows[keep]
    size = df.groupby(['store_id', 'product_id']).size()
    if not (size == 90).all() or len(df) != len(size) * 90:
        raise ValueError('Có cặp không đủ 90 ngày train')
    if not np.isin(mats['hours_stock_status'], [0, 1]).all():
        raise ValueError('hours_stock_status có giá trị khác 0/1')
    mats['hours_stock_status'] = mats['hours_stock_status'].astype(np.int8)   # chỉ so sánh == 1 và cộng
    gc.collect()
    return df, mats, int(len(size)), rows


t_start = time.time()
TRAIN, MATS, N_PAIRS, FILE_ROWS = read_train(args.data_path, args.pairs)
SERIES_NUM = len(TRAIN) // 90
STOCK_POINTS = int(MATS['hours_stock_status'][:, 6:22].sum())
print(f'[task12] data_path={args.data_path}', flush=True)
print(f'[task12] train_rows={len(TRAIN)} pairs={N_PAIRS} '
      f'dt_min={TRAIN["dt"].min()} dt_max={TRAIN["dt"].max()} '
      f'stockout_points_6_21={STOCK_POINTS} ram_gb={ram_gb():.1f}', flush=True)

exp_dir = os.path.abspath(args.author_exp)
sys.path[:0] = [exp_dir, os.path.dirname(exp_dir)]   # exp/ (data, model) và pypots đi kèm repo
os.makedirs(args.work_dir, exist_ok=True)
os.chdir(args.work_dir)                                # app.py ghi ./demand/ và ./save/ vào đây

import data.generate_data as gd      # noqa: E402
import app                           # noqa: E402
import pypots, torch                 # noqa: E402
print(f'[task12] pypots_path={os.path.dirname(pypots.__file__)} torch={torch.__version__} '
      f'cuda={torch.cuda.is_available()} '
      f'gpu={torch.cuda.get_device_name(0) if torch.cuda.is_available() else "none"}', flush=True)

ORIG_LOAD_DATA = app.load_data
ORIG_EVAL_MNAR = app.evaluation_mnar
ORIG_DEMAND_RECOVERY = app._demand_recovery


def load_data_lowmem(CONFIG):
    """Cùng phép tính với generate_data.load_data của tác giả, ít tốn RAM hơn."""
    hours_sale_full = MATS['hours_sale']
    hours_stock_status = MATS['hours_stock_status']
    hours_sale_origin = hours_sale_full.reshape(SERIES_NUM * 3, 30, 24)[..., 6:22]
    hours_stock_status = hours_stock_status.reshape(SERIES_NUM * 3, 30, 24)[..., 6:22]
    hours_sale = np.where(hours_stock_status == 1, np.nan, hours_sale_origin)
    covariate = TRAIN[['discount', 'holiday_flag', 'precpt', 'avg_temperature']].values.reshape(SERIES_NUM * 3, 30, 4)
    covariate = covariate / (covariate.max(axis=1, keepdims=True) + 0.1)

    hours_sale, valid_idx = gd.mimic_missing(hours_sale, p=CONFIG['missing_rate'],
                                             max_missing_patch=7, min_missing_patch=3)

    # Tác giả: concat [doanh số, 4 biến ngoại sinh, giờ/15] ở float64 rồi pypots đổi sang float32.
    # Ở đây cấp phát thẳng mảng float32 và điền từng kênh -> cùng giá trị đầu vào mô hình.
    X = np.empty(hours_sale.shape + (6,), dtype=np.float32)
    X[..., 0] = hours_sale
    X[..., 1:5] = covariate[:, :, None, :]
    X[..., 5] = np.arange(16) / 15
    del hours_sale
    X = X.reshape(-1, 30 * 16, 6)
    valid_idx = valid_idx.reshape(-1, 30 * 16, 1)
    print(valid_idx.sum())
    hours_sale_origin = hours_sale_origin.reshape(-1, 30 * 16, 1)
    # pypots tự tạo norm_val = np.ones(X.shape) ở float64 (3,5 GB) rồi copy sang float32 (1,7 GB) mỗi lần
    # tạo dataset -> hết RAM ngay khi bắt đầu predict. Truyền sẵn norm_val toàn số 1 dạng (n, 1, 6):
    # mô hình nhân dec_out * norm_val theo broadcast nên kết quả y hệt (nhân với 1), chỉ tốn 3,6 MB.
    norm_val = np.ones((X.shape[0], 1, X.shape[-1]), dtype=np.float32)
    out = {
        'train_set': {'X': X, 'norm_val': norm_val},
        'ts_origin': hours_sale_origin,
        'valid_idx': valid_idx,
        'params': {'n_steps': 30 * 16, 'n_features': 6, 'patch_len': 16, 'OT': 1},
    }
    n_total = int(X[..., 0].size)
    n_nan = int(np.isnan(X[..., 0]).sum())
    n_art = int(valid_idx.sum())
    n_stock = n_nan - n_art
    print(f'[task12] n_samples={X.shape[0]} n_points_6_21={n_total} '
          f'stockout_points={n_stock} (khớp dữ liệu: {n_stock == STOCK_POINTS}) '
          f'artificially_masked={n_art} actual_mask_ratio={n_art / (n_total - n_stock):.6f} '
          f'ram_gb={ram_gb():.1f}', flush=True)
    gc.collect()
    return out


def evaluation_mnar_lowmem(X, imputation):
    """Cùng công thức với app.evaluation_mnar của tác giả, dùng mảng đã nạp sẵn."""
    hours_sale_origin = MATS['hours_sale'].reshape(SERIES_NUM * 3, 30, 24)
    stock_hour_X = np.isnan(X[..., 0].reshape(-1, 30, 16)).sum(axis=-1).reshape(-1, 90).reshape(-1)
    stock_hour_origin = MATS['hours_stock_status'][:, 6:22].sum(axis=1)
    hours_sale_impute = hours_sale_origin.copy()
    hours_sale_impute[..., 6:22] = imputation.reshape(-1, 30, 16)
    sale_amount_pred = hours_sale_impute.sum(axis=-1).reshape(-1, 90).reshape(-1)
    valid_idx = (stock_hour_X > 0) & (stock_hour_origin == 0)
    sale_amount = TRAIN['sale_amount'].values
    print('wape', (np.abs(sale_amount_pred - sale_amount) * valid_idx).sum() / (sale_amount * valid_idx).sum())
    print('wpe', ((sale_amount_pred - sale_amount) * valid_idx).sum() / (sale_amount * valid_idx).sum())
    print(f'[task12] eval_days={int(valid_idx.sum())} ram_gb={ram_gb():.1f}', flush=True)


DECOUPLING_COLS = ['city_id', 'store_id', 'product_id', 'dt', 'holiday_flag', 'discount',
                   'sale_amount', 'stock_hour6_22_cnt']


def recovered_daily_demand(imputation):
    """sale_amount_pred: thay giờ 6..21 tại đúng các giờ hết hàng bằng giá trị khôi phục, giữ nguyên
    8 giờ đêm và các giờ quan sát được, rồi cộng đủ 24 giờ (cùng công thức _demand_recovery của tác giả)."""
    if not (imputation >= 0).all():
        raise ValueError('imputation có giá trị âm (lẽ ra _imputation đã chặn âm)')
    hours = MATS['hours_sale'].astype(np.float64).reshape(SERIES_NUM * 3, 30, 24)   # bản sao, MATS giữ nguyên
    stock = MATS['hours_stock_status'].reshape(SERIES_NUM * 3, 30, 24)[..., 6:22] == 1
    business = hours[..., 6:22]                          # view vào lát giờ kinh doanh 6..21
    business[stock] = imputation.reshape(-1, 30, 16)[stock]
    return hours.sum(axis=-1).reshape(-1), int(stock.sum())


def demand_recovery_lowmem(imputation):
    """Thay app._demand_recovery: đọc train.parquet local, ghi Parquet 19 cột gốc + sale_amount_pred."""
    pred, n_replaced = recovered_daily_demand(imputation)
    table = pq.read_table(args.data_path).take(pa.array(FILE_ROWS))    # cùng thứ tự (store_id, product_id, dt)
    for col in ['store_id', 'product_id', 'dt']:
        if not np.array_equal(table.column(col).to_numpy(zero_copy_only=False), TRAIN[col].to_numpy()):
            raise ValueError(f'Thứ tự khóa {col} của Parquet xuất ra không khớp dữ liệu đã nạp')
    table = table.append_column('sale_amount_pred', pa.array(pred, type=pa.float64()))
    out = args.out_parquet or os.path.join(args.work_dir, 'demand', 'demand.parquet')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pq.write_table(table, out)
    df = table.select(DECOUPLING_COLS + ['sale_amount_pred']).to_pandas()
    n_rows, n_cols = table.num_rows, table.num_columns
    del table
    gc.collect()
    print(f'[task12] demand_written path={out} rows={n_rows} cols={n_cols} '
          f'replaced_stockout_hours={n_replaced} (khớp dữ liệu: {n_replaced == STOCK_POINTS}) '
          f'pred_min={pred.min():.6f} pred_mean={pred.mean():.6f} ram_gb={ram_gb():.1f}', flush=True)
    return df


def verify_recovery_equivalence(CONFIG, X):
    """So sale_amount_pred của bản viết lại với _demand_recovery gốc của tác giả (cùng imputation)."""
    rng = np.random.default_rng(1)
    observed = X[..., :1]
    # Giống đầu ra mô hình: giờ quan sát giữ nguyên X (float32), giờ hết hàng là giá trị khôi phục.
    imp = np.where(np.isnan(observed), rng.random(observed.shape) * 0.5, observed).astype(np.float32)
    pred_new, _ = recovered_daily_demand(imp)
    tmp = os.path.join(args.work_dir, '_verify_recovery')
    os.makedirs(tmp, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(tmp)                                   # bản gốc ghi ./demand/demand.parquet -> để riêng chỗ khác
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            ref = ORIG_DEMAND_RECOVERY(imp)
    finally:
        os.chdir(cwd)
    same_keys = all(np.array_equal(ref[c].to_numpy(), TRAIN[c].to_numpy()) for c in ['store_id', 'product_id', 'dt'])
    diff = float(np.abs(ref['sale_amount_pred'].to_numpy() - pred_new).max())
    # Chênh lệch duy nhất được phép: tác giả ghi đè cả lát 6..21 bằng X float32 ở giờ quan sát,
    # bản viết lại giữ nguyên giá trị float64 gốc -> chỉ lệch do làm tròn float32.
    ok = same_keys and diff < 1e-4
    print(f'[task12] recovery_equivalence keys={same_keys} max_abs_diff_sale_amount_pred={diff:.3e} '
          f'recovery_equivalence_ok={ok}', flush=True)
    if not ok:
        raise SystemExit('Bản viết lại _demand_recovery KHÔNG trùng bản gốc – dừng, không huấn luyện.')


def verify_equivalence(CONFIG):
    """So bản gốc của tác giả với bản viết lại trên cùng dữ liệu, cùng seed."""
    df_hf = TRAIN.copy()                     # giả lập dataset['train'].to_pandas() của Hugging Face
    for col in LISTS:
        obj = np.empty(len(df_hf), dtype=object)
        m = MATS[col].astype(np.int64) if col == 'hours_stock_status' else MATS[col]
        for i in range(len(df_hf)):
            obj[i] = m[i]
        df_hf[col] = obj

    class _Split:
        def to_pandas(self):
            return df_hf.sample(frac=1, random_state=0)   # xáo trộn: tác giả tự sort lại

    fake_hf = lambda *a, **k: {'train': _Split()}
    gd.load_dataset = fake_hf
    app.load_dataset = fake_hf
    quiet = io.StringIO
    with contextlib.redirect_stdout(quiet()):
        app.set_seed(seed_value=args.seed)
        ref = ORIG_LOAD_DATA(CONFIG)
        app.set_seed(seed_value=args.seed)
        new = load_data_lowmem(CONFIG)
    same_X = np.array_equal(ref['train_set']['X'].astype(np.float32), new['train_set']['X'], equal_nan=True)
    same_mask = np.array_equal(ref['valid_idx'], new['valid_idx'])
    same_origin = np.array_equal(ref['ts_origin'], new['ts_origin'])
    rng = np.random.default_rng(0)
    imp = (rng.random(new['train_set']['X'].shape[:2] + (1,)) * 0.3).astype(np.float32)
    buf_ref, buf_new = quiet(), quiet()
    with contextlib.redirect_stdout(buf_ref):
        ORIG_EVAL_MNAR(ref['train_set']['X'], imp)
    with contextlib.redirect_stdout(buf_new):
        evaluation_mnar_lowmem(new['train_set']['X'], imp)
    lines_ref = [l for l in buf_ref.getvalue().splitlines() if l.startswith('wape') or l.startswith('wpe')]
    lines_new = [l for l in buf_new.getvalue().splitlines() if l.startswith('wape') or l.startswith('wpe')]
    same_eval = lines_ref == lines_new and len(lines_ref) == 2
    ok = same_X and same_mask and same_origin and same_eval
    print(f'[task12] equivalence X={same_X} valid_idx={same_mask} ts_origin={same_origin} '
          f'evaluation_mnar={same_eval} ({lines_ref} vs {lines_new}) equivalence_ok={ok}', flush=True)
    if ok and CONFIG['missing_rate'] == 0:
        verify_recovery_equivalence(CONFIG, new['train_set']['X'])
    gd.load_dataset = app.load_dataset = None
    del df_hf, ref, new
    gc.collect()
    if not ok:
        raise SystemExit('Bản viết lại KHÔNG trùng bản gốc – dừng, không huấn luyện.')


app.load_data = load_data_lowmem
app.evaluation_mnar = evaluation_mnar_lowmem
app._demand_recovery = demand_recovery_lowmem

app.CONFIG.update({
    'model': args.model,
    'missing_rate': args.missing_rate,
    'EPOCHS': args.epochs,
    'batch_size': args.batch_size,
    'saving_path': args.saving_path or os.path.join(args.work_dir, 'save'),
})
print('[task12] CONFIG ' + json.dumps(app.CONFIG, ensure_ascii=False), flush=True)
print(f'[task12] seed={args.seed}', flush=True)

if args.verify_equivalence:
    verify_equivalence(app.CONFIG)

_orig_load_model = app.load_model


def load_model_logged(CONFIG):
    m = _orig_load_model(CONFIG)
    _orig_fit, _orig_predict = m.fit, m.predict

    def fit_logged(*a, **k):
        print(f'[task12] fit_start ram_gb={ram_gb():.1f}', flush=True)
        if args.resume_ckpt:
            # Tiếp tục sau khi bị ngắt: giữ nguyên _imputation của tác giả, thay huấn luyện bằng nạp checkpoint.
            # set_seed trước load_data như CLI gốc -> cùng mặt nạ thiếu như lượt đã huấn luyện.
            loaded = torch.load(args.resume_ckpt, map_location=m.device, weights_only=False)
            state = loaded.state_dict() if isinstance(loaded, torch.nn.Module) else loaded.model.state_dict()
            m.model.load_state_dict(state)
            print(f'[task12] resumed_from_checkpoint={args.resume_ckpt} (bỏ qua huấn luyện)', flush=True)
        else:
            _orig_fit(*a, **k)
        print(f'[task12] fit_end ram_gb={ram_gb():.1f}', flush=True)

    def predict_logged(*a, **k):
        print(f'[task12] predict_start ram_gb={ram_gb():.1f}', flush=True)
        res = _orig_predict(*a, **k)
        print(f'[task12] predict_end shape={res["imputation"].shape} ram_gb={ram_gb():.1f}', flush=True)
        return res

    m.fit, m.predict = fit_logged, predict_logged
    return m


app.load_model = load_model_logged

app.set_seed(seed_value=args.seed)   # như CLI gốc: set_seed rồi demand_recovery
app.demand_recovery(app.CONFIG)      # >0: _imputation -> evaluation_mnar (wape, wpe); =0: _demand_recovery -> evaluation_decoupling
print(f'[task12] finished elapsed_sec={time.time() - t_start:.0f} ram_gb={ram_gb():.1f}', flush=True)
