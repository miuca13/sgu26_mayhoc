"""Gộp 8 notebook EDA con (E0.1 -> E0.8) thành 1 notebook tổng hợp chạy từ trên xuống dưới.

Cách dùng (đứng ở thư mục gốc repo):
    python notebooks/eda_notebooks/gop_eda.py
Kết quả: notebooks/eda_notebooks/00_EDA_tong_hop_Han.ipynb (chưa có output) -> mở và Run All.
Cần chạy 01_cleaning.ipynb trước để có data/processed/hourly_clean.csv (phần E0.4 -> E0.8).

Quy tắc: 8 notebook con là nguồn gốc. Khi sửa code EDA thì sửa trong notebook con tương ứng,
rồi chạy lại script này. Script chỉ chép ô, bỏ các ô lặp lại (ô log, thông tin, cài đặt, đọc dữ liệu,
chuẩn bị riêng, nhật ký riêng) và không sửa nội dung ô phân tích nào.

Tạo 13/11/2026 – Cao Ngọc Hân.
"""
import copy
import datetime
import json
from pathlib import Path

THU_MUC = Path(__file__).resolve().parent
NGUON = [
    ("E0.1", "00_E0.1_cach_ghi_va_thoi_gian_Han.ipynb", "Dữ liệu thô"),
    ("E0.2", "00_E0.2_khoang_thieu_Han.ipynb", "Dữ liệu thô"),
    ("E0.3", "00_E0.3_phan_bo_va_quan_he_muc_phut_Han.ipynb", "Dữ liệu thô"),
    ("E0.4", "02_E0.4_phan_bo_cong_suat_theo_gio_Han.ipynb", "Dữ liệu theo giờ"),
    ("E0.5", "02_E0.5_rq1_theo_gio_va_thu_Han.ipynb", "Dữ liệu theo giờ"),
    ("E0.6", "02_E0.6_rq1_theo_thang_mua_xu_huong_Han.ipynb", "Dữ liệu theo giờ"),
    ("E0.7", "02_E0.7_rq1_chu_ky_va_cong_to_phu_Han.ipynb", "Dữ liệu theo giờ"),
    ("E0.8", "02_E0.8_rq2_tuong_quan_Han.ipynb", "Dữ liệu theo giờ"),
]
TEN_RA = "00_EDA_tong_hop_Han"

# Ô cài đặt / đọc dữ liệu lặp lại ở nhiều notebook con: chỉ giữ lần xuất hiện đầu tiên
CHI_GIU_MOT_LAN = ("import zipfile", "from pathlib import Path", "raw = pd.read_csv(FILE")
LUON_BO = ("# [CHUẨN BỊ RIÊNG]", "## Nhật ký", "## Log lên W&B", "# W&B")


def src(c):
    return "".join(c["source"])


def o_md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)}


def o_code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": text.strip("\n").splitlines(keepends=True)}


def lam_sach(c):
    c = copy.deepcopy(c)
    c["metadata"] = {}
    c.pop("id", None)
    if c["cell_type"] == "code":
        c["execution_count"], c["outputs"] = None, []
    return c


nbs = [(ma, ten, nhom, json.loads((THU_MUC / ten).read_text(encoding="utf-8"))) for ma, ten, nhom in NGUON]
o_moi, da_gap = [], set()

o_log = lam_sach(nbs[0][3]["cells"][0])
o_log["source"] = src(o_log).replace(f'"{Path(NGUON[0][1]).stem}"', f'"{TEN_RA}"').splitlines(keepends=True)
o_moi.append(o_log)

