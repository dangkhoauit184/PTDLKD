# Thông tin chạy thực nghiệm — Task 11 (SSA_TimesNet)

- **Mã cấu hình:** `SSA_TimesNet`
- **Thư mục thực thi:** `Task11_SSA_TimesNet/`
- **Dữ liệu Train (Khôi phục TimesNet từ Task 10):**
  - Tên tệp: `demand_timesnet.parquet` (4.500.000 dòng × 20 cột, 81.562.029 bytes)
  - SHA-256: `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694`
  - Cột đặc trưng lịch sử đưa vào SSA: `sale_amount_pred`
- **Dữ liệu Eval (từ Task 6):**
  - Tên tệp: `eval.parquet` (350.000 dòng, 50.000 cặp)
  - SHA-256: `678caca15afed20239f2ea79208856fe18dad17fd444472c7d7e930edfa685bd`
  - Cột đối chiếu đánh giá (Ground Truth): `sale_amount`
- **Điều kiện lọc đánh giá:** `stock_hour6_22_cnt == 0` (`eligible_eval_rows = 206562`, `Low Sale = 153208`, `High Sale = 53354`)
- **Quy tắc phân nhóm:** `psd = mean(sale_amount)` tính trên doanh số gốc của tập train (`Overall: psd >= 0`, `Low Sale: psd < 1`, `High Sale: psd >= 1`)
- **Tệp đầu ra bàn giao:**
  - `results/ssa_timesnet_metrics.csv`
  - `results/ssa_raw_vs_timesnet_comparison.csv`
  - `results/full/ssa_timesnet.log`
  - `results/run_metadata.json`