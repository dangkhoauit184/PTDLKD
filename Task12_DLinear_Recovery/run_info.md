# Thông tin chạy Task 12 — DLinear: khôi phục nhu cầu tiềm ẩn

**Cách tái lập:** mở `notebooks/12_dlinear_recovery.ipynb` trên Colab (GPU T4), sửa `DRIVE_TRAIN`, `OUT_DIR` ở mục 0 nếu cần, chạy lần lượt các ô.

## Đầu vào
| Mục | Giá trị |
|---|---|
| File train | `train.parquet` Task 6 — SHA-256 `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96` (khớp Task 6: True) |
| Quy mô | 4.500.000 dòng × 19 cột, 50.000 cặp × 90 ngày → 150.000 mẫu × 480 bước × 6 kênh |
| Eval | Không dùng |

## Mã và môi trường
- Repo nhóm: nhánh `feature/task12-dlinear-recovery`. Mã tác giả `Dingdong-Inc/frn-50k-baseline` @ `8af694a09a5a427d1d50648d348c022565a781f2`, chạy `latent_demand_recovery/exp/app.py` với `pypots` đi kèm repo; **không sửa file nào của tác giả** (các thay thế nằm trong runner `run_task12.py` ghi ở mục 3 của notebook).
- Python 3.13.16, torch 2.14.1+cu130, NumPy 2.4.6, pandas 2.2.3, pyarrow 23.0.1, pygrinder 0.4, tsdb 0.3.1; GPU: Tesla T4, 15360 MiB; RAM 12.7 GB.

## Siêu tham số DLinear (theo `models.py`, giữ nguyên)
`n_steps=480`, `n_features=6`, `moving_avg_window_size=17` (`patch_len // 2 * 2 + 1`, `patch_len=16`), `individual=False`, `d_model=64`, `ORT_weight=MIT_weight=1`, `epochs=5`, `batch_size=128`, `patience=5`, Adam `lr=0.001`, `weight_decay=1e-5`.
> Bảng phân công ghi `individual=True`; mã gốc tác giả truyền `individual=False`. Nhóm giữ đúng mã gốc.

## Thay đổi so với mã tác giả (chỉ trong runner)
- `load_data`, `evaluation_mnar`: giống Task 9 (đọc `train.parquet` local, sắp xếp `store_id, product_id, dt`, X float32 một lần cấp phát, `norm_val` toàn số 1 dạng `(n, 1, 6)`). DLinear dùng chung `DatasetForSAITS` và nhân `imputed_data * inputs['norm_val']` như TimesNet nên kết quả không đổi.
- `_demand_recovery`: đọc `train.parquet` local; chặn âm (đã có trong `_imputation`); chỉ thay `hours_sale_origin[..., 6:22]` tại đúng các giờ hết hàng, giữ nguyên 8 giờ đêm và giờ quan sát được; cộng 24 giờ thành `sale_amount_pred`; ghi Parquet bằng PyArrow (19 cột gốc nguyên vẹn + `sale_amount_pred`, không ghi cột index). So với bản gốc (ghi đè cả lát 6..21 bằng X float32), `sale_amount_pred` chỉ lệch do làm tròn float32: lượt chạy thử đo được `max_abs_diff = 2.474e-07`.
- Kiểm chứng tương đương ở lượt chạy thử (200 cặp): MNAR `equivalence_ok=True`; khôi phục `equivalence_ok=True`, `recovery_equivalence_ok=True`.
- `evaluation_decoupling`, `mimic_missing`, `set_seed`, `_imputation`, mô hình: nguyên mã tác giả.

## Lượt 1 — MNAR (`--missing_rate 0.3`, seed 1024)
| Mục | Nhóm | Bài báo (Bảng 2) |
|---|---|---|
| WAPE | 30.32% | 29.99% |
| WPE | -14.38% | -1.28% |
| Điểm giờ che thêm | 9,163,425 (Task 9: 9,163,425) | – |
| Ngày được đánh giá | 783,078 (Task 9: 783,078) | – |
| Tỷ lệ che thực tế | 0.158843 | – |

`missing_rate = 0.3` lấy theo ví dụ README của repo tác giả (giống Task 9), chưa xác minh là cấu hình chính xác của bài báo. Chạy liền một mạch. Thời gian: 276 giây; RAM tiến trình cao nhất: 8.4 GB.

## Lượt 2 — Khôi phục thực tế (`--missing_rate 0`, seed 2024)
- Seed thực dùng: `2024` (theo kế hoạch Task 2, giống Task 10).
- Số giờ hết hàng được thay: 14,311,536. Chạy liền một mạch. Thời gian: 375 giây; RAM cao nhất: 7.3 GB.

| Decoupling Score | Nhóm | Bài báo (Bảng 2) |
|---|---|---|
| Raw Sales (`sale_amount`) | -0.566447 | -0.57 |
| DLinear (`sale_amount_pred`) | -0.151151 | -0.16 |

## Tệp bàn giao `demand_dlinear.parquet` (cho Task 13, Task 14)
- Quy mô: 4.500.000 dòng × 20 cột (19 cột gốc + `sale_amount_pred`); đối soát `results/demand_file_check.csv`: mọi bộ đếm lỗi = 0; `sale_amount`, `hours_sale` gốc giữ nguyên 100%.
- Kích thước: `81,531,473` bytes | SHA-256: `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b`
- Đường dẫn Drive: `/content/drive/MyDrive/PTDLKD/Task12_DLinear_Recovery/full/demand_dlinear.parquet`
- Link chia sẻ: https://drive.google.com/file/d/1MDcD7cOyzcnoBu48I6eGUkSfwx8b3hkh/view?usp=drive_link
- Checkpoint `.pypots` (MNAR và khôi phục): https://drive.google.com/drive/folders/18MjIAn0RF705AxhluhvgomYmNepY5kTo?usp=sharing

## Lệnh đã chạy
```
/usr/bin/python3 -u /content/run_task12.py --author_exp /content/frn-50k-baseline/latent_demand_recovery/exp --data_path /content/frn_cache/train.parquet --work_dir /content/task12_work/full_mnar --model DLinear --missing_rate 0.3 --seed 1024 --batch_size 128 --epochs 5 --saving_path /content/drive/MyDrive/PTDLKD/Task12_DLinear_Recovery/checkpoints/mnar
/usr/bin/python3 -u /content/run_task12.py --author_exp /content/frn-50k-baseline/latent_demand_recovery/exp --data_path /content/frn_cache/train.parquet --work_dir /content/task12_work/full_recovery --model DLinear --missing_rate 0 --seed 2024 --batch_size 128 --epochs 5 --saving_path /content/drive/MyDrive/PTDLKD/Task12_DLinear_Recovery/checkpoints/recovery --out_parquet /content/task12_work/full/demand_dlinear.parquet
```
