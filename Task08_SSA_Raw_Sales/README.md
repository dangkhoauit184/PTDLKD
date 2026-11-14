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
- [Notebook đã chạy](notebooks/08_ssa_raw_sales.ipynb): xác nhận dữ liệu, dự báo và đánh giá.
- [CSV kết quả](results/ssa_raw_sales_metrics.csv): đủ ba dòng Overall, Low Sale và High Sale, dùng làm mốc cho Task 11.
- [Log SSA](results/full/ssa_raw_sales.log): WAPE/WPE ở dạng tỷ lệ; CSV lưu ở dạng phần trăm. MAE giữ đơn vị doanh số chuẩn hóa.
- [Thông tin chạy lại](run_info.md) và [metadata của lượt kiểm chứng](results/run_metadata.json): phiên bản thư viện và SHA-256 của hai file đầu vào.

## 4. Chạy lại

1. Mở notebook trên Colab hoặc Jupyter, dùng CPU có đủ RAM. Cần NumPy, pandas và PyArrow.
2. Chọn thư mục chứa hai Parquet đã xác nhận ở [Task 6](../Task06_Data_Preparation/README.md). Trên Colab, sửa `project_dir` hoặc `data_dir` ở ô đầu cho đúng tên thư mục Drive của bạn. Trên máy cá nhân, mặc định đọc hai file ở thư mục gốc dự án.
3. Chạy tất cả các ô. Nếu file thiếu hoặc SHA-256 khác Task 6, notebook dừng trước khi chạy SSA. Hai file dữ liệu chỉ được đọc.
4. Lấy CSV, log và metadata từ `output_dir` (mặc định `task08_outputs` trong thư mục dự án trên Drive, hoặc `Task08_SSA_Raw_Sales/results` khi chạy local). Kết quả đạt khi CSV có ba nhóm và chỉ số khớp log sau khi đổi đơn vị.
