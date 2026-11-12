# BÁO CÁO TASK 1: ĐỌC BÀI BÁO VÀ CHỐT PHẠM VI NGHIÊN CỨU
**Môn học:** Phân tích Dữ liệu Kinh doanh (IS403)  
**Tên bài báo:** *FreshRetailNet-50K: A Stockout-Annotated Censored Demand Dataset for Latent Demand Recovery and Forecasting in Fresh Retail*  
**Tác giả:** Yangyang Wang, Jiawei Gu, Li Long, Xin Li, Li Shen, Zhouyu Fu, Xiangjun Zhou, Xu Jiang (Dingdong Ltd.)  
**Nguồn:** arXiv:2505.16319v5  

---

## 1. Giới thiệu và Mục tiêu của Task
* **Mục tiêu:** 
  1. Thấu hiểu bối cảnh kinh doanh của ngành bán lẻ đồ tươi sống và hiện tượng che khuất nhu cầu do hết hàng (Demand Censoring).
  2. Phân tích cơ chế dữ liệu khuyết không ngẫu nhiên (MNAR - Missing Not At Random) và vòng lặp sai lệch dự báo thấp (Under-forecasting Bias Loop).
  3. Đối chiếu khung nghiên cứu lý thuyết trong bài báo với khả năng triển khai thực tế của nhóm.
  4. Xác định chính xác bảng kết quả mục tiêu cần tái lập (Bảng 2 & Bảng 3 trong bài báo gốc).

---

## 2. Mô tả Dataset và Các Thuộc tính Liên quan theo Bài báo
Bài báo công bố bộ dữ liệu lớn **FreshRetailNet-50K** thu thập từ hệ thống phân phối thực tế của Dingdong Fresh:
* **Quy mô:** $50.000$ chuỗi thời gian (cặp `store_id` – `product_id`) trải dài trên $898$ cửa hàng kho tại $18$ thành phố lớn, đại diện cho $863$ SKU tươi sống.
* **Độ phân giải:** Theo từng giờ (Hourly), tổng quy mô xấp xỉ $0,1$ tỷ bản ghi theo giờ.
* **Thời gian:** Khoảng thời gian 90 ngày (tháng 3 đến tháng 6 năm 2024).
* **Đặc tính then chốt:** Bộ dữ liệu đầu tiên trong ngành hàng tươi sống được gắn nhãn tình trạng tồn kho theo giờ (`hours_stock_status`), cho phép phân biệt rõ giữa "không ai muốn mua" ($s_t = 0$ và doanh số $= 0$) với "muốn mua nhưng hết hàng" ($s_t = 1$ và doanh số $= 0$).

---

## 3. Các Thư viện, Công cụ và Công nghệ Sử dụng
* **Nền tảng nghiên cứu:** PyPOTS (Python Toolbox for Partially Observed Time Series) - thư viện mã nguồn mở chuyên dụng cho bài toán missing value imputation trên chuỗi thời gian.
* **Framework học sâu:** PyTorch, PyTorch Lightning, PyTorch-Forecasting.
* **Quản lý dữ liệu:** Hugging Face Datasets (`Dingdong-Inc/FreshRetailNet-50K`), Apache Arrow/Parquet.

---

## 4. Quy trình Xử lý và Phân tích Dữ liệu
Bài báo đề xuất khung tiếp cận 2 giai đoạn (Two-Stage Framework):
1. **Giai đoạn 1 (Latent Demand Recovery):** Biến đổi bài toán khôi phục nhu cầu thành bài toán nội suy chuỗi thời gian (time-series imputation) với mặt nạ là nhãn hết hàng $s_t$:
   $$d_t = y_t \odot s_t + \hat{d}_t \odot (1 - s_t)$$
   Trong đó, khi còn hàng ($s_t = 1$), giữ nguyên doanh số quan sát $y_t$; khi hết hàng ($s_t = 0$), thay thế bằng giá trị ước lượng $\hat{d}_t$ từ mô hình.