muc_luc = "\n".join(f"| {ma} | {nhom} | `{ten}` |" for ma, ten, nhom in NGUON)
o_moi.append(o_md(f"""
# EDA tổng hợp E0.1 → E0.8 (Dự báo điện năng hộ gia đình)

| | |
|---|---|
| **Tác giả** | Cao Ngọc Hân – Nhóm 11 |
| **Ngày tạo** | {datetime.date.today():%d/%m/%Y} – sinh tự động bằng `notebooks/eda_notebooks/gop_eda.py` từ 8 notebook con |
| **Đọc vào** | `data/raw/individual+household+electric+power+consumption.zip`, `data/processed/hourly_clean.csv` |
| **Ghi ra** | Giống 8 notebook con, cộng thêm `data/eda_data/eda_00_kho_khan_xu_ly.csv`, `data/eda_data/eda_goi_y_nhan_xet.md`, `data/eda_data/eda_00_tom_tat.txt` |
| **Chạy sau** | `01_cleaning.ipynb` (cần `hourly_clean.csv` cho phần E0.4 → E0.8) |

Đây là **bản chính thức đọc từ trên xuống dưới** của toàn bộ phần EDA. Nội dung từng phần chép nguyên
từ notebook con, chỉ bỏ các ô chuẩn bị bị lặp lại.

| Phần | Dữ liệu | Notebook con (nguồn gốc) |
|---|---|---|
{muc_luc}

**Sửa code:** sửa trong notebook con, rồi chạy `python notebooks/eda_notebooks/gop_eda.py` để sinh lại file này.
"""))

for ma, ten, nhom, nb in nbs:
    o_moi.append(o_md(f"---\n# Phần {ma}\n> Nguồn: `notebooks/eda_notebooks/{ten}`"))
    for i, c in enumerate(nb["cells"]):
        s = src(c).strip()
        if i <= 1 or s.startswith(LUON_BO):
            continue
        if c["cell_type"] == "code" and s.startswith(CHI_GIU_MOT_LAN):
            if s in da_gap:
                continue
            da_gap.add(s)
        o_moi.append(lam_sach(c))

o_moi.append(o_md("---\n# Tổng hợp toàn bộ EDA\nBảng khó khăn dữ liệu (E0.1 → E0.3) và các câu gợi ý nhận xét có số tự điền (E0.4 → E0.8)."))
o_moi.append(o_code('''
bang_kk = pd.DataFrame(kho_khan)
bang_kk.index = range(1, len(bang_kk) + 1)
bang_kk.to_csv(DIR_DATA / "eda_00_kho_khan_xu_ly.csv", encoding="utf-8-sig", index_label="STT")
with pd.option_context("display.max_colwidth", None):
    display(bang_kk)

tom_tat = (f"EDA dữ liệu thô: {fmt(n_dong)} dòng × {n_cot} cột, mỗi phút 1 dòng, "
           f"từ {ts.iloc[0]:%d/%m/%Y %H:%M} đến {ts.iloc[-1]:%d/%m/%Y %H:%M}.\\n"
           + "\\n".join(f"  {i}. {r['Khó khăn']}: {r['Bằng chứng (số thật)']} → {r['Cách xử lý']} ({r['Xử lý ở đâu']})."
                       for i, r in bang_kk.iterrows()))
(DIR_DATA / "eda_00_tom_tat.txt").write_text(tom_tat, encoding="utf-8")

goi_y = "# Câu gợi ý nhận xét EDA (số liệu tự điền từ các notebook E0.4 → E0.8)\\n\\n" + "\\n".join(notes)
(DIR_DATA / "eda_goi_y_nhan_xet.md").write_text(goi_y, encoding="utf-8")
log.info("Tóm tắt khó khăn dữ liệu:\\n" + tom_tat)
log.info(goi_y)
'''))
o_moi.append(o_md("## Nhật ký\n\n- 13/11/2026 – Gộp 8 notebook EDA con (E0.1 → E0.8) thành bản hoàn chỉnh `00_EDA_tong_hop_Han.ipynb` bằng script `gop_eda.py`. Commit `...`."))

ra = {"cells": o_moi, "metadata": nbs[0][3]["metadata"], "nbformat": 4, "nbformat_minor": 4}
(THU_MUC / f"{TEN_RA}.ipynb").write_text(json.dumps(ra, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"Đã tạo {TEN_RA}.ipynb: {len(o_moi)} ô (gộp từ {len(nbs)} notebook)")
