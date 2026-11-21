# Báo cáo Task 10: Khôi phục nhu cầu tiềm ẩn bằng TimesNet tại giờ hết hàng thực tế

## 1. Tóm tắt thiết lập thực nghiệm
- **Mô hình & cấu hình:** `TimesNet` trong `latent_demand_recovery` của tác giả (`frn-50k-baseline` tại commit `8af694a`), chạy ở chế độ khôi phục thực tế `--missing_rate 0` (không tạo thêm điểm thiếu nhân tạo, không sử dụng tập `eval`), `EPOCHS = 5`, `batch_size = 128`, `lr = 0.001`, `n_steps = 480`, `n_features = 6`, `top_k = 7`, `n_kernels = 5`.
- **Hạt giống ngẫu nhiên & môi trường:** Đặt `seed = 2024` theo kế hoạch thực nghiệm ở Task 2 (ghi nhận tường minh trong [code_changes.diff](../Task10_TimesNet_Recovery/code_changes.diff) và log `ACTIVE_SEED = 2024`). Thực thi trên Google Colab với GPU **NVIDIA L4** (`Python 3.13.16`, `PyTorch 2.14.1+cu130`), hoàn tất huấn luyện 5 epoch (`loss: 0.0628 -> 0.0602`), khôi phục và đánh giá trong `84,66` phút.
- **Dữ liệu đầu vào:** Tập `train.parquet` chuẩn đã xác nhận ở Task 6 (`4.500.000` dòng × `19` cột, SHA-256: `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96`). Cả `load_data` và `_demand_recovery` đều đọc cùng tệp này và sắp xếp ổn định theo khóa `['store_id', 'product_id', 'dt']`.

## 2. Kết quả Decoupling Score ($\rho_{DS}$) và đối chiếu Bảng 2
| Phương pháp | Cột dữ liệu | $\rho_{DS}$ thực chạy (log) | $\rho_{DS}$ làm tròn | $\rho_{DS}$ bài báo (Bảng 2) | Chênh lệch |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Raw Sales (Doanh số gốc)** | `sale_amount` | `-0.566447` | **-0.57** | -0.57 | **0.00** |
| **TimesNet (Nhu cầu khôi phục)** | `sale_amount_pred` | `0.069918` | **+0.07** | +0.07 | **0.00** |

## 3. Kiểm định tệp `demand_timesnet.parquet` và ý nghĩa nghiệp vụ
- **Độ chính xác tái lập Bảng 2:** Chỉ số tách rời $\rho_{DS}$ của cả doanh số gốc (`-0.566447`) lẫn nhu cầu khôi phục bằng TimesNet (`+0.069918`) khớp hoàn toàn với con số công bố trong Bảng 2 của bài báo (`-0.57` và `+0.07`) ở độ chính xác hai chữ số thập phân. Việc $\rho_{DS}$ dịch chuyển từ tương quan nghịch mạnh (`-0.57` — càng hết hàng nhiều giờ thì doanh số ghi nhận càng tụt giảm) về sát `0` (`+0.07`) chứng minh TimesNet đã bóc tách thành công nhu cầu thực khỏi rào cản thiếu hụt tồn kho.
- **Thống kê nhu cầu trước và sau khôi phục:** Trên toàn bộ `4.500.000` dòng `train`, trung bình doanh số ngày tăng từ `0.9986` (`sale_amount` quan sát) lên `1.2065` (`sale_amount_pred`, tăng khoảng `+20.8%`), trung vị tăng từ `0.7000` lên `0.8000` — phản ánh trực tiếp lượng cầu bị che khuất trong khoảng `19.88%` số giờ kinh doanh hết hàng đã phát hiện ở bước EDA.
- **Đảm bảo toàn vẹn dữ liệu đầu vào cho Task 11:** Tệp `demand_timesnet.parquet` (`81.562.029` bytes, SHA-256: `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694`) đạt `0` lỗi trên tất cả hạng mục kiểm tra trong [demand_file_check.csv](../Task10_TimesNet_Recovery/results/demand_file_check.csv) (đủ `4.500.000` dòng × `20` cột, không trùng/thiếu/thừa khóa, không có giá trị NaN/vô cực/âm, và giữ nguyên 100% giá trị gốc của `sale_amount` để Task 11 dùng tính `psd` phân nhóm công bằng với Task 8).

## 4. Bàn giao
[Notebook đã chạy](../Task10_TimesNet_Recovery/notebooks/10_timesnet_recovery.ipynb), [diff mã nguồn](../Task10_TimesNet_Recovery/code_changes.diff), [bảng Decoupling Score](../Task10_TimesNet_Recovery/results/decoupling_metrics.csv), [bảng kiểm định tệp Parquet](../Task10_TimesNet_Recovery/results/demand_file_check.csv), [log đầy đủ](../Task10_TimesNet_Recovery/results/full/timesnet_recovery.log), [metadata JSON](../Task10_TimesNet_Recovery/results/run_metadata.json) và [biên bản chạy kèm link Drive `demand_timesnet.parquet`](../Task10_TimesNet_Recovery/run_info.md).