2. **Giai đoạn 2 (Demand Forecasting):** Tích lũy nhu cầu theo giờ đã khôi phục thành nhu cầu ngày $D_t = \sum_{\tau=1}^{24} d_{t,\tau}$, sau đó thực hiện dự báo đa bước cho $7$ ngày tương lai:
   $$\hat{D}_{T+1:T+7} = f(D_{T-H:T}, P, W, C)$$

---

## 5. Phương pháp Thực hiện và Giải thích Kiến trúc Mô hình
### 5.1. Mô hình Khôi phục Nhu cầu Ẩn (Giai đoạn 1)
Bài báo đánh giá 7 kiến trúc tiêu biểu:
* **TimesNet:** Mô hình hóa biến thiên thời gian 2D đa chu kỳ (trong ngày và giữa các ngày) thông qua biến đổi Fourier (FFT) và khối Inception 2D.
* **ImputeFormer:** Tận dụng tính chất ma trận hạng thấp (low-rank spatial-temporal attention) để khôi phục cấu trúc không-thời gian.
* **SAITS:** Kiến trúc Self-Attention kết hợp loss liên hợp (ORT và MIT) để bắt phụ thuộc dài hạn.
* **iTransformer:** Đảo ngược chiều biểu diễn, áp dụng attention trên chiều biến (channels/features) thay vì chiều thời gian.
* **GPVAE & CSDI:** Mô hình sinh xác suất (Gaussian Process VAE) và mô hình khuếch tán điều kiện (Diffusion).
* **DLinear:** Baseline phân rã xu hướng và mùa vụ qua các tầng tuyến tính một lớp cực kỳ tinh gọn.

### 5.2. Mô hình Dự báo Tương lai (Giai đoạn 2)
* **SSA (Similar Scenario Average):** Phương pháp thống kê phi tham số, tìm kiếm các ngày lịch sử có điều kiện tương đồng (khuyến mãi, khoảng cách ngày, thứ trong tuần, lượng mưa) và tính trung bình có trọng số.
* **TFT (Temporal Fusion Transformer):** Mạng nơ-ron học sâu tích hợp multi-head attention với cơ chế Variable Selection Networks và gating GRN để xử lý đồng thời biến quá khứ và biến tương lai đã biết trước.
* **DLinear:** Dự báo đa biến tuyến tính trực tiếp.

---

## 6. Kết quả Thực nghiệm trong Bài báo (Mục tiêu Tái lập)

### Bảng 2: Hiệu năng Khôi phục Nhu cầu trên Thử nghiệm Mô phỏng MNAR
| Chỉ số | Raw Sale | TimesNet | ImputeFormer | SAITS | iTransformer | GPVAE | CSDI | DLinear |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **WAPE (%)** | – | **27.62%** | 35.65% | 61.54% | 33.30% | 55.36% | 44.26% | 29.99% |
| **WPE (%)** | – | **1.43%** | -2.62% | -5.97% | -2.09% | 1.06% | -3.21% | -1.28% |
| **$\rho_{DS}$** | -0.57 | **0.07** | -0.26 | -0.50 | -0.22 | -0.15 | -0.27 | -0.16 |

### Bảng 3: Hiệu năng Dự báo 7 Ngày Khi Kết Hợp Các Phương Pháp Khôi Phục Khác Nhau
| Phương pháp Khôi phục | SSA: WAPE | SSA: WPE | TFT: WAPE | TFT: WPE | DLinear: WAPE | DLinear: WPE |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Nhóm Overall (Toàn bộ chuỗi)** | | | | | | |
| TimesNet | **29.79%** | 1.39% | **29.02%** | 2.58% | 30.73% | 6.88% |
| ImputeFormer | 29.80% | -4.19% | 29.54% | 2.77% | 30.27% | 1.91% |
| iTransformer | 29.76% | -2.12% | 29.26% | 0.57% | 30.69% | 4.35% |
| DLinear | 30.00% | -1.49% | 29.71% | 2.63% | 30.60% | 4.02% |
| Raw Sales (Gốc) | 31.97% | -10.50% | 31.75% | -7.37% | 31.56% | -4.89% |
| **Nhóm High Sale (Bán chạy - 20% SKU)** | | | | | | |
| TimesNet | **23.98%** | -1.12% | **23.03%** | 0.87% | 23.58% | 2.98% |
| Raw Sales (Gốc) | 27.40% | -12.26% | 27.95% | -11.46% | 25.68% | -7.63% |
| **Nhóm Low Sale (Bán chậm / Đuôi dài)** | | | | | | |
| TimesNet | 37.87% | 4.89% | 37.33% | 7.78% | 40.73% | 12.37% |
| Raw Sales (Gốc) | 38.33% | -8.03% | 37.04% | -1.72% | 39.78% | -1.03% |

