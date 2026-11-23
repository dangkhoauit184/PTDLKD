# Báo cáo Task 12 — Khôi phục nhu cầu tiềm ẩn bằng DLinear

**Người thực hiện:** Khanh | **Nhánh:** `feature/task12-dlinear-recovery` | **Thư mục:** `Task12_DLinear_Recovery/`

## 1. Mục tiêu
Tái lập cột **DLinear** của Bảng 2 (khôi phục nhu cầu) bằng mã gốc của tác giả, đối chứng với TimesNet (Task 9, Task 10), và tạo tệp `demand_dlinear.parquet` cho hai cấu hình dự báo `SSA_DLinear` (Task 13) và `DLinear_DLinear` (Task 14).

## 2. Phương pháp
- **Mô hình DLinear** (Zeng và cộng sự, AAAI 2023): tách chuỗi thành thành phần xu hướng (trung bình trượt cửa sổ 17) và thành phần mùa vụ, mỗi thành phần đi qua một lớp tuyến tính. Trong bài toán điền dữ liệu thiếu (PyPOTS), mô hình nhận thêm mặt nạ thiếu và được huấn luyện bằng hai loss ORT (tái tạo điểm quan sát) và MIT (điền điểm che ngẫu nhiên).
- **Đầu vào:** 150.000 mẫu × 480 bước (30 ngày × 16 giờ 6..21) × 6 kênh (doanh số giờ với giờ hết hàng = NaN, `discount`, `holiday_flag`, `precpt`, `avg_temperature`, chỉ số giờ/15).
- **Siêu tham số:** giữ nguyên `models.py` — `moving_avg_window_size=17`, `individual=False`, `d_model=64`, 5 epoch, batch 128, Adam lr 0,001. (Bảng phân công ghi `individual=True`; mã gốc dùng `False`.)
- **Lượt 1 – MNAR:** `missing_rate=0.3`, seed 1024; che thêm điểm giờ quan sát được bằng `mimic_missing`, đo WAPE/WPE trên tổng doanh số ngày của các ngày có điểm che và không hết hàng thật.
- **Lượt 2 – Khôi phục:** `missing_rate=0`, seed 2024; điền giá trị tại các giờ hết hàng thật, cộng 24 giờ thành `sale_amount_pred`; Decoupling Score đo mức tương quan giữa số giờ hết hàng và nhu cầu (càng gần 0 càng tốt).
- **Thay đổi kỹ thuật:** kế thừa runner tiết kiệm RAM của Task 9; viết lại `_demand_recovery` đọc dữ liệu local và chỉ thay đúng giờ hết hàng. Lượt chạy thử 200 cặp xác nhận bản viết lại trùng bản gốc (`equivalence_ok=True`, `recovery_equivalence_ok=True`, chênh `sale_amount_pred` tối đa 2,47e-07 do làm tròn float32).

## 3. Kết quả
| Chỉ số | DLinear (nhóm) | DLinear (bài báo) | TimesNet (nhóm) | TimesNet (bài báo) |
|---|---|---|---|---|
| WAPE MNAR | **30,32%** | 29,99% | 27,81% | 27,62% |
| WPE MNAR | **−14,38%** | −1,28% | 2,04% | 1,43% |
| Decoupling Score | **−0,15** (−0,151151) | −0,16 | +0,07 | +0,07 |
| Raw Sales Decoupling | −0,57 (−0,566447) | −0,57 | −0,57 | −0,57 |

- Lượt MNAR (seed 1024): che thêm 9.163.425 điểm giờ (tỷ lệ thực tế 15,88%), đánh giá trên 783.078 ngày — trùng Task 9. Training loss 0,1112 → 0,0782 sau 5 epoch; 276 giây; RAM cao nhất 8,4 GB trên Colab T4.
- Lượt khôi phục (seed 2024): thay 14.311.536 giờ hết hàng; training loss 0,1044 → 0,0732; 375 giây; RAM cao nhất 7,3 GB.

