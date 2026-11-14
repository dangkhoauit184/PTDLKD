# Thông tin chạy thực nghiệm — Task 8 (SSA_RawSales)

- **Mã cấu hình:** `SSA_RawSales`
- **Thư mục thực thi gốc:** `demand_forecasting/SSA`
- **Câu lệnh tham chiếu:** `python ssa_forecasting.py` (chế độ mặc định, không bật cờ `--demand`)
- **Dữ liệu Train:** `/content/drive/MyDrive/PTLDKD/data/train.parquet` (4.500.000 dòng, 50.000 cặp, 90 ngày: `2024-03-28` → `2024-06-25`)
- **Dữ liệu Eval:** `/content/drive/MyDrive/PTLDKD/data/eval.parquet` (350.000 dòng, 50.000 cặp, 7 ngày: `2024-06-26` → `2024-07-02`)
- **Điều kiện lọc đánh giá:** `stock_hour6_22_cnt == 0` (206.562 dòng hợp lệ)
- **Quy tắc phân nhóm:** `psd = mean(sale_amount)` trên tập train (`Overall: psd >= 0`, `Low Sale: psd < 1`, `High Sale: psd >= 1`)
- **Đường dẫn log:** `results/full/ssa_raw_sales.log`
- **Đường dẫn metrics:** `results/ssa_raw_sales_metrics.csv`