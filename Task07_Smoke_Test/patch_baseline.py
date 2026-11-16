"""Add smoke input-path options to the pinned FRN baseline checkout."""
from pathlib import Path
from typing import List, Tuple
import sys


def patch_file(root: Path, relative: str, edits: List[Tuple[str, str]]) -> None:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    changed = False
    for old, new in edits:
        if new in text:
            continue  # idempotent for notebook reruns
        if old not in text:
            raise RuntimeError(f"Could not find expected source block in {path}: {old[:100]!r}")
        text = text.replace(old, new, 1)
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: patch_baseline.py PATH_TO_FRN_BASELINE")
    root = Path(sys.argv[1]).resolve()
    patch_file(root, "latent_demand_recovery/exp/data/generate_data.py", [
        ("def load_data(CONFIG):\n    dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n    data = dataset['train'].to_pandas()",
         "def load_data(CONFIG):\n    train_path = CONFIG.get('train_path')\n    if train_path:\n        data = pd.read_parquet(train_path)\n    else:\n        dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n        data = dataset['train'].to_pandas()")
    ])
    patch_file(root, "latent_demand_recovery/exp/app.py", [
        ("def _demand_recovery(imputation):\n    dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n    data = dataset['train'].to_pandas()",
         "def _demand_recovery(imputation, train_path=None, output_path=None):\n    if train_path:\n        data = pd.read_parquet(train_path)\n    else:\n        dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n        data = dataset['train'].to_pandas()"),
        ("data.to_parquet(f'./demand/demand.parquet')", "data.to_parquet(output_path or f'./demand/demand.parquet')"),
        ("demand_df = _demand_recovery(imputation)",
         "demand_df = _demand_recovery(imputation, CONFIG.get('train_path'), CONFIG.get('output_path'))"),
        ("    args = parser.parse_args()\n    print(args)",
         "    parser.add_argument('--train_path', type=str, default=None)\n    parser.add_argument('--output_path', type=str, default=None)\n    parser.add_argument('--epochs', type=int, default=5)\n    args = parser.parse_args()\n    print(args)"),
        ("    CONFIG['missing_rate'] = args.missing_rate\n    ## set random seed",
         "    CONFIG['missing_rate'] = args.missing_rate\n    CONFIG['train_path'] = args.train_path\n    CONFIG['output_path'] = args.output_path\n    CONFIG['EPOCHS'] = args.epochs\n    ## set random seed")
    ])
    patch_file(root, "demand_forecasting/SSA/ssa_forecasting.py", [
        ("def ssa_predict(demand_df, target_col='sale_amount'):\n    dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n    eval_df = dataset['eval'].to_pandas()",
         "def ssa_predict(demand_df, target_col='sale_amount', eval_path=None):\n    if eval_path:\n        eval_df = pd.read_parquet(eval_path)\n    else:\n        dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n        eval_df = dataset['eval'].to_pandas()"),
        ("    print(metric)\n\ndef evaluation(pdf,",
         "    print(metric)\n    return metric\n\ndef evaluation(pdf,"),
        ("    args = parser.parse_args()\n    if args.demand:",
         "    parser.add_argument('--train_path', type=str, default=None)\n    parser.add_argument('--eval_path', type=str, default=None)\n    parser.add_argument('--metrics_path', type=str, default=None)\n    args = parser.parse_args()\n    if args.demand:"),
        ("        dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n        demand_df = dataset['train'].to_pandas()\n    ssa_predict(demand_df, target_col)",
         "        if args.train_path:\n            demand_df = pd.read_parquet(args.train_path)\n        else:\n            dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n            demand_df = dataset['train'].to_pandas()\n    metric = ssa_predict(demand_df, target_col, args.eval_path)\n    if args.metrics_path:\n        metric.to_csv(args.metrics_path, index=False)")
    ])
    print(f"Applied smoke-path CLI patch to {root}")


if __name__ == "__main__":
    main()
