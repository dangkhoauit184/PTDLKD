# Task 10 — Run Info (TimesNet Latent Demand Recovery)

- **Thời điểm hoàn tất (UTC):** 2026-11-20T15:30:56.214935+00:00
- **Người thực hiện:** TV5
- **Môi trường chạy:** Google Colab | GPU: `NVIDIA L4` | Python `3.13.16` | PyTorch `2.14.1+cu130` | NumPy `2.4.6` | pandas `2.2.3`
- **Repo nhóm đối chiếu:** nhánh `feature/task10-timesnet-recovery` (từ commit nền `cedd08f` trên `main`)
- **Mã tác giả đối chiếu (`frn-50k-baseline`):** commit `8af694a09a5a427d1d50648d348c022565a781f2`
- **Thay đổi mã nguồn trên bản sao:** Xem [code_changes.diff](code_changes.diff) (đồng bộ đọc `train.parquet` local + sắp xếp `['store_id', 'product_id', 'dt']` cho cả `load_data` và `_demand_recovery`, đặt seed `2024`).

## Lệnh chạy chính thức
```bash
cd latent_demand_recovery/exp
FRN_LOCAL_TRAIN_PARQUET=/content/frn_cache/train.parquet python -u app.py --model TimesNet --missing_rate 0
```

## Cấu hình thực tế
- **Model:** `TimesNet`
- **Missing rate:** `0.0` (chỉ khôi phục tại giờ hết hàng thực tế; `valid_idx.sum() == 0`; không tạo điểm thiếu nhân tạo; không dùng tập `eval`)
- **Seed thực dùng:** `2024` — Chạy theo kế hoạch Task 2 (đã sửa `set_seed(seed_value=2024)` trong bản sao `app.py`, xem `code_changes.diff`).
- **Siêu tham số baseline:** `epochs=5`, `batch_size=128`, `lr=0.001`, `weight_decay=1e-5`, `patience=5`, `n_layers=2`, `d_model=64`, `d_ffn=32`, `top_k=7`, `n_kernels=5`, `dropout=0.0`, `apply_nonstationary_norm=True`, `OT=1`
- **Dữ liệu đầu vào:** `train.parquet` (`4.500.000` dòng × `19` cột, SHA-256: `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96` — khớp Task 6)
- **Đầu vào TimesNet:** `(150000, 480, 6)` — 6 đặc trưng (`hours_sale`, `discount`, `holiday_flag`, `precpt`, `avg_temperature`, `hour_index/15`), mỗi cặp 90 ngày chia 3 đoạn × 30 ngày × 16 giờ (`6..21`).
- **Thời gian chạy:** `84.66` phút

## Kết quả chính
- **Decoupling score (Raw Sales — `sale_amount`):** `-0.566447` (bài báo Bảng 2: `-0.57`)
- **Decoupling score (TimesNet — `sale_amount_pred`):** `0.069918` (bài báo Bảng 2: `0.07`)
- **Bảng điểm tách rời:** [results/decoupling_metrics.csv](results/decoupling_metrics.csv)
- **Log đầy đủ:** [results/full/timesnet_recovery.log](results/full/timesnet_recovery.log)
- **Đối soát file nhu cầu:** Xem [results/demand_file_check.csv](results/demand_file_check.csv) (`4.500.000` dòng × `20` cột, tất cả số đếm lỗi = `0`) và [results/run_metadata.json](results/run_metadata.json).

## Liên kết tệp lớn trên Google Drive (mở quyền cho Task 11)
- **File chính `demand_timesnet.parquet`** (`81,562,029` bytes | SHA-256: `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694`):
  - Đường dẫn Drive: `/content/drive/MyDrive/PTDLKD/Task10_TimesNet_Recovery/full/demand_timesnet.parquet`
  - Link chia sẻ Drive: https://drive.google.com/file/d/1f9db-U9f9C9OFS-V2EcmQv4FIU3bguR3/view?usp=sharing
- **Checkpoint TimesNet (`save/TimesNet/`):**
  - Đường dẫn Drive: `/content/drive/MyDrive/PTDLKD/Task10_TimesNet_Recovery/full/checkpoint_TimesNet`
  - Link chia sẻ Drive: https://drive.google.com/drive/folders/18D53nPab5toFuyuAQ00rRBrG_86WKKkR?usp=drive_link
- **Mảng ước lượng theo giờ & thứ tự khóa:** `TimesNet_imputation_0.0.npy` + `key_order.parquet` (sắp xếp tăng dần theo `store_id`, `product_id`, `dt`) nằm trong cùng thư mục `full/`.
