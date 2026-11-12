# BÁO CÁO TASK 5: KHÁM PHÁ VÀ PHÂN TÍCH THỐNG KÊ MÔ TẢ DỮ LIỆU (EDA)
**Môn học:** Phân tích Dữ liệu Kinh doanh (IS403)  
**Notebooks triển khai:** 
* `Task05_EDA/notebooks/Task5_EDA_01_tai_du_lieu.ipynb`
* `Task05_EDA/notebooks/Task5_EDA_02_thong_ke_mo_ta.ipynb`  

---

## 1. Giới thiệu và Mục tiêu của Task
* **Mục tiêu:**
  1. Khám phá sâu các đặc trưng thống kê của bộ dữ liệu bán lẻ đồ tươi sống FreshRetailNet-50K trên tập train ($4.500.000$ dòng, $50.000$ chuỗi, $90$ ngày).
  2. Phân tích phân phối doanh số ngày và độ thưa thớt (sparsity) của dữ liệu theo từng giờ.
  3. Đo lường mức độ và quy luật xảy ra của hiện tượng hết hàng (Stockout) theo khung giờ trong ngày và theo danh mục sản phẩm.
  4. Nhận diện các chu kỳ thời gian (trong ngày, theo thứ trong tuần, xu hướng dài hạn) và kiểm tra tương quan của các biến ngoại sinh (giảm giá, khuyến mãi, ngày lễ, thời tiết).
  5. Rút ra các kết luận định lượng cốt lõi làm cơ sở biện giải cho kết quả mô hình hóa ở Giai đoạn 1 (TimesNet) và Giai đoạn 2 (SSA/TFT).

---

## 2. Mô tả Dataset và Phạm vi Phân tích
* **Tập dữ liệu phân tích:** Tập `train` ($4.500.000$ bản ghi, từ ngày 28/03/2024 đến 25/06/2024). Tập `eval` chỉ dùng để kiểm tra độ phủ cấu trúc, không đưa vào phân tích EDA nhằm tránh rò rỉ thông tin đánh giá (Data Leakage).
* **Các quy ước chuẩn hóa được áp dụng:**
  * Cột `hours_stock_status`: $1$ = Hết hàng (Stockout), $0$ = Còn hàng (In-stock).
  * Khung giờ kinh doanh cốt lõi: $16$ giờ từ $06:00$ đến $21:59$ (mẫu số chuẩn là $16$ giờ/ngày, tương ứng $72.000.000$ điểm giờ quan sát).
  * Doanh số (`sale_amount`, `hours_sale`) là giá trị đã được chuẩn hóa, không có đơn vị tiền tệ/số lượng tuyệt đối.

---

## 3. Các Thư viện và Công cụ Sử dụng
* `numpy`, `pandas`, `pyarrow`: Xử lý mảng và truy vấn dữ liệu hiệu năng cao.
* `matplotlib`, `seaborn`: Thiết kế trực quan hóa dữ liệu học thuật chuẩn publication.
* `scipy.stats`: Tính toán các chỉ số thống kê phân phối (skewness, kurtosis, percentile ratios).

---

## 4. Quy trình Xử lý và Phân tích Dữ liệu
1. **Bước 1 (Notebook 1):** Tải dữ liệu từ Hugging Face, tối ưu hóa bộ nhớ RAM bằng cách tách và lưu mảng 24 giờ thành các file nhị phân `train_hours_sale.npy` và `train_hours_stock.npy`.
2. **Bước 2 (Notebook 2):** Tiến hành phân tích thống kê đa chiều:
   * Phân tích phân phối đơn biến của doanh số ngày và giờ.
   * Phân tích hiện tượng hết hàng và kiểm định giả thuyết "doanh số = 0 do không có nhu cầu hay do hết hàng".
   * Phân tích chuỗi thời gian: tính chu kỳ tuần, biến thiên giờ trong ngày.
   * Phân tích mức độ tập trung Pareto của sản phẩm và cửa hàng.
   * Phân tích quan hệ quan sát được với các biến ngoại sinh.

---

## 5. Kết Quả Thực Nghiệm, Biểu Đồ và Bảng Số Liệu

