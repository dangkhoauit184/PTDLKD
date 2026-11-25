# Báo cáo Task 14 - DLinear Forecasting

## Tóm tắt

Task 14 đã chạy thành công cả ba cấu hình DLinear:

- `DLinear_RawSales`
- `DLinear_TimesNet`
- `DLinear_DLinear`

File `demand_dlinear.parquet` đã được tìm thấy ngoài workspace, đối chiếu đúng SHA-256 và sao chép vào thư mục Task 14.

## Thay đổi mã nguồn

- `Exp_Main.data_organization` đọc trực tiếp `train.parquet` và `eval.parquet` thay vì Hugging Face.
- Thêm `--train_path` và `--eval_path`.
- Giữ nguyên cách truyền `--revin False`; Python argparse vẫn chuyển chuỗi `"False"` thành `True`.
- Giữ `--des` riêng cho từng cấu hình.

## Kết quả

Bảng chi tiết nằm tại [dlinear_forecasting_metrics.csv](../Task14_DLinear_Forecasting/results/dlinear_forecasting_metrics.csv).

- RawSales Overall: WAPE `31.5419%`, WPE `-5.2075%`.
- TimesNet Overall: WAPE `30.5450%`, WPE `+6.2130%`.
- Tổng mẫu `psd>=0`: `206562`.
- `DLinear_DLinear` Overall: WAPE `30.7643%`, WPE `+4.6253%`.
- CSV có 9 dòng completed: 3 cấu hình × 3 nhóm.
