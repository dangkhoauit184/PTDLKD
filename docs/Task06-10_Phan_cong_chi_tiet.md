# Phân công Task 6–10 — Tái lập FreshRetailNet-50K

Tài liệu này chuẩn hóa phần việc tiếp theo dựa trên [README của nhóm](../README.md), phần chốt phạm vi ở [báo cáo Task 1](../reports/Task01_Report.md) và kế hoạch ưu tiên ở [báo cáo Task 2](../reports/Task02_Report.md). Bản repo nhóm đối chiếu: `da2e3cc` trên `main`. Bản mã tác giả đối chiếu: [frn-50k-baseline, commit 8af694a](https://github.com/Dingdong-Inc/frn-50k-baseline/tree/8af694a09a5a427d1d50648d348c022565a781f2).

## Phạm vi và phân công

**Luồng chính:** Task 8 chạy `SSA_RawSales`; Task 10 chạy TimesNet trên giờ hết hàng thực tế; Task 11 dùng đầu ra Task 10 để chạy `SSA_TimesNet` và đối chiếu với Task 8. Hai cấu hình SSA là trọng tâm đã nêu trong báo cáo Task 1–2. Task 9 đánh giá thêm TimesNet khi tạo thiếu nhân tạo. [Bảng 2 và Bảng 3 của bài báo](https://arxiv.org/html/2505.16319v5#S5) là nguồn đối chiếu.

Danh mục [15 cấu hình dự báo](../Task02_Experiment_Plan/docs/15_forecasting_configurations.md) và bảy mô hình khôi phục là danh mục tham chiếu. Các lượt chạy thêm TFT, DLinear dự báo hoặc sáu mô hình khôi phục còn lại chỉ mở rộng khi nhóm chốt riêng. Các số đã ghi trong README và báo cáo là **số tham chiếu từ bài báo**; chỉ ghi vào cột kết quả của nhóm khi có log của lượt chạy tương ứng.

| Người | Task | Việc chính | Đầu ra cần có |
|---|---|---|---|
| TV1 | **6 — Chốt đầu vào thực nghiệm** | Kiểm tra và dùng lại Parquet do Task 3 tạo; chỉ chuyển lại nếu chưa có bản phù hợp | Notebook, thông tin nguồn và bảng đối soát hai tập |
| TV2 | **7 — Chạy thử TimesNet → SSA** | Chạy cả hai nhánh SSA trên cùng tập thử 100 cặp | Danh sách cặp, Parquet nhu cầu mẫu, log và chỉ số thử |
| TV3 | **8 — SSA trên doanh số gốc** | Chạy `SSA_RawSales` trên dữ liệu đầy đủ | Bảng chỉ số ba nhóm và log |
| TV4 | **9 — TimesNet với thiếu nhân tạo** | Chạy TimesNet MNAR trên train đầy đủ | WAPE/WPE và cấu hình tạo thiếu |
| TV5 | **10 — TimesNet trên giờ hết hàng thực tế** | Khôi phục nhu cầu trên train đầy đủ và tính decoupling score | `demand_timesnet.parquet`, bảng điểm và log |

**Làm độc lập:** Mỗi người có một notebook, một thư mục kết quả và một nhánh riêng. TV2–TV5 có thể dùng bản dữ liệu đã đối soát ở Task 3–4 hoặc tự nạp từ CSV gốc. Không ai phải chờ đầu ra của một task khác trong 6–10. Task 7 và Task 10 huấn luyện độc lập ở hai quy mô; Task 9 và Task 10 là hai chế độ khác nhau.

## Quy ước dùng chung

| Nội dung | Yêu cầu |
|---|---|
| Dữ liệu | Cùng nguồn FreshRetailNet-50K đã đối soát ở [Task 4](../reports/Task04_Report.md). Train: **4.500.000 dòng**, từ **28/03 đến 25/06/2024**; eval: **350.000 dòng**, từ **26/06 đến 02/07/2024**. Cả hai cùng 50.000 cặp cửa hàng–sản phẩm, lần lượt 90 và 7 ngày/cặp. |
| Định dạng | Giữ khóa `store_id, product_id, dt`, ngày `YYYY-MM-DD`, đủ 19 cột gốc ở đầu vào. Hai cột theo giờ là danh sách 24 số. Sắp xếp theo khóa trước khi tạo mảng chuỗi. |
| Giá trị ngoại lệ | Giữ nguyên dữ liệu gốc, gồm 34 dòng `discount > 1` được gắn REVIEW. Báo cáo Task 4 có **đề xuất** clip, nhưng lượt tái lập chính không áp dụng thay đổi đó. Nếu thử clip, lưu thành lượt riêng có ghi rõ. |
| Nhãn và khung giờ | Theo mã nguồn, `hours_stock_status = 1` là hết hàng; dùng lát `[6:22]` tương ứng 06:00 đến trước 22:00. TimesNet dùng 3 đoạn 30 ngày/cặp, 480 bước và 6 đặc trưng/đoạn. Không dùng eval để khôi phục hoặc huấn luyện TimesNet. |
| Thiết lập Colab | Dùng [hướng dẫn Task 3](../Task03_Environment_Setup/README.md) làm điểm xuất phát. Ghi Python, phiên bản thư viện và GPU thực tế. Chạy kiểm tra đọc dữ liệu/import trước lượt chính; với TimesNet, kiểm tra CUDA và chạy thử một lô trước. Lưu lỗi và phiên bản thay đổi nếu cần sửa môi trường. |
| Nạp dữ liệu | Repo tác giả mặc định nạp Hugging Face. Nếu chạy file trên Drive, sửa cách nạp ở **mọi điểm liên quan**: train, eval, đối soát và xuất nhu cầu. Với task thử, không để bất kỳ bước nào tự nạp lại tập đầy đủ. |
| Chỉ số và log | WAPE/WPE xuất theo phần trăm, giữ dấu WPE; MAE giữ đơn vị doanh số chuẩn hóa; decoupling score giữ nguyên. Tách `smoke/` và `full/`. Lượt chưa có chỉ số ghi `failed` hoặc `not_run` và để trống số, không điền 0. |

**Mỗi task nộp `run_info.md`** ghi tên dữ liệu, số dòng/cặp, commit repo nhóm và commit mã tác giả, phiên bản môi trường, lệnh chạy, tham số thực tế, seed nếu có, thay đổi so với mã tác giả, và đường dẫn đầu ra trên Drive. Làm việc trên nhánh `feature/task<số>-<tên>` theo [Contribution Guide](Contribution_Guide.md). Notebook, mã và báo cáo lưu trong thư mục task trên GitHub; dữ liệu, checkpoint, log và CSV kết quả lưu Drive theo `.gitignore`.

## TV1 — Task 6: Chốt dữ liệu đầu vào thực nghiệm

**Thư mục:** `Task06_Data_Preparation/`. **Mục tiêu:** xác nhận một cặp file đầu vào có thể dùng lại, không làm lại toàn bộ Task 4 hoặc EDA.

1. Tìm `train.parquet` và `eval.parquet` do Task 3 tạo. Ghi nguồn, tên file và phiên bản. Đối chiếu với hai tập đã dùng ở Task 4. Nếu không xác nhận được bản Parquet hiện có, tạo bản mới từ hai CSV đã kiểm tra; chuyển chuỗi `hours_sale`, `hours_stock_status` thành danh sách số, không sửa giá trị.
2. Đọc lại Parquet. Kiểm tra đủ 19 cột, số dòng, khoảng ngày, hai mảng 24 phần tử, khóa duy nhất và đủ 90/7 ngày cho mỗi cặp. Xác nhận hai tập cùng 50.000 cặp và không chồng lặp khóa ngày. Đối chiếu giá trị với CSV theo khóa hoặc xác nhận nguồn chuyển đổi và ghi phương pháp đối chiếu đã dùng.
3. Chạy một ô đọc mẫu và tạo đầu vào TimesNet theo thứ tự khóa. Kiểm tra dạng **480 bước × 6 đặc trưng** trên mẫu; xác nhận SSA có thể ghép đúng 90 ngày train và 7 ngày eval theo mỗi cặp. Task này dừng ở dữ liệu, chưa huấn luyện.

**Bàn giao:**

- `06_prepare_data.ipynb`: lưu output đọc lại hai file, kết quả đối chiếu với CSV gốc và kích thước mẫu đầu vào TimesNet. Ghi rõ đối chiếu toàn bộ hay theo mẫu.
- `input_check.csv`: đúng **2 dòng**, `train` và `eval`. Mỗi dòng ghi đường dẫn, số cột, số dòng, số cặp, ngày đầu/cuối, số khóa trùng, số chuỗi thiếu ngày, số mảng sai kích thước và trạng thái. Kỳ vọng lần lượt **4.500.000** và **350.000** dòng dữ liệu, mỗi tập **50.000** cặp.
- `run_info.md`: ghi rõ đường dẫn của từng Parquet, file nguồn tương ứng, cách xác nhận dữ liệu khớp và dùng lại bản Task 3 hay chuyển mới từ CSV. Nếu dùng lại bản Task 3, gửi link bản đó, không cần tạo bản sao.

**Xong khi:** người nhận mở được hai file và chạy lại notebook đối soát, xác nhận đầu vào giữ nguyên dữ liệu và cấu trúc của hai tập.

**Đã hoàn thành:** xem [báo cáo và kết quả Task 6](../reports/Task06_Report.md). Hai Parquet hiện có được xác nhận khớp toàn bộ CSV đã kiểm tra ở Task 4.

## TV2 — Task 7: Chạy thử TimesNet → SSA

**Thư mục:** `Task07_Smoke_Test/`. **Mục tiêu:** kiểm tra một lượt chạy khép kín trên tập nhỏ.

1. Chọn **100 cặp** có đủ 90 ngày train và 7 ngày eval. Giữ cả chuỗi của từng cặp. Nên có giờ hết hàng ở train và mẫu eval hợp lệ để đánh giá. Lọc cả hai tập theo cùng danh sách; xác nhận **9.000 dòng train, 700 dòng eval**.
2. Chạy SSA với lịch sử `sale_amount` trên tập thử. Lưu log. Nếu đổi cách nạp, sửa cả chỗ nạp train trong phần chạy SSA và chỗ nạp eval trong `ssa_predict`.
3. Chạy TimesNet trên train thử với `--missing_rate 0`. Giảm số epoch cho lượt thử nếu cần và ghi lại. Với repo tác giả, cần bảo đảm cả `load_data` lẫn `_demand_recovery` đọc cùng một train thử. Đổi tên Parquet đầu ra thành `demand_timesnet_smoke.parquet`.
4. Đọc lại Parquet: đủ 9.000 khóa của train thử và có `sale_amount_pred` hữu hạn, không âm. Chạy SSA với `--demand --demand_path <file_parquet_thử>` trên đúng eval thử.
5. Ghi WAPE/WPE của `Overall` cho hai nhánh. Nếu nhóm Low Sale hoặc High Sale không có mẫu hợp lệ, ghi rõ; nếu `Overall` không có chỉ số hữu hạn, kiểm tra lại dữ liệu thử.

**Bàn giao:**

- `07_smoke_test.ipynb`: lưu output lọc **9.000 dòng train và 700 dòng eval**, đầu ra TimesNet và bảng chỉ số của hai lần chạy SSA.
- `smoke_pairs.csv`: **100 cặp duy nhất**, có cột `store_id`, `product_id`. `demand_timesnet_smoke.parquet`: **9.000 dòng**, đúng khóa train thử, có `sale_amount_pred`.
- `smoke_metrics.csv`: ít nhất **2 dòng Overall**, một dòng `SSA_RawSales` và một dòng `SSA_TimesNet`. Ghi `config_id,group,wape_pct,wpe_pct,status`; giữ các nhóm còn lại nếu có kết quả hợp lệ.
- `smoke/ssa_raw.log`, `smoke/timesnet.log`, `smoke/ssa_timesnet.log` và `run_info.md`. Ghi rõ các tham số đã giảm cho lượt thử, nếu có, để không dùng nhầm khi chạy đầy đủ.

**Xong khi:** hai nhánh SSA đều chạy hết và cho chỉ số hữu hạn trên cùng tập thử. Gắn nhãn `smoke` cho tất cả các file của lượt này; không chép số thử vào Bảng 3.

## TV3 — Task 8: SSA trên doanh số gốc

**Thư mục:** `Task08_SSA_Raw_Sales/`. **Mã cấu hình:** `SSA_RawSales`.

1. Đọc train và eval đầy đủ. Dùng `sale_amount` của **90 ngày train** làm lịch sử; lấy các biến tương lai theo cách của repo. Dùng `sale_amount` trong eval làm giá trị đối chiếu, không đưa vào lịch sử.
2. Chạy [ssa_forecasting.py](https://github.com/Dingdong-Inc/frn-50k-baseline/blob/8af694a09a5a427d1d50648d348c022565a781f2/demand_forecasting/SSA/ssa_forecasting.py) từ thư mục `demand_forecasting/SSA`, chế độ mặc định, không bật `--demand`. Nếu dùng Drive, nạp đúng hai tập đã xác nhận.
3. Dùng điều kiện đánh giá của repo: chỉ lấy dòng eval có `stock_hour6_22_cnt == 0`. `psd` là doanh số ngày **gốc trung bình trong train** theo từng cặp. Chia `Overall: psd >= 0`, `Low Sale: psd < 1`, `High Sale: psd >= 1`. Cách chia này khác nhóm top 20% sản phẩm trong EDA. Với SSA, tính chỉ số theo ngày rồi lấy trung bình theo mã nguồn.
4. Xuất WAPE, WPE và MAE cho ba nhóm. Đối chiếu WAPE/WPE với cột SSA, dòng Raw Sales của [Bảng 3](https://arxiv.org/html/2505.16319v5#S5.SS3). MAE là chỉ số phụ từ script. Ghi chênh lệch WAPE/WPE theo **điểm phần trăm**.

**Bàn giao:**

- `08_ssa_raw_sales.ipynb`: lưu output xác nhận train/eval đầy đủ, số dòng eval đủ điều kiện sau lọc và kết quả của ba nhóm.
- `ssa_raw_sales_metrics.csv`: đúng **3 dòng** cho `Overall`, `Low Sale`, `High Sale`, cùng `config_id=SSA_RawSales`. Mỗi dòng ghi số nhóm tự chạy và số tham chiếu của đúng nhóm trong Bảng 3. Tính chênh lệch bằng **số nhóm trừ số bài báo**; MAE chỉ ghi số nhóm chạy.
- `full/ssa_raw_sales.log` và `run_info.md`: log phải có kết quả ba nhóm khớp CSV; ghi lệnh chạy và đường dẫn của cả train lẫn eval.

Mẫu cột:

```text
config_id,group,wape_pct,wpe_pct,mae,paper_wape_pct,paper_wpe_pct,delta_wape_pp,delta_wpe_pp,status
```

**Xong khi:** có log chạy trên dữ liệu đầy đủ và ba dòng chỉ số tự chạy. SSA không tạo checkpoint huấn luyện.

## TV4 — Task 9: Đánh giá TimesNet khi tạo thiếu nhân tạo

**Thư mục:** `Task09_TimesNet_MNAR/`. **Mục tiêu:** lấy WAPE/WPE của TimesNet cho phần tham chiếu Bảng 2. Task 9 không xuất nhu cầu làm đầu vào dự báo.

1. Chạy TimesNet ở chế độ `--missing_rate > 0` trong `latent_demand_recovery/exp`. Nếu nhóm chưa chốt mức khác, dùng ví dụ `python app.py --model TimesNet --missing_rate 0.3` và seed `1024` của CLI gốc. Ghi `0.3` là **tham số mô phỏng theo ví dụ repo**, không khẳng định là tỷ lệ thiếu thực tế đạt đúng 30% hoặc là cấu hình chính xác của bài báo.
2. Kiểm tra trước trên tập nhỏ; sau đó chạy train đầy đủ. Nếu đọc local, xác nhận `load_data` và `evaluation_mnar` dùng đúng cùng tập và thứ tự khóa. Lấy số phần tử che thêm mà loader ghi ra, nếu có; lưu seed, số epoch, batch size và tham số tạo thiếu thực tế.
3. Lấy WAPE/WPE từ `evaluation_mnar`. Theo mã tác giả, chỉ số tính trên tổng doanh số **theo ngày**, xét các ngày có điểm bị che thêm và không có hết hàng thực trong khung giờ dùng để khôi phục. Giữ quy tắc này khi đối chiếu với TimesNet trong [Bảng 2](https://arxiv.org/html/2505.16319v5#S5.SS2).
4. Nếu nhóm mở rộng thêm mô hình sau này, dùng cùng nguồn dữ liệu và thiết lập tạo thiếu để so sánh. Việc mở rộng không phải điều kiện nộp Task 9 hiện tại.

**Bàn giao:**

- `09_timesnet_mnar.ipynb`: lưu output xác nhận nguồn train, cấu hình tạo thiếu và WAPE/WPE của lượt chạy đầy đủ. Tách output chạy thử nếu notebook có cả hai lượt.
- `mnar_metrics.csv`: **1 dòng TimesNet** với WAPE/WPE thực chạy, tham số tạo thiếu, seed, số epoch và batch size. Cột `n_artificially_masked_hours` ghi số giờ che thêm nếu loader có báo; để trống nếu không ghi nhận được.
- `full/timesnet_mnar.log` và `run_info.md`: log phải chứa hai chỉ số dùng trong CSV. Ghi rõ giá trị `missing_rate` là tham số mô phỏng, và dùng thiết lập theo bài báo đã xác minh hay theo ví dụ repo.

Mẫu cột:

```text
model,missing_rate,seed,epochs,batch_size,n_artificially_masked_hours,wape_pct,wpe_pct,status,log_path
```

**Xong khi:** có WAPE/WPE hữu hạn và cấu hình đủ để chạy lại. Bảng 2 dùng kết quả này để đối chiếu; không lấy các số công bố làm kết quả của nhóm.

## TV5 — Task 10: Khôi phục nhu cầu bằng TimesNet tại giờ hết hàng thực tế

**Thư mục:** `Task10_TimesNet_Recovery/`. **Mục tiêu:** tạo đầu vào TimesNet trên toàn bộ train cho `SSA_TimesNet` ở Task 11.

1. Từ `latent_demand_recovery/exp`, chạy TimesNet với `--missing_rate 0`; xác nhận không tạo thêm điểm thiếu nhân tạo và không dùng eval để huấn luyện. Dùng bộ 6 đặc trưng và cách cắt chuỗi của repo. Đối chiếu tham số từ mã thực tế trước khi chạy; baseline gốc dùng **5 epoch, batch size 128, learning rate 0.001**.
2. Báo cáo Task 2 ghi **seed 2024** cho Task 10; CLI gốc gọi `set_seed(seed_value=1024)` và không nhận tham số `--seed`. Nếu chạy theo kế hoạch nhóm, đặt seed 2024 tại lời gọi này trong bản sao mã và lưu thay đổi. Nếu chạy nguyên bản, ghi seed 1024 và ghi đây là lượt baseline gốc. Không tự ghi 2024 vào báo cáo nếu log/mã chạy dùng 1024. Không dùng mức 20 epoch nêu như lựa chọn trong báo cáo làm mặc định baseline.
3. Với dữ liệu local, bảo đảm `load_data` và `_demand_recovery` dùng cùng tập train, cùng thứ tự khóa. Chạy hết train đầy đủ; lấy `demand/demand.parquet`, lưu trên Drive thành `demand_timesnet.parquet`. Trong đầu ra gốc, `hours_sale` vẫn là doanh số giờ quan sát; `sale_amount_pred` mới là **nhu cầu ngày sau khôi phục**. Nếu cần mảng ước lượng theo giờ, lưu riêng file imputation của lượt chạy và ghi thứ tự khóa.
4. Đọc lại file nhu cầu. Kiểm tra **4.500.000 dòng**, khóa duy nhất và trùng khớp tập train, đủ cột gốc cộng `sale_amount_pred`, giá trị nhu cầu ngày hữu hạn và không âm. Lưu bằng chứng đối soát và đường dẫn file.
5. Ghi decoupling score in từ `evaluation_decoupling` cho **Raw Sales** (`sale_amount`) và **TimesNet** (`sale_amount_pred`). Chỉ số này dùng cho phần tham chiếu Bảng 2. Lượt này không có đáp án nhu cầu thật tại giờ hết hàng để tính WAPE/WPE khôi phục; WAPE/WPE MNAR lấy từ Task 9.

**Bàn giao:**

- `10_timesnet_recovery.ipynb`: lưu output xác nhận lượt chạy `missing_rate=0`, seed thực dùng, hai decoupling score và kết quả đọc lại file nhu cầu.
- `demand_timesnet.parquet`: file chính chuyển cho Task 11, có **4.500.000 dòng**, giữ **19 cột gốc** và thêm `sale_amount_pred`. Gửi đúng link của lượt chạy đầy đủ, tránh nhầm file `demand.parquet` của lượt thử.
- `demand_file_check.csv`: ghi đường dẫn file, số dòng, số khóa trùng, số khóa thiếu hoặc thừa so với train, và số giá trị `sale_amount_pred` thiếu, không hữu hạn hoặc âm. Các số đếm lỗi kỳ vọng bằng **0**.
- `decoupling_metrics.csv`: đúng **2 dòng**, `Raw Sales` và `TimesNet`, với các cột `method,decoupling_score,log_path`. Điểm ghi đúng như log, không đổi sang phần trăm.
- `full/timesnet_recovery.log` và `run_info.md`: ghi lệnh, cấu hình, link Parquet và link checkpoint nếu lượt chạy có lưu. Link Parquet cần mở được với người làm Task 11.

**Xong khi:** file nhu cầu đầy đủ đã đối soát, mở được từ Drive và có log/config tương ứng. Task này dừng sau khôi phục; TV5 không phải chạy SSA để hoàn thành Task 10.

## Mẫu bàn giao cho từng thành viên

Mỗi người gửi link notebook hoặc nhánh GitHub và link **thư mục Drive của đúng lượt chạy**. Trước khi gửi, mở thử link, kiểm tra notebook có output và đối chiếu số trong CSV với log. Có thể dùng mẫu sau:

```text
Task / người thực hiện:
Notebook hoặc nhánh GitHub:
Thư mục kết quả trên Drive:
File đầu ra chính và quy mô (số dòng/cặp hoặc số dòng chỉ số):
Kết quả chính / trạng thái:
Thiết lập khác với kế hoạch hoặc lượt chưa xong (nếu có):
```

## Sau Task 6–10

**Task 11 — SSA trên nhu cầu TimesNet:** dùng `demand_timesnet.parquet` từ Task 10 làm lịch sử `sale_amount_pred`; đánh giá trên cùng eval, cùng cách chia nhóm và cách tính chỉ số như Task 8. Giữ `sale_amount` gốc để tính `psd` cho cả hai cấu hình. Đặt cạnh nhau `SSA_RawSales` và `SSA_TimesNet` cho Overall, Low Sale, High Sale; ghi riêng **số nhóm chạy, số bài báo, chênh lệch**. Đây là bước kế tiếp, chưa giao cho ai trong bảng 6–10.