Tệp `demand_dlinear.parquet`: 4.500.000 dòng × 20 cột, 81.531.473 bytes, SHA-256 `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b`; đối soát 0 lỗi.

## 4. Thảo luận
- **WAPE tái lập được:** DLinear 30,32% so với 29,99% của bài báo (+0,33 điểm %), mức lệch tương đương TimesNet ở Task 9 (+0,19). Thứ hạng giữ nguyên: DLinear kém TimesNet khoảng 2,5 điểm WAPE, như bài báo (2,37).
- **WPE không tái lập được:** −14,38% so với −1,28% của bài báo. DLinear của nhóm khôi phục nhu cầu tại các điểm bị che **thấp hơn thực tế khoảng 14%**, trong khi TimesNet chỉ lệch +2,04%. Vì dữ liệu, mặt nạ che (trùng Task 9) và công thức đánh giá đã được kiểm chứng trùng mã gốc, còn mô hình dùng nguyên mã tác giả, chênh lệch nằm ở cơ chế huấn luyện trong mã nguồn công bố: (1) khác với `_TimesNet` có bước `nonstationary_norm` chuẩn hóa theo các giờ còn hàng, lớp `_DLinear` trong `pypots` của tác giả điền `0.0` vào toàn bộ các vị trí khuyết (~45% số bước) rồi đưa thẳng qua bộ lọc trung bình trượt `AvgPool1d(17)` và huấn luyện bằng loss `L1/MAE` trên dữ liệu 69% số giờ bằng 0 (Task 5), làm đường xu hướng và dự đoán bị kéo thấp mạnh; (2) khác phiên bản thư viện (`torch 2.14` so với `2.0.1` của tác giả) và tính không tất định trên GPU; (3) bài báo có thể đã chạy DLinear với cấu hình khác mã công bố (`models.py` đặt `individual=False`).
- **Decoupling Score tái lập được:** DLinear −0,15 so với −0,16 của bài báo; Raw Sales −0,566447 trùng Task 10. DLinear chỉ giảm tương quan âm giữa số giờ hết hàng và nhu cầu từ −0,57 xuống −0,15, tức nhu cầu khôi phục vẫn còn bị kéo thấp ở những ngày hết hàng nhiều, kém xa TimesNet (+0,07). Điều này nhất quán với WPE âm ở lượt MNAR.
- **Tác động lên Task 13, 14:** bài báo cho SSA_DLinear Overall WAPE 30,00% / WPE −1,49%. Do nhu cầu DLinear của nhóm thiên thấp, SSA_DLinear và DLinear_DLinear có thể cho WPE âm hơn số bài báo; nên đọc kết quả hai task đó cùng với phát hiện này.
- **Hướng kiểm tra thêm (ngoài phạm vi tái lập):** chạy lại lượt MNAR với `individual=True` hoặc nhiều epoch hơn (mỗi lượt chỉ ~5 phút) để thử giả thuyết (1) và (3); kết quả phải ghi rõ là cấu hình ngoài mã gốc.

## 5. Bàn giao
- [Notebook đã chạy](../Task12_DLinear_Recovery/notebooks/12_dlinear_recovery.ipynb), [runner tiết kiệm RAM](../Task12_DLinear_Recovery/run_task12.py), [chỉ số MNAR](../Task12_DLinear_Recovery/results/dlinear_mnar_metrics.csv), [chỉ số Decoupling](../Task12_DLinear_Recovery/results/dlinear_decoupling_metrics.csv), [đối soát Parquet](../Task12_DLinear_Recovery/results/demand_file_check.csv), [log MNAR](../Task12_DLinear_Recovery/results/full/dlinear_mnar.log), [log khôi phục](../Task12_DLinear_Recovery/results/full/dlinear_recovery.log), [metadata](../Task12_DLinear_Recovery/results/run_metadata.json) và [biên bản kèm link Google Drive](../Task12_DLinear_Recovery/run_info.md) (đã mở quyền truy cập công khai và kiểm chứng SHA-256 `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b` cho Task 13 và Task 14 ngày 23/11/2026).
