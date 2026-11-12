# Task 4: Kiểm Tra và Đối Soát Chất Lượng Dữ Liệu (Data Validation)

## 📌 Tổng Quan
Task 4 do **Đăng Khoa** thực hiện, chịu trách nhiệm thiết lập hệ thống kiểm định chất lượng toàn diện trên $100\%$ các bản ghi của bộ dữ liệu FreshRetailNet-50K ($4.500.000$ dòng train và $350.000$ dòng eval).

## 🎯 Mục Tiêu Đã Hoàn Thành
1. Xây dựng notebook kiểm định tự động theo lô (`04_data_validation_colab.ipynb`) chạy mượt mà trên CPU với RAM $< 2\text{ GB}$.
2. Thiết lập và đánh giá **48 quy tắc kiểm định** nghiêm ngặt về schema, null, trùng lặp, logic nghiệp vụ mảng 24 giờ.
3. Xác nhận tính toàn vẹn đạt **$100\%$**: cả $50.000$ chuỗi thời gian đều là bảng cân đối hoàn hảo, không thiếu bất kỳ ngày nào.
4. Phát hiện $34$ bản ghi có `discount > 1.0` (max 1.088) trong tập train và đề xuất giải pháp xử lý.

## 📁 Cấu Trúc Thư Mục
* [notebooks/04_data_validation_colab.ipynb](notebooks/04_data_validation_colab.ipynb): Notebook hoàn chỉnh chạy được trên Google Colab và Local.
* **Kết quả đối soát:**
  * [results/validation_summary.csv](results/validation_summary.csv): Bảng tổng hợp trạng thái 98 hạng mục kiểm tra.
  * [results/column_profile.csv](results/column_profile.csv): Hồ sơ kiểu dữ liệu, số lượng null, giá trị min/max của 19 cột.
  * [results/issue_examples.csv](results/issue_examples.csv): Các dòng mẫu vi phạm để kiểm tra chi tiết.
  * [results/pairs_only_in_train.csv](results/pairs_only_in_train.csv) / [results/pairs_only_in_eval.csv](results/pairs_only_in_eval.csv): Đối soát chéo độ phủ $50.000$ cặp chuỗi ($0$ vi phạm).
  * [results/overlapping_keys.csv](results/overlapping_keys.csv): Xác minh tính không trùng lặp thời gian giữa train và eval ($0$ vi phạm).
  * [results/run_info.json](results/run_info.json): Thông số môi trường và cấu hình chi tiết của lượt chạy kiểm định.

## 🔗 Liên Kết Báo Cáo
Xem báo cáo đầy đủ chuẩn học thuật tại: [Task04_Report.md](../reports/Task04_Report.md).
