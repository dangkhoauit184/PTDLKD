# Task 11 — Dự báo SSA trên dữ liệu khôi phục TimesNet (`SSA_TimesNet`)

## 1. Mục tiêu
Chạy mô hình thống kê Similar Scenario Average (SSA) trên lịch sử nhu cầu đã khôi phục bằng TimesNet (`sale_amount_pred` từ Task 10) và lập bảng đối chiếu trực tiếp với `SSA_RawSales` (Task 8) cùng cột SSA của Bảng 3 bài báo *FreshRetailNet-50K*.

## 2. Bảng đối chiếu kết quả (`SSA_RawSales` vs `SSA_TimesNet`)
| Phân nhóm | Cấu hình | WAPE (%) | WPE (%) | MAE | Paper WAPE (%) | Paper WPE (%) | Delta WAPE (pp) | Delta WPE (pp) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** (`psd >= 0`) | `SSA_RawSales` (Task 8) | 31.97 | -10.50 | 0.3982 | 31.97 | -10.50 | 0.00 | 0.00 | completed |
| **Overall** (`psd >= 0`) | `SSA_TimesNet` (Task 11) | 29.79 | 1.40 | 0.3709 | 29.79 | 1.39 | 0.00 | 0.01 | completed |
| **Low Sale** (`psd < 1`) | `SSA_RawSales` (Task 8) | 38.33 | -8.03 | 0.2691 | 38.33 | -8.03 | 0.00 | 0.00 | completed |
| **Low Sale** (`psd < 1`) | `SSA_TimesNet` (Task 11) | 37.87 | 4.96 | 0.2656 | 37.87 | 4.89 | 0.00 | 0.07 | completed |
| **High Sale** (`psd >= 1`) | `SSA_RawSales` (Task 8) | 27.40 | -12.26 | 0.7761 | 27.40 | -12.26 | 0.00 | 0.00 | completed |
| **High Sale** (`psd >= 1`) | `SSA_TimesNet` (Task 11) | 23.98 | -1.15 | 0.6790 | 23.98 | -1.12 | 0.00 | -0.03 | completed |

## 3. Cấu trúc thư mục
- `notebooks/11_ssa_timesnet.ipynb`: Notebook chạy thực nghiệm trên Google Colab.
- `results/ssa_timesnet_metrics.csv`: Chỉ số 3 phân nhóm của `SSA_TimesNet`.
- `results/ssa_raw_vs_timesnet_comparison.csv`: Bảng đặt song song 6 dòng giữa Task 8 và Task 11.
- `results/full/ssa_timesnet.log`: Log đầu ra gốc.
- `results/run_metadata.json`: Siêu dữ liệu xác nhận số dòng hợp lệ, mã SHA-256 và thông số chạy.