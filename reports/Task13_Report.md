# Báo cáo Task 13: Dự báo nhu cầu bằng SSA trên dữ liệu khôi phục DLinear (`SSA_DLinear`) & Tổng hợp Cột SSA

**Người thực hiện:** Phạm Đăng Khoa (`dangkhoauit184`) | **Nhánh:** `feature/task13-ssa-dlinear` | **Thư mục:** `Task13_SSA_DLinear/`

## 1. Mục tiêu và Thiết lập thực nghiệm
- **Mục tiêu:** Đánh giá hiệu năng dự báo 7 ngày của thuật toán thống kê **Similar Scenario Average (SSA)** khi sử dụng chuỗi nhu cầu khôi phục từ mô hình tuyến tính **DLinear** (`SSA_DLinear`), qua đó hoàn thiện đối chứng toàn diện ba cấp độ dữ liệu lịch sử trên cột **SSA** của Bảng 3: doanh số thô bị che khuất (`SSA_RawSales` — [Task 8](Task08_Report.md)), khôi phục tuyến tính (`SSA_DLinear` — Task 13) và khôi phục chu kỳ 2D (`SSA_TimesNet` — [Task 11](Task11_Report.md)).
- **Đầu vào lịch sử (90 ngày `train`):** Cột `sale_amount_pred` từ `demand_dlinear.parquet` của [Task 12](Task12_Report.md) (`4.500.000` dòng × `20` cột, `81.531.473` bytes, SHA-256: `2cd9091adec89b129d0c726e3be658b9becf027b4ece1e3b725feb74176ab65b`).
- **Đầu vào đối chiếu (7 ngày `eval`):** Cột `sale_amount` thực tế từ `eval.parquet` chuẩn của [Task 6](Task06_Report.md) (`350.000` dòng × `19` cột, `5.451.872` bytes, SHA-256: `61cfd3cb60d767d38ba9e640be64e982a15b2918ca0ba14fe0283c5a2eac6872`), lọc đúng **206.562** dòng không hết hàng (`stock_hour6_22_cnt == 0`).
- **Phân nhóm `psd` đồng bộ tuyệt đối:** `psd` được tính bằng trung bình `sale_amount` **gốc** trong tập `train` (`dt <= '2024-06-25'`), giữ nguyên `Low Sale = 153.208` dòng (`psd < 1`) và `High Sale = 53.354` dòng (`psd >= 1`) trùng khớp 100% với Task 8 và Task 11.

## 2. Kết quả định lượng và Tổng hợp 3 cấu hình cột SSA (Bảng 3)

| Phân nhóm | Cấu hình | WAPE thực chạy | WPE thực chạy | MAE | WAPE bài báo | WPE bài báo | Chênh lệch WAPE | Chênh lệch WPE |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** (`206.562` dòng) | `SSA_RawSales` (Task 8) | 31.97% | -10.50% | 0.3982 | 31.97% | -10.50% | 0.00 pp | 0.00 pp |
| | **`SSA_DLinear` (Task 13)** | **30.12%** | **-0.58%** | **0.3749** | 30.00% | -1.49% | **+0.12 pp** | **+0.91 pp** |
| | `SSA_TimesNet` (Task 11) | 29.79% | +1.40% | 0.3709 | 29.79% | +1.39% | 0.00 pp | +0.01 pp |
| **Low Sale** (`153.208` dòng) | `SSA_RawSales` (Task 8) | 38.33% | -8.03% | 0.2691 | 38.33% | -8.03% | 0.00 pp | 0.00 pp |
| | **`SSA_DLinear` (Task 13)** | **38.00%** | **+3.69%** | **0.2664** | *(không in)* | *(không in)* | – | – |
| | `SSA_TimesNet` (Task 11) | 37.87% | +4.96% | 0.2656 | 37.87% | +4.89% | 0.00 pp | +0.07 pp |
| **High Sale** (`53.354` dòng) | `SSA_RawSales` (Task 8) | 27.40% | -12.26% | 0.7761 | 27.40% | -12.26% | 0.00 pp | 0.00 pp |
| | **`SSA_DLinear` (Task 13)** | **24.46%** | **-3.64%** | **0.6925** | *(không in)* | *(không in)* | – | – |
| | `SSA_TimesNet` (Task 11) | 23.98% | -1.15% | 0.6790 | 23.98% | -1.12% | 0.00 pp | -0.03 pp |

