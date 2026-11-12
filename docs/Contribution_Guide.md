# Hướng Dẫn Cộng Tác Mã Nguồn Dành Cho Nhóm 5 Thành Viên

Tài liệu này quy định quy trình làm việc chung trên GitHub của nhóm nhằm đảm bảo tính toàn vẹn của mã nguồn, tránh xung đột (merge conflicts) và không làm mất bài của nhau.

---

## 1. Nguyên Tắc Cốt Lõi
1. **Không commit trực tiếp lên nhánh `main`:** Mọi thành viên phải tạo nhánh riêng (feature branch) cho nhiệm vụ của mình. Nhánh `main` chỉ chứa phiên bản ổn định đã được kiểm tra và đồng thuận.
2. **Không commit file dữ liệu lớn:** File `.csv`, `.parquet`, `.npy`, checkpoints `.ckpt` tuyệt đối không đẩy lên GitHub (đã được cấu hình trong `.gitignore`). Hãy lưu dữ liệu lớn trên Google Drive cá nhân hoặc Google Drive nhóm.
3. **Commit thường xuyên với thông điệp rõ ràng:** Mỗi commit nên giải quyết một phần việc cụ thể.
4. **Pull code mới nhất trước khi bắt đầu làm:** Luôn đồng bộ mã nguồn từ `main` về máy trước khi tạo nhánh hoặc code tiếp.

---

## 2. Quy Trình Làm Việc Chi Tiết (Git Workflow)

### Bước 1: Clone Repository về máy cá nhân
```bash
git clone https://github.com/dangkhoauit184/PTDLKD.git
cd PTDLKD
```

### Bước 2: Tạo nhánh mới cho Task phụ trách
Quy ước đặt tên nhánh: `feature/task<số_task>-<tên_nhiệm_vụ>` hoặc `fix/<nội_dung>`
* Ví dụ:
  * Thành viên làm Task 1: `feature/task01-paper-review`
  * Thành viên làm Task 2: `feature/task02-experiment-plan`
  * Thành viên làm Task 3: `feature/task03-colab-environment`
  * Thành viên làm Task 4: `feature/task04-data-validation`
  * Thành viên làm Task 5: `feature/task05-eda-analysis`

Lệnh tạo và chuyển sang nhánh mới:
```bash
# Đảm bảo đang ở main và cập nhật mới nhất
git checkout main
git pull origin main

# Tạo nhánh mới và chuyển sang nhánh đó
git checkout -b feature/task04-data-validation
```

### Bước 3: Thực hiện công việc và Commit
Chỉ chỉnh sửa hoặc bổ sung file trong thư mục Task tương ứng (`Task01_...`, `Task04_...`, v.v.).

Kiểm tra trạng thái trước khi commit:
```bash
git status
```
*Đảm bảo không có file dữ liệu nặng (train.csv, train.parquet,...) trong danh sách Untracked files.*

Thêm file và commit theo chuẩn **Conventional Commits**:
```bash
git add Task04_Data_Validation/
git commit -m "feat(task04): bổ sung bảng kết quả đối soát validation_summary"
```
*Tiền tố commit phổ biến:*
* `feat`: Thêm tính năng mới, notebook mới, bảng phân tích mới.
* `fix`: Sửa lỗi trong notebook, sửa đường dẫn file, sửa công thức.
* `docs`: Cập nhật tài liệu, README, báo cáo markdown.
* `refactor`: Dọn dẹp code, tối ưu hóa không làm đổi kết quả.

### Bước 4: Đẩy nhánh lên GitHub
```bash
git push -u origin feature/task04-data-validation
```

### Bước 5: Tạo Pull Request (PR) trên GitHub
1. Truy cập vào repository: `https://github.com/dangkhoauit184/PTDLKD`.
2. Bấm vào **"Compare & pull request"**.
3. Điền tiêu đề và mô tả PR:
   - Mô tả ngắn gọn phần việc đã làm.
   - Kết quả đạt được (kèm số liệu hoặc ảnh chụp notebook nếu có).
   - Đánh dấu người duyệt (Reviewers).
4. Ít nhất 1 thành viên khác trong nhóm xem xét (Review) và bấm **Approve**.
5. Chọn **"Merge pull request"** (khuyến nghị chọn *Squash and merge* hoặc *Rebase and merge* để lịch sử commit gọn gàng).

### Bước 6: Đồng bộ nhánh `main` sau khi merge
Sau khi PR đã được merge trên GitHub, các thành viên cập nhật lại nhánh `main` ở máy cá nhân:
```bash
git checkout main
git pull origin main
```

---

## 3. Cách Xử Lý Khi Gặp Xung Đột (Merge Conflicts)
Nếu nhánh của bạn bị báo Conflict khi merge vào `main`:
```bash
git checkout feature/task-cua-ban
git pull origin main
```
* Mở các file bị conflict trong VS Code / PyCharm.
* Trao đổi trực tiếp với thành viên liên quan để chọn giữ phần code chính xác.
* Lưu file, sau đó:
```bash
git add <file_da_sua>
git commit -m "fix: giải quyết merge conflict với nhánh main"
git push origin feature/task-cua-ban
```

---

## 4. Hướng Dẫn Mời Thành Viên Cộng Tác Vào Repo
Người quản lý repository (`dangkhoauit184`) thực hiện:
1. Vào trang repo `https://github.com/dangkhoauit184/PTDLKD`.
2. Chọn tab **Settings** $\rightarrow$ **Collaborators** ở thanh bên trái.
3. Bấm **"Add people"**.
4. Nhập username GitHub hoặc email của 4 thành viên còn lại trong nhóm và gửi lời mời.
5. Các thành viên kiểm tra email hoặc thông báo GitHub để **Accept invitation**.
