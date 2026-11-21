# Task 7 — Chạy thử TimesNet → SSA

`07_smoke_test.ipynb` chọn cố định 100 cặp có đủ 90 ngày train và 7 ngày eval, lưu danh sách cặp, lọc hai split theo cùng danh sách, rồi chạy SSA trên sale_amount và trên demand do TimesNet phục hồi.

## Kết quả chạy thử

- 100 cặp duy nhất; 9.000 dòng train và 700 dòng eval.
- Có giờ hết hàng trong train và ít nhất một giờ eval hợp lệ ở mỗi cặp.
- TimesNet chạy với `--missing_rate 0 --epochs 2`; `patience=1` để đáp ứng ràng buộc `patience < epochs` của mô hình. Mặc định baseline là 5 epoch và patience 5.
- Parquet đầu ra có 9.000 khóa train khớp; `sale_amount_pred` hữu hạn và không âm.
- SSA RawSales Overall: WAPE 35.60%, WPE -6.15%.
- SSA TimesNet Overall: WAPE 35.11%, WPE -0.63%.
- Low Sale và High Sale đều có mẫu hợp lệ ở cả hai nhánh.

Chi tiết tham số và điều kiện mẫu nằm trong `run_info.md`; log nằm trong `smoke/`. Đây là kết quả smoke test, không dùng thay số liệu Bảng 3.

## Tệp bàn giao

- [07_smoke_test.ipynb](07_smoke_test.ipynb) và [patch_baseline.py](patch_baseline.py): notebook có output thực chạy của các bước lọc, chạy TimesNet, kiểm tra Parquet và bảng metrics.
- [smoke_pairs.csv](smoke_pairs.csv): 100 cặp duy nhất (`store_id`, `product_id`).
- [smoke_metrics.csv](smoke_metrics.csv): WAPE/WPE theo nhánh (`SSA_RawSales`, `SSA_TimesNet`) và phân nhóm.
- [smoke/ssa_raw.log](smoke/ssa_raw.log), [smoke/timesnet.log](smoke/timesnet.log), [smoke/ssa_timesnet.log](smoke/ssa_timesnet.log): log thực chạy ba giai đoạn.
- [run_info.md](run_info.md) và [Báo cáo Task 7](../reports/Task07_Report.md): thông tin nguồn dữ liệu, môi trường, tham số và SHA-256 của tệp `demand_timesnet_smoke.parquet` (`9.000` dòng; tệp `.parquet` không lưu trên GitHub theo [Contribution Guide](../docs/Contribution_Guide.md)).

Các tệp Parquet trung gian được sinh tự động khi chạy notebook và bị loại trừ khỏi Git qua `.gitignore`.
