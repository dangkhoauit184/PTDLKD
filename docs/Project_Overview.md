# Tổng Quan Dự Án: FreshRetailNet-50K (IS403)

## 1. Bối cảnh Kinh doanh (Business Context)
Trong ngành bán lẻ thực phẩm tươi sống (Fresh Retail - rau củ quả, thịt cá, hải sản, đồ đông lạnh), việc quản lý chuỗi cung ứng gặp phải thách thức rất lớn:
* **Hạn sử dụng cực ngắn (Short Shelf-life):** Sản phẩm hư hỏng nhanh chóng nếu tồn kho kéo dài.
* **Thời gian giao hàng siêu tốc (Instant Delivery):** Mô hình kho vệ tinh (Frontier Warehouse / Dark Store) như của Dingdong Fresh phục vụ khách hàng trong bán kính 3 km, cam kết giao hàng trong 30 phút.
* **Nhu cầu khách hàng biến động dữ dội (Demand Volatility):** Phụ thuộc mạnh vào thời tiết, ngày trong tuần, chương trình khuyến mãi và thời điểm trong ngày.
* **Tính thay thế cao (High Substitutability):** Khách hàng sẵn sàng chuyển sang sản phẩm khác nếu mặt hàng họ tìm kiếm bị hết.

## 2. Vấn đề Cốt lõi: Hiện tượng Che khuất Nhu cầu (Demand Censoring)
Khi một sản phẩm hết hàng (Stockout) trên kệ kho lúc 11:00 sáng, hệ thống chỉ ghi nhận doanh số thực tế bán được đến thời điểm đó (ví dụ: 100 đơn vị). Trong suốt khoảng thời gian còn lại của ngày, doanh số ghi nhận bằng **0**:
$$\text{Observed Sales } y_t = \min(\text{True Demand } d_t, \text{Available Inventory } I_t)$$
* Khi $I_t = 0$ (hết hàng), $y_t = 0$, trong khi nhu cầu thực sự $d_t$ vẫn tồn tại.
* **Hậu quả - Vòng lặp sai lệch dự báo thấp (Under-forecasting Bias Loop):**
  $$\text{Hết hàng} \longrightarrow \text{Doanh số bị cắt cụt} \longrightarrow \text{Mô hình học doanh số thấp} \longrightarrow \text{Dự báo thiếu} \longrightarrow \text{Nhập hàng ít} \longrightarrow \text{Hết hàng trầm trọng hơn}$$
* **Bản chất dữ liệu khuyết không ngẫu nhiên (MNAR - Missing Not At Random):** Việc "mất dữ liệu bán hàng" có tương quan trực tiếp với nhu cầu: nhu cầu càng cao thì hàng càng nhanh hết. Do đó, các phương pháp nội suy truyền thống (MAR/MCAR) đều bị chệch nghiêm trọng.

## 3. Khung Giải pháp Hai Giai đoạn (Two-Stage Framework)

Dự án tái lập quy trình 2 giai đoạn do Dingdong Fresh đề xuất trong bài báo:

```
[Dữ liệu thô 50K chuỗi]
  │ (Doanh số theo giờ y_t + Nhãn kho hours_stock_status + Khuyến mãi + Thời tiết + Lịch)
  ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Giai đoạn 1: Khôi phục Nhu cầu Ẩn (Latent Demand Recovery)             │
│ • Xem bài toán như Time-Series Imputation trên khung giờ [6:22]        │
│ • Giữ nguyên y_t khi còn hàng (hours_stock_status=0, tức s_t=1);       │
│   ước lượng d_t khi hết hàng (hours_stock_status=1, tức s_t=0)         │
│ • Mô hình trọng tâm: TimesNet (đối chiếu ImputeFormer, SAITS, DLinear) │
│ • Đầu ra: demand_timesnet.parquet (19 cột gốc + sale_amount_pred ngày) │
└────────────────────────────────────────────────────────────────────────┘
  │
  ▼ (Tích lũy 24 giờ thành nhu cầu ngày D_t)
┌────────────────────────────────────────────────────────────────────────┐
│ Giai đoạn 2: Dự báo Nhu cầu Kháng Hết hàng (Censoring-Robust Forecast) │
│ • Dự báo 7 ngày tiếp theo (Multi-horizon forecasting)                 │
│ • Mô hình: SSA (Similar Scenario Average), TFT, DLinear               │
│ • So sánh 2 Pipeline: Raw Sales Pipeline vs Imputation-Augmented       │
│ • Đánh giá: WAPE, WPE, Decoupling Score                               │
└────────────────────────────────────────────────────────────────────────┘
```

## 4. Mục tiêu Học thuật của Nhóm
1. Tái lập đầy đủ, khách quan và minh bạch các thực nghiệm trong Bảng 2 và Bảng 3 của bài báo.
2. Kiểm chứng xem việc áp dụng TimesNet để khôi phục nhu cầu có thực sự giúp giảm sai số WAPE và đưa độ thiên lệch WPE về gần 0 trên phương pháp dự báo SSA hay không.
3. Đánh giá tính ứng dụng thực tiễn trong bài toán tối ưu tồn kho chuỗi bán lẻ.
