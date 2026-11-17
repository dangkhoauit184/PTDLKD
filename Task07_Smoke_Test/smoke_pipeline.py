from __future__ import annotations

import csv
import hashlib
import importlib
import re
import platform
import shlex
import shutil
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = Path(__file__).resolve().parent
SMOKE_DIR = TASK_DIR / "smoke"
WORK_DIR = SMOKE_DIR / "tmp"
PAIR_SEED = 2024
MODEL_SEED = 1024
EPOCHS = 1
BATCH_SIZE = 128
DATASET_ID = "Dingdong-Inc/FreshRetailNet-50K"
AUTHOR_COMMIT = "8af694a09a5a427d1d50648d348c022565a781f2"
REPO_COMMIT = "19483da785f171cb28699e3cba2ae16d6512089a"
EXPECTED_SHA256 = {
    "train": "b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96",
    "eval": "61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872",
}
KEYS = ["store_id", "product_id"]
KEY_COLS = ["store_id", "product_id", "dt"]
CANDIDATE_COLS = [
    "store_id",
    "product_id",
    "dt",
    "hours_stock_status",
    "stock_hour6_22_cnt",
    "sale_amount",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def command_text(command: list[str]) -> str:
    return shlex.join([str(part) for part in command])


def append_log(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(text.rstrip() + "\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one {label} source block; found {count}.")
    return text.replace(old, new, 1)


def write_pairs(pairs: list[tuple], path: Path) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(KEYS)
        writer.writerows(pairs)


def write_metrics(records: list[dict], statuses: dict[str, str]) -> None:
    path = TASK_DIR / "smoke_metrics.csv"
    fields = ["config_id", "group", "wape_pct", "wpe_pct", "status"]
    by_key = {(row["config_id"], row["group"]): row for row in records}
    required = [
        ("SSA_RawSales", "Overall"),
        ("SSA_TimesNet", "Overall"),
    ]
    for key in required:
        if key not in by_key:
            config_id, group = key
            by_key[key] = {
                "config_id": config_id,
                "group": group,
                "wape_pct": "",
                "wpe_pct": "",
                "status": statuses.get(config_id, "not_run"),
            }
    ordered = []
    group_order = {"Overall": 0, "Low Sale": 1, "High Sale": 2}
    for row in by_key.values():
        ordered.append(row)
    ordered.sort(
        key=lambda row: (
            0 if row["config_id"] == "SSA_RawSales" else 1,
            group_order.get(row["group"], 3),
        )
    )
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in ordered:
            writer.writerow({field: row.get(field, "") for field in fields})


def render_run_info(
    *,
    source: str,
    source_hashes: dict[str, str],
    counts: dict[str, object],
    versions: dict[str, str],
    statuses: dict[str, str],
    commands: list[str],
    errors: list[str],
    demand_hash: str = "",
) -> str:
    now = datetime.now(timezone.utc).isoformat()
    source_lines = [f"- Nguồn: {source or 'chưa xác định'}"]
    for split in ("train", "eval"):
        digest = source_hashes.get(split, "")
        source_lines.append(
            f"- SHA-256 {split}: {digest or 'chưa kiểm tra'}"
        )
    for split in ("train_smoke", "eval_smoke"):
        digest = source_hashes.get(split, "")
        if digest:
            source_lines.append(f"- SHA-256 {split}: `{digest}`")
    version_lines = [
        f"- Python: {versions.get('python', platform.python_version())}",
        f"- NumPy: {versions.get('numpy', 'chưa import được')}",
        f"- pandas: {versions.get('pandas', 'chưa import được')}",
        f"- PyArrow: {versions.get('pyarrow', 'chưa import được')}",
        f"- PyTorch/CUDA: {versions.get('torch', 'chưa import được')}",
    ]
    status_lines = [
        f"- `SSA_RawSales`: **{statuses.get('SSA_RawSales', 'not_run')}**",
        f"- `TimesNet`: **{statuses.get('TimesNet', 'not_run')}**",
        f"- `SSA_TimesNet`: **{statuses.get('SSA_TimesNet', 'not_run')}**",
    ]
    count_lines = [
        f"- Cặp đã chọn: {counts.get('pairs', 0)} / 100",
        f"- Train đã kiểm tra: {counts.get('train_rows', 0)} / 9.000 dòng; "
        f"{counts.get('train_keys', 0)} khóa duy nhất",
        f"- Eval đã kiểm tra: {counts.get('eval_rows', 0)} / 700 dòng; "
        f"{counts.get('eval_keys', 0)} khóa duy nhất",
        f"- Eval hợp lệ (`stock_hour6_22_cnt == 0`): "
        f"{counts.get('eval_valid_rows', 0)} dòng",
    ]
    command_lines = [f"- `{command}`" for command in commands] or [
        "- Chưa chạy lệnh mô hình."
    ]
    error_lines = [f"- {error.replace(chr(10), ' ')}" for error in errors] or [
        "- Không có lỗi được ghi nhận."
    ]
    return "\n".join(
        [
            "# Task 7 — Thông tin lượt chạy smoke",
            "",
            f"- Thời điểm ghi: `{now}`",
            f"- Repo baseline: `{REPO_COMMIT}`",
            f"- Mã tác giả FreshRetailNet-50K: "
            f"`{AUTHOR_COMMIT}` ([repo](https://github.com/Dingdong-Inc/frn-50k-baseline/tree/{AUTHOR_COMMIT})).",
            f"- Dataset dự phòng chính thức: `{DATASET_ID}`.",
            f"- Seed chọn cặp: `{PAIR_SEED}`.",
            f"- TimesNet: `--model TimesNet --missing_rate 0 --epochs {EPOCHS} "
            f"--batch_size {BATCH_SIZE} --seed {MODEL_SEED}`.",
            "- Eval chỉ dùng để chọn/đánh giá cặp; không dùng để huấn luyện.",
            "",
            "## Nguồn dữ liệu",
            "",
            *source_lines,
            "- Khi chọn cặp thành công, train/eval thử được ghi thành Parquet riêng "
            "và truyền đường dẫn tường minh cho TimesNet lẫn SSA.",
            "",
            "## Môi trường",
            "",
            *version_lines,
            "",
            "## Kiểm tra dữ liệu",
            "",
            *count_lines,
            "- Đầu ra nhu cầu: "
            + (
                f"`demand_timesnet_smoke.parquet`, SHA-256 `{demand_hash}`."
                if demand_hash
                else "`demand_timesnet_smoke.parquet` chưa được tạo."
            ),
            "",
            "## Trạng thái",
            "",
            *status_lines,
            "",
            "## Lệnh chạy",
            "",
            *command_lines,
            "",
            "## Lỗi / giới hạn",
            "",
            *error_lines,
            "",
            "Các CSV, Parquet và log thuộc dữ liệu/kết quả của lượt chạy; giữ ngoài Git "
            "theo `docs/Contribution_Guide.md`. Không chép kết quả smoke vào Bảng 3.",
            "",
        ]
    )


def write_final_artifacts(
    *,
    pairs: list[tuple],
    records: list[dict],
    statuses: dict[str, str],
    source: str,
    source_hashes: dict[str, str],
    counts: dict[str, object],
    versions: dict[str, str],
    commands: list[str],
    errors: list[str],
    demand_hash: str = "",
) -> None:
    write_pairs(pairs, TASK_DIR / "smoke_pairs.csv")
    write_metrics(records, statuses)
    (TASK_DIR / "run_info.md").write_text(
        render_run_info(
            source=source,
            source_hashes=source_hashes,
            counts=counts,
            versions=versions,
            statuses=statuses,
            commands=commands,
            errors=errors,
            demand_hash=demand_hash,
        ),
        encoding="utf-8",
        newline="\n",
    )


def load_runtime() -> dict:
    modules = {}
    versions = {"python": sys.version.split()[0]}
    failures = []
    for name in ("numpy", "pandas", "pyarrow", "torch"):
        try:
            module = importlib.import_module(name)
            modules[name] = module
            versions[name] = str(getattr(module, "__version__", "unknown"))
        except Exception as exc:
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
    if "torch" in modules:
        torch = modules["torch"]
        cuda = bool(torch.cuda.is_available())
        device = torch.cuda.get_device_name(0) if cuda else "CPU"
        versions["torch"] = f"{versions['torch']} ({'CUDA' if cuda else 'CPU'}: {device})"
    def version_tuple(value: str) -> tuple[int, ...]:
        parts = [int(part) for part in re.findall(r"\d+", value)[:3]]
        return tuple(parts + [0] * (3 - len(parts)))

    version_constraints = {
        "numpy": (version_tuple("1.23.5"), version_tuple("2.0.0")),
        "pandas": (version_tuple("1.5.3"), version_tuple("3.0.0")),
        "pyarrow": (version_tuple("12.0.0"), None),
        "torch": (version_tuple("2.0.1"), None),
    }
    for name, (minimum, maximum) in version_constraints.items():
        if name not in modules:
            continue
        observed = version_tuple(versions[name])
        if observed < minimum or (maximum is not None and observed >= maximum):
            failures.append(
                f"{name} {versions[name]} is outside the Task 3 supported range."
            )
    if failures:
        raise RuntimeError("Required imports failed: " + "; ".join(failures))
    return modules | {"versions": versions}


def load_source(modules: dict) -> tuple[str, dict, object, object, bool]:
    import pandas as pd
    import pyarrow.dataset as ds
    import pyarrow.parquet as pq

    local_paths = {
        "train": ROOT / "train.parquet",
        "eval": ROOT / "eval.parquet",
    }
    source_hashes = {}
    if all(path.is_file() for path in local_paths.values()):
        for split, path in local_paths.items():
            observed = sha256_file(path)
            if observed != EXPECTED_SHA256[split]:
                raise ValueError(
                    f"{path} hash {observed} does not match the Task 6 reference "
                    f"{EXPECTED_SHA256[split]}."
                )
            source_hashes[split] = observed
        return (
            "Task 6 Parquet in project root (SHA-256 verified)",
            source_hashes,
            local_paths,
            ds,
            True,
        )
    from datasets import load_dataset

    dataset = load_dataset(DATASET_ID)
    return (
        f"Hugging Face `{DATASET_ID}` (`train` and `eval` splits)",
        source_hashes,
        dataset,
        pq,
        False,
    )


def pair_key_frame(frame):
    import pandas as pd

    return pd.MultiIndex.from_frame(frame[KEYS])


def scan_candidate_summaries(source_data, is_local, ds, np):
    def has_outage(value) -> bool:
        status = np.asarray(value)
        if status.shape != (24,):
            return False
        return bool(np.nansum(status[6:22]) > 0)

    train_summary = {}
    eval_summary = {}
    pair_days = {}
    for split in ("train", "eval"):
        for frame in iter_source_frames(
            source_data, split, is_local, CANDIDATE_COLS, ds
        ):
            frame["dt"] = frame["dt"].astype(str)
            if split == "train":
                frame["_outage"] = frame["hours_stock_status"].map(has_outage)
                grouped = frame.groupby(KEYS, sort=False).agg(
                    rows=("dt", "size"), outage=("_outage", "any")
                )
                for (store_id, product_id), row in grouped.iterrows():
                    summary = train_summary.setdefault((store_id, product_id), [0, False])
                    summary[0] += int(row["rows"])
                    summary[1] = summary[1] or bool(row["outage"])
            else:
                valid = frame["stock_hour6_22_cnt"].eq(0)
                positive = valid & frame["sale_amount"].gt(0)
                frame["_valid"] = valid
                frame["_valid_positive"] = positive
                grouped = frame.groupby(KEYS, sort=False).agg(
                    rows=("dt", "size"),
                    valid_rows=("_valid", "sum"),
                    valid_positive=("_valid_positive", "sum"),
                )
                for (store_id, product_id), row in grouped.iterrows():
                    pair = (store_id, product_id)
                    summary = eval_summary.setdefault(pair, [0, 0, 0])
                    summary[0] += int(row["rows"])
                    summary[1] += int(row["valid_rows"])
                    summary[2] += int(row["valid_positive"])
                for store_id, product_id, dt in frame.loc[
                    positive, KEYS + ["dt"]
                ].itertuples(index=False, name=None):
                    pair_days.setdefault((store_id, product_id), set()).add(dt)

    eligible = [
        pair
        for pair, (train_rows, outage) in train_summary.items()
        if train_rows == 90
        and outage
        and pair in eval_summary
        and eval_summary[pair][0] == 7
        and eval_summary[pair][1] > 0
        and eval_summary[pair][2] > 0
    ]
    eligible.sort()
    if len(eligible) < 100:
        raise ValueError(
            f"Only {len(eligible)} eligible store-product pairs; 100 are required."
        )
    return eligible, pair_days


def choose_pairs(eligible, pair_days, np):
    rng = np.random.default_rng(PAIR_SEED)
    order = [eligible[int(i)] for i in rng.permutation(len(eligible))]
    selected = []
    covered_days = set()
    for pair in order:
        new_days = pair_days.get(pair, set()) - covered_days
        if new_days:
            selected.append(pair)
            covered_days.update(new_days)
        if len(covered_days) == 7:
            break
    if len(covered_days) != 7:
        raise ValueError(
            "Could not select pairs with positive eligible eval sales on all seven days."
        )
    selected_set = set(selected)
    for pair in order:
        if len(selected) == 100:
            break
        if pair not in selected_set:
            selected.append(pair)
            selected_set.add(pair)
    return selected


def iter_source_frames(source_data, split, is_local, columns, ds):
    import pandas as pd

    if is_local:
        dataset = ds.dataset(str(source_data[split]), format="parquet")
        scanner = dataset.scanner(columns=columns, batch_size=65536)
        for batch in scanner.to_batches():
            yield batch.to_pandas()
        return
    for batch in source_data[split].iter(batch_size=65536):
        yield pd.DataFrame({name: batch[name] for name in columns})


def read_selected(source_data, split, pairs, is_local, ds):
    import pandas as pd

    if is_local:
        expression = None
        for store_id, product_id in pairs:
            term = (ds.field("store_id") == store_id) & (
                ds.field("product_id") == product_id
            )
            expression = term if expression is None else expression | term
        dataset = ds.dataset(str(source_data[split]), format="parquet")
        batches = dataset.scanner(filter=expression, batch_size=65536).to_batches()
        frames = [batch.to_pandas() for batch in batches]
        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True)

    index = pd.MultiIndex.from_tuples(pairs, names=KEYS)
    frames = []
    for batch in source_data[split].iter(batch_size=65536):
        frame = pd.DataFrame(batch)
        mask = pair_key_frame(frame).isin(index)
        if mask.any():
            frames.append(frame.loc[mask])
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def validate_sample(train_df, eval_df, pairs):
    import numpy as np
    import pandas as pd

    train_df = train_df.sort_values(KEY_COLS).reset_index(drop=True)
    eval_df = eval_df.sort_values(KEY_COLS).reset_index(drop=True)
    if len(pairs) != 100 or len(set(pairs)) != 100:
        raise ValueError("Selected pair list is not exactly 100 unique pairs.")
    if len(train_df) != 9000 or len(eval_df) != 700:
        raise ValueError(
            f"Expected 9000/700 rows; observed {len(train_df)}/{len(eval_df)}."
        )
    for name, frame, days in (("train", train_df, 90), ("eval", eval_df, 7)):
        if frame.duplicated(KEY_COLS).any():
            raise ValueError(f"{name} contains duplicate store-product-date keys.")
        pair_days = frame.groupby(KEYS)["dt"].nunique()
        pair_rows = frame.groupby(KEYS).size()
        if len(pair_days) != 100 or not pair_days.eq(days).all() or not pair_rows.eq(days).all():
            raise ValueError(f"{name} does not contain exactly {days} unique days per pair.")
        observed_pairs = set(pair_key_frame(frame).unique().tolist())
        if observed_pairs != set(pairs):
            raise ValueError(f"{name} pair keys do not match smoke_pairs.csv.")
    if int(eval_df["stock_hour6_22_cnt"].eq(0).sum()) < 1:
        raise ValueError("Eval has no valid stock_hour6_22_cnt == 0 row.")
    if not np.isfinite(eval_df.loc[eval_df["stock_hour6_22_cnt"].eq(0), "sale_amount"]).all():
        raise ValueError("Eligible eval sale_amount contains non-finite values.")
    eligible = eval_df.loc[eval_df["stock_hour6_22_cnt"].eq(0)]
    if eligible["sale_amount"].sum() <= 0 or eligible.groupby("dt")["sale_amount"].sum().le(0).any():
        raise ValueError("Overall SSA WAPE needs positive eligible sales on every eval day.")
    return train_df, eval_df


def prepare_author_source() -> tuple[Path, Path, Path]:
    baseline = WORK_DIR / "author-source"
    if not baseline.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--no-checkout",
                "https://github.com/Dingdong-Inc/frn-50k-baseline.git",
                str(baseline),
            ],
            check=True,
        )
    current = git_output("rev-parse", "HEAD", cwd=baseline)
    if current != AUTHOR_COMMIT:
        subprocess.run(
            ["git", "fetch", "--depth", "1", "origin", AUTHOR_COMMIT],
            cwd=str(baseline),
            check=True,
        )
        subprocess.run(
            ["git", "checkout", "--detach", AUTHOR_COMMIT],
            cwd=str(baseline),
            check=True,
        )
    actual = git_output("rev-parse", "HEAD", cwd=baseline)
    if actual != AUTHOR_COMMIT:
        raise RuntimeError(f"Author source commit mismatch: {actual}")

    runtime_root = WORK_DIR / "runtime"
    if runtime_root.exists():
        shutil.rmtree(runtime_root)
    runtime_root.mkdir(parents=True)
    shutil.copytree(
        baseline / "latent_demand_recovery",
        runtime_root / "latent_demand_recovery",
    )
    return (
        baseline,
        runtime_root,
        runtime_root / "latent_demand_recovery" / "exp",
    )


