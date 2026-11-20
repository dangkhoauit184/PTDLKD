# BÁO CÁO TASK 2: LẬP KẾ HOẠCH THỰC NGHIỆM VÀ ĐẶC TẢ SIÊU THAM SỐ
**Môn học:** Phân tích Dữ liệu Kinh doanh (IS403)  
**Nội dung:** Kế hoạch thực nghiệm chi tiết tái lập Bảng 2 & Bảng 3 (FreshRetailNet-50K)  

---

## 1. Giới thiệu và Mục tiêu của Task
* **Mục tiêu:**
  1. Xây dựng kế hoạch thực nghiệm hệ thống, khả thi và bám sát tài liệu gốc.
  2. Định nghĩa chi tiết 15 cấu hình dự báo kết hợp giữa các thuật toán dự báo và nguồn dữ liệu nhu cầu.
  3. Bóc tách và chuẩn hóa bộ siêu tham số (Hyperparameters) của các mô hình trong `models.py` và `app.py`.
  4. Xác lập quy ước đặt tên thư mục, file kết quả và quy trình kiểm thử (seed, metric tracking).

---

## 2. Mô tả Dataset và Phân đoạn Dữ liệu Thực nghiệm
* **Tập Train (Huấn luyện):** $4.500.000$ dòng ($50.000$ chuỗi $\times$ $90$ ngày, từ 28/03/2024 đến 25/06/2024).
  * Trong Giai đoạn 1 (Khôi phục), 90 ngày được chia thành 3 lát cắt 30 ngày $\rightarrow$ Tạo thành $150.000$ mẫu chuỗi thời gian.
  * Mỗi ngày tập trung vào khung giờ hoạt động chính **06:00 đến 22:00 (16 giờ)** $\rightarrow$ Chiều dài chuỗi mỗi mẫu là $30 \times 16 = 480$ time steps.
* **Tập Eval (Đánh giá):** $350.000$ dòng ($50.000$ chuỗi $\times$ $7$ ngày, từ 26/06/2024 đến 02/07/2024).
  * Dự báo trước 7 ngày (rolling forecast $H=7$).
  * **Quy tắc Ground Truth then chốt:** Khi đánh giá dự báo trên tập Eval, hệ thống lọc điều kiện `stock_hour6_22_cnt == 0` (chỉ đánh giá trên những ngày thực sự không bị hết hàng trong khung giờ mở cửa) để đảm bảo đáp án so sánh là nhu cầu thực sự uncensored.

---

## 3. Các Thư viện, Công cụ và Công nghệ Sử dụng
* `pypots.imputation`: TimesNet, DLinear, SAITS, iTransformer, GPVAE, CSDI, ImputeFormer.
* `pypots.optim`: Adam, RAdam với các lịch trình điều chỉnh tốc độ học (Learning Rate Schedulers).
* `pandas`, `numpy`, `pyarrow`: Xử lý mảng tensor nhiều chiều và lưu trữ parquet tốc độ cao.

---

## 4. Danh Sách 15 Cấu Hình Thực Nghiệm Dự Báo (Task 2 – Bảng 3)

| STT | Mô hình Dự báo (Forecaster) | Nguồn Dữ liệu Nhu cầu (Demand Source) | Mã Cấu hình (Config ID) | Mục đích Thực nghiệm |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **SSA** | **Raw Sales (Doanh số gốc)** | `SSA_RawSales` | **Baseline mốc đối chứng của nhóm** |
| **2** | **SSA** | **TimesNet (Nhu cầu khôi phục)** | `SSA_TimesNet` | **Mục tiêu tái lập trọng tâm của nhóm** |
| 3 | SSA | ImputeFormer | `SSA_ImputeFormer` | Đối chiếu với cơ chế low-rank attention |
| 4 | SSA | iTransformer | `SSA_iTransformer` | Đối chiếu với inverted channel attention |
| 5 | SSA | DLinear | `SSA_DLinear` | Đối chiếu với phương pháp tuyến tính nhẹ |
| 6 | TFT | Raw Sales | `TFT_RawSales` | Mốc baseline trên mô hình học sâu |
| 7 | TFT | TimesNet | `TFT_TimesNet` | Kiểm chứng tổ hợp tốt nhất bài báo (SOTA) |
| 8 | TFT | ImputeFormer | `TFT_ImputeFormer` | Đánh giá TFT với ImputeFormer |
| 9 | TFT | iTransformer | `TFT_iTransformer` | Đánh giá TFT với iTransformer |
| 10 | TFT | DLinear | `TFT_DLinear` | Đánh giá TFT với DLinear |
| 11 | DLinear | Raw Sales | `DLinear_RawSales` | Đánh giá baseline phân rã tuyến tính |
| 12 | DLinear | TimesNet | `DLinear_TimesNet` | DLinear dự báo trên TimesNet |
| 13 | DLinear | ImputeFormer | `DLinear_ImputeFormer` | DLinear dự báo trên ImputeFormer |
| 14 | DLinear | iTransformer | `DLinear_iTransformer` | DLinear dự báo trên iTransformer |
| 15 | DLinear | DLinear | `DLinear_DLinear` | Pipeline end-to-end hoàn toàn bằng DLinear |

