# Thông tin chạy Task 14 — Dự báo 7 ngày bằng Mạng học sâu DLinear (Bảng 3)

**Cách tái lập và kiểm chứng:** mở [notebooks/14_dlinear_forecasting.ipynb](notebooks/14_dlinear_forecasting.ipynb) để kiểm tra khớp SHA-256 của 4 tệp Parquet, đối soát bản vá [code_changes.diff](code_changes.diff), kiểm tra 4 tệp log thực thi GPU và tổng hợp bảng chỉ số 9 dòng (hoặc đặt biến môi trường `TASK14_RUN_GPU=1` trên Colab GPU T4 / máy CUDA để huấn luyện lại từ đầu).

## 1. Dữ liệu đầu vào (đối soát SHA-256 100%)

| Tệp dữ liệu | Nguồn | Quy mô | SHA-256 |
|---|---|---|---|
| `train.parquet` | [Task 6](../Task06_Data_Preparation/README.md) (`Task06_Data_Preparation/train.parquet`) | `4.500.000 × 19` (`61.075.680` bytes) | `b7e01c711bc4fa0598c4a8cf4e8b97769275b1afa1792d98fd8428c76838bc96` |
| `eval.parquet` | [Task 6](../Task06_Data_Preparation/README.md) (`Task06_Data_Preparation/eval.parquet`) | `350.000 × 19` (`5.451.872` bytes) | `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872` |
| `demand_timesnet.parquet` | [Task 10](../Task10_TimesNet_Recovery/run_info.md) (Google Drive) | `4.500.000 × 20` (`81.562.029` bytes) | `c34f4eafe087d225865a624ef24d213af566496541458c3075f6e596d9f1d694` |
| `demand_dlinear.parquet` | [Task 12](../Task12_DLinear_Recovery/run_info.md) (Google Drive) | `4.500.000 × 20` (`81.531.473` bytes) | `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b` |

## 2. Môi trường chạy thực tế và Bản vá mã nguồn

