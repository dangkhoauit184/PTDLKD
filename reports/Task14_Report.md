# Báo cáo Task 14: Dự báo Nhu cầu 7 Ngày bằng Mạng Học Sâu `DLinear` (`DLinear_RawSales`, `DLinear_TimesNet`, `DLinear_DLinear`)

**Người thực hiện:** Dương Trọng Toàn (`UTAKaoru`) | **Nhánh:** `feature/task14-dlinear-forecasting` | **Thư mục:** `Task14_DLinear_Forecasting/`

## 1. Mục tiêu và Thiết lập Thực nghiệm
- **Mục tiêu:** Đánh giá mô hình dự báo chuỗi thời gian học sâu **DLinear** (phân rã xu hướng – mùa vụ với cửa sổ trung bình trượt 28 ngày kèm chuẩn hóa `RevIN`) trên 3 nguồn dữ liệu lịch sử để tái lập cột **DLinear** trong Bảng 3 của bài báo *FreshRetailNet-50K*, đồng thời đối chứng chéo với phương pháp thống kê **SSA** ([Task 8](Task08_Report.md), [Task 11](Task11_Report.md), [Task 13](Task13_Report.md)).
- **Cấu hình chuẩn theo mã tác giả (`demand_forecasting/DLinear` @ `8af694a`):**
  - Siêu tham số cố định: `fix_seed = 2025`, `features = MS` (`enc_in = 7` đặc trưng ngoại sinh & mục tiêu), `total_seq_len = 90`, `seq_len = 62`, `moving_avg = 28`, `pred_len = 7`, `scale = True` (`StandardScaler` trên từng chuỗi), `loss = mae` (`L1Loss`), `batch_size = 1024`, `train_epochs = 6` (`1.100.000` cửa sổ trượt = `1.074` bước/epoch), `learning_rate = 0.001` (`type1` decay).
  - Bảo toàn hành vi gốc của cờ `--revin False` trong `train_predict.sh` (`parser.add_argument('--revin', type=bool)` chuyển chuỗi `"False"` thành `True`, tức thực tế kích hoạt lớp chuẩn hóa `RevIN`).
  - Bản vá tối thiểu ([code_changes.diff](../Task14_DLinear_Forecasting/code_changes.diff)): bổ sung `--train_path` và `--eval_path` để `Exp_Main.data_organization` nạp trực tiếp `train.parquet` gốc ([Task 6](Task06_Report.md)) khi tính `psd`, đảm bảo phân nhóm `Overall = 206.562`, `Low Sale = 153.208`, `High Sale = 53.354` trùng khớp 100% với cột SSA.
  - Môi trường chạy thực tế: Windows CUDA GPU (`PyTorch 2.0.1+cu118`, `Python 3.8.20` — trùng phiên bản PyTorch gốc của tác giả).

## 2. Kết quả Định lượng và Đối chiếu Bảng 3

| Cấu hình | Phân nhóm | WAPE thực chạy | WPE thực chạy | MAE | WAPE bài báo | WPE bài báo | Chênh lệch WAPE | Chênh lệch WPE |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`DLinear_RawSales`** | **Overall** | **31.54%** | **-5.21%** | 0.3932 | 31.56% | -4.89% | **-0.02 pp** | -0.32 pp |
| | **Low Sale** (`psd < 1`) | **39.71%** | **-1.31%** | 0.2781 | 39.78% | -1.03% | **-0.07 pp** | -0.28 pp |
| | **High Sale** (`psd >= 1`) | **25.70%** | **-7.97%** | 0.7310 | 25.68% | -7.63% | **+0.02 pp** | -0.34 pp |
| **`DLinear_TimesNet`** | **Overall** | **30.55%** | **+6.21%** | 0.3797 | 30.73% | +6.88% | **-0.18 pp** | -0.67 pp |
| | **Low Sale** (`psd < 1`) | **40.45%** | **+11.61%** | 0.2824 | 40.73% | +12.37% | **-0.28 pp** | -0.76 pp |
| | **High Sale** (`psd >= 1`) | **23.46%** | **+2.37%** | 0.6649 | 23.58% | +2.98% | **-0.12 pp** | -0.61 pp |
| **`DLinear_DLinear`** | **Overall** | **30.76%** | **+4.63%** | 0.3824 | 30.60% | +4.02% | **+0.16 pp** | +0.61 pp |
| | **Low Sale** (`psd < 1`) | **40.73%** | **+10.75%** | 0.2843 | *(không in)* | *(không in)* | – | – |
| | **High Sale** (`psd >= 1`) | **23.63%** | **+0.26%** | 0.6700 | *(không in)* | *(không in)* | – | – |

