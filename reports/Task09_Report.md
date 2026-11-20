# Báo cáo Task 09: TimesNet với thiếu nhân tạo (MNAR)

## 1. Tóm tắt thiết lập thực nghiệm
- **Mô hình:** TimesNet trong `latent_demand_recovery` của tác giả (`frn-50k-baseline` tại commit `8af694a`), dùng `pypots` đi kèm repo, `CONFIG` mặc định (5 epoch, batch 128, lr 0,001), seed 1024 như CLI gốc.
- **Dữ liệu:** tập `train.parquet` (4.500.000 dòng, 50.000 cặp cửa hàng–sản phẩm × 90 ngày), chia thành 150.000 mẫu 30 ngày × 16 giờ (giờ 6..21) × 6 kênh (doanh số theo giờ, 4 biến ngoại sinh chuẩn hóa, vị trí giờ). Giờ hết hàng thực được coi là thiếu.
- **Thiếu nhân tạo:** hàm `mimic_missing` của tác giả với `missing_rate = 0.3` – **tham số mô phỏng theo ví dụ README của repo**, chưa xác minh là cấu hình chính xác của bài báo. Thực tế che thêm 9.163.425 điểm giờ, bằng **15,88%** số điểm giờ quan sát được.
- **Tiêu chuẩn đánh giá:** `evaluation_mnar` của tác giả – so tổng doanh số theo ngày sau khi điền giá trị mô hình khôi phục vào các giờ 6..21 với doanh số thật, chỉ trên 783.078 ngày có điểm bị che thêm và không có hết hàng thực.

## 2. Kết quả định lượng và đối chiếu Bảng 2
| Mô hình | WAPE thực chạy | WPE thực chạy | WAPE bài báo | WPE bài báo | Chênh lệch WAPE | Chênh lệch WPE |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **TimesNet** | 27.81% | +2.04% | 27.62% | +1.43% | +0.19 pp | +0.61 pp |

## 3. Nhận xét kỹ thuật và ý nghĩa nghiệp vụ
- **Độ sát với Bảng 2 và xu hướng sai số:** WAPE tự chạy (`27.81%`) bám rất sát mức công bố của bài báo (`27.62%`, chênh `+0.19 pp`), thấp hơn rõ rệt so với mức tham chiếu của các mô hình khôi phục khác trong Bảng 2 (như DLinear `29.99%` hay ImputeFormer `35.65%`). WPE mang dấu dương nhẹ ở cả kết quả tự chạy (`+2.04%`) và bài báo (`+1.43%`, chênh `+0.61 pp`), cho thấy mô hình khôi phục đã triệt tiêu độ chệch âm do thiếu hàng mà không gây thổi phồng nhu cầu quá mức.
- **Giải thích cơ chế tạo thiếu và độ lệch nhỏ:** Hàm `mimic_missing` kết hợp che theo cụm nhiều ngày liên tiếp (`conti_idx`, độ dài 3–7 ngày) và che nửa đầu/nửa cuối ngày (`intra_idx`) để mô phỏng hành vi cạn tồn kho thực tế, nên tham số `missing_rate = 0.3` tạo ra tỷ lệ che thực tế `15,88%` trên các giờ còn hàng (`9.163.425 / 57.688.464` điểm giờ). Phần tạo thiếu hoàn toàn tất định theo `seed = 1024` (số điểm che và training loss từng epoch `0.0643 -> 0.0619` lặp lại khớp nhau qua hai lần huấn luyện độc lập ngày 16/11 và 17/11). Độ chênh nhỏ so với bài báo có thể đến từ khác biệt phiên bản thư viện/phần cứng (`Python 3.13`, `PyTorch 2.14.1+cu130` trên GPU Tesla T4 so với `PyTorch 2.0.1`) và việc bài báo không công bố tường minh tham số `missing_rate` đã dùng cho Bảng 2.
- **Tối ưu hóa bộ nhớ có kiểm chứng tương đương:** Để vận hành trong giới hạn 12,7 GB RAM của Google Colab miễn phí, `load_data` và `evaluation_mnar` được tối ưu cấp phát `float32` một lần và truyền sẵn `norm_val` dạng `(n, 1, 6)` khi dự đoán (giữ RAM đỉnh ở `9,2 GB`). Bản tối ưu đã được kiểm chứng cho kết quả trùng khớp 100% với hàm gốc trên tập thử 200 cặp (`equivalence_ok=True`) và là cơ sở kỹ thuật trực tiếp để triển khai Task 10. Chi tiết ở [run_info.md](../Task09_TimesNet_MNAR/run_info.md).

## 4. Bàn giao

[Notebook đã chạy](../Task09_TimesNet_MNAR/notebooks/09_timesnet_mnar.ipynb), [CSV kết quả](../Task09_TimesNet_MNAR/results/mnar_metrics.csv), [log huấn luyện](../Task09_TimesNet_MNAR/results/full/timesnet_mnar.log), [log dự đoán và đánh giá](../Task09_TimesNet_MNAR/results/full/timesnet_mnar_predict_from_ckpt.log), [log chạy thử](../Task09_TimesNet_MNAR/results/smoke/timesnet_mnar_smoke.log) và [hướng dẫn tái lập](../Task09_TimesNet_MNAR/run_info.md). Checkpoint mô hình lưu trên Drive, không đưa lên GitHub.