- **Người thực hiện:** Dương Trọng Toàn (`UTAKaoru`).
- **Repo nhóm đối chiếu:** nhánh `feature/task14-dlinear-forecasting` tách từ commit nền `84520f9` trên `main`.
- **Mã tác giả đối chiếu:** [`Dingdong-Inc/frn-50k-baseline` @ `8af694a09a5a427d1d50648d348c022565a781f2`](https://github.com/Dingdong-Inc/frn-50k-baseline/tree/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/DLinear) (`demand_forecasting/DLinear`).
- **Môi trường huấn luyện GPU:** Windows CUDA (`Use GPU: cuda:0`), Conda env `frn50k`, Python `3.8.20`, PyTorch `2.0.1+cu118` (đúng phiên bản PyTorch gốc của tác giả; đặt `--num_workers 0` trên Windows để tránh lỗi tiến trình con DataLoader).
- **Thay đổi mã nguồn ([code_changes.diff](code_changes.diff)):**
  1. Thêm hai tham số `--train_path` và `--eval_path` vào `main.py`.
  2. Cập nhật `Exp_Main.data_organization` trong `exp/exp_main.py` đọc trực tiếp `train.parquet` gốc và `eval.parquet` thay vì gọi `load_dataset("Dingdong-Inc/FreshRetailNet-50K")` — bảo đảm **`psd` luôn được tính từ `sale_amount` gốc của `train.parquet`** cho cả 3 cấu hình (`Overall = 206.562`, `Low Sale = 153.208`, `High Sale = 53.354`).
  3. **Giữ nguyên 100%** kiến trúc mô hình `DLinear`, `fix_seed = 2025`, cách truyền cờ `--revin False` (`bool("False") == True` bật chuẩn hóa `RevIN` đúng như `train_predict.sh` gốc của tác giả), `scale=True`, `loss=mae`, `features=MS`, `total_seq_len=90`, `seq_len=62`, `moving_avg=28`, `pred_len=7`, `enc_in=7`, `batch_size=1024`, `train_epochs=6`, `learning_rate=0.001`.

## 3. Lệnh thực thi chính thức

```bash
# 1. DLinear_RawSales (des=raw_l1)
python -u main.py --is_training 1 --train_only True --model DLinear --scale True --loss mae --features MS \
  --data censored_dataset --data_path <train.parquet> --train_path <train.parquet> --eval_path <eval.parquet> \
  --target sale_amount --revin False --total_seq_len 90 --seq_len 62 --pred_len 7 --moving_avg 28 --enc_in 7 \
  --des raw_l1 --do_predict --itr 1 --batch_size 1024 --train_epochs 6 --learning_rate 0.001 --num_workers 0

# 2. DLinear_TimesNet (des=timesnet_l1)
python -u main.py --is_training 1 --train_only True --model DLinear --scale True --loss mae --features MS \
  --data recovered_dataset --data_path <demand_timesnet.parquet> --train_path <train.parquet> --eval_path <eval.parquet> \
  --target sale_amount_pred --revin False --total_seq_len 90 --seq_len 62 --pred_len 7 --moving_avg 28 --enc_in 7 \
  --des timesnet_l1 --do_predict --itr 1 --batch_size 1024 --train_epochs 6 --learning_rate 0.001 --num_workers 0

# 3. DLinear_DLinear (des=dlinear_l1)
python -u main.py --is_training 1 --train_only True --model DLinear --scale True --loss mae --features MS \
  --data recovered_dataset --data_path <demand_dlinear.parquet> --train_path <train.parquet> --eval_path <eval.parquet> \
  --target sale_amount_pred --revin False --total_seq_len 90 --seq_len 62 --pred_len 7 --moving_avg 28 --enc_in 7 \
  --des dlinear_l1 --do_predict --itr 1 --batch_size 1024 --train_epochs 6 --learning_rate 0.001 --num_workers 0
```

*(Ghi chú kỹ thuật về log: trong đầu ra stdout cuối mỗi lượt, `pandas` mặc định rút gọn chiều ngang bằng dấu `...` ở các cột giữa, nhưng hàm `cal_metrics` của `exp_main.py` đồng thời ghi đầy đủ toàn bộ 10 cột ra `results/<setting>/metrics_res.parquet`; bảng [dlinear_forecasting_metrics.csv](results/dlinear_forecasting_metrics.csv) được trích xuất trực tiếp từ `metrics_res.parquet` và khớp 100% các cột `sample_cnt`, `mae` in trong log).*

## 4. Tóm tắt trạng thái các lượt chạy

| Lượt chạy | `--des` | Cửa sổ `train` | Số chuỗi `pred` | Loss Epoch 1 → 6 | `exit_code` | Log thực thi |
|---|---|---:|---:|---|---:|---|
| Smoke (200 cặp) | `raw_smoke` | `4.400` | `200` | `0.3842 → 0.3618` | `0` | [results/smoke/dlinear_smoke.log](results/smoke/dlinear_smoke.log) |
| `DLinear_RawSales` | `raw_l1` | `1.100.000` | `50.000` | `0.2660 → 0.2625` | `0` | [results/full/dlinear_raw_sales.log](results/full/dlinear_raw_sales.log) |
| `DLinear_TimesNet` | `timesnet_l1` | `1.100.000` | `50.000` | `0.2210 → 0.2181` | `0` | [results/full/dlinear_timesnet.log](results/full/dlinear_timesnet.log) |
| `DLinear_DLinear` | `dlinear_l1` | `1.100.000` | `50.000` | `0.2449 → 0.2417` | `0` | [results/full/dlinear_dlinear.log](results/full/dlinear_dlinear.log) |

- **Bảng kết quả 9 dòng chuẩn 10 cột:** [results/dlinear_forecasting_metrics.csv](results/dlinear_forecasting_metrics.csv) (giá trị gốc 4 chữ số thập phân lưu kèm trong [results/run_metadata.json](results/run_metadata.json)).
- **Báo cáo phân tích:** [../reports/Task14_Report.md](../reports/Task14_Report.md) (trọng số `.pth` và mảng dự báo `.npy` không đẩy lên Git theo quy ước).
