# Đề tài cuối kỳ – Dự báo công suất tiêu thụ điện năng hộ gia đình (Nhóm 11)

Repo nhóm: https://github.com/SGU-MayHoc-Nhom11/Nhom11_DuBaoDienNang_GiuaKy
Thư mục này chỉ chứa phần Cao Ngọc Hân (3124411083, nhóm trưởng) làm. Bản đầy đủ, lịch sử commit, phần của Linh và Nhung xem ở repo nhóm (README repo nhóm ghi người làm và mã commit từng file).

## Phần Hân làm
- Dữ liệu: tải bộ UCI, kiểm tra SHA-256, mô tả dữ liệu gốc (`src/00_raw_info.py`, 30–31/10).
- Tiền xử lý: `notebooks/tien_xu_ly/01_cleaning.ipynb` – làm sạch, tổng hợp theo giờ (01/11, chạy lại có log 13/11).
- EDA: E0.1–E0.3 dữ liệu thô mức phút, E0.4–E0.8 theo giờ trả lời RQ1, RQ2; bản gộp `00_EDA_tong_hop_Han` sinh bằng `gop_eda.py` (01/11, tách notebook 13–14/11).
- Nhập Experiment Log lên W&B: `notebooks/nhap_wandb/07_nhap_wandb_experiment_log_Han.ipynb` (14/11).
- Nhóm trưởng: quy ước, kế hoạch, phân công, GitHub Issues, Drive kết quả, sổ thí nghiệm, gom thư mục repo, README, kiểm tra chéo.

## Trong thư mục này
- `notebooks/`: notebook của Hân.
- `logs/`: log từng lần chạy (`eda_log`, `tien_xu_ly_log`, `nhap_wandb_log`).
- `figures/`: hình EDA và tiền xử lý.
- `src/00_raw_info.py`: mô tả dữ liệu gốc.

Notebook đọc dữ liệu theo đường dẫn của repo nhóm; muốn chạy lại thì clone repo nhóm.
