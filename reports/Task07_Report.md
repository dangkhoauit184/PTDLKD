# Báo cáo Task 07: Chạy thử khép kín quy trình `TimesNet → SSA` trên tập nhỏ (`Smoke Test`)

## 1. Mục tiêu và thiết lập kiểm thử
- **Mục tiêu:** Xác minh toàn bộ luồng dữ liệu hai giai đoạn (`train_smoke` → `TimesNet --missing_rate 0` → `demand_timesnet_smoke.parquet` → `SSA_RawSales` & `SSA_TimesNet` trên `eval_smoke`) vận hành thông suốt, không rò rỉ tập `eval` vào quá trình khôi phục và không đọc nhầm tập dữ liệu đầy đủ.
- **Tập dữ liệu thử:** Chọn cố định **100 cặp** (`store_id`, `product_id`) với `seed = 20261116` thỏa điều kiện đủ 90 ngày `train` (có hết hàng) và 7 ngày `eval` (có dòng `stock_hour6_22_cnt == 0`), thu được **9.000 dòng `train`** và **700 dòng `eval`**.
- **Tham số rút gọn cho lượt thử:** `TimesNet` chạy trên CPU với `--missing_rate 0`, `epochs = 2`, `patience = 1` (giảm từ mức baseline `5` epoch), `batch_size = 128`, `seed = 1024`.

## 2. Kết quả kiểm tra đường ống (Chỉ số `smoke` — không dùng cho Bảng 3)
| Cấu hình (`smoke`) | Phân nhóm | WAPE (%) | WPE (%) | Trạng thái |
| :--- | :--- | :---: | :---: | :---: |
| **`SSA_RawSales`** | **Overall** (`psd >= 0`) | 35.60% | -6.15% | `ok` |
| | **Low Sale** (`psd < 1`) | 40.38% | -10.58% | `ok` |
| | **High Sale** (`psd >= 1`) | 32.22% | -2.44% | `ok` |
| **`SSA_TimesNet`** | **Overall** (`psd >= 0`) | 35.11% | -0.63% | `ok` |
| | **Low Sale** (`psd < 1`) | 39.53% | -5.01% | `ok` |
| | **High Sale** (`psd >= 1`) | 32.03% | +3.04% | `ok` |

## 3. Đánh giá kỹ thuật
- Tệp `demand_timesnet_smoke.parquet` sinh ra đủ `9.000` dòng, khớp chính xác thứ tự khóa với tập `train` thử, toàn bộ giá trị `sale_amount_pred` hữu hạn và không âm; decoupling score trên mẫu 100 cặp dịch chuyển từ `-0.508354` về `-0.217262`.
- Cả hai nhánh SSA đều đọc đúng tập `eval` 700 dòng và xuất chỉ số hữu hạn ở cả ba phân nhóm. Ngay trên mẫu nhỏ 2 epoch, xu hướng giảm WAPE và kéo WPE từ âm về sát `0` đã xuất hiện nhất quán với giả thuyết của bài báo.
- **Giới hạn sử dụng:** Đây là kết quả kiểm tra kỹ thuật đường ống (`smoke`), không đại diện cho toàn bộ 50.000 chuỗi và không đưa vào bảng đối chiếu chính thức của đồ án.

## 4. Bàn giao
[Notebook đã chạy](../Task07_Smoke_Test/07_smoke_test.ipynb), [script vá đường dẫn](../Task07_Smoke_Test/patch_baseline.py), [danh sách 100 cặp](../Task07_Smoke_Test/smoke_pairs.csv), [bảng chỉ số smoke](../Task07_Smoke_Test/smoke_metrics.csv), ba file log trong [Task07_Smoke_Test/smoke/](../Task07_Smoke_Test/smoke/) và [biên bản chạy](../Task07_Smoke_Test/run_info.md).
