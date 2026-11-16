# Task 7 — Chạy thử TimesNet → SSA

Notebook smoke test: `07_smoke_test.ipynb`. Mở từ thư mục gốc PTDLKD trong môi trường Python của Task 3. Notebook tải dataset chính thức, cố định 100 cặp đủ 90 ngày train/7 ngày eval, clone mã tác giả tại commit `8af694a09a5a427d1d50648d348c022565a781f2`, áp dụng các thay đổi đường dẫn smoke và chạy hai nhánh SSA.

TimesNet dùng `--missing_rate 0 --epochs 1` cho lượt thử (mặc định baseline là 5 epoch). Notebook xác nhận số dòng, khóa và `sale_amount_pred`, rồi ghi metrics, logs và `run_info.md` vào thư mục này.

## Trạng thái hiện tại

Notebook và patch đã được chuẩn bị. Chưa chạy được trong runtime Codex hiện tại vì Windows Application Control chặn nạp extension NumPy native được cài trong workspace. Vì vậy các chỉ số đang để trống với `not_run`; không có Parquet hay cặp thử được báo là đã tạo. Chạy notebook trong môi trường tương thích để hoàn tất smoke test.

Parquet thuộc nhóm dữ liệu sinh ra khi chạy và không commit lên repo theo quy ước dự án. Lưu bản Parquet smoke cùng logs vào thư mục kết quả được chia sẻ sau khi notebook chạy xong.