---

## 7. Phân tích, Đánh giá và Nhận xét Chuyên sâu
1. **TimesNet thể hiện sự vượt trội toàn diện:**
   * Đạt WAPE thấp nhất ($27.62\%$) và đưa độ lệch hướng WPE về sát $0$ ($1.43\%$).
   * Chỉ số tách rời Decoupling Score $\rho_{DS}$ đạt $+0.07$ (tiến gần về $0$ so với $-0.57$ của dữ liệu thô), chứng minh TimesNet đã loại bỏ thành công sự phụ thuộc của nhu cầu vào tình trạng thiếu hụt nguồn cung.
2. **Khắc phục triệt để hiện tượng Under-Forecasting:**
   * Trên dữ liệu doanh số gốc (Raw Sales), mô hình dự báo luôn bị lệch âm nghiêm trọng (WPE từ $-7.37\%$ đến $-12.26\%$), chứng tỏ mô hình liên tục dự báo thiếu nhu cầu.
   * Khi được hỗ trợ bởi dữ liệu khôi phục từ TimesNet, WPE của TFT đạt $+0.87\%$ (ở nhóm High Sale) và $+2.58\%$ (ở nhóm Overall), giải quyết triệt để vòng lặp sai lệch.
3. **Hiệu ứng phân hóa theo nhóm sản phẩm:**
   * Nhóm **High Sale** hưởng lợi nhiều nhất: WAPE giảm từ $27.95\%$ xuống $23.03\%$ (giảm tuyệt đối $4.92\%$). Vì hàng bán chạy có tần suất hết hàng cao nhất nên việc khôi phục mang lại giá trị kinh tế lớn nhất.
   * Nhóm **Low Sale** tiềm ẩn rủi ro: Dữ liệu thưa khiến một số mô hình bị thiên lệch dự báo thừa (Over-forecasting, WPE lên tới $+12.37\%$), có thể gây tăng tỷ lệ hủy hàng tươi sống.

---

## 8. Kết luận và Chốt Phạm Vi Đồ Án Của Nhóm
* **Chốt phạm vi cốt lõi:** Nhóm thống nhất tập trung tái lập nhánh thực nghiệm có tính đại diện cao nhất:
  1. *Thực nghiệm 1 (Baseline):* Thuật toán dự báo **SSA trên doanh số gốc (Raw Sales)** $\rightarrow$ Báo cáo WAPE, WPE, MAE trên 3 nhóm (Overall, High-sale, Low-sale).
  2. *Thực nghiệm 2 (Proposed):* Huấn luyện **TimesNet** để khôi phục nhu cầu trên $50.000$ chuỗi $\rightarrow$ Xuất file `demand.parquet`.
  3. *Thực nghiệm 3 (Comparison):* Thuật toán dự báo **SSA trên nhu cầu đã khôi phục** $\rightarrow$ Đối chiếu trực tiếp độ cải thiện chỉ số với Thực nghiệm 1.
* **Hạn chế được ghi nhận:** Việc huấn luyện mô hình sâu trên $50.000$ chuỗi thời gian đỏi hỏi tài nguyên tính toán lớn (GPU VRAM và thời gian huấn luyện); nhóm sẽ giải quyết thông qua tối ưu hóa môi trường ở Task 3.
