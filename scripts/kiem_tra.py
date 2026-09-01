#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kiem_tra.py — Bắt các dấu hiệu "văn dịch máy" và "văn mẫu AI" trong tiếng Việt học thuật.

Chỉ bắt lỗi CƠ HỌC (những thứ regex xác định được chắc chắn).
Nhịp điệu và độ tự nhiên vẫn cần người đọc đánh giá lại.

Nguyên tắc: thà sót còn hơn báo oan.

Mọi signal đều đọc từ patterns/*.yml qua scripts/catalog.py, nên không có luật
nào được định nghĩa lần thứ hai ở đây. Chế độ nào áp dụng luật nào là do trường
che_do trong catalog quyết định.

    python scripts/kiem_tra.py bai.md [--che-do hoc-thuat|ky-thuat|cong-viec|doi-thuong]
"""

import argparse, re, sys, unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog

# Fix UTF-8 encoding on Windows console
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ------------------------------------------------------- phân loại từng dòng

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`\n]+`")
URL = re.compile(r"https?://\S+|www\.\S+")
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
MA_NGUON = re.compile(
    r"\b(function|contract|require|return|import|public|private|external|"
    r"uint256|address|struct|const|let|var|def|class|if|for|while)\b"
    r"|[{}();]\s*$|=>|::|\)\s*\{"
)

VAN, TIEU_DE, CODE, BANG, CHU_THICH = "van", "tieu_de", "code", "bang", "chu_thich"

# Chú thích hình/bảng và mục tài liệu tham khảo không phải văn xuôi.
CHU_THICH_RE = re.compile(r"^\**\s*(Hình|Bảng|Biểu đồ|Sơ đồ|Figure|Table)\s*\d", re.I)
TLTK_RE = re.compile(r"^\**\s*(TÀI LIỆU THAM KHẢO|\[\d+\])", re.I)


def phan_loai(text):
    """Trả về [(so_dong, noi_dung, loai)]. Tách văn xuôi khỏi tiêu đề, code, bảng."""
    ket_qua, trong_fence = [], False
    for i, dong in enumerate(text.split("\n"), 1):
        d = dong.strip()
        if FENCE.match(d):
            trong_fence = not trong_fence
            continue
        if trong_fence or not d:
            continue
        if CHU_THICH_RE.match(d) or TLTK_RE.match(d):
            ket_qua.append((i, d, CHU_THICH)); continue
        if d.startswith("|") or re.match(r"^[\|\+\-\s:]+$", d):
            ket_qua.append((i, d, BANG)); continue
        if MA_NGUON.search(d):
            ket_qua.append((i, d, CODE)); continue
        if d.startswith("#") or re.match(r"^\**(CHƯƠNG|PHỤ LỤC|MỤC LỤC|DANH MỤC|TÀI LIỆU)\b", d):
            ket_qua.append((i, re.sub(r"^#+\s*", "", d).strip("* "), TIEU_DE)); continue
        if re.match(r"^\**\d+(\.\d+)*\.?\s+\S", d) and not re.search(r"[.!?]\s*$", d) and len(d) < 90:
            ket_qua.append((i, d.strip("* "), TIEU_DE)); continue
        d = INLINE_CODE.sub(" ", MD_LINK.sub(r"\1", URL.sub(" ", d)))
        d = re.sub(r"^\s*[\-\*\+•]\s+", "", d).strip("* ")
        if d:
            ket_qua.append((i, d, VAN))
    return ket_qua


def van_xuoi(dong_pl):
    return [(i, d) for i, d, l in dong_pl if l == VAN]


def tach_cau(dong_van):
    ra = []
    for i, d in dong_van:
        for c in re.split(r"(?<![0-9])(?<=[\.\!\?…])\s+", d):
            c = c.strip()
            if c:
                ra.append((i, c))
    return ra


def dem_am_tiet(cau):
    return len(re.findall(r"[^\W\d_]+", cau, re.UNICODE))


def chuan_hoa(s):
    return unicodedata.normalize("NFC", s.lower().strip())


TRICH_DAN = re.compile(r"“[^”]*”")


def che_trich_dan(dong):
    """Thay phần trong “ ” bằng khoảng trắng.

    Trích dẫn nguyên văn phải giữ đúng chữ của nguồn, kể cả khi nguồn dùng
    khẩu ngữ hay xưng hô 'bạn'. Xem references/false-positives.md mục 6.
    """
    return TRICH_DAN.sub(lambda m: " " * len(m.group(0)), dong)


# ------------------------------------------------------- luật lấy từ catalog

CATALOG = catalog.nap_catalog()

# mã lỗi của linter -> mã pattern trong catalog
MA_PATTERN = {
    "gach-ngang": "VA-L2-14",
    "cham-phay": "VA-L1-05",
    "mot-cach": "VA-L1-03",
    "bi-dong": "VA-L1-02",
    "ngoac-kep": "VA-L1-14",
    "so-thap-phan": "VA-L1-06",
    "cau-cut": "VA-L1-07",
    "doi-xung": "VA-L2-09",
    "danh-tu-hoa": "VA-L1-04",
    "rao-don": "VA-L2-24",
    "lap-tu-noi": "VA-L1-13",
    "thieu-lien-ket": "VA-L1-01",
    "tieu-de-hoa": "VA-L2-17",
    "lech-register": "VA-L1-08",
    "thoi-phong": "VA-L2-01",
    "sao-ngu": "VA-L2-07",
    "nguon-mo-ho": "VA-L2-05",
    "xung-ho": "VA-L1-11",
    "bi-dong-trung": "VA-L1-15",
    "ngay-thang": "VA-L1-16",
    "chuoi-cua": "VA-L1-17",
}

GACH_CHEN = catalog.bien_dich(CATALOG, "VA-L2-14")
CHAM_PHAY = catalog.bien_dich(CATALOG, "VA-L1-05")
MOT_CACH = catalog.bien_dich(CATALOG, "VA-L1-03")
BI_DONG = catalog.bien_dich(CATALOG, "VA-L1-02")
NGOAC_THANG = catalog.bien_dich(CATALOG, "VA-L1-14")
SO_THAP_PHAN = catalog.bien_dich(CATALOG, "VA-L1-06")
DOI_XUNG = catalog.bien_dich(CATALOG, "VA-L2-09")
DANH_TU_HOA = catalog.bien_dich(CATALOG, "VA-L1-04")
KHAU_NGU = catalog.bien_dich(CATALOG, "VA-L1-08")
XUNG_HO_BAN = catalog.bien_dich(CATALOG, "VA-L1-11")
BI_DONG_TRUNG_RE = catalog.bien_dich(CATALOG, "VA-L1-15")
NGAY_THANG = catalog.bien_dich(CATALOG, "VA-L1-16")
CHUOI_CUA = catalog.bien_dich(CATALOG, "VA-L1-17")

THOI_PHONG_RE = catalog.bien_dich_cum_tu(CATALOG, "VA-L2-01")
SAO_NGU_RE = catalog.bien_dich_cum_tu(CATALOG, "VA-L2-07")
NGUON_MO_HO_RE = catalog.bien_dich_cum_tu(CATALOG, "VA-L2-05")

TU_NOI = CATALOG["VA-L1-13"]["phrases"]
TU_NOI_RE = catalog.bien_dich_cum_tu(CATALOG, "VA-L1-13")
RAO_DON = [chuan_hoa(c) for c in CATALOG["VA-L2-24"]["phrases"]]

# Từ nối lặp quá nhiều lần thì văn đơn điệu. Đây là ngưỡng chỉnh tay, không phải luật.
TU_NOI_DE_LAP = ["vì vậy", "do đó", "tuy nhiên", "ngoài ra", "bên cạnh đó",
                 "đồng thời", "hơn nữa", "vì thế"]


class Loi:
    def __init__(s, ma, dong, trich, goi_y, muc="nang"):
        s.ma, s.dong, s.trich, s.goi_y, s.muc = ma, dong, trich, goi_y, muc
        s.pattern = MA_PATTERN.get(ma, "")


def quet(text, che_do="hoc-thuat", nguong_cut=6, nguong_chuoi=3):
    pl = phan_loai(text)
    dv = van_xuoi(pl)
    cau = tach_cau(dv)
    loi = []
    G = lambda *a, **k: loi.append(Loi(*a, **k))

    def bat(ma):
        """Chế độ đang chạy có áp dụng luật này không? Do che_do trong catalog quyết định."""
        return catalog.ap_dung_cho(CATALOG, MA_PATTERN[ma], che_do)

    for i, d in dv:
        d = che_trich_dan(d)
        d_ngoai_ngoac = re.sub(r"\([^)]*\)", " ", d)
        if bat("gach-ngang"):
            for m in GACH_CHEN.finditer(d_ngoai_ngoac):
                G("gach-ngang", i, d[:90], "Tiếng Việt học thuật không dùng gạch ngang chen giữa câu. "
                  "Tách thành hai câu hoặc thay bằng dấu phẩy và từ nối.")
        if bat("cham-phay") and CHAM_PHAY.search(d):
            G("cham-phay", i, d[:90], "Tiếng Việt không dùng chấm phẩy giữa câu. Thay bằng dấu phẩy hoặc tách câu.")
        if bat("mot-cach"):
            for m in MOT_CACH.finditer(d):
                G("mot-cach", i, m.group(0), "Bỏ 'một cách', giữ nguyên tính từ (dấu vết dịch đuôi '-ly').")
        if bat("bi-dong"):
            for m in BI_DONG.finditer(d):
                G("bi-dong", i, m.group(0)[:90], "Đảo thành chủ động, hoặc dùng 'do ... thực hiện'.")
        if bat("so-thap-phan"):
            for m in SO_THAP_PHAN.finditer(d):
                G("so-thap-phan", i, m.group(0),
                  f"Tiếng Việt viết {m.group(0).replace('.', ',')}.", muc="nhe")
        if bat("thoi-phong"):
            for m in THOI_PHONG_RE.finditer(d):
                G("thoi-phong", i, m.group(0), "Thổi phồng tầm quan trọng. Nêu sự thật trực tiếp.", muc="nhe")
        if bat("sao-ngu"):
            for m in SAO_NGU_RE.finditer(d):
                G("sao-ngu", i, m.group(0), "Sáo ngữ AI trừu tượng. Thay bằng từ vựng kỹ thuật cụ thể.", muc="nhe")
        if bat("nguon-mo-ho"):
            for m in NGUON_MO_HO_RE.finditer(d):
                G("nguon-mo-ho", i, m.group(0), "Nguồn mơ hồ. Dẫn trích dẫn cụ thể ([1]) hoặc nêu thẳng sự kiện.")
        if bat("ngay-thang"):
            for m in NGAY_THANG.finditer(d):
                G("ngay-thang", i, m.group(0),
                  "Tiếng Việt viết ngày trước tháng, dạng 18/6/2026.")
        if bat("chuoi-cua"):
            for m in CHUOI_CUA.finditer(d):
                G("chuoi-cua", i, m.group(0)[:90],
                  "Chuỗi 'của' lồng nhau là văn dịch. Bỏ bớt hoặc đảo lại cụm danh từ.", muc="nhe")
        if bat("bi-dong-trung"):
            for m in BI_DONG_TRUNG_RE.finditer(d):
                G("bi-dong-trung", i, m.group(0), "Thừa động từ phụ (văn dịch Trung). Bỏ 'tiến hành/thực hiện'.", muc="nhe")
        if bat("lech-register"):
            for m in KHAU_NGU.finditer(d):
                G("lech-register", i, m.group(1), "Khẩu ngữ trong văn học thuật.", muc="nhe")
        if bat("xung-ho"):
            for m in XUNG_HO_BAN.finditer(d):
                G("xung-ho", i, m.group(0), "Không xưng hô 'bạn' trong văn học thuật. "
                  "Dùng 'chúng tôi', 'tác giả' hoặc lược chủ ngữ.")

    if bat("ngoac-kep"):
        n_ngoac = sum(len(NGOAC_THANG.findall(d)) for _, d in dv)
        if n_ngoac:
            G("ngoac-kep", 0, f"{n_ngoac} dấu \" thẳng", "Dùng “ ” thay cho \" \".", muc="nhe")

    # Câu cụt liên tiếp
    if bat("cau-cut"):
        chuoi, dong_truoc = [], None
        for dong, c in cau + [(None, "x " * 20)]:
            if dong == dong_truoc and dem_am_tiet(c) <= nguong_cut:
                chuoi.append(c)
            else:
                if len(chuoi) >= nguong_chuoi:
                    G("cau-cut", dong_truoc, " / ".join(chuoi)[:120],
                      "Nối lại bằng dấu phẩy và từ nối. Nhịp câu cụt liên tiếp là cú pháp dịch tiếng Anh.")
                chuoi = [c] if dem_am_tiet(c) <= nguong_cut else []
            dong_truoc = dong

    if bat("doi-xung"):
        dx = [(i, m.group(0)) for i, d in dv for m in DOI_XUNG.finditer(d)]
        for i, tr in dx[1:]:
            G("doi-xung", i, tr[:90], "Cấu trúc đối xứng lặp nhiều lần nghe rất máy. "
              "Giữ tối đa một lần, còn lại viết thẳng.", muc="nhe")

    toan = chuan_hoa(" ".join(d for _, d in dv))
    tong_am = sum(dem_am_tiet(c) for _, c in cau) or 1

    if bat("danh-tu-hoa"):
        n_dth = len(DANH_TU_HOA.findall(toan))
        md = n_dth / tong_am * 100
        if md > 2.0:
            G("danh-tu-hoa", 0, f"{n_dth} lần / {tong_am} âm tiết ({md:.1f}%)",
              "Chuyển 'việc/sự + động từ' về động từ trực tiếp.", muc="nhe")

    if bat("rao-don"):
        for r in RAO_DON:
            n = toan.count(r)
            if n >= 2:
                G("rao-don", 0, f"'{r}' xuất hiện {n} lần",
                  "Cụm rào đón lặp lại là dấu hiệu văn máy rõ nhất. Bỏ hẳn.",
                  muc="nhe")

    tn = [chuan_hoa(m.group(0)) for m in TU_NOI_RE.finditer(toan)]
    dem = Counter(tn)
    if bat("lap-tu-noi"):
        for t in TU_NOI_DE_LAP:
            if dem.get(t, 0) >= 5:
                G("lap-tu-noi", 0, f"'{t}' xuất hiện {dem[t]} lần",
                  "Đổi sang từ nối khác cùng chức năng để tránh đơn điệu.", muc="nhe")
    if bat("thieu-lien-ket") and tong_am >= 200 and len(tn) / tong_am * 100 < 3.0:
        G("thieu-lien-ket", 0, f"{len(tn)} từ nối / {tong_am} âm tiết ({len(tn)/tong_am*100:.1f}%)",
          "Câu đang đứng rời nhau. Tiếng Việt cần 4-5% từ nối để mạch văn liền mạch.", muc="nhe")

    # Tiêu đề viết hoa kiểu Anh
    if bat("tieu-de-hoa"):
        for i, d, l in pl:
            if l != TIEU_DE:
                continue
            td = re.sub(r"^\d+(\.\d+)*\.?\s*", "", d)
            td = re.sub(r"\([^)]*\)", "", td)
            chu = [w for w in re.findall(r"[^\W\d_]+", td, re.UNICODE) if len(w) > 2]
            if len(chu) < 4 or td.isupper():
                continue
            co_dau = [w for w in chu[1:] if re.search(
                r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]",
                w, re.I
            )]
            if len(co_dau) < 3:
                continue
            hoa = sum(1 for w in co_dau if w[0].isupper())
            if hoa >= len(co_dau) * 0.6:
                G("tieu-de-hoa", i, td.strip()[:90],
                  "Tiếng Việt chỉ viết hoa chữ đầu tiêu đề và tên riêng, không viết hoa từng chữ như tiếng Anh.")

    dai = [dem_am_tiet(c) for _, c in cau]
    tk = {
        "so_cau": len(cau), "so_am_tiet": tong_am,
        "tb_cau": sum(dai) / len(dai) if dai else 0,
        "so_dong_van": len(dv), "so_tieu_de": sum(1 for _, _, l in pl if l == TIEU_DE),
        "so_code": sum(1 for _, _, l in pl if l in (CODE, BANG, CHU_THICH))
    }
    return loi, tk


TEN = {
    "gach-ngang": "Gạch ngang chen giữa câu",
    "cham-phay": "Dấu chấm phẩy",
    "mot-cach": "'một cách' thừa (dịch -ly)",
    "bi-dong": "Bị động kiểu 'được ... bởi'",
    "ngoac-kep": "Ngoặc kép thẳng thay vì cong",
    "so-thap-phan": "Số thập phân dùng dấu chấm",
    "cau-cut": "Câu cụt liên tiếp",
    "doi-xung": "Cấu trúc đối xứng lặp",
    "danh-tu-hoa": "Danh từ hóa dày đặc",
    "rao-don": "Cụm rào đón lặp",
    "lap-tu-noi": "Lặp một từ nối",
    "thieu-lien-ket": "Thiếu từ nối liên kết",
    "tieu-de-hoa": "Tiêu đề viết hoa kiểu Anh",
    "lech-register": "Lệch văn phong (khẩu ngữ)",
    "thoi-phong": "Thổi phồng tầm quan trọng",
    "sao-ngu": "Sáo ngữ AI trừu tượng",
    "nguon-mo-ho": "Dẫn nguồn mơ hồ",
    "xung-ho": "Xưng hô 'bạn' trong văn học thuật",
    "bi-dong-trung": "Thừa động từ phụ 'tiến hành/thực hiện'",
    "ngay-thang": "Ngày tháng viết kiểu Anh",
    "chuoi-cua": "Chuỗi 'của' lồng nhau"
}


def main():
    p = argparse.ArgumentParser(
        description="Kiểm tra các dấu hiệu văn dịch máy và văn mẫu AI trong tiếng Việt học thuật.",
        epilog="Exit code 0 khi không còn lỗi nặng, 1 khi vẫn còn."
    )
    p.add_argument("duong_dan", help="Đường dẫn tới file cần kiểm tra, hoặc '-' để đọc từ stdin")
    p.add_argument("--che-do", choices=["hoc-thuat", "ky-thuat", "cong-viec", "doi-thuong"],
                   default="hoc-thuat",
                   help="Chế độ văn phong, xem references/registers.md. Mặc định: hoc-thuat")
    p.add_argument("--nguong-cau-cut", type=int, default=6,
                   help="Số âm tiết tối đa để coi là câu cụt. Mặc định: 6")
    p.add_argument("--nguong-chuoi-cut", type=int, default=3,
                   help="Số câu cụt liền nhau mới tính là lỗi. Mặc định: 3")
    a = p.parse_args()

    text = sys.stdin.read() if a.duong_dan == "-" else open(a.duong_dan, encoding="utf-8").read()
    loi, tk = quet(text, a.che_do, a.nguong_cau_cut, a.nguong_chuoi_cut)

    print(f"Chế độ: {a.che_do} | {tk['so_cau']} câu, {tk['so_am_tiet']} âm tiết, "
          f"trung bình {tk['tb_cau']:.1f} âm tiết/câu")
    print(f"Đã bỏ qua: {tk['so_tieu_de']} tiêu đề, {tk['so_code']} dòng mã/bảng/chú thích")
    print("=" * 68)
    if not loi:
        print("Không phát hiện lỗi cơ học. Phần nhịp điệu vẫn cần tự đọc lại.")
        return 0

    nhom = {}
    for l in loi:
        nhom.setdefault(l.ma, []).append(l)
    nang = sum(1 for l in loi if l.muc == "nang")
    for ma, ds in sorted(nhom.items(), key=lambda x: (x[1][0].muc != "nang", -len(x[1]))):
        print(f"\n{'[!]' if ds[0].muc == 'nang' else '[.]'} {TEN.get(ma, ma)} "
              f"[{ds[0].pattern}] — {len(ds)} chỗ")
        for l in ds[:5]:
            print(f"    {('dòng ' + str(l.dong)) if l.dong else 'toàn bài'}: {l.trich}")
        if len(ds) > 5:
            print(f"    ... còn {len(ds) - 5} chỗ nữa")
        print(f"    → {ds[0].goi_y}")
    print("\n" + "=" * 68)
    print(f"Tổng: {len(loi)} lỗi ({nang} lỗi nặng)")
    return 1 if nang else 0


if __name__ == "__main__":
    sys.exit(main())
