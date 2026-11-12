# Danh Sách 15 Cấu Hình Thực Nghiệm Dự Báo (Task 2 – Bảng 3)

15 cấu hình thử nghiệm kết hợp giữa 3 thuật toán dự báo và 5 nguồn dữ liệu nhu cầu (doanh số gốc + 4 mô hình khôi phục tốt nhất):

| STT | Mô hình Dự báo (Forecaster) | Nguồn Dữ liệu Nhu cầu (Demand Source) | Mã cấu hình thực nghiệm | Nhóm ưu tiên thực hiện |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **SSA (Similar Scenario Average)** | **Raw Sales (Doanh số gốc)** | `SSA_RawSales` | **Ưu tiên 1 (Mốc baseline)** |
| **2** | **SSA** | **TimesNet (Nhu cầu khôi phục)** | `SSA_TimesNet` | **Ưu tiên 1 (Tái lập cốt lõi)** |
| 3 | SSA | ImputeFormer | `SSA_ImputeFormer` | Ưu tiên 2 |
| 4 | SSA | iTransformer | `SSA_iTransformer` | Ưu tiên 2 |
| 5 | SSA | DLinear | `SSA_DLinear` | Ưu tiên 2 |
| 6 | TFT (Temporal Fusion Transformer) | Raw Sales | `TFT_RawSales` | Ưu tiên 3 |
| 7 | TFT | TimesNet | `TFT_TimesNet` | Ưu tiên 3 |
| 8 | TFT | ImputeFormer | `TFT_ImputeFormer` | Mở rộng |
| 9 | TFT | iTransformer | `TFT_iTransformer` | Mở rộng |
| 10 | TFT | DLinear | `TFT_DLinear` | Mở rộng |
| 11 | DLinear | Raw Sales | `DLinear_RawSales` | Ưu tiên 3 |
| 12 | DLinear | TimesNet | `DLinear_TimesNet` | Ưu tiên 3 |
| 13 | DLinear | ImputeFormer | `DLinear_ImputeFormer` | Mở rộng |
| 14 | DLinear | iTransformer | `DLinear_iTransformer` | Mở rộng |
| 15 | DLinear | DLinear | `DLinear_DLinear` | Mở rộng |
