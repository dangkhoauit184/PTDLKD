# Task 11 — Dự báo SSA trên dữ liệu khôi phục TimesNet (`SSA_TimesNet`)

## 1. Mục tiêu
Chạy mô hình thống kê Similar Scenario Average (SSA) trên lịch sử nhu cầu đã khôi phục bằng TimesNet (`sale_amount_pred` từ [Task 10](../Task10_TimesNet_Recovery/run_info.md)) và lập bảng đối chiếu trực tiếp với `SSA_RawSales` ([Task 8](../Task08_SSA_Raw_Sales/README.md)) cùng cột **SSA** trong Bảng 3 bài báo *FreshRetailNet-50K*.

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
- [Notebook đã chạy](notebooks/11_ssa_timesnet.ipynb): kiểm tra SHA-256 theo Task 10 & Task 6, dự báo SSA và xuất bảng đối chiếu.
- [CSV kết quả `SSA_TimesNet`](results/ssa_timesnet_metrics.csv): chỉ số 3 phân nhóm chuẩn 10 cột.
- [CSV đối chiếu song song](results/ssa_raw_vs_timesnet_comparison.csv): bảng 6 dòng đặt cạnh nhau `SSA_RawSales` và `SSA_TimesNet`.
- [Log SSA](results/full/ssa_timesnet.log): đầu ra tỷ lệ gốc.
- [Thông tin chạy lại](run_info.md), [metadata kiểm chứng](results/run_metadata.json) và [báo cáo Task 11](../reports/Task11_Report.md).

## 4. Chạy lại
1. Mở [notebooks/11_ssa_timesnet.ipynb](notebooks/11_ssa_timesnet.ipynb) trên Google Colab hoặc máy cá nhân (cần `numpy`, `pandas`, `pyarrow`).
2. Trên Colab, notebook tự tải `demand_timesnet.parquet` từ Google Drive của Task 10 và đọc `eval.parquet` trong thư mục dự án. Trên máy cá nhân, đặt `eval.parquet` ở thư mục gốc dự án và trỏ `TASK11_DEMAND_PARQUET` tới bản `demand_timesnet.parquet` đã tải.
3. Chạy toàn bộ các ô: notebook kiểm tra khớp SHA-256, xác nhận `206.562` dòng `eval` hợp lệ (`Low Sale = 153.208`, `High Sale = 53.354`) và ghi kết quả vào `results/`.
