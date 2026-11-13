# BÁO CÁO TASK 4: KIỂM TRA VÀ ĐỐI SOÁT CHẤT LƯỢNG DỮ LIỆU (DATA VALIDATION)
**Môn học:** Phân tích Dữ liệu Kinh doanh (IS403)  
**Người thực hiện:** Đăng Khoa (Thành viên nhóm phụ trách Task 4)  
**Notebook triển khai:** `Task04_Data_Validation/notebooks/04_data_validation_colab.ipynb`  
**Kết quả đối soát:** `Task04_Data_Validation/results/`  

---

## 1. Giới thiệu và Mục tiêu của Task
* **Mục tiêu:**
  1. Thực hiện kiểm định chất lượng toàn diện (Data Quality Assurance / Validation) trên $100\%$ các bản ghi của cả hai tập dữ liệu `train` ($4.500.000$ dòng) và `eval` ($350.000$ dòng).
  2. Xác minh tính toàn vẹn của cấu trúc (Schema), kiểu dữ liệu, các giá trị thiếu (Null/NaN/Blank), tính duy nhất của khóa chính và tính đầy đủ của các chuỗi thời gian.
  3. Kiểm tra tính nhất quán logic nghiệp vụ giữa các cột số liệu (tổng doanh số 24 giờ so với doanh số ngày; số giờ hết hàng so với mảng trạng thái kho trong khung 06:00–22:00).
  4. Lập bảng hồ sơ thuộc tính (Column Profile) và phát hiện các giá trị bất thường (Anomalies) để phục vụ cho các task mô hình hóa tiếp theo.
* **Nguyên tắc thực thi:** Chỉ đọc file đầu vào (Read-only), không tự ý xóa hoặc can thiệp sửa đổi dữ liệu gốc trong bước này.

---

## 2. Mô tả Dataset và Bộ Quy Tắc Kiểm Định
Bộ dữ liệu FreshRetailNet-50K gồm 19 thuộc tính:
* **7 cột định danh:** `city_id`, `store_id`, `management_group_id`, `first_category_id`, `second_category_id`, `third_category_id`, `product_id`.
* **3 cột thời gian & doanh số:** `dt`, `sale_amount`, `hours_sale` (chuỗi 24 phần tử).
* **2 cột trạng thái hết hàng:** `stock_hour6_22_cnt`, `hours_stock_status` (chuỗi 24 phần tử nhị phân).
* **7 cột ngoại sinh:** `discount`, `holiday_flag`, `activity_flag`, `precpt`, `avg_temperature`, `avg_humidity`, `avg_wind_level`.

### Bộ 48 Quy Tắc Kiểm Định (Validation Rules) Được Thiết Lập:
1. **Kiểm tra Schema & Kích thước:** Kiểm tra đủ 19 cột, số dòng khớp chính xác $4.500.000$ (train) và $350.000$ (eval).
2. **Kiểm tra Dữ liệu Thiếu:** Phát hiện mọi giá trị Null, NaN, chuỗi rỗng trên 19 cột.
3. **Kiểm tra Kiểu Dữ Liệu & Tính Hữu Hạn:** Đảm bảo toàn bộ các cột số là số thực hữu hạn (không chứa $\pm\infty$).
4. **Kiểm tra Khóa Chính & Tính Trùng Lặp:** Khóa `(store_id, product_id, dt)` phải là duy nhất trên từng tập.
5. **Kiểm tra Độ Đầy Đủ Chuỗi (Sequence Completeness):** Đúng $50.000$ cặp `(store_id, product_id)`; tập train có đủ $90$ ngày liên tục ($28/03/2024$ đến $25/06/2024$); tập eval có đủ $7$ ngày liên tục ($26/06/2024$ đến $02/07/2024$).
6. **Kiểm tra Giao Thoa Hai Tập (Cross-Split Checks):**
   * $100\%$ các cặp trong train xuất hiện trong eval (không có cặp nào chỉ có ở train hoặc eval).
   * Không trùng lặp bất kỳ ngày nào giữa train và eval trên cùng một cặp.
7. **Kiểm tra Logic Nghiệp Vụ:**
   * Mảng `hours_sale` có đúng 24 phần tử số không âm.
   * Mảng `hours_stock_status` có đúng 24 phần tử nhị phân ($0$ hoặc $1$).
   * Tính nhất quán doanh số: $\sum_{\tau=0}^{23} \text{hours\_sale}[\tau] \approx \text{sale\_amount}$ (với sai số tuyệt đối $\text{atol} = 10^{-6}$, sai số tương đối $\text{rtol} = 10^{-5}$).
   * Tính nhất quán tồn kho: $\sum_{\tau=6}^{21} \text{hours\_stock\_status}[\tau] == \text{stock\_hour6\_22\_cnt}$.

---