def patch_timesnet(runtime_root: Path, exp_dir: Path) -> Path:
    data_path = exp_dir / "data" / "generate_data.py"
    data_text = data_path.read_text(encoding="utf-8")
    data_text = replace_once(
        data_text,
        '    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")\n'
        "    data = dataset['train'].to_pandas()\n",
        '    data = pd.read_parquet(CONFIG["train_path"])\n',
        "TimesNet load_data dataset read",
    )
    data_path.write_text(data_text, encoding="utf-8", newline="\n")

    app_path = exp_dir / "app.py"
    app_text = app_path.read_text(encoding="utf-8")
    app_text = replace_once(
        app_text,
        "def _demand_recovery(imputation):\n"
        '    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")\n'
        "    data = dataset['train'].to_pandas()\n",
        "def _demand_recovery(imputation, CONFIG):\n"
        '    data = pd.read_parquet(CONFIG["train_path"])\n',
        "TimesNet _demand_recovery dataset read",
    )
    app_text = replace_once(
        app_text,
        "    data.to_parquet(f'./demand/demand.parquet')\n",
        '    data.to_parquet(CONFIG["demand_path"], index=False)\n',
        "TimesNet demand output path",
    )
    app_text = replace_once(
        app_text,
        "        demand_df = _demand_recovery(imputation)\n",
        "        demand_df = _demand_recovery(imputation, CONFIG)\n",
        "TimesNet recovery call",
    )
    app_text = replace_once(
        app_text,
        "    args = parser.parse_args()\n",
        '    parser.add_argument("--train_path", required=True)\n'
        '    parser.add_argument("--demand_path", required=True)\n'
        '    parser.add_argument("--epochs", type=int, default=1)\n'
        '    parser.add_argument("--batch_size", type=int, default=128)\n'
        '    parser.add_argument("--seed", type=int, default=1024)\n'
        "    args = parser.parse_args()\n",
        "TimesNet smoke CLI arguments",
    )
    app_text = replace_once(
        app_text,
        "    CONFIG['missing_rate'] = args.missing_rate\n",
        "    CONFIG['missing_rate'] = args.missing_rate\n"
        "    CONFIG['train_path'] = args.train_path\n"
        "    CONFIG['demand_path'] = args.demand_path\n"
        "    CONFIG['EPOCHS'] = args.epochs\n"
        "    CONFIG['batch_size'] = args.batch_size\n",
        "TimesNet smoke config",
    )
    app_text = replace_once(
        app_text,
        "    set_seed(seed_value=1024)\n",
        "    set_seed(seed_value=args.seed)\n",
        "TimesNet smoke seed",
    )
    app_path.write_text(app_text, encoding="utf-8", newline="\n")
    return app_path