### 5.1. Phân Phối Doanh Số và Độ Thưa Thớt (Sparsity)
| Chỉ tiêu Thống kê Doanh số | Giá trị Đo lường | Ý nghĩa Nghiệp vụ |
| :--- | :---: | :--- |
| Doanh số trung bình / ngày (`mean`) | **$0.999$** | Chuẩn hóa quanh mức 1.0 |
| Trung vị (`median`) | **$0.700$** | Phân phối lệch phải mạnh |
| Độ lệch chuẩn (`std`) | **$1.410$** | Biến động lớn giữa các ngày |
| Hệ số bất đối xứng (`skewness`) | **$8.470$** | Đuôi dài ở phía doanh số cao |
| Giá trị lớn nhất (`max`) | **$44.90$** | Xuất hiện các ngày bán đột biến |
| Tỷ lệ dòng có doanh số ngày $= 0$ | **$4.46\%$** | Tỷ lệ ngày hoàn toàn không bán được |
| Tỷ lệ giờ có doanh số $= 0$ (khung 6..21) | **$69.06\%$** | Dữ liệu giờ cực kỳ thưa thớt |
| Tỷ lệ giờ có doanh số $= 0$ (cả 24 giờ) | **$77.78\%$** | Ban đêm lượng giao dịch xấp xỉ 0 |

### 5.2. Thống Kê Hiện Tượng Hết Hàng (Stockout Insights)
* **Tỷ lệ hết hàng trung bình:** Chiếm **$19.88\%$** tổng số giờ trong khung giờ kinh doanh $6..21$ (tương đương $\approx 20\%$ đúng như bài báo công bố).
* **Mức độ ảnh hưởng:** **$44.27\%$** số cặp cửa hàng–sản phẩm–ngày có ít nhất $1$ giờ bị hết hàng.
* **Thời gian hết hàng trung bình:** Vào những ngày có hết hàng, sản phẩm bị hết trung bình **$7.18$ giờ/ngày**. Có **$4.04\%$** số ngày bị hết hàng toàn bộ $16$ giờ.
* **Quy luật chữ U theo giờ trong ngày (Diurnal U-shape):**
  * Tỷ lệ hết hàng thấp nhất lúc **$07:00$ sáng ($5.0\%$)** ngay sau khi kho vệ tinh hoàn tất đợt nhập hàng rạng sáng.
  * Tỷ lệ hết hàng tăng dần liên tục trong ngày và đạt đỉnh cao nhất lúc **$22:00$ đêm ($41.9\%$)**.

### 5.3. Bóc Tách Nguyên Nhân Doanh Số Bằng 0
* Khi cửa hàng **KHÔNG hết hàng**: Tỷ lệ ngày có doanh số $= 0$ chỉ là **$1.87\%$**.
* Khi cửa hàng **CÓ hết hàng**: Tỷ lệ ngày có doanh số $= 0$ tăng vọt lên **$7.72\%$** (gấp hơn $4.1$ lần).
$\rightarrow$ **Chứng minh:** Phần lớn các trường hợp doanh số bằng 0 là do thiếu hụt nguồn cung (Stockout) chứ không phải do người tiêu dùng không có nhu cầu.

### 5.4. Tính Tập Trung Nhu Cầu (Pareto Principle)
* **Quy luật $20 - 87$ ở cấp độ sản phẩm:** Top **$20\%$** sản phẩm bán chạy nhất chiếm tới **$87.0\%$** tổng doanh số toàn mạng lưới.
* **Ở cấp độ chuỗi:** Top **$20\%$** chuỗi thời gian chiếm **$48.5\%$** tổng doanh số.
* **Ở cấp độ địa lý:** Thành phố $0$ chiếm tỷ trọng áp đảo với **$51.6\%$** tổng số bản ghi ($2.322.990 / 4.500.000$ dòng).

### 5.5. Đặc Tính Chu Kỳ Thời Gian
* **Chu kỳ ngày trong tuần (Weekly Seasonality):** Thứ Bảy và Chủ Nhật có doanh số cao hơn ngày thường từ **$18\%$ đến $20\%$**.
* **Đỉnh bán hàng trong ngày:**
  * *Ngày thường:* Xuất hiện 2 đỉnh rõ rệt vào lúc **$09:00 - 10:00$ sáng** (chuẩn bị bữa trưa) và **$16:00$ chiều** (chuẩn bị bữa tối).
  * *Cuối tuần:* Xuất hiện 1 đỉnh cực lớn duy nhất vào lúc **$09:00 - 10:00$ sáng** với cường độ vượt trội.