## 3. Phân tích Chuyên môn và Đối chứng Đa Mô hình (`SSA` vs `DLinear`)

1. **Độ chính xác tái lập vượt trội trên toàn bộ 7 ô công bố của Bảng 3:**
   - Nhờ chạy đúng trên `PyTorch 2.0.1+cu118` và bảo toàn cơ chế `RevIN`, toàn bộ 7 chỉ số WAPE có số tham chiếu trong Bảng 3 đều bám sát bài báo với độ lệch tuyệt đối chỉ từ **0.02 đến 0.28 điểm phần trăm** (`DLinear_RawSales` lệch `-0.02 pp` ở Overall và `+0.02 pp` ở High Sale; `DLinear_TimesNet` tốt hơn số công bố `0.18 pp` ở Overall và `0.12 pp` ở High Sale; `DLinear_DLinear` lệch `+0.16 pp` ở Overall).
2. **Hiệu quả khử che khuất nhu cầu trên mạng học sâu `DLinear`:**
   - Khi huấn luyện trên doanh số thô (`DLinear_RawSales`), mô hình vẫn bị thiên lệch dự báo thiếu rõ rệt (`WPE = -5.21%` Overall và **`-7.97%`** ở High Sale).
   - Khi chuyển sang dữ liệu đã khôi phục (`DLinear_TimesNet` và `DLinear_DLinear`), WAPE trên `Overall` giảm từ **31.54%** xuống **30.55%** (`-0.99 pp`) và **30.76%** (`-0.78 pp`); đặc biệt ở nhóm mặt hàng chủ lực **High Sale**, WAPE giảm mạnh từ **25.70%** xuống **23.46%** (`-2.24 pp`, MAE từ `0.7310` xuống `0.6649`) và loại bỏ hoàn toàn thiên lệch dự báo âm.
3. **So sánh kiến trúc dự báo `DLinear` (Task 14) với `SSA` (Task 8, 11, 13):**
   - **Ở nhóm hàng bán chạy (`High Sale` — chiếm 87% doanh số):** Mạng học sâu **`DLinear` vượt trội `SSA` trên cả 3 nguồn dữ liệu** (`RawSales`: `25.70%` vs `27.40%`; `DLinear Recovery`: `23.63%` vs `24.46%`; `TimesNet Recovery`: **`23.46%`** vs `23.98%`) nhờ khả năng học trực tiếp xu hướng – mùa vụ liên tục trên chuỗi có tín hiệu dày.
   - **Ở nhóm hàng bán chậm (`Low Sale` — chuỗi thưa nhiều ngày bằng 0):** `DLinear` kết hợp chuẩn hóa theo cửa sổ `RevIN` dễ khuếch đại dự báo dương khi chuỗi lịch sử được bù thêm nhu cầu (`WPE = +11.61%` ở `DLinear_TimesNet`, khớp hiện tượng `+12.37%` trong bài báo gốc), dẫn tới WAPE trên `Low Sale` cao hơn thuật toán trung bình kịch bản `SSA` (`40.45%` vs `37.87%`). Đây chính là lý do trên `Overall`, `SSA_TimesNet` (`29.79%`) đạt WAPE thấp hơn nhẹ so với `DLinear_TimesNet` (`30.55%`), tái khẳng định nhận định của bài báo rằng chỉ các kiến trúc phi tuyến giàu ngữ cảnh như **TFT** (Task 15) mới đồng thời vượt `SSA` trên cả hai nhóm.

## 4. Bàn giao
- [Notebook kiểm chứng có đầy đủ output](../Task14_DLinear_Forecasting/notebooks/14_dlinear_forecasting.ipynb), [bản vá mã nguồn](../Task14_DLinear_Forecasting/code_changes.diff), [bảng chỉ số 9 dòng](../Task14_DLinear_Forecasting/results/dlinear_forecasting_metrics.csv), [metadata](../Task14_DLinear_Forecasting/results/run_metadata.json), [biên bản chạy](../Task14_DLinear_Forecasting/run_info.md) và 4 tệp log UTF-8 ([smoke](../Task14_DLinear_Forecasting/results/smoke/dlinear_smoke.log), [raw_sales](../Task14_DLinear_Forecasting/results/full/dlinear_raw_sales.log), [timesnet](../Task14_DLinear_Forecasting/results/full/dlinear_timesnet.log), [dlinear](../Task14_DLinear_Forecasting/results/full/dlinear_dlinear.log)).