def patch_ssa(source_path: Path, patched_path: Path) -> Path:
    text = source_path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "def ssa_predict(demand_df, target_col='sale_amount'):\n"
        '    dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")\n'
        "    eval_df = dataset['eval'].to_pandas()\n",
        "def ssa_predict(demand_df, target_col='sale_amount', eval_df=None):\n"
        "    if eval_df is None:\n"
        '        dataset = load_dataset("Dingdong-Inc/FreshRetailNet-50K")\n'
        "        eval_df = dataset['eval'].to_pandas()\n",
        "SSA explicit eval path",
    )
    text = replace_once(
        text,
        "    print(metric)\n",
        "    print(metric)\n    return metric\n",
        "SSA metric return",
    )
    main_at = text.find("if __name__ == '__main__':")
    if main_at < 0:
        raise RuntimeError("Pinned SSA source has no CLI entry point.")
    text = text[:main_at] + """if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_path")
    parser.add_argument("--eval_path", required=True)
    parser.add_argument("--metrics_path", required=True)
    parser.add_argument(
        "--demand_path",
        default='../../latent_demand_recovery/exp/demand/demand.parquet',
    )
    parser.add_argument("--demand", action='store_true')
    args = parser.parse_args()
    if args.demand:
        target_col = 'sale_amount_pred'
        demand_df = pd.read_parquet(args.demand_path)
    else:
        if not args.train_path:
            parser.error("--train_path is required unless --demand is set")
        target_col = 'sale_amount'
        demand_df = pd.read_parquet(args.train_path)
    eval_df = pd.read_parquet(args.eval_path)
    metric = ssa_predict(demand_df, target_col, eval_df=eval_df)
    metric.to_csv(args.metrics_path, index=False)
"""
    patched_path.parent.mkdir(parents=True, exist_ok=True)
    patched_path.write_text(text, encoding="utf-8", newline="\n")
    return patched_path


