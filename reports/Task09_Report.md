# Báo cáo Task 09: TimesNet với thiếu nhân tạo (MNAR)

## 1. Tóm tắt thiết lập thực nghiệm
- **Mô hình:** TimesNet trong `latent_demand_recovery` của tác giả (`frn-50k-baseline` tại commit `8af694a`), dùng `pypots` đi kèm repo, `CONFIG` mặc định (5 epoch, batch 128, lr 0,001), seed 1024 như CLI gốc.
- **Dữ liệu:** tập `train.parquet` (4.500.000 dòng, 50.000 cặp cửa hàng–sản phẩm × 90 ngày), chia thành 150.000 mẫu 30 ngày × 16 giờ (giờ 6..21) × 6 kênh (doanh số theo giờ, 4 biến ngoại sinh chuẩn hóa, vị trí giờ). Giờ hết hàng thực được coi là thiếu.
- **Thiếu nhân tạo:** hàm `mimic_missing` của tác giả với `missing_rate = 0.3` – **tham số mô phỏng theo ví dụ README của repo**, chưa xác minh là cấu hình chính xác của bài báo. Thực tế che thêm 9.163.425 điểm giờ, bằng **15,88%** số điểm giờ quan sát được.
- **Tiêu chuẩn đánh giá:** `evaluation_mnar` của tác giả – so tổng doanh số theo ngày sau khi điền giá trị mô hình khôi phục vào các giờ 6..21 với doanh số thật, chỉ trên 783.078 ngày có điểm bị che thêm và không có hết hàng thực.

## 2. Kết quả định lượng và đối chiếu Bảng 2
| Mô hình | WAPE thực chạy | WPE thực chạy | WAPE bài báo | WPE bài báo | Chênh lệch WAPE | Chênh lệch WPE |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **TimesNet** | 27.81% | 2.04% | 27.62% | 1.43% | +0.19 pp | +0.61 pp |

## 3. Nhận xét
- WAPE gần khớp Bảng 2 (chênh 0,19 điểm phần trăm). WPE dương ở cả kết quả nhóm và bài báo, tức mô hình khôi phục hơi cao hơn doanh số thật trên các ngày bị che; mức chênh WPE là 0,61 điểm phần trăm.
- Các nguồn chênh lệch có thể có: môi trường khác tác giả (Python 3.13, torch 2.14 trên GPU T4 thay vì torch 2.0.1), tính không tất định của huấn luyện trên GPU, và việc chưa xác nhận `missing_rate = 0.3` là cấu hình bài báo dùng. Phần nạp dữ liệu và tạo thiếu là tất định: số điểm che thêm giống nhau ở mọi lần chạy, và training loss từng epoch của hai lần huấn luyện độc lập (16/11, 17/11) trùng nhau.
- Để chạy được với 12,7 GB RAM của Colab miễn phí, `load_data`/`evaluation_mnar` được viết lại (cùng công thức, cùng thứ tự số ngẫu nhiên) và `norm_val` được truyền sẵn ở dạng nhỏ. Bản viết lại được kiểm chứng trùng bản gốc trên 200 cặp (`equivalence_ok=True`). Chi tiết ở `run_info.md`.

## 4. Bàn giao

[Notebook đã chạy](../Task09_TimesNet_MNAR/notebooks/09_timesnet_mnar.ipynb), [CSV kết quả](../Task09_TimesNet_MNAR/results/mnar_metrics.csv), [log huấn luyện](../Task09_TimesNet_MNAR/results/full/timesnet_mnar.log), [log dự đoán và đánh giá](../Task09_TimesNet_MNAR/results/full/timesnet_mnar_predict_from_ckpt.log), [log chạy thử](../Task09_TimesNet_MNAR/results/smoke/timesnet_mnar_smoke.log) và [hướng dẫn tái lập](../Task09_TimesNet_MNAR/run_info.md). Checkpoint mô hình lưu trên Drive, không đưa lên GitHub.