*(Trong tệp CSV kết quả, 4 cột `paper_*` và `delta_*` của `SSA_DLinear` ở hai nhóm con `Low Sale` và `High Sale` được để trống vì Bảng 3 bài báo gốc không công bố số cho hai dòng này).*

## 3. Phân tích chuyên môn và Liên kết chuỗi nhân quả Bảng 2 → Bảng 3

1. **Khớp sát số công bố Bảng 3 ở nhóm `Overall`:**
   - `SSA_DLinear` đạt WAPE **30.12%** so với **30.00%** của bài báo (chênh lệch chỉ **+0.12 điểm phần trăm**) và WPE **-0.58%** so với **-1.49%** của bài báo (cùng mang dấu âm nhẹ sát 0, chênh **+0.91 pp**). Kết quả này xác nhận tệp `demand_dlinear.parquet` xuất từ Task 12 hoàn toàn hợp lệ và tái lập chính xác hành vi dự báo hạ nguồn của bài báo.
2. **Thứ tự cải thiện đơn điệu nhất quán tuyệt đối trên mọi phân nhóm (`RawSales` → `DLinear` → `TimesNet`):**
   - Cả hai thước đo sai số **WAPE** và **MAE** đều giảm đơn điệu theo đúng thứ hạng chất lượng khôi phục ở Bảng 2 trên cả ba phân nhóm:
     - `Overall`: WAPE `31.97%` → **`30.12%`** → `29.79%` | MAE `0.3982` → **`0.3749`** → `0.3709`.
     - `Low Sale`: WAPE `38.33%` → **`38.00%`** → `37.87%` | MAE `0.2691` → **`0.2664`** → `0.2656`.
     - `High Sale`: WAPE `27.40%` → **`24.46%`** → `23.98%` | MAE `0.7761` → **`0.6925`** → `0.6790`.
   - Ngay cả một mô hình khôi phục tuyến tính đơn giản như `DLinear` cũng giúp giảm **1.85 điểm phần trăm** WAPE trên `Overall` (và **2.94 điểm phần trăm** trên `High Sale`), đồng thời kéo WPE từ `-10.50%` về `-0.58%` — chứng minh bước **khôi phục nhu cầu bị che khuất (Stage 1)** đóng vai trò quyết định trước khi dự báo.
3. **Giải thích mối liên hệ trực tiếp với hiện tượng thiên lệch âm của `DLinear` ở Task 12:**
   - Ở [Task 12](Task12_Report.md), `DLinear` có Decoupling Score đạt **-0.15** (vẫn còn tương quan âm với số giờ hết hàng, so với **+0.07** của `TimesNet`) và WPE MNAR âm (`-14.38%`) do chỉ khôi phục tại đúng 19,88% giờ hết hàng nhưng bị kéo thấp bởi các chuỗi giờ bằng 0.
   - Khi tổng hợp lên cấp ngày (`sale_amount_pred` trung bình đạt `1.1438` đơn vị/ngày so với `0.9986` của doanh số thô), phần nhu cầu bù thêm ở các giờ hết hàng giúp xóa phần lớn thiên lệch âm của `SSA_RawSales` (`-10.50%` → `-0.58%` ở `Overall`). Tuy nhiên, ở nhóm mặt hàng bán chạy thường xuyên hết hàng kéo dài (**High Sale**), hạn chế tách rời chưa triệt để của `DLinear` làm `SSA_DLinear` vẫn còn dự báo thiếu **-3.64%**, trong khi `SSA_TimesNet` rút ngắn độ lệch này xuống chỉ còn **-1.15%** và giảm thêm **0.48 pp** WAPE (`23.98%` so với `24.46%`).

## 4. Bàn giao
- [Notebook đã chạy](../Task13_SSA_DLinear/notebooks/13_ssa_dlinear.ipynb), [bảng chỉ số `SSA_DLinear`](../Task13_SSA_DLinear/results/ssa_dlinear_metrics.csv), [bảng tổng hợp 3 cấu hình cột SSA](../Task13_SSA_DLinear/results/ssa_all_3configs_summary.csv), [log gốc](../Task13_SSA_DLinear/results/full/ssa_dlinear.log), [metadata](../Task13_SSA_DLinear/results/run_metadata.json) và [biên bản chạy](../Task13_SSA_DLinear/run_info.md).