def run_logged(command: list[str], cwd: Path, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(f"$ {command_text(command)}\n")
        stream.flush()
        result = subprocess.run(
            command,
            cwd=str(cwd),
            stdout=stream,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        stream.write(f"\nexit_code={result.returncode}\n")
    if result.returncode:
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}: "
            f"{command_text(command)}"
        )


def metric_records(config_id: str, frame, train_df, eval_df) -> list[dict]:
    import numpy as np

    labels = {
        "psd>=0": "Overall",
        "psd<1": "Low Sale",
        "psd>=1": "High Sale",
    }
    psd = train_df.groupby(KEYS, as_index=False)["sale_amount"].mean()
    psd = psd.rename(columns={"sale_amount": "psd"})
    eligible = eval_df.loc[eval_df["stock_hour6_22_cnt"].eq(0)].merge(
        psd, on=KEYS, how="left", validate="many_to_one"
    )
    result = []
    for condition, label in labels.items():
        if condition == "psd>=0":
            group_rows = eligible.loc[eligible["psd"] >= 0]
        elif condition == "psd<1":
            group_rows = eligible.loc[eligible["psd"] < 1]
        else:
            group_rows = eligible.loc[eligible["psd"] >= 1]
        source_row = frame.loc[frame["group"].eq(condition)]
        if group_rows.empty:
            result.append(
                {
                    "config_id": config_id,
                    "group": label,
                    "wape_pct": "",
                    "wpe_pct": "",
                    "status": "no_valid_rows",
                }
            )
            continue
        if source_row.empty:
            result.append(
                {
                    "config_id": config_id,
                    "group": label,
                    "wape_pct": "",
                    "wpe_pct": "",
                    "status": "failed",
                    "_finite": False,
                }
            )
            continue
        row = source_row.iloc[0]
        wape = float(row["wape"])
        wpe = float(row["wpe"])
        finite = np.isfinite(wape) and np.isfinite(wpe)
        result.append(
            {
                "config_id": config_id,
                "group": label,
                "wape_pct": wape * 100 if finite else "",
                "wpe_pct": wpe * 100 if finite else "",
                "status": "completed" if finite else "failed",
                "_finite": finite,
            }
        )
    return result


