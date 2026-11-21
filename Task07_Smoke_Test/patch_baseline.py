"""Patch the pinned FreshRetailNet baseline for filtered smoke Parquets."""
from pathlib import Path
from typing import List, Tuple
import sys

SAFE_DATASET_IMPORT = (
    "from datasets import load_dataset",
    "try:\n    from datasets import load_dataset\nexcept ImportError:\n    load_dataset = None",
)


def replace_once(text: str, old: str, new: str, path: Path) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Expected source block missing in {path}: {old[:100]!r}")
    return text.replace(old, new, 1)


def patch_file(root: Path, relative: str, edits: List[Tuple[str, str]]) -> None:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in edits:
        text = replace_once(text, old, new, path)
    if text != original:
        path.write_text(text, encoding="utf-8")


def add_cli_options(path: Path, flags: List[str], options: str, anchor: str) -> None:
    text = path.read_text(encoding="utf-8")
    present = [flag in text for flag in flags]
    if all(present):
        return
    if any(present):
        raise RuntimeError(f"Partial smoke CLI options already exist in {path}; inspect before patching.")
    if anchor not in text:
        raise RuntimeError(f"CLI insertion point missing in {path}")
    path.write_text(text.replace(anchor, options + anchor, 1), encoding="utf-8")


def set_smoke_module(path: Path, expected_marker: str, content: str) -> None:
    current = path.read_text(encoding="utf-8")
    if content.strip() in current:
        return
    if expected_marker not in current:
        raise RuntimeError(f"Unexpected module content; refusing to replace {path}")
    path.write_text(content, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: patch_baseline.py PATH_TO_FRN_BASELINE")
    root = Path(sys.argv[1]).resolve()

    generator = "latent_demand_recovery/exp/data/generate_data.py"
    app = "latent_demand_recovery/exp/app.py"
    ssa = "demand_forecasting/SSA/ssa_forecasting.py"
    for relative in (generator, app, ssa):
        patch_file(root, relative, [SAFE_DATASET_IMPORT])

    patch_file(root, generator, [
        ("def load_data(CONFIG):\n    dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n    data = dataset['train'].to_pandas()",
         "def load_data(CONFIG):\n    train_path = CONFIG.get('train_path')\n    if train_path:\n        data = pd.read_parquet(train_path)\n    else:\n        dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n        data = dataset['train'].to_pandas()")
    ])

    patch_file(root, app, [
        ("def _demand_recovery(imputation):\n    dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n    data = dataset['train'].to_pandas()",
         "def _demand_recovery(imputation, train_path=None, output_path=None):\n    if train_path:\n        data = pd.read_parquet(train_path)\n    else:\n        dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n        data = dataset['train'].to_pandas()"),
        ("data.to_parquet(f'./demand/demand.parquet')", "data.to_parquet(output_path or f'./demand/demand.parquet')"),
        ("demand_df = _demand_recovery(imputation)",
         "demand_df = _demand_recovery(imputation, CONFIG.get('train_path'), CONFIG.get('output_path'))"),
        ("    CONFIG['missing_rate'] = args.missing_rate\n    ## set random seed",
         "    CONFIG['missing_rate'] = args.missing_rate\n    CONFIG['train_path'] = args.train_path\n    CONFIG['output_path'] = args.output_path\n    CONFIG['EPOCHS'] = args.epochs\n    CONFIG['patience'] = min(CONFIG['patience'], args.epochs - 1)\n    ## set random seed")
    ])
    add_cli_options(root / app, ['--train_path', '--output_path', '--epochs'],
                    "    parser.add_argument('--train_path', type=str, default=None)\n"
                    "    parser.add_argument('--output_path', type=str, default=None)\n"
                    "    parser.add_argument('--epochs', type=int, default=5)\n",
                    "    args = parser.parse_args()\n")

    patch_file(root, ssa, [
        ("def ssa_predict(demand_df, target_col='sale_amount'):\n    dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n    eval_df = dataset['eval'].to_pandas()",
         "def ssa_predict(demand_df, target_col='sale_amount', eval_path=None):\n    if eval_path:\n        eval_df = pd.read_parquet(eval_path)\n    else:\n        dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n        eval_df = dataset['eval'].to_pandas()"),
        ("    print(metric)\n\ndef evaluation(pdf,",
         "    print(metric)\n    return metric\n\ndef evaluation(pdf,"),
        ("        dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n        demand_df = dataset['train'].to_pandas()\n    ssa_predict(demand_df, target_col)",
         "        if args.train_path:\n            demand_df = pd.read_parquet(args.train_path)\n        else:\n            dataset = load_dataset(\"Dingdong-Inc/FreshRetailNet-50K\")\n            demand_df = dataset['train'].to_pandas()\n    metric = ssa_predict(demand_df, target_col, args.eval_path)\n    if args.metrics_path:\n        metric.to_csv(args.metrics_path, index=False)")
    ])
    add_cli_options(root / ssa, ['--train_path', '--eval_path', '--metrics_path'],
                    "    parser.add_argument('--train_path', type=str, default=None)\n"
                    "    parser.add_argument('--eval_path', type=str, default=None)\n"
                    "    parser.add_argument('--metrics_path', type=str, default=None)\n",
                    "    args = parser.parse_args()\n")

    # Import only TimesNet in this smoke clone. The upstream package initializer
    # eagerly imports every model family, which also imports unrelated sklearn/tsdb
    # native extensions. This does not change the TimesNet implementation.
    set_smoke_module(root / "latent_demand_recovery/pypots/__init__.py",
                     "from . import imputation, optim, utils",
                     '"""Smoke-only package root; avoid eagerly loading unrelated families."""\n')
    set_smoke_module(root / "latent_demand_recovery/pypots/imputation/__init__.py",
                     "from .brits import BRITS",
                     '"""Expose TimesNet only for the isolated smoke run."""\nfrom .timesnet import TimesNet\n__all__ = ["TimesNet"]\n')
    set_smoke_module(root / "latent_demand_recovery/pypots/data/__init__.py",
                     "from .generating import",
                     '"""Expose only dataset classes needed by the TimesNet smoke run."""\n'
                     'from .dataset import BaseDataset, SUPPORTED_DATASET_FILE_FORMATS\n'
                     '__all__ = ["BaseDataset", "SUPPORTED_DATASET_FILE_FORMATS"]\n')
    set_smoke_module(root / "latent_demand_recovery/pypots/utils/metrics/__init__.py",
                     "from .classification import",
                     "from .error import calc_mae, calc_mse, calc_rmse, calc_mre, calc_reg_focal, calc_mbe\n"
                     "__all__ = ['calc_mae', 'calc_mse', 'calc_rmse', 'calc_mre', 'calc_reg_focal', 'calc_mbe']\n")
    set_smoke_module(root / "latent_demand_recovery/pypots/utils/logging.py",
                     "from tsdb.utils.logging import Logger",
                     'import logging\nlogger = logging.getLogger("PyPOTS running log")\n')
    # TimesNet imports SAITS' dataset helpers, which only need these two
    # tensor operations. The upstream pygrinder initializer eagerly imports
    # tsdb/sklearn native extensions that may be unavailable on Windows.
    pygrinder_stub = root / "latent_demand_recovery/exp/pygrinder.py"
    pygrinder_stub.write_text(
        '"""Minimal smoke-only tensor helpers used by the TimesNet dataset."""\n'
        'import torch\n'
        'def mcar(X, p=0.2):\n'
        '    if p <= 0: return X\n'
        '    mask = torch.rand_like(X) < p\n'
        '    return X.masked_fill(mask, float("nan"))\n'
        'def fill_and_get_mask_torch(X):\n'
        '    mask = (~torch.isnan(X)).to(torch.float32)\n'
        '    return torch.nan_to_num(X, nan=0.0), mask\n', encoding="utf-8"
    )
    patch_file(root, "latent_demand_recovery/exp/model/models.py", [
        ("from pypots.imputation import DLinear, TimesNet, PatchTST, SAITS, BRITS, ETSformer, Autoformer, Informer, Transformer, iTransformer, GPVAE, CSDI, ImputeFormer",
         "from pypots.imputation import TimesNet"),
        ("from pypots.utils.metrics import calc_mae, calc_mse, calc_rmse, calc_mre, calc_reg_focal, calc_mbe",
         "from pypots.utils.metrics import calc_mae"),
    ])
    print(f"Smoke-path options ready in {root}")


if __name__ == "__main__":
    main()
