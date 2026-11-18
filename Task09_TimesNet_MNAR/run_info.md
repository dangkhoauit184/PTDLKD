# Thông tin chạy Task 9 — TimesNet MNAR

**Cách tái lập:** mở `notebooks/09_timesnet_mnar.ipynb` trên Colab (GPU T4), sửa `DATA_PATH`, `OUT_DIR` ở mục 0 nếu cần, rồi chạy lần lượt các ô (xem [README](README.md) mục 4).

## Đầu vào

| Mục | Giá trị |
|---|---|
| File train | `train.parquet` (106.436.287 byte), tải trực tiếp từ Hugging Face `Dingdong-Inc/FreshRetailNet-50K`, file `data/train.parquet` |
| SHA-256 | `6706832db892bbae4969c19d87e07975d2543d2ba7d7d4756360654785de5a3d` |
| Trùng file Parquet Task 6 | Không (Task 6 tạo Parquet riêng, SHA khác) – cùng split train: 4.500.000 dòng, 50.000 cặp × 90 ngày, 19 cột, không trùng khóa |
| Khoảng ngày | 2024-03-28 – 2024-06-25 |
| Eval | Không dùng |

## Mã và môi trường

- Repo nhóm: nhánh `feature/task09-timesnet-mnar`. Mã tác giả: `Dingdong-Inc/frn-50k-baseline` tại `8af694a09a5a427d1d50648d348c022565a781f2`, chạy `latent_demand_recovery/exp/app.py` với `pypots` đi kèm repo.
- Môi trường (Colab): Python 3.13.16, torch 2.14.1+cu130, NumPy 2.4.6, pandas 2.2.3, PyArrow 23.0.1, pygrinder 0.4, tsdb 0.3.1; GPU Tesla T4 (15 GB); RAM 12,7 GB.
- Không cài torch 2.0.1/NumPy 1.23.5 theo `requirements.txt` của tác giả vì không có bản cho Python 3.13 của Colab; dùng bản có sẵn. `pygrinder`, `tsdb` cài với `--no-deps`.

## Tham số thực tế

| Tham số | Giá trị | Ghi chú |
|---|---|---|
| model | TimesNet | |
| missing_rate | 0.3 | **Tham số mô phỏng theo ví dụ README của repo** (`python app.py --model TimesNet --missing_rate 0.3`); chưa xác minh là cấu hình chính xác của bài báo |
| Tỷ lệ che thực tế | 0,158843 | 9.163.425 điểm che thêm / 57.688.464 điểm giờ quan sát (không hết hàng) trong giờ 6..21 |
| Số điểm giờ che thêm | 9.163.425 | in bởi `load_data` (`valid_idx.sum()`); giống nhau ở cả ba lần nạp dữ liệu (16/11, 17/11, 18/11) |
| seed | 1024 | giữ như CLI gốc (`set_seed(seed_value=1024)`) |
| epochs / batch size | 5 / 128 | mặc định `CONFIG` của tác giả; các tham số khác giữ nguyên (lr 0,001, d_model 64, d_ffn 32, n_layers 2, top_k/n_patches 7, patience 5) |

## Thay đổi so với mã tác giả

- **Giữ nguyên:** mô hình TimesNet và `pypots` đi kèm repo, `CONFIG` (trừ `saving_path`), `mimic_missing`, `set_seed`, `_imputation` (fit → predict → cắt kênh OT → `np.where(imputation > 0, imputation, 0)`), thứ tự gọi `set_seed` → `demand_recovery`.
- **Viết lại `load_data` và `evaluation_mnar` để chạy được với 12,7 GB RAM** (bản gốc bị tắt tiến trình, `mã thoát -9`, ở bước tạo dữ liệu): đọc `train.parquet` local thay vì Hugging Face; sắp xếp theo `store_id, product_id, dt` như tác giả; tạo mảng đầu vào float32 bằng một lần cấp phát thay vì nhiều lần `np.concatenate` ở float64 (pypots vốn đổi sang float32 trước khi đưa vào mô hình); `evaluation_mnar` dùng lại mảng đã nạp. Công thức và thứ tự gọi số ngẫu nhiên giữ nguyên; hai hàm dùng chung một bộ dữ liệu → cùng tập, cùng thứ tự khóa.
- **Kiểm chứng tương đương** ở lượt chạy thử (200 cặp, cùng seed): mảng đầu vào, mặt nạ điểm che thêm, `ts_origin` và WAPE/WPE của bản viết lại trùng bản gốc của tác giả (`equivalence_ok=True`, xem log chạy thử).
- **Truyền sẵn `norm_val` toàn số 1 dạng `(n, 1, 6)`** cho bước dự đoán. Khi không có `norm_val`, pypots tự tạo `np.ones(X.shape)` ở float64 (3,5 GB) và một bản float32 (1,7 GB), làm tiến trình bị tắt vì hết RAM ngay khi bắt đầu predict. Mô hình chỉ nhân đầu ra với `norm_val` theo broadcast nên kết quả không đổi. Lần huấn luyện (17/11) chạy trước khi có sửa đổi này, tức dùng `norm_val` mặc định của pypots – cùng giá trị 1.
- **Tiếp tục từ checkpoint:** với `--resume_ckpt`, `model.fit` được thay bằng nạp checkpoint (`torch.load(..., weights_only=False)` rồi `load_state_dict`), phần còn lại của `_imputation` giữ nguyên.
- Ghi thêm các dòng `[task09]` vào log (nguồn dữ liệu, số điểm che thêm, tỷ lệ che thực tế, RAM trước/sau huấn luyện và dự đoán, số ngày được đánh giá).

