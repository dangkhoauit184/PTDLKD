# Task 13 — Dự báo SSA trên dữ liệu khôi phục DLinear (`SSA_DLinear`) & Tổng hợp Cột SSA

## 1. Mục tiêu
Chạy mô hình thống kê Similar Scenario Average (SSA) trên lịch sử nhu cầu đã khôi phục bằng DLinear (`sale_amount_pred` từ [Task 12](../Task12_DLinear_Recovery/run_info.md)), đối chiếu với dòng **DLinear** thuộc cột **SSA** trong Bảng 3 bài báo *FreshRetailNet-50K*, và lập bảng tổng hợp trọn vẹn cả **3 cấu hình thuộc cột SSA** (`SSA_RawSales`, `SSA_DLinear`, `SSA_TimesNet`).

## 2. Tổng hợp kết quả 3 cấu hình cột SSA (trên cùng 206.562 dòng `eval` hợp lệ)

| Phân nhóm | Cấu hình | WAPE (%) | WPE (%) | MAE | Paper WAPE (%) | Paper WPE (%) | Delta WAPE (pp) | Delta WPE (pp) | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** (`psd >= 0`) | `SSA_RawSales` (Task 8) | 31.97 | -10.50 | 0.3982 | 31.97 | -10.50 | 0.00 | 0.00 | completed |
| **Overall** (`psd >= 0`) | **`SSA_DLinear` (Task 13)** | **30.12** | **-0.58** | **0.3749** | 30.00 | -1.49 | **+0.12** | **+0.91** | completed |
| **Overall** (`psd >= 0`) | `SSA_TimesNet` (Task 11) | 29.79 | +1.40 | 0.3709 | 29.79 | +1.39 | 0.00 | +0.01 | completed |
| **Low Sale** (`psd < 1`) | `SSA_RawSales` (Task 8) | 38.33 | -8.03 | 0.2691 | 38.33 | -8.03 | 0.00 | 0.00 | completed |
| **Low Sale** (`psd < 1`) | **`SSA_DLinear` (Task 13)** | **38.00** | **+3.69** | **0.2664** | – | – | – | – | completed |
| **Low Sale** (`psd < 1`) | `SSA_TimesNet` (Task 11) | 37.87 | +4.96 | 0.2656 | 37.87 | +4.89 | 0.00 | +0.07 | completed |
| **High Sale** (`psd >= 1`) | `SSA_RawSales` (Task 8) | 27.40 | -12.26 | 0.7761 | 27.40 | -12.26 | 0.00 | 0.00 | completed |
| **High Sale** (`psd >= 1`) | **`SSA_DLinear` (Task 13)** | **24.46** | **-3.64** | **0.6925** | – | – | – | – | completed |
| **High Sale** (`psd >= 1`) | `SSA_TimesNet` (Task 11) | 23.98 | -1.15 | 0.6790 | 23.98 | -1.12 | 0.00 | -0.03 | completed |

*(Ghi chú: Bảng 3 của bài báo gốc không in số tham chiếu cho `SSA_DLinear` ở hai nhóm con `Low Sale` và `High Sale`, nên các ô tham chiếu/chênh lệch tương ứng trong CSV được để trống theo đúng quy ước).*

## 3. Cấu trúc thư mục
- [Notebook đã chạy](notebooks/13_ssa_dlinear.ipynb): xác minh SHA-256 theo Task 12 & Task 6, dự báo `SSA_DLinear` và tổng hợp 3 cấu hình cột SSA.
- [CSV kết quả `SSA_DLinear`](results/ssa_dlinear_metrics.csv): chỉ số 3 phân nhóm chuẩn 10 cột.
- [CSV tổng hợp 3 cấu hình SSA](results/ssa_all_3configs_summary.csv): bảng 9 dòng đặt cạnh nhau `SSA_RawSales`, `SSA_DLinear` và `SSA_TimesNet`.
- [Log SSA](results/full/ssa_dlinear.log): đầu ra tỷ lệ gốc.
- [Thông tin chạy lại](run_info.md), [metadata lượt chạy](results/run_metadata.json) và [báo cáo Task 13](../reports/Task13_Report.md).

## 4. Chạy lại
1. Mở [notebooks/13_ssa_dlinear.ipynb](notebooks/13_ssa_dlinear.ipynb) trên Google Colab hoặc máy cá nhân (cần `numpy`, `pandas`, `pyarrow`).
2. Trên Colab, notebook tự tải `demand_dlinear.parquet` từ Google Drive của Task 12 (`ID: 1MDcD7cOyzcnoBu48I6eGUkSfwx8b3hkh`) và đọc `eval.parquet` trong thư mục dự án. Trên máy cá nhân, đặt `eval.parquet` ở thư mục gốc dự án và trỏ `TASK13_DEMAND_PARQUET` tới bản `demand_dlinear.parquet` đã tải.
3. Chạy toàn bộ các ô: notebook kiểm tra khớp SHA-256, xác nhận `206.562` dòng `eval` hợp lệ (`Low Sale = 153.208`, `High Sale = 53.354`) và xuất toàn bộ tệp vào `results/`.
