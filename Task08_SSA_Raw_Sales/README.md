# Task 08 — Thực nghiệm SSA trên doanh số gốc (`SSA_RawSales`)

## 1. Mục tiêu
Chạy mô hình thống kê Similar Scenario Average (SSA) trên dữ liệu doanh số gốc (`sale_amount`) để đối chiếu với cột **SSA** (dòng **Raw Sales**) trong Bảng 3 của bài báo *FreshRetailNet-50K*.

## 2. Kết quả đối chiếu
| Group | WAPE (%) | WPE (%) | MAE | Paper WAPE (%) | Paper WPE (%) | Delta WAPE (pp) | Delta WPE (pp) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** (`psd >= 0`) | 31.97 | -10.50 | 0.3982 | 31.97 | -10.50 | 0.00 | 0.00 | completed |
| **Low Sale** (`psd < 1`) | 38.33 | -8.03 | 0.2691 | 38.33 | -8.03 | 0.00 | 0.00 | completed |
| **High Sale** (`psd >= 1`) | 27.40 | -12.26 | 0.7761 | 27.40 | -12.26 | 0.00 | 0.00 | completed |

## 3. Cấu trúc thư mục
- `notebooks/08_ssa_raw_sales.ipynb`: Notebook thực thi đầy đủ trên Google Colab.
- `results/ssa_raw_sales_metrics.csv`: Bảng chỉ số tổng hợp 3 nhóm.
- `results/full/ssa_raw_sales.log`: File log gốc xuất ra từ thực nghiệm.
- `run_info.md`: Chi tiết tham số và đường dẫn dữ liệu đầu vào.