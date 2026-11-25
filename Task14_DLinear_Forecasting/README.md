# Task 14 — Dự báo Nhu cầu 7 Ngày bằng Mạng Học Sâu `DLinear` (`Task14_DLinear_Forecasting`)

## 1. Mục tiêu
Tái lập cột **DLinear** trong Bảng 3 của bài báo *FreshRetailNet-50K* trên cả **3 nguồn dữ liệu lịch sử**: doanh số gốc bị che khuất (`DLinear_RawSales`), nhu cầu khôi phục bằng TimesNet (`DLinear_TimesNet` — [Task 10](../Task10_TimesNet_Recovery/README.md)) và nhu cầu khôi phục bằng DLinear (`DLinear_DLinear` — [Task 12](../Task12_DLinear_Recovery/README.md)) trên cùng **206.562** dòng `eval` không hết hàng (`stock_hour6_22_cnt == 0`).

## 2. Kết quả đối chiếu Bảng 3 (9 dòng = 3 cấu hình × 3 phân nhóm)

| Cấu hình | Phân nhóm | WAPE (%) | WPE (%) | MAE | Paper WAPE (%) | Paper WPE (%) | Delta WAPE (pp) | Delta WPE (pp) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`DLinear_RawSales`** | **Overall** (`psd >= 0`) | **31.54** | **-5.21** | 0.3932 | 31.56 | -4.89 | **-0.02** | -0.32 | completed |
| | **Low Sale** (`psd < 1`) | **39.71** | **-1.31** | 0.2781 | 39.78 | -1.03 | **-0.07** | -0.28 | completed |
| | **High Sale** (`psd >= 1`) | **25.70** | **-7.97** | 0.7310 | 25.68 | -7.63 | **+0.02** | -0.34 | completed |
| **`DLinear_TimesNet`** | **Overall** (`psd >= 0`) | **30.55** | **+6.21** | 0.3797 | 30.73 | +6.88 | **-0.18** | -0.67 | completed |
| | **Low Sale** (`psd < 1`) | **40.45** | **+11.61** | 0.2824 | 40.73 | +12.37 | **-0.28** | -0.76 | completed |
| | **High Sale** (`psd >= 1`) | **23.46** | **+2.37** | 0.6649 | 23.58 | +2.98 | **-0.12** | -0.61 | completed |
| **`DLinear_DLinear`** | **Overall** (`psd >= 0`) | **30.76** | **+4.63** | 0.3824 | 30.60 | +4.02 | **+0.16** | +0.61 | completed |
| | **Low Sale** (`psd < 1`) | **40.73** | **+10.75** | 0.2843 | – | – | – | – | completed |
| | **High Sale** (`psd >= 1`) | **23.63** | **+0.26** | 0.6700 | – | – | – | – | completed |

*(Ghi chú: Bảng 3 của bài báo gốc không in số tham chiếu cho `DLinear_DLinear` ở hai nhóm con `Low Sale` và `High Sale`, nên 4 cột tham chiếu/chênh lệch tương ứng trong CSV được để trống đúng quy ước).*

## 3. Cấu trúc thư mục bàn giao
- [Notebook đã chạy kiểm chứng](notebooks/14_dlinear_forecasting.ipynb): xác nhận SHA-256 của 4 tệp Parquet, kiểm tra bản vá, đối soát log thực thi GPU và so sánh cột `SSA` vs `DLinear`.
- [Bản vá mã nguồn tác giả](code_changes.diff): thêm `--train_path` và `--eval_path` vào `demand_forecasting/DLinear` (`8af694a`).
- [Bảng chỉ số 9 dòng chuẩn 10 cột](results/dlinear_forecasting_metrics.csv) và [metadata lượt chạy](results/run_metadata.json).
- Log thực thi: [Smoke 200 cặp](results/smoke/dlinear_smoke.log), [`DLinear_RawSales`](results/full/dlinear_raw_sales.log), [`DLinear_TimesNet`](results/full/dlinear_timesnet.log), [`DLinear_DLinear`](results/full/dlinear_dlinear.log).
- [Biên bản chạy chi tiết](run_info.md) và [Báo cáo phân tích Task 14](../reports/Task14_Report.md).
