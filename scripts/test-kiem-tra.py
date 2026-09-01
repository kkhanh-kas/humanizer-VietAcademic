#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test-kiem-tra.py — Test hồi quy cho scripts/kiem_tra.py.

Hai loại case:
  - "phai_bao": câu lỗi thật, linter phải bắt được mã lỗi đó.
  - "khong_duoc_bao": quy ước học thuật hợp lệ, linter không được báo oan.

    python scripts/test-kiem-tra.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kiem_tra

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


# (mô tả, văn bản, mã lỗi)
PHAI_BAO = [
    ("Bị động tác thể thật",
     "Dữ liệu được thu thập bởi hệ thống cảm biến.", "bi-dong"),
    ("Ba câu cụt liền nhau",
     "Hệ thống không cảnh báo. Không ghi nhận lỗi. Chỉ ghi log.", "cau-cut"),
    ("Xưng hô 'bạn' ngoài trích dẫn",
     "Bạn có thể thấy thuật toán chạy rất nhanh.", "xung-ho"),
    ("Khẩu ngữ ngoài trích dẫn",
     "Mô hình này chạy khá ổn đấy.", "lech-register"),
    ("Gạch ngang chen giữa câu",
     "Hệ thống xác thực — vốn theo chuẩn OAuth 2.0 — cho phép phân quyền.", "gach-ngang"),
    ("Dấu chấm phẩy",
     "Mô hình đạt độ chính xác cao; thời gian huấn luyện giảm rõ rệt.", "cham-phay"),
    ("'một cách' thừa",
     "Thuật toán xử lý một cách hiệu quả các yêu cầu đồng thời.", "mot-cach"),
    ("Số thập phân dùng dấu chấm",
     "Độ chính xác đạt 94.7% trên tập kiểm thử.", "so-thap-phan"),
    ("Thừa động từ phụ",
     "Nhóm nghiên cứu tiến hành thực hiện việc phân tích dữ liệu.", "bi-dong-trung"),
    ("Ngày tháng viết kiểu Mỹ",
     "Hệ thống được nghiệm thu vào 06/18/2026 theo biên bản.", "ngay-thang"),
    ("Tên tháng tiếng Anh",
     "Bộ dữ liệu công bố ngày June 18, 2026 trên kho lưu trữ mở.", "ngay-thang"),
    ("Chuỗi 'của' lồng nhau",
     "Hiệu năng của mô hình của hệ thống vẫn chưa ổn định.", "chuoi-cua"),
]

# (mô tả, văn bản, mã lỗi không được xuất hiện)
KHONG_DUOC_BAO = [
    ("'bởi vì' là liên từ nguyên nhân",
     "Kết quả được ghi nhận trong nhiều thử nghiệm bởi vì mô hình đã hội tụ ổn định.",
     "bi-dong"),
    ("'bởi lẽ' là liên từ nguyên nhân",
     "Mẫu dữ liệu được lọc kỹ bởi lẽ nhiễu nền rất lớn.",
     "bi-dong"),
    ("'bởi vậy' là liên từ nguyên nhân",
     "Tham số được hiệu chỉnh lại bởi vậy sai số giảm đáng kể.",
     "bi-dong"),
    ("Hai câu ngắn liền nhau là nhịp hợp lệ",
     "Mô hình đạt kết quả tốt. Chi tiết trình bày ở Chương 4.",
     "cau-cut"),
    ("'bạn' trong trích dẫn nguyên văn",
     "Người tham gia trả lời: “Bạn nên thử lại sau.”",
     "xung-ho"),
    ("Khẩu ngữ trong trích dẫn nguyên văn",
     "Một sinh viên nhận xét: “Giao diện dùng cũng ổn đấy.”",
     "lech-register"),
    ("Khoảng số hợp lệ dùng gạch nối",
     "Thời gian huấn luyện kéo dài 1–12 tháng tùy quy mô dữ liệu.",
     "gach-ngang"),
    ("Ngoặc kép cong là chuẩn",
     "Nghiên cứu áp dụng kỹ thuật “tinh chỉnh” trên mô hình nền.",
     "ngoac-kep"),
    ("Ngày viết đúng chuẩn Việt Nam",
     "Hệ thống được nghiệm thu vào ngày 18/6/2026 theo biên bản.",
     "ngay-thang"),
    ("Ngày mơ hồ thì không đoán bừa",
     "Biên bản lập ngày 6/7/2026 tại phòng thí nghiệm.",
     "ngay-thang"),
    ("Một 'của' duy nhất là bình thường",
     "Hiệu năng của mô hình vẫn chưa ổn định trên tập kiểm thử.",
     "chuoi-cua"),
]


# (chế độ, văn bản, mã lỗi phải có, mã lỗi không được có)
THEO_CHE_DO = [
    ("ky-thuat", "Bạn hãy chạy lệnh sau để khởi động dịch vụ.", None, "xung-ho"),
    ("hoc-thuat", "Bạn hãy chạy lệnh sau để khởi động dịch vụ.", "xung-ho", None),
    ("doi-thuong", "Độ chính xác đạt 94.7% trong lần chạy vừa rồi.", None, "so-thap-phan"),
    ("hoc-thuat", "Độ chính xác đạt 94.7% trong lần chạy vừa rồi.", "so-thap-phan", None),
    ("doi-thuong", "Bài viết được chỉnh sửa bởi biên tập viên.", "bi-dong", None),
]


def ma_loi(text, che_do="hoc-thuat"):
    loi, _ = kiem_tra.quet(text, che_do=che_do)
    return {l.ma for l in loi}


def main():
    that_bai = []

    for mo_ta, text, ma in PHAI_BAO:
        if ma not in ma_loi(text):
            that_bai.append(f"[phải báo] {mo_ta}: thiếu mã '{ma}' cho «{text}»")

    for mo_ta, text, ma in KHONG_DUOC_BAO:
        if ma in ma_loi(text):
            that_bai.append(f"[báo oan] {mo_ta}: dính mã '{ma}' cho «{text}»")

    # Mỗi mã lỗi của linter phải trỏ tới một pattern có thật trong catalog.
    for ma, pid in kiem_tra.MA_PATTERN.items():
        if pid not in kiem_tra.CATALOG:
            that_bai.append(f"[catalog] Mã '{ma}' trỏ tới pattern không tồn tại: '{pid}'")
    for ma in kiem_tra.TEN:
        if ma not in kiem_tra.MA_PATTERN:
            that_bai.append(f"[catalog] Mã '{ma}' chưa được gắn với pattern nào")

    for che_do, text, phai_co, khong_duoc in THEO_CHE_DO:
        co = ma_loi(text, che_do)
        if phai_co and phai_co not in co:
            that_bai.append(f"[chế độ {che_do}] thiếu mã '{phai_co}' cho «{text}»")
        if khong_duoc and khong_duoc in co:
            that_bai.append(f"[chế độ {che_do}] không được báo '{khong_duoc}' cho «{text}»")

    tong = len(PHAI_BAO) + len(KHONG_DUOC_BAO) + len(THEO_CHE_DO)
    print(f"Chạy {tong} case ({len(PHAI_BAO)} phải báo, {len(KHONG_DUOC_BAO)} không được báo, "
          f"{len(THEO_CHE_DO)} theo chế độ)")
    print("=" * 68)
    if that_bai:
        for t in that_bai:
            print(f"  ✗ {t}")
        print(f"\nThất bại: {len(that_bai)}/{tong}")
        return 1

    print(f"Tất cả {tong} case đều đạt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
