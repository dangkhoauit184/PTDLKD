# Task 09 — TimesNet với thiếu nhân tạo (MNAR)

## 1. Mục tiêu
Chạy TimesNet trong `latent_demand_recovery` của tác giả với thiếu nhân tạo (`--missing_rate 0.3`) để lấy WAPE/WPE, đối chiếu với cột **TimesNet** trong **Bảng 2** của bài báo *FreshRetailNet-50K*. Task 9 không xuất nhu cầu làm đầu vào dự báo (phần đó thuộc Task 10).

## 2. Kết quả đối chiếu
| Mô hình | missing_rate | Số điểm giờ che thêm | WAPE (%) | WPE (%) | Paper WAPE (%) | Paper WPE (%) | Delta WAPE (pp) | Delta WPE (pp) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TimesNet** | 0.3 | 9.163.425 | 27.81 | 2.04 | 27.62 | 1.43 | +0.19 | +0.61 | ok |

- `missing_rate = 0.3` là **tham số mô phỏng theo ví dụ README của repo tác giả**, chưa xác minh là cấu hình chính xác của bài báo. Tỷ lệ che thực tế là **15,88%** số điểm giờ quan sát được trong giờ 6..21.
- WAPE/WPE tính theo `evaluation_mnar` của tác giả: tổng doanh số theo ngày, chỉ trên 783.078 ngày có điểm bị che thêm và không hết hàng thực.

## 3. Cấu trúc thư mục
- [Notebook đã chạy](notebooks/09_timesnet_mnar.ipynb): cài môi trường, xác nhận dữ liệu, chạy thử có kiểm chứng tương đương, chạy đầy đủ, lưu kết quả.
- [CSV kết quả](results/mnar_metrics.csv): 1 dòng TimesNet, WAPE/WPE theo %, giữ dấu WPE.
- [Log huấn luyện đầy đủ](results/full/timesnet_mnar.log) và [log dự đoán + đánh giá từ checkpoint](results/full/timesnet_mnar_predict_from_ckpt.log): hai dòng `wape`, `wpe` (dạng tỷ lệ) nằm trong log thứ hai.
- [Log chạy thử](results/smoke/timesnet_mnar_smoke.log): 200 cặp, có dòng `equivalence_ok=True`.
- [Thông tin chạy lại](run_info.md) và [metadata](results/run_metadata.json): môi trường, SHA-256 dữ liệu, tham số, lệnh chạy, thay đổi so với mã tác giả.

## 4. Chạy lại
1. Mở notebook trên Colab, chọn **GPU T4**. Không cần dữ liệu có sẵn: nếu `DATA_PATH` chưa có file, mục 0 tự tải `data/train.parquet` từ Hugging Face (`Dingdong-Inc/FreshRetailNet-50K`).
2. Chạy lần lượt mục 0 → 5. Mục 5 (200 cặp, khoảng 2 phút) phải in `equivalence_ok=True` và `CHẠY THỬ OK`.
3. Chạy mục 6 (khoảng 3 giờ huấn luyện + 15 phút dự đoán trên T4). Checkpoint được lưu lên Drive (`task09_outputs/checkpoints/`). Nếu phiên bị ngắt sau dòng `Saved the model`, chạy lại mục 0 → 4 rồi ô **6b** để dự đoán từ checkpoint mà không huấn luyện lại.
4. Chạy mục 7 để ghi CSV, metadata và `run_info.md` vào `OUT_DIR` (mặc định `MyDrive/PTDLKD/task09_outputs`). Kết quả đạt khi CSV có `status = ok` và hai chỉ số khớp log sau khi đổi sang %.

Checkpoint (`.pypots`) và file imputation `.npy` không đưa lên GitHub.