* **Xu hướng tăng trưởng (Non-stationarity):** Tổng doanh số toàn mạng lưới tăng khoảng $50\%$ sau 90 ngày (từ $\approx 40.000$ lên $\approx 60.000$ đơn vị chuẩn hóa), đồng thời tỷ lệ hết hàng giảm từ $37\%$ xuống $15 - 20\%$.

---

## 6. Phân Tích Quan Hệ Với Các Biến Ngoại Sinh

1. **Khuyến mãi và Giảm giá:**
   * Khi có chương trình khuyến mãi (`activity_flag = 1`), doanh số quan sát tăng trung bình $+20\%$.
   * Tuy nhiên, tỷ lệ hết hàng cũng tăng từ $43.0\%$ lên $53.8\%$. Điều này cho thấy khuyến mãi kích thích nhu cầu tăng vọt dẫn đến hết hàng nhanh hơn $\rightarrow$ Doanh số ghi nhận bị cắt cụt nhiều hơn bình thường.
2. **Biến dị thường ở `discount`:**
   * Phát hiện $16.039$ dòng ($0.36\%$) có `discount = 0.0`. Đây là các mặt hàng bán rất chạy (doanh số TB $14.5$/ngày), gợi ý đây là lỗi thiếu giá hoặc quy ước nội bộ, không phải giảm giá $100\%$.
3. **Đặc điểm Thời tiết:**
   * Dữ liệu thời tiết được ghi nhận theo cấp độ **cửa hàng - ngày** (mọi sản phẩm trong cùng một cửa hàng vào một ngày có chung một giá trị thời tiết).
   * Cột lượng mưa `precpt` có $62.9\%$ giá trị nằm trong khoảng $(1; 5]$, chỉ $0.2\%$ bằng $0$, mang tính chất giá trị chỉ số chuẩn hóa chứ không phải milimet mưa thực tế.

---

## 7. Đánh Giá Ý Nghĩa Đối Với Việc Tái Lập Bài Báo

| Phát hiện từ EDA | Ý nghĩa Đối với Giai đoạn 1 (TimesNet) | Ý nghĩa Đối với Giai đoạn 2 (Dự báo SSA/TFT) |
| :--- | :--- | :--- |
| **Quy luật chữ U của hết hàng** | Phù hợp với cơ chế MNAR: giờ chiều và tối bị che nhiều nhất. TimesNet với kiến trúc 2D Inception bắt rất tốt chu kỳ ngày. | Nếu không khôi phục, mô hình dự báo sẽ luôn đoán doanh số chiều/tối thấp hơn thực tế. |
| **Dữ liệu giờ thưa thớt (69% số giờ = 0)** | Cần hàm mất mát chống zero-inflated (như MAE thay vì MSE). | Cần tích lũy từ giờ lên ngày trước khi đưa vào dự báo để giảm nhiễu. |
| **Độ tập trung cao (20% SKU chiếm 87%)** | Sai số WAPE bị chi phối bởi nhóm High-Sale. Khôi phục đúng nhóm này mang lại bước nhảy vọt chỉ số. | Cần báo cáo kết quả tách biệt giữa High Sale ($\text{psd} \ge 1$) và Low Sale ($\text{psd} < 1$). |
| **Xu hướng tăng 50% trong 90 ngày** | Dữ liệu không dừng (non-stationary); cần chuẩn hóa Non-stationary Transformer trong TimesNet. | Tập eval rơi vào đỉnh doanh số cao nhất $\rightarrow$ Dễ bị dự báo thiếu (Under-forecasting) nếu dùng mô hình tĩnh. |

---

## 8. Kết Luận
Task 5 đã cung cấp bức tranh định lượng hoàn chỉnh, chuẩn xác và khoa học về bản chất của bài toán bán lẻ đồ tươi sống trên FreshRetailNet-50K:
* Hiện tượng che khuất nhu cầu (Censoring) là có thật, diễn ra trên $44.27\%$ các ngày và đạt đỉnh vào các giờ cao điểm buổi tối.
* Việc áp dụng mô hình 2 giai đoạn (sử dụng TimesNet khôi phục trước khi dự báo bằng SSA) là hoàn toàn có cơ sở khoa học vững chắc từ đặc tính dữ liệu.