## Lịch sử chạy

| Ngày | Tài khoản Colab | Việc | Kết quả |
|---|---|---|---|
| 16/11 | thành viên phụ trách Task 9 | Chạy thử 200 cặp + kiểm chứng tương đương | `equivalence_ok=True`; WAPE 28,55%, WPE −17,12% (chỉ kiểm tra luồng chạy) |
| 16/11 | thành viên phụ trách Task 9 | Huấn luyện đầy đủ 5 epoch (khoảng 3 giờ) | Xong huấn luyện; tiến trình dừng khi bắt đầu dự đoán, checkpoint lưu local nên mất |
| 17/11 | thành viên khác (hạn mức GPU tính theo tài khoản) | Huấn luyện đầy đủ 5 epoch, checkpoint lưu Drive | Training loss từng epoch giống hệt lần 16/11 (0,0643 → 0,0619); `mã thoát -9` (hết RAM) khi bắt đầu dự đoán → `results/full/timesnet_mnar.log` |
| 18/11 | cùng tài khoản 17/11 | Chạy thử lại tới bước kiểm chứng (`equivalence_ok=True`, sau đó dừng tay); ô 6b: nạp checkpoint 17/11, dự đoán, đánh giá | **WAPE 27,81%, WPE 2,04%**, `mã thoát 0`, 826 giây, RAM cao nhất 9,2 GB → `results/full/timesnet_mnar_predict_from_ckpt.log` |

## Kết quả

| Lượt | Quy mô | Epoch | WAPE | WPE | Trạng thái |
|---|---|---|---|---|---|
| Đầy đủ (huấn luyện 17/11 + dự đoán 18/11) | 50.000 cặp, 150.000 mẫu | 5 | 27,81% | 2,04% | ok |
| Bài báo (Bảng 2, TimesNet) | – | – | 27,62% | 1,43% | số công bố, chỉ để đối chiếu |

Số ngày được đánh giá: 783.078. Chênh lệch: WAPE +0,19 điểm %, WPE +0,61 điểm %.

## File kết quả

- `results/mnar_metrics.csv`: 1 dòng TimesNet (WAPE/WPE theo %, giữ dấu WPE).
- `results/full/timesnet_mnar.log`: log huấn luyện đầy đủ (17/11).
- `results/full/timesnet_mnar_predict_from_ckpt.log`: log dự đoán + đánh giá từ checkpoint (18/11), chứa hai dòng `wape`, `wpe` dùng cho CSV.
- `results/smoke/timesnet_mnar_smoke.log`: log chạy thử 18/11 (tới bước kiểm chứng tương đương).
- `results/run_metadata.json`: môi trường, SHA-256, tham số, lệnh chạy.
- Checkpoint `checkpoints/TimesNet/20261117_T014722/TimesNet.pypots` lưu trên Drive của tài khoản chạy 17/11; file imputation `.npy` chỉ lưu tạm trên Colab. Cả hai không đưa lên GitHub.

## Lệnh đã chạy

Huấn luyện (17/11):
```
/usr/bin/python3 -u /content/run_task09.py --author_exp /content/frn-50k-baseline/latent_demand_recovery/exp --data_path /content/drive/MyDrive/FRN50K/raw/data/train.parquet --work_dir /content/task09_work/full --model TimesNet --missing_rate 0.3 --seed 1024 --batch_size 128 --epochs 5 --saving_path /content/drive/MyDrive/PTDLKD/task09_outputs/checkpoints
```

Dự đoán + đánh giá từ checkpoint (18/11):
```
/usr/bin/python3 -u /content/run_task09.py --author_exp /content/frn-50k-baseline/latent_demand_recovery/exp --data_path /content/drive/MyDrive/FRN50K/raw/data/train.parquet --work_dir /content/task09_work/full --model TimesNet --missing_rate 0.3 --seed 1024 --batch_size 128 --epochs 5 --resume_ckpt /content/drive/MyDrive/PTDLKD/task09_outputs/checkpoints/TimesNet/20261117_T014722/TimesNet.pypots
```

Ghi chú: ô cuối của notebook in ra `run_info.md` tự động sinh lúc chạy; file này là bản đã bổ sung lịch sử chạy và sửa câu nguyên nhân (tiến trình bị tắt vì hết RAM, không phải do Colab ngắt kết nối).