## 3. Các Thư viện và Kỹ Thuật Sử Dụng
* **Công cụ cốt lõi:** Python 3.12, Pandas 3.0.1, NumPy 2.3.5.
* **Kỹ thuật đọc theo lô (Batch Processing):** Đọc dữ liệu theo từng khối `BATCH_SIZE = 20_000` dòng để kiểm soát tiêu thụ bộ nhớ RAM dưới $2\text{ GB}$, cho phép chạy mượt mà ngay cả trên CPU thông thường.
* **Bộ phân tích JSON chuẩn hóa:** Phân tích các cột mảng chuỗi (`hours_sale`, `hours_stock_status`) bằng bộ phân tích `json.loads` nghiêm ngặt, tuyệt đối không dùng lệnh `eval()` nhằm đảm bảo an toàn thực thi và tốc độ.

---

## 4. Quy Trình Xử Lý và Phân Tích Kiểm Định
Quy trình thực hiện tuần tự qua 5 bước trong notebook:
1. **Khởi tạo và cấu hình:** Thiết lập đường dẫn dữ liệu, thông số kỳ vọng (`EXPECTED`) và các ngưỡng sai số.
2. **Kiểm định tập Train:** Quét qua $4.500.000$ dòng, thu thập metadata phân phối min/max, kiểm tra 48 quy tắc và ghi lại tối đa 5 mẫu vi phạm cho mỗi lỗi.
3. **Kiểm định tập Eval:** Quét qua $350.000$ dòng với quy trình tương tự.
4. **Đối soát chéo (Cross-split validation):** Kiểm tra độ phủ của $50.000$ chuỗi và tính không trùng lặp thời gian giữa hai tập.
5. **Xuất báo cáo tự động:** Lưu trữ kết quả kiểm định vào thư mục định danh theo thời gian UTC (`validation_summary.csv`, `column_profile.csv`, `issue_examples.csv`, `run_info.json`).

---

## 5. Kết Quả Thực Nghiệm và Bảng Đối Soát Tổng Hợp

### 5.1. Bảng Tổng Hợp Trạng Thái Kiểm Định (Trích xuất từ `validation_summary.csv`)
* **Tổng số quy tắc được đánh giá:** 97 hạng mục kiểm tra trên hai tập và phần đối chiếu giữa hai tập.
* **Trạng thái:**
  * **96 hạng mục đạt trạng thái `OK` ($0$ trường hợp vi phạm).**
  * **1 hạng mục trạng thái `REVIEW` (Cần xác minh nghiệp vụ).**

| Tập dữ liệu | Hạng mục Kiểm tra | Số vi phạm | Số mẫu đánh giá | Trạng thái | Ghi chú kết quả |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Train** | `schema_columns` | 0 | 19 | **OK** | Đầy đủ đúng 19 cột |
| **Train** | `row_count_matches_reference` | 0 | 1 | **OK** | Đúng $4.500.000$ dòng |
| **Train** | `row_with_missing_or_blank` | 0 | 4.500.000 | **OK** | Không có dòng nào null/rỗng |
| **Train** | `duplicate_keys_excess_rows` | 0 | 4.500.000 | **OK** | Khóa `(store, product, dt)` duy nhất |
| **Train** | `pair_count_matches_50000` | 0 | 1 | **OK** | Đúng $50.000$ cặp cửa hàng-sản phẩm |
| **Train** | `incomplete_or_duplicated_series` | 0 | 50.000 | **OK** | $100\%$ các cặp đủ đúng 90 ngày |
| **Train** | `negative_daily_sales` | 0 | 4.500.000 | **OK** | Không có doanh số ngày âm |
| **Train** | `negative_hourly_sales` | 0 | 4.500.000 | **OK** | Không có doanh số giờ âm |
| **Train** | `hourly_sum_vs_daily_sales` | 0 | 4.500.000 | **OK** | $100\%$ tổng giờ khớp doanh số ngày |
| **Train** | `stock_count_vs_hours_6_22` | 0 | 4.500.000 | **OK** | $100\%$ khớp số giờ hết hàng |
| **Train** | `discount_outside_0_1` | **34** | 4.500.000 | **REVIEW** | 34 dòng có `discount > 1.0` (max 1.088) |
| **Eval** | `row_count_matches_reference` | 0 | 1 | **OK** | Đúng $350.000$ dòng |
| **Eval** | `pair_count_matches_50000` | 0 | 1 | **OK** | Đúng $50.000$ cặp |
| **Eval** | `incomplete_or_duplicated_series` | 0 | 50.000 | **OK** | $100\%$ các cặp đủ đúng 7 ngày |
| **Eval** | `hourly_sum_vs_daily_sales` | 0 | 350.000 | **OK** | $100\%$ khớp hoàn toàn |
| **Eval** | `stock_count_vs_hours_6_22` | 0 | 350.000 | **OK** | $100\%$ khớp hoàn toàn |
| **Eval** | `discount_outside_0_1` | 0 | 350.000 | **OK** | $100\%$ nằm trong $[0.0, 1.0]$ |
| **Cross** | `pairs_only_in_train` | 0 | 50.000 | **OK** | $0$ cặp lệch |
| **Cross** | `pairs_only_in_eval` | 0 | 50.000 | **OK** | $0$ cặp lệch |
| **Cross** | `overlapping_keys` | 0 | 350.000 | **OK** | Không có trùng lặp ngày giữa 2 tập |

