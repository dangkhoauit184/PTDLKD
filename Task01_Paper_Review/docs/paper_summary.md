# Tóm Tắt Bài Báo FreshRetailNet-50K

## 1. Bài toán Kinh doanh & Cơ chế Censoring
Hàng tươi sống (rau, thịt, hải sản, trái cây, đồ đông lạnh...) có hạn sử dụng ngắn và nhu cầu biến động mạnh. Mô hình “frontier warehouse” của Dingdong bán trong bán kính khoảng 3 km, giao hàng trong 30 phút. Mô hình này có ba đặc điểm khiến stockout xảy ra thường xuyên:
1. Tập khách hàng hạn chế theo bán kính.
2. Hàng hư hỏng nhanh.
3. Mức độ thay thế giữa các sản phẩm cao.

### Vì sao Doanh số Quan sát (Observed Sales) khác Nhu cầu Thực (Latent Demand)
* Doanh số: $y_t = \min(\text{Nhu cầu } d_t, \text{Tồn kho khả dụng } I_t)$. Sau thời điểm hết hàng, doanh số bằng 0 dù nhu cầu vẫn tồn tại.
* Các bộ dữ liệu hiện có (M5, Favorita, Walmart) coi “doanh số = 0” là “không có nhu cầu” và không có nhãn stockout để phân biệt hai trường hợp.
* Dữ liệu gộp theo ngày hoặc tuần che mất tín hiệu stockout. Theo bài báo, một ngày hết hàng chỉ làm doanh số tuần giảm khoảng 10%, nên khó phát hiện và khó gán nhãn.

### Cơ chế Dữ liệu Khuyết Không Ngẫu Nhiên (MNAR)
Việc “mất dữ liệu” phụ thuộc chính vào giá trị bị mất (nhu cầu cao thì dễ hết hàng hơn):
* Xác suất stockout có dạng chữ U theo giờ: sau nhập hàng lúc 6h sáng, tỷ lệ stockout dưới 2%, sau đó tăng đều và đạt đỉnh 26% lúc 20h.
* Giảm giá sâu liên quan đến tăng stockout ($\beta = -0.046; p = 0.018$).
* Mưa làm tăng stockout ($\beta = 0.108; p = 0.05$), được giải thích bằng sự dịch chuyển nhu cầu từ offline sang online.
* Do đó phần khuyết không thể coi là missing-at-random (MAR), và các phương pháp imputation chuẩn sẽ bị chệch.

## 2. Vòng Lặp Lệch Dự Báo Thấp (Under-Forecasting Bias Loop)
Hết hàng $\to$ doanh số bị cắt cụt $\to$ mô hình học từ doanh số cắt cụt $\to$ dự báo thấp $\to$ đặt hàng/nhập kho thấp $\to$ lại hết hàng. Vòng lặp này gây lãng phí (hư hỏng) và mất doanh thu (hết hàng).

## 3. Khung Giải Pháp Hai Giai Đoạn (Two-Stage Framework)
* **Giai đoạn 1 (Latent Demand Recovery):**
  $$d = y \odot s + \hat{d} \odot (1 - s), \quad \hat{d} = f_\theta(y \odot s, p, w, c, s)$$
  Ý tưởng: giữ nguyên doanh số ở những giờ còn hàng, chỉ thay bằng giá trị ước lượng $\hat{d}$ ở những giờ hết hàng.
* **Giai đoạn 2 (Censoring-Robust Forecasting):**
  Nhu cầu đã khôi phục được gộp thành nhu cầu ngày $D_t = \sum_{\tau=1}^{24} d_\tau$, sau đó dự báo trước 7 ngày:
  $$\hat{D}_{T+1:T+7} = f(D_{T-H:T}, P, W, C)$$
