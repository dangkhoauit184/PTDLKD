# Task 5: Khám Phá và Phân Tích Thống Kê Mô Tả Dữ Liệu (EDA)

## 📌 Tổng Quan
Task 5 thực hiện phân tích thống kê mô tả đa chiều trên tập huấn luyện $4.500.000$ bản ghi, làm sáng tỏ các đặc tính nghiệp vụ quan trọng về doanh số, hiện tượng hết hàng và ảnh hưởng của các biến ngoại sinh.

## 🎯 Mục Tiêu Đã Hoàn Thành
1. Tối ưu hóa lưu trữ RAM bằng cách trích xuất mảng 24 giờ thành các file NumPy nhị phân (`train_hours_sale.npy`, `train_hours_stock.npy`).
2. Khám phá phân phối doanh số lệch phải mạnh (`mean = 0.999`, `median = 0.700`, `skewness = 8.47`).
3. Khám phá nghịch lý thưa thớt: chỉ $4.46\%$ số ngày có doanh số $= 0$, nhưng có tới $69.06\%$ số giờ trong khung $6..21$ bằng $0$.
4. Chứng minh hiện tượng hết hàng ($19.88\%$ số giờ) có quy luật **chữ U theo giờ** (đạt đỉnh $41.9\%$ lúc 22h).
5. Xác thực quy luật Pareto: $20\%$ sản phẩm chiếm $87.0\%$ tổng doanh số bán ra.

## 📁 Cấu Trúc Thư Mục
* [notebooks/Task5_EDA_01_tai_du_lieu.ipynb](notebooks/Task5_EDA_01_tai_du_lieu.ipynb): Tải dữ liệu, kiểm tra cấu trúc sơ bộ và tiền xử lý tối ưu RAM.
* [notebooks/Task5_EDA_02_thong_ke_mo_ta.ipynb](notebooks/Task5_EDA_02_thong_ke_mo_ta.ipynb): Phân tích thống kê chi tiết, trực quan hóa và kiểm định giả thuyết.
* [results/summary_statistics.json](results/summary_statistics.json): File tổng hợp các chỉ số thống kê quan trọng nhất.

## 🔗 Liên Kết Báo Cáo
Xem báo cáo đầy đủ chuẩn học thuật tại: [Task05_Report.md](../reports/Task05_Report.md).
