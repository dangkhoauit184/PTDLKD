# Task 7 smoke run status

Status: `not_run` — the local execution environment could not load PyTorch/NumPy native extensions installed in the writable workspace (blocked by Windows Application Control). This is not a completed smoke test.

Prepared: notebook, pinned author baseline reference, and an idempotent patch script so `load_data`, `_demand_recovery`, and SSA raw/recovered evaluation accept the same filtered train/eval Parquets.

Run settings configured in the notebook: 100 eligible pairs (seed 20261116), train/eval rows 9,000/700, TimesNet `--missing_rate 0 --epochs 1` (baseline default 5 epochs), SSA evaluation on the same 700 eval rows. No finite metrics, pair sample, or TimesNet Parquet were generated locally. The notebook writes these artifacts after successful runs. Do not use smoke metrics in Table 3.
