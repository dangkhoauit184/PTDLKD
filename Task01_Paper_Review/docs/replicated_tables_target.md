# Mục Tiêu Tái Lập: Bảng 2 & Bảng 3 Của Bài Báo

## Bảng 2: Hiệu năng Khôi phục Nhu cầu trên Thử nghiệm Mô phỏng MNAR
| Chỉ số | Raw Sale | TimesNet | ImputeFormer | SAITS | iTransformer | GPVAE | CSDI | DLinear |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **WAPE (%)** | – | **27.62%** | 35.65% | 61.54% | 33.30% | 55.36% | 44.26% | 29.99% |
| **WPE (%)** | – | **1.43%** | -2.62% | -5.97% | -2.09% | 1.06% | -3.21% | -1.28% |
| **$\rho_{DS}$** | -0.57 | **0.07** | -0.26 | -0.50 | -0.22 | -0.15 | -0.27 | -0.16 |

### Nhận xét phân tích về Bảng 2:
1. **TimesNet dẫn đầu:** Cả về sai số WAPE (27.62%) và WPE (1.43%). Điều này khớp với đặc trưng dữ liệu chuỗi hàng tươi sống có hai tầng chu kỳ rõ rệt (đỉnh 9h/16h trong ngày và hiệu ứng cuối tuần).
2. **DLinear là baseline đáng chú ý:** WAPE 29.99%, chỉ kém TimesNet 2.37% nhưng cấu trúc tuyến tính đơn giản và tốc độ chạy cực nhanh.
3. **Decoupling Score ($\rho_{DS}$):** Chỉ TimesNet đưa tương quan giữa tỷ lệ stockout và nhu cầu khôi phục về gần 0 (0.07, so với -0.57 của doanh số thô).

---

## Bảng 3: Hiệu năng Dự báo với Các Phương Pháp Khôi Phục Khác Nhau
| Phương pháp khôi phục | SSA: WAPE | SSA: WPE | TFT: WAPE | TFT: WPE | DLinear: WAPE | DLinear: WPE |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Nhóm Overall** | | | | | | |
| TimesNet | **29.79%** | 1.39% | **29.02%** | 2.58% | 30.73% | 6.88% |
| ImputeFormer | 29.80% | -4.19% | 29.54% | 2.77% | 30.27% | 1.91% |
| iTransformer | 29.76% | -2.12% | 29.26% | 0.57% | 30.69% | 4.35% |
| DLinear | 30.00% | -1.49% | 29.71% | 2.63% | 30.60% | 4.02% |
| Raw Sales (Gốc) | 31.97% | -10.50% | 31.75% | -7.37% | 31.56% | -4.89% |
| **Nhóm Low Sale** | | | | | | |
| TimesNet | 37.87% | 4.89% | 37.33% | 7.78% | 40.73% | 12.37% |
| Raw Sales (Gốc) | 38.33% | -8.03% | 37.04% | -1.72% | 39.78% | -1.03% |
| **Nhóm High Sale** | | | | | | |
| TimesNet | **23.98%** | -1.12% | **23.03%** | 0.87% | 23.58% | 2.98% |
| Raw Sales (Gốc) | 27.40% | -12.26% | 27.95% | -11.46% | 25.68% | -7.63% |

### Nhận xét phân tích về Bảng 3:
1. **Khử censoring giảm sai số ở Overall:** Với SSA, WAPE giảm từ 31.97% xuống 29.79%; với TFT giảm từ 31.75% xuống 29.02%. WPE chuyển từ âm nặng sang xấp xỉ 0.
2. **Hiệu ứng mạnh nhất ở High Sale:** Raw Sales có WPE -12.26% (SSA), sau khi khôi phục bằng TimesNet chỉ còn -1.12%. WAPE giảm từ 27.40% xuống 23.98%.
