# Thông tin chạy Task 8 — SSA_RawSales

**Cách tái lập kết quả trong repo:** mở [notebook](notebooks/08_ssa_raw_sales.ipynb), đặt `data_dir` trỏ tới hai Parquet của Task 6, rồi chạy tất cả các ô theo thứ tự. Kết quả bàn giao xuất từ notebook. `python ssa_forecasting.py` là lệnh tham chiếu trong [mã tác giả](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/SSA/ssa_forecasting.py), không phải lệnh đã dùng cho lượt kiểm chứng này.

## Đầu vào và thiết lập

| Tập | File | Số dòng | Khoảng ngày |
|---|---|---:|---|
| Train | `train.parquet` | 4.500.000 | 28/03–25/06/2024 |
| Eval | `eval.parquet` | 350.000 | 26/06–02/07/2024 |

Cả hai tập có cùng 50.000 cặp cửa hàng–sản phẩm. SHA-256 của từng file được kiểm tra với [biên bản Task 6](../Task06_Data_Preparation/results/20261113T082302850933Z/run_info.md) và ghi vào [run_metadata.json](results/run_metadata.json). Notebook không tải lại hoặc ghi đè dữ liệu.

- **Lượt kiểm chứng đã lưu:** Windows CPU, Python 3.12.14, NumPy 2.3.5, pandas 3.0.1, PyArrow 26.0.1. Các số trong lượt này khớp với log đã merge của Task 8.
- **Đánh giá:** chỉ dùng 206.562 dòng eval có `stock_hour6_22_cnt == 0`. Tính từng chỉ số theo ngày rồi lấy trung bình qua 7 ngày.
- **Phân nhóm:** `psd` là doanh số ngày gốc trung bình trên train của từng cặp. Overall: `psd >= 0`; Low Sale: `psd < 1`; High Sale: `psd >= 1`.
- **Mã tham chiếu:** `Dingdong-Inc/frn-50k-baseline` tại `8af694a`. Công thức trọng số, quy tắc lịch, ngưỡng nhóm và cách tính chỉ số được giữ nguyên. Notebook chỉ kiểm tra đầu vào, lỗi đánh giá và bàn giao kết quả. SSA không dùng seed hoặc checkpoint huấn luyện.

## File kết quả

- [CSV ba nhóm](results/ssa_raw_sales_metrics.csv): cột `_pct` là phần trăm; `_pp` là điểm phần trăm, bằng số thực chạy trừ số bài báo.
- [Log](results/full/ssa_raw_sales.log): WAPE và WPE ở dạng tỷ lệ. MAE giống đơn vị ở cả CSV và log.
- [Metadata](results/run_metadata.json): thông tin môi trường, SHA-256, số dòng đầu vào và số dòng eval đủ điều kiện.
