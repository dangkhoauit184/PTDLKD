# Thông tin chạy Task 7 — Smoke Test (`TimesNet → SSA`)

- **Thời điểm hoàn tất:** `2026-11-21 23:40:32.473517`
- **Người thực hiện:** TV2 (`UTAKaoru`)
- **Repo nhóm đối chiếu:** tách từ `19483da785f171cb28699e3cba2ae16d6512089a` (đồng bộ chuẩn hóa trên `cedd08f`).
- **Mã tác giả đối chiếu (`frn-50k-baseline`):** commit `8af694a09a5a427d1d50648d348c022565a781f2`.

## 1. Nguồn dữ liệu và cách chọn mẫu thử
- **Nguồn nạp:** khi biến môi trường `FRN_DATA_DIR` chưa trỏ tới thư mục chứa hai Parquet của Task 6, notebook tự tải hai split chính thức `data/train.parquet` và `data/eval.parquet` từ Hugging Face (`Dingdong-Inc/FreshRetailNet-50K`) vào bộ nhớ đệm cục bộ. Khi chạy lại có thể đặt `FRN_DATA_DIR=<thư_mục_Parquet_Task_6>` để dùng trực tiếp bản đã đối soát ở Task 6.
- **Điều kiện chọn mẫu:** lọc các cặp có đủ 90 ngày `train`, 7 ngày `eval`, có ít nhất 1 ngày `train` bị hết hàng (`stock_hour6_22_cnt > 0`) và ít nhất 1 ngày `eval` không hết hàng (`stock_hour6_22_cnt == 0`); chọn ngẫu nhiên cố định **100 cặp** với `random_state = 20261116` (lưu tại [smoke_pairs.csv](smoke_pairs.csv)).
- **Quy mô tập thử:** `train_smoke.parquet` có đúng **9.000 dòng** (100 cặp × 90 ngày), `eval_smoke.parquet` có đúng **700 dòng** (100 cặp × 7 ngày), không trùng khóa `(store_id, product_id, dt)`. Tập `eval` chỉ dùng cho bước đánh giá SSA, không đưa vào huấn luyện hay khôi phục TimesNet.

## 2. Môi trường và thay đổi phục vụ chạy thử
- **Môi trường chạy:** Windows CPU (`task07-venv`), Python `3.10+`, PyTorch CPU, pandas, NumPy, PyArrow, `pypots` đi kèm `frn-50k-baseline`.
- **Bản vá cục bộ ([patch_baseline.py](patch_baseline.py)):**
  - Bổ sung tham số đường dẫn tường minh `--train_path`, `--output_path`, `--epochs` cho `app.py` / `generate_data.py` (đảm bảo cả `load_data` lẫn `_demand_recovery` đọc cùng `train_smoke.parquet`) và `--train_path`, `--eval_path`, `--metrics_path` cho `ssa_forecasting.py` (đảm bảo cả hai nhánh SSA đọc cùng `eval_smoke.parquet`).
  - Cô lập import trong bản sao `pypots` để chỉ nạp mô hình `TimesNet` và hàm mất mát liên quan khi chạy trên Windows CPU, không sửa đổi kiến trúc hay công thức tính của `TimesNet` và `SSA`.

## 3. Tham số và lệnh chạy thực tế
- **TimesNet smoke:** `--model TimesNet --missing_rate 0 --epochs 2` (giảm từ mặc định `5` epoch để kiểm tra luồng chạy; `patience` tự giảm từ `5` xuống `1` để thỏa `patience < epochs`), `batch_size = 128`, `seed = 1024` theo CLI gốc.
- **Lệnh thực thi (ghi log tại `smoke/`):**
  1. `python ssa_forecasting.py --train_path <train_smoke.parquet> --eval_path <eval_smoke.parquet> --metrics_path <ssa_raw_metrics_smoke.csv>` → [smoke/ssa_raw.log](smoke/ssa_raw.log)
  2. `python app.py --model TimesNet --missing_rate 0 --epochs 2 --train_path <train_smoke.parquet> --output_path <Task07_Smoke_Test/demand_timesnet_smoke.parquet>` → [smoke/timesnet.log](smoke/timesnet.log)
  3. `python ssa_forecasting.py --demand --demand_path <Task07_Smoke_Test/demand_timesnet_smoke.parquet> --eval_path <eval_smoke.parquet> --metrics_path <ssa_timesnet_metrics_smoke.csv>` → [smoke/ssa_timesnet.log](smoke/ssa_timesnet.log)

## 4. Kiểm định đầu ra và kết quả smoke
- **Tệp nhu cầu mẫu `demand_timesnet_smoke.parquet`:** sinh cục bộ khi chạy notebook (`282.202` bytes, SHA-256: `558ad5415e328720cfe3902275aeb608ce1a9aa697e088b3556fd45b169332dc`; không đẩy tệp `.parquet` lên GitHub theo quy ước nhóm). Đã xác nhận đủ `9.000` dòng, khớp 100% khóa với `train_smoke`, cột `sale_amount_pred` hữu hạn và không âm; decoupling score trên mẫu 100 cặp dịch chuyển từ `-0.508354` (`sale_amount`) về `-0.217262` (`sale_amount_pred`).
- **Chỉ số dự báo trên tập thử ([smoke_metrics.csv](smoke_metrics.csv)):**
  - `SSA_RawSales`: Overall WAPE `35.60%`, WPE `-6.15%` | Low Sale `40.38%`, `-10.58%` | High Sale `32.22%`, `-2.44%`.
  - `SSA_TimesNet`: Overall WAPE `35.11%`, WPE `-0.63%` | Low Sale `39.53%`, `-5.01%` | High Sale `32.03%`, `+3.04%`.
- **Lưu ý bắt buộc:** Toàn bộ chỉ số trên thuộc lượt chạy thử (`smoke`) với 100 cặp và 2 epoch nhằm xác nhận tính khép kín của pipeline; **tuyệt đối không sử dụng làm kết quả chính thức để đối chiếu Bảng 2 hoặc Bảng 3**.