---

## 5. Đặc Tả Siêu Tham Số Chi Tiết (Hyperparameters)

### 5.1. Cấu hình Mặc định Toàn cục (`CONFIG` trong `app.py`)
* `n_steps`: $480$ ($30 \text{ ngày} \times 16 \text{ giờ/ngày}$).
* `n_features`: $6$ đặc trưng (`hours_sale`, `discount`, `holiday_flag`, `precpt`, `avg_temperature`, `hour_normalized`).
* `batch_size`: $128$.
* `lr` (Learning Rate): $0.001$.
* `weight_decay`: $1\text{e-}5$.
* `optimizer`: `Adam`.
* `patience` (Early stopping): $5$ epochs.
* `EPOCHS`: $5$ (mặc định trong `CONFIG` của `app.py` dùng cho lượt tái lập chính; mức $20$ chỉ xét khi thử nghiệm mở rộng riêng).
* `OT` (Observed Target): $1$ (kênh doanh số).

### 5.2. Tham số Kiến trúc Riêng Từng Mô hình (`models.py`)
1. **TimesNet:**
   * `n_layers`: $2$
   * `top_k`: $7$ (bắt 7 tần số chu kỳ biên độ lớn nhất qua FFT)
   * `n_kernels`: $5$ (kích thước bộ lọc Inception 2D)
   * `d_model`: $64$, `d_ffn`: $32$
   * `apply_nonstationary_norm`: `True`
2. **ImputeFormer:**
   * `n_layers`: $2$
   * `n_temporal_heads`: $4$
   * `d_input_embed`: $64$, `d_learnable_embed`: $64$ (`CONFIG['d_model']`), `d_proj`: $64$
   * `ORT_weight`: $1.0$, `MIT_weight`: $1.0$
3. **SAITS:**
   * `n_layers`: $2$, `n_heads`: $4$, `d_k`: $16$, `d_v`: $16$, `d_model`: $64$
   * `diagonal_attention_mask`: `True`
   * `customized_loss_func`: `calc_mae`
4. **DLinear:**
   * `moving_avg_window_size`: `patch_len // 2 * 2 + 1` ($17$)
   * `individual`: `False`
   * `ORT_weight`: $1.0$, `MIT_weight`: $1.0$

---

## 6. Công Thức Chỉ Số Đo Lường (Evaluation Metrics)

1. **WAPE (Weighted Absolute Percentage Error):**
   $$\text{WAPE} = \frac{\sum_{i,t} |y_{i,t} - \hat{y}_{i,t}|}{\sum_{i,t} y_{i,t}}$$
2. **WPE (Weighted Percentage Error - Đo độ thiên vị hệ thống):**
   $$\text{WPE} = \frac{\sum_{i,t} (\hat{y}_{i,t} - y_{i,t})}{\sum_{i,t} y_{i,t}}$$
   * **Lưu ý chi tiết thực thi trong mã tác giả:**
     * Ở Giai đoạn 1 (`evaluation_mnar` trong `app.py`), WAPE và WPE được tính gộp trên toàn bộ các ngày hợp lệ trong `train` (các ngày có ít nhất 1 giờ bị che nhân tạo và không có hết hàng thực trong khung `6..21`).
     * Ở Giai đoạn 2 (`evaluation` trong `ssa_forecasting.py`), WAPE, WPE và MAE được tính **riêng cho từng ngày `dt`** trên các dòng `eval` thỏa `stock_hour6_22_cnt == 0` thuộc từng nhóm (`Overall: psd >= 0`, `Low Sale: psd < 1`, `High Sale: psd >= 1`, với `psd` là doanh số ngày gốc trung bình trong `train`), sau đó **lấy trung bình cộng qua 7 ngày**.