def group_diagnostics(train_df, eval_df) -> str:
    psd = train_df.groupby(KEYS, as_index=False)["sale_amount"].mean()
    psd = psd.rename(columns={"sale_amount": "psd"})
    eligible = eval_df.loc[eval_df["stock_hour6_22_cnt"].eq(0)].merge(
        psd, on=KEYS, how="left", validate="many_to_one"
    )
    lines = ["Eval diagnostic rows (stock_hour6_22_cnt == 0):"]
    for label, condition in (
        ("Overall", eligible["psd"] >= 0),
        ("Low Sale", eligible["psd"] < 1),
        ("High Sale", eligible["psd"] >= 1),
    ):
        subset = eligible.loc[condition]
        lines.append(
            f"{label}: rows={len(subset)}, target_sum={subset['sale_amount'].sum()}, "
            f"days={subset['dt'].nunique()}"
        )
    return "\n".join(lines)


def run_pipeline() -> int:
    TASK_DIR.mkdir(parents=True, exist_ok=True)
    SMOKE_DIR.mkdir(parents=True, exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    for filename in ("ssa_raw.log", "timesnet.log", "ssa_timesnet.log"):
        (SMOKE_DIR / filename).write_text(
            "Task 7 smoke execution has not started.\n",
            encoding="utf-8",
            newline="\n",
        )

    statuses = {
        "SSA_RawSales": "not_run",
        "TimesNet": "not_run",
        "SSA_TimesNet": "not_run",
    }
    records = []
    pairs = []
    source = ""
    source_hashes = {}
    counts = {
        "pairs": 0,
        "train_rows": 0,
        "train_keys": 0,
        "eval_rows": 0,
        "eval_keys": 0,
        "eval_valid_rows": 0,
    }
    versions = {"python": sys.version.split()[0]}
    commands = []
    errors = []
    demand_hash = ""
    train_smoke = None
    eval_smoke = None

    try:
        runtime = load_runtime()
        versions.update(runtime["versions"])
        np = runtime["numpy"]
        import pandas as pd

        source, source_hashes, source_data, ds, is_local = load_source(runtime)
        eligible, pair_days = scan_candidate_summaries(
            source_data, is_local, ds, np
        )
        pairs = choose_pairs(eligible, pair_days, np)
        train_smoke = read_selected(
            source_data, "train", pairs, is_local, ds
        )
        eval_smoke = read_selected(
            source_data, "eval", pairs, is_local, ds
        )
        train_smoke, eval_smoke = validate_sample(train_smoke, eval_smoke, pairs)
        counts.update(
            {
                "pairs": len(pairs),
                "train_rows": len(train_smoke),
                "train_keys": int(train_smoke[KEY_COLS].drop_duplicates().shape[0]),
                "eval_rows": len(eval_smoke),
                "eval_keys": int(eval_smoke[KEY_COLS].drop_duplicates().shape[0]),
                "eval_valid_rows": int(
                    eval_smoke["stock_hour6_22_cnt"].eq(0).sum()
                ),
            }
        )
        write_pairs(pairs, TASK_DIR / "smoke_pairs.csv")
        input_dir = WORK_DIR / "inputs"
        input_dir.mkdir(parents=True, exist_ok=True)
        train_path = input_dir / "train_smoke.parquet"
        eval_path = input_dir / "eval_smoke.parquet"
        train_smoke.to_parquet(train_path, engine="pyarrow", index=False)
        eval_smoke.to_parquet(eval_path, engine="pyarrow", index=False)
        train_sha = sha256_file(train_path)
        eval_sha = sha256_file(eval_path)
        source_hashes["train_smoke"] = train_sha
        source_hashes["eval_smoke"] = eval_sha
        append_log(
            SMOKE_DIR / "ssa_raw.log",
            f"Data source: {source}\n"
            f"train_path={train_path} sha256={train_sha} rows={len(train_smoke)}\n"
            f"eval_path={eval_path} sha256={eval_sha} rows={len(eval_smoke)}\n"
            f"pairs={len(pairs)} eval_valid_rows={counts['eval_valid_rows']}\n"
            f"{group_diagnostics(train_smoke, eval_smoke)}",
        )
    except Exception as exc:
        errors.append(f"Data/preflight: {type(exc).__name__}: {exc}")
        for log_name in ("ssa_raw.log", "timesnet.log", "ssa_timesnet.log"):
            append_log(
                SMOKE_DIR / log_name,
                f"NOT_RUN: data/runtime precondition failed: "
                f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}",
            )
        write_final_artifacts(
            pairs=pairs,
            records=records,
            statuses=statuses,
            source=source,
            source_hashes=source_hashes,
            counts=counts,
            versions=versions,
            commands=commands,
            errors=errors,
        )
        print(errors[-1], file=sys.stderr)
        return 1

    try:
        baseline, runtime_root, exp_dir = prepare_author_source()
        author_sha = git_output("rev-parse", "HEAD", cwd=baseline)
        ssa_source = baseline / "demand_forecasting" / "SSA" / "ssa_forecasting.py"
        ssa_script = patch_ssa(ssa_source, WORK_DIR / "ssa_forecasting_smoke.py")
        raw_metrics_path = WORK_DIR / "ssa_raw_metrics.csv"
        raw_command = [
            sys.executable,
            str(ssa_script),
            "--train_path",
            str(train_path),
            "--eval_path",
            str(eval_path),
            "--metrics_path",
            str(raw_metrics_path),
        ]
        commands.append(command_text(raw_command))
        append_log(
            SMOKE_DIR / "ssa_raw.log",
            f"Author source commit: {author_sha}\n{group_diagnostics(train_smoke, eval_smoke)}",
        )
        run_logged(raw_command, ssa_script.parent, SMOKE_DIR / "ssa_raw.log")
        raw_frame = pd.read_csv(raw_metrics_path)
        raw_records = metric_records(
            "SSA_RawSales", raw_frame, train_smoke, eval_smoke
        )
        overall = next(row for row in raw_records if row["group"] == "Overall")
        if not overall.get("_finite", False):
            raise RuntimeError(
                "SSA_RawSales Overall has no finite WAPE/WPE. "
                + group_diagnostics(train_smoke, eval_smoke)
            )
        records.extend(
            {key: value for key, value in row.items() if not key.startswith("_")}
            for row in raw_records
        )
        statuses["SSA_RawSales"] = "completed"
    except Exception as exc:
        statuses["SSA_RawSales"] = "failed"
        errors.append(f"SSA_RawSales: {type(exc).__name__}: {exc}")
        append_log(
            SMOKE_DIR / "ssa_raw.log",
            f"FAILED: {type(exc).__name__}: {exc}\n{traceback.format_exc()}",
        )

    if statuses["SSA_RawSales"] == "completed":
        demand_path = TASK_DIR / "demand_timesnet_smoke.parquet"
        output_preexisted = demand_path.exists()
        try:
            if output_preexisted:
                raise FileExistsError(
                    "demand_timesnet_smoke.parquet already exists; move it aside "
                    "before rerunning to avoid overwriting user data."
                )
            baseline, runtime_root, exp_dir = prepare_author_source()
            app_path = patch_timesnet(runtime_root, exp_dir)
            model_command = [
                sys.executable,
                str(app_path),
                "--model",
                "TimesNet",
                "--missing_rate",
                "0",
                "--train_path",
                str(train_path),
                "--demand_path",
                str(demand_path),
                "--epochs",
                str(EPOCHS),
                "--batch_size",
                str(BATCH_SIZE),
                "--seed",
                str(MODEL_SEED),
            ]
            commands.append(command_text(model_command))
            log_path = SMOKE_DIR / "timesnet.log"
            append_log(
                log_path,
                f"Author source commit: {git_output('rev-parse', 'HEAD', cwd=baseline)}\n"
                f"load_data train_path={train_path}\n"
                f"_demand_recovery train_path={train_path}\n"
                f"demand_path={demand_path}\n"
                f"missing_rate=0 epochs={EPOCHS} batch_size={BATCH_SIZE} "
                f"seed={MODEL_SEED}\n",
            )
            run_logged(model_command, exp_dir, log_path)
            generated = pd.read_parquet(demand_path, engine="pyarrow")
            generated = generated.sort_values(KEY_COLS).reset_index(drop=True)
            expected = train_smoke.sort_values(KEY_COLS).reset_index(drop=True)
            if len(generated) != 9000 or generated.duplicated(KEY_COLS).any():
                raise ValueError("Demand output does not have 9000 unique train keys.")
            if not generated[KEY_COLS].equals(expected[KEY_COLS]):
                raise ValueError("Demand output keys/order differ from the smoke train.")
            pred = generated["sale_amount_pred"].to_numpy(dtype=float)
            if not np.isfinite(pred).all() or (pred < 0).any():
                raise ValueError("sale_amount_pred is non-finite or negative.")
            if not np.array_equal(
                generated["sale_amount"].to_numpy(),
                expected["sale_amount"].to_numpy(),
                equal_nan=True,
            ):
                raise ValueError("Demand output source sale_amount changed.")
            counts["demand_rows"] = len(generated)
            counts["demand_keys"] = int(generated[KEY_COLS].drop_duplicates().shape[0])
            demand_hash = sha256_file(demand_path)
            statuses["TimesNet"] = "completed"
        except Exception as exc:
            statuses["TimesNet"] = "not_run" if isinstance(
                exc, (ImportError, ModuleNotFoundError, OSError, MemoryError)
            ) else "failed"
            errors.append(f"TimesNet: {type(exc).__name__}: {exc}")
            append_log(
                SMOKE_DIR / "timesnet.log",
                f"{statuses['TimesNet'].upper()}: {type(exc).__name__}: {exc}\n"
                f"{traceback.format_exc()}",
            )
            if not output_preexisted and demand_path.exists():
                demand_path.unlink()
        finally:
            runtime_root = WORK_DIR / "runtime"
            if runtime_root.exists():
                shutil.rmtree(runtime_root)
    else:
        append_log(
            SMOKE_DIR / "timesnet.log",
            "NOT_RUN: SSA_RawSales did not complete successfully.\n",
        )

    if statuses["TimesNet"] == "completed":
        try:
            ssa_script = WORK_DIR / "ssa_forecasting_smoke.py"
            demand_path = TASK_DIR / "demand_timesnet_smoke.parquet"
            demand_metrics_path = WORK_DIR / "ssa_timesnet_metrics.csv"
            demand_command = [
                sys.executable,
                str(ssa_script),
                "--demand",
                "--demand_path",
                str(demand_path),
                "--eval_path",
                str(eval_path),
                "--metrics_path",
                str(demand_metrics_path),
            ]
            commands.append(command_text(demand_command))
            append_log(
                SMOKE_DIR / "ssa_timesnet.log",
                f"train_path/demand_path={demand_path} sha256={demand_hash}\n"
                f"eval_path={eval_path} sha256={sha256_file(eval_path)} rows=700\n"
                f"{group_diagnostics(train_smoke, eval_smoke)}",
            )
            run_logged(
                demand_command,
                ssa_script.parent,
                SMOKE_DIR / "ssa_timesnet.log",
            )
            demand_frame = pd.read_csv(demand_metrics_path)
            demand_records = metric_records(
                "SSA_TimesNet", demand_frame, train_smoke, eval_smoke
            )
            overall = next(
                row for row in demand_records if row["group"] == "Overall"
            )
            if not overall.get("_finite", False):
                raise RuntimeError(
                    "SSA_TimesNet Overall has no finite WAPE/WPE. "
                    + group_diagnostics(train_smoke, eval_smoke)
                )
            records.extend(
                {key: value for key, value in row.items() if not key.startswith("_")}
                for row in demand_records
            )
            statuses["SSA_TimesNet"] = "completed"
        except Exception as exc:
            statuses["SSA_TimesNet"] = "failed"
            errors.append(f"SSA_TimesNet: {type(exc).__name__}: {exc}")
            append_log(
                SMOKE_DIR / "ssa_timesnet.log",
                f"FAILED: {type(exc).__name__}: {exc}\n{traceback.format_exc()}",
            )
    else:
        append_log(
            SMOKE_DIR / "ssa_timesnet.log",
            "NOT_RUN: demand recovery did not complete successfully.\n",
        )

    write_final_artifacts(
        pairs=pairs,
        records=records,
        statuses=statuses,
        source=source,
        source_hashes=source_hashes,
        counts=counts,
        versions=versions,
        commands=commands,
        errors=errors,
        demand_hash=demand_hash,
    )
    return 0 if all(value == "completed" for value in statuses.values()) else 1


if __name__ == "__main__":
    raise SystemExit(run_pipeline())
