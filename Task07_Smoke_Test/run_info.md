# Task 7 smoke run

Completed at runtime: 2026-11-21 23:40:32.473517

- Pair seed: 20261116; selected pairs: 100
- Train rows: 9000; eval rows: 700
- Eligibility: exactly 90 train rows and 7 eval rows per pair; >=1 train stockout; >=1 eval row with stock_hour6_22_cnt == 0.
- TimesNet: model=TimesNet, missing_rate=0, epochs=2 (reduced from default 5), patience=1 (reduced from default 5 to satisfy patience < epochs), seed=1024 from baseline.
- SSA raw and recovered demand: both used the same filtered train/eval files.
- Outputs are smoke results and must not be copied into Table 3.