### 5.2. Bảng Hồ Sơ Thuộc Tính Số Liệu (Trích xuất từ `column_profile.csv`)
| Cột | Dtype | Nulls | Train Min | Train Max | Eval Min | Eval Max | Nhận xét |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `city_id` | int64 | 0 | 0.0 | 17.0 | 0.0 | 17.0 | 18 thành phố (mã 0..17) |
| `store_id` | int64 | 0 | 0.0 | 897.0 | 0.0 | 897.0 | 898 cửa hàng (mã 0..897) |
| `product_id` | int64 | 0 | 0.0 | 864.0 | 0.0 | 864.0 | 865 sản phẩm (mã 0..864) |
| `sale_amount` | float64 | 0 | 0.0 | 44.9 | 0.0 | 49.9 | Doanh số chuẩn hóa, lệch phải |
| `stock_hour6_22_cnt` | int64 | 0 | 0.0 | 16.0 | 0.0 | 16.0 | Tối đa 16 giờ hết hàng/ngày |
| `discount` | float64 | 0 | 0.0 | **1.088** | 0.0 | 1.0 | Giá trị chuẩn $[0, 1]$, có 34 ngoại lệ |
| `precpt` | float64 | 0 | 0.0 | 42.5 | 0.4949 | 14.8418 | Lượng mưa |
| `avg_temperature` | float64 | 0 | 12.06 | 30.88 | 26.4 | 32.29 | Nhiệt độ tăng dần theo mùa hè |
| `avg_humidity` | float64 | 0 | 27.35 | 100.0 | 51.47 | 86.38 | Độ ẩm hợp lệ trong $[0, 100]$ |
| `avg_wind_level` | float64 | 0 | 0.97 | 3.85 | 1.05 | 3.68 | Cấp độ gió ổn định |

---

## 6. Phân Tích Sâu Các Phát Hiện Quan Trọng

1. **Tính Toàn Vẹn Cực Cao Của Dữ Liệu:**
   * Cả $50.000$ chuỗi đều là bảng cân đối hoàn hảo (balanced panel dataset). Không có chuỗi nào bị đứt gãy giữa chừng, không thiếu bất kỳ ngày nào trong suốt 90 ngày train và 7 ngày eval.
   * Tính nhất quán nội tại đạt $100\%$: Doanh số tổng ngày khớp hoàn toàn với tổng 24 giờ. Số giờ hết hàng khớp tuyệt đối với số lượng bit $1$ trong lát cắt `hours_stock_status[6:22]`.
2. **Ý Nghĩa Khung Giờ Hoạt Động (06:00 – 22:00):**
   * Kết quả đối soát xác nhận rõ ràng rằng cột `stock_hour6_22_cnt` **chỉ tính cho 16 giờ ban ngày (từ 6h sáng đến trước 22h tối)**, không phải 24 giờ. Điều này phản ánh chính xác giờ mở cửa của các kho hàng tươi sống Dingdong Fresh.
3. **Phân Tích 34 Bản Ghi `discount > 1.0`:**
   * Trong tập train, có 34 dòng ghi nhận giá trị discount lớn hơn $1.0$ (giá trị cao nhất đạt $1.088$).
   * Nguồn gốc của các giá trị này chưa được xác minh. Chúng chiếm khoảng 0,00076% số dòng train và được giữ ở trạng thái REVIEW.

---

## 7. Kết Luận và Đề Xuất Cho Toàn Nhóm
* **Kết luận chất lượng dữ liệu:** Bộ dữ liệu FreshRetailNet-50K trong thư mục dự án **đáp ứng các kiểm tra cấu trúc đã thực hiện**; còn một mục REVIEW về discount.
* **Đề xuất hướng xử lý kỹ thuật cho Task 5 (EDA) và Task 8–11 (Mô hình hóa):**
  1. Thống nhất quy ước: Trong `hours_stock_status`, giá trị $1$ là hết hàng và $0$ là còn hàng.
  2. Mẫu số chuẩn khi tính tỷ lệ hết hàng là **$16$ giờ/ngày** (khung giờ hoạt động 6..21).
  3. Giữ nguyên 34 dòng discount trong lượt tái lập chính. [Task 6](../Task06_Data_Preparation/) đã xác nhận các giá trị này vẫn khớp giữa CSV và Parquet.
