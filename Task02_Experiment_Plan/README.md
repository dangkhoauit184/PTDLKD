# Task 2: Lập Kế Hoạch Thực Nghiệm & Đặc Tả Siêu Tham Số

## 📌 Tổng Quan
Task 2 thiết lập ma trận thực nghiệm khoa học, chuẩn hóa các siêu tham số mô hình và định nghĩa quy ước lưu trữ kết quả để tránh xung đột trong quá trình làm việc nhóm.

## 🎯 Mục Tiêu
1. Lên danh sách 15 cấu hình dự báo kết hợp giữa 3 thuật toán dự báo (SSA, TFT, DLinear) và 5 nguồn dữ liệu nhu cầu (Raw Sales + 4 mô hình khôi phục).
2. Trích xuất và hệ thống hóa siêu tham số của 7 mô hình khôi phục nhu cầu trong `models.py`.
3. Chuẩn hóa công thức các chỉ số đánh giá: WAPE, WPE, Decoupling Score ($\rho_{DS}$).
4. Định nghĩa quy tắc phân nhóm: Overall, High Sale (top 20% chuỗi), Low Sale (80% còn lại).

## 📁 Cấu Trúc Thư Mục
* [docs/15_forecasting_configurations.md](docs/15_forecasting_configurations.md): Bảng chi tiết 15 cấu hình dự báo thực nghiệm.
* [docs/model_hyperparameters.md](docs/model_hyperparameters.md): Bảng tổng hợp siêu tham số các mô hình Imputation trong PyPOTS.

## 🔗 Liên Kết Báo Cáo
Xem báo cáo đầy đủ chuẩn học thuật tại: [Task02_Report.md](../reports/Task02_Report.md).