3. **Decoupling Score ($\rho_{DS}$):**
   $$\rho_{DS} = \frac{\sum_{g \in \mathcal{G}} \mu_g \cdot \text{Pearson}(C_g, \hat{D}_g)}{\sum_{g \in \mathcal{G}} \mu_g}$$
   * Theo hàm `evaluation_decoupling` (`app.py`): xét các ngày có hết hàng (`stock_hour6_22_cnt > 0`), gom theo từng nhóm $g = (\text{store\_id}, \text{product\_id}, \text{holiday\_flag})$ có trên 3 mức `stock_hour6_22_cnt` khác nhau (`nunique > 3`), tính tương quan Pearson giữa số giờ hết hàng $C_g$ (`stock_hour6_22_cnt`) và doanh số ngày (`sale_amount` hoặc `sale_amount_pred`), rồi lấy trung bình trọng số theo $\mu_g$ (doanh số ngày trung bình của cặp đó vào những ngày `stock_hour6_22_cnt == 0`).
   * Doanh số thô trên bài báo có $\rho_{DS} = -0.57$. Giá trị $\rho_{DS} \to 0$ thể hiện việc tách thành công nhu cầu ước lượng khỏi mức độ thiếu hụt tồn kho.

---

## 7. Quy Ước Đặt Tên Thư Mục, Log Và File Kết Quả

Cấu trúc dự kiến ban đầu khi lập kế hoạch ở Task 2:
```text
outputs/
├── task1_latent_recovery/
│   ├── {model_name}/
│   │   ├── checkpoints/best_model.ckpt
│   │   ├── logs/train_seed2024.log
│   │   └── recovered_demand/rec_hourly_{model_name}_seed2024.parquet
│
└── task2_forecasting/
    ├── {forecaster_name}/
    │   ├── raw_sales/
    │   │   ├── logs/eval_raw.log
    │   │   └── metrics_raw.json
    │   └── recovered_{recovery_model}/
    │       ├── logs/eval_{recovery_model}.log
    │       └── metrics_{recovery_model}.json
```

> **Cập nhật chuẩn hóa khi triển khai thực tế (từ Task 6–11):** Để mỗi thành viên làm việc độc lập trên nhánh Git riêng mà không xung đột đường dẫn, nhóm chuẩn hóa sang các thư mục cấp cao `Task06_Data_Preparation/`, `Task07_Smoke_Test/`, `Task08_SSA_Raw_Sales/`, `Task09_TimesNet_MNAR/`, `Task10_TimesNet_Recovery/`, `Task11_SSA_TimesNet/` (lưu CSV chỉ số, `run_info.md`, `run_metadata.json` và log nhỏ trên Git; lưu dữ liệu Parquet, `.npy` và checkpoint `.pypots` trên Google Drive). Đối với TimesNet, các lượt baseline giữ `seed=1024` và `EPOCHS=5` theo CLI gốc của `app.py` (nếu thử `seed=2024` phải ghi tách biệt trong `run_info.md`). Chi tiết quy định tại [docs/Task06-10_Phan_cong_chi_tiet.md](../docs/Task06-10_Phan_cong_chi_tiet.md).

---

## 8. Kết luận và Kế hoạch Thực hiện
* **Kế hoạch ưu tiên thực hiện của nhóm:**
  - *Giai đoạn 1:* Chạy cấu hình `SSA_RawSales` (Task 8) để hoàn thành mốc đánh giá baseline.
  - *Giai đoạn 2:* Đánh giá `TimesNet` với thiếu nhân tạo MNAR đối chiếu Bảng 2 (Task 9) và chạy khôi phục nhu cầu trên giờ hết hàng thực tế xuất `demand_timesnet.parquet` (Task 10).
  - *Giai đoạn 3:* Chạy cấu hình `SSA_TimesNet` (Task 11) trên cùng tập `eval` và quy tắc phân nhóm như Task 8 để so sánh trực tiếp với Bảng 3 bài báo.
