# Task 12 — Khôi phục nhu cầu tiềm ẩn bằng DLinear (Bảng 2 & xuất Parquet)

## 1. Mục tiêu
Chạy mô hình khôi phục thứ hai **DLinear** bằng mã gốc của tác giả (`latent_demand_recovery/exp/app.py`, `frn-50k-baseline @ 8af694a`) ở hai chế độ:
1. **MNAR** (`--missing_rate 0.3`, seed 1024): lấy WAPE/WPE để đối chiếu cột **DLinear** trong **Bảng 2** và so với TimesNet (Task 9).
2. **Khôi phục thực tế** (`--missing_rate 0`, seed 2024): xuất `demand_dlinear.parquet` cho **Task 13** (`SSA_DLinear`) và **Task 14** (`DLinear_DLinear`), tính **Decoupling Score** đối chiếu Bảng 2.

## 2. Kết quả đối chiếu Bảng 2
| Chỉ số | Nhóm tự chạy | Bài báo | Chênh lệch | TimesNet (Task 9/10) |
| :--- | :---: | :---: | :---: | :---: |
| WAPE MNAR (%) | **30.32** | 29.99 | +0.33 pp | 27.81 |
| WPE MNAR (%) | **-14.38** | -1.28 | -13.10 pp | 2.04 |
| Decoupling — Raw Sales | **-0.566447** (-0.57) | -0.57 | 0.00 | -0.57 |
| Decoupling — Recovered | **-0.151151** (-0.15) | -0.16 | +0.01 | +0.07 |

- Lượt MNAR che **9.163.425** điểm giờ, đánh giá trên **783.078** ngày, trùng Task 9 (cùng seed 1024, cùng `train.parquet`).
- **WAPE và Decoupling Score tái lập được; WPE MNAR thì không** (DLinear của nhóm khôi phục thấp hơn thực tế ~14%, bài báo ~1,3%). Quy trình dữ liệu/đánh giá đã kiểm chứng trùng mã gốc (`equivalence_ok=True`), phần mô hình dùng nguyên mã tác giả; nguyên nhân lệch chưa xác định — xem [báo cáo](../reports/Task12_Report.md).
- Siêu tham số giữ nguyên `models.py`: `n_steps=480`, `n_features=6`, `moving_avg_window_size=17`, `individual=False`, `d_model=64`, `epochs=5`, `batch_size=128`, `lr=0.001`.

## 3. Tệp `demand_dlinear.parquet` (bàn giao Task 13, Task 14)
- `4.500.000` dòng × `20` cột (`19` cột gốc + `sale_amount_pred`), `81.531.473` bytes, SHA-256 `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b`.
- Đối soát ([results/demand_file_check.csv](results/demand_file_check.csv)): 0 khóa trùng/thiếu/thừa, 0 giá trị thiếu/vô cực/âm; `sale_amount`, `hours_sale` gốc giữ nguyên.
- Link Google Drive: xem [run_info.md](run_info.md). File Parquet và checkpoint `.pypots` **không** đưa lên GitHub.

## 4. Cấu trúc thư mục
- [Notebook đã chạy](notebooks/12_dlinear_recovery.ipynb): xác minh SHA-256, chạy thử 200 cặp có kiểm chứng tương đương, chạy MNAR và khôi phục đầy đủ, đối soát file, xuất chỉ số.
- [run_task12.py](run_task12.py): runner (kế thừa Task 9) — notebook tự ghi lại file này ở mục 3.
- [results/dlinear_mnar_metrics.csv](results/dlinear_mnar_metrics.csv), [results/dlinear_decoupling_metrics.csv](results/dlinear_decoupling_metrics.csv), [results/demand_file_check.csv](results/demand_file_check.csv)
- Log: [results/full/dlinear_mnar.log](results/full/dlinear_mnar.log), [results/full/dlinear_recovery.log](results/full/dlinear_recovery.log), [results/smoke/dlinear_smoke.log](results/smoke/dlinear_smoke.log); [metadata](results/run_metadata.json), [biên bản chạy](run_info.md), [báo cáo Task 12](../reports/Task12_Report.md).

## 5. Chạy lại
1. Mở notebook trên Colab, chọn **GPU T4**. Đặt `train.parquet` Task 6 ở `MyDrive/PTDLKD/train.parquet` (hoặc sửa `DRIVE_TRAIN`).
2. Chạy mục 0 → 4. Mục 4 phải in `CHẠY THỬ OK`.
3. Chạy mục 5 (MNAR) và mục 6 (khôi phục). Nếu bị ngắt sau dòng `Saved the model`, chạy lại mục 0 → 3 rồi ô **5b** / **6b** để dự đoán từ checkpoint.
4. Chạy mục 7 → 11. Kết quả đạt khi số điểm che = 9.163.425, `demand_file_check.csv` toàn 0, và CSV khớp log.
