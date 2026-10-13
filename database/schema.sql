-- SCHEMA CƠ SỞ DỮ LIỆU ĐỒ ÁN SE104 - NHÓM 30
-- Khớp 100% với Biểu đồ thực thể liên kết (ERD - Hình 2.18) và Biểu đồ lớp phân tích (Hình 2.17)

-- 1. Bảng Môn Học (MonHoc)
CREATE TABLE IF NOT EXISTS MonHoc (
    maMon VARCHAR(20) PRIMARY KEY,
    tenMon VARCHAR(100) NOT NULL
);

-- 2. Bảng Câu Hỏi (CauHoi) - Liên kết với MonHoc (QĐ1)
CREATE TABLE IF NOT EXISTS CauHoi (
    maCauHoi VARCHAR(20) PRIMARY KEY,
    maMon VARCHAR(20) NOT NULL,
    doKho VARCHAR(20) NOT NULL CHECK (doKho IN ('Dễ', 'Trung Bình', 'Phức Tạp', 'Khó')),
    noiDung TEXT NOT NULL,
    FOREIGN KEY (maMon) REFERENCES MonHoc(maMon) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 3. Bảng Đề Thi (DeThi) - Liên kết với MonHoc (QĐ2)
CREATE TABLE IF NOT EXISTS DeThi (
    maDe VARCHAR(20) PRIMARY KEY,
    maMon VARCHAR(20) NOT NULL,
    hocKy VARCHAR(20) NOT NULL,
    namHoc VARCHAR(20) NOT NULL,
    ngayThi DATE NOT NULL,
    thoiLuong INTEGER NOT NULL CHECK (thoiLuong >= 30 AND thoiLuong <= 180),
    FOREIGN KEY (maMon) REFERENCES MonHoc(maMon) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 4. Bảng Thực thể kết hợp Đề Thi - Câu Hỏi (DeThi_CauHoi)
-- Quan hệ nhiều - nhiều giữa Đề thi và Câu hỏi (Mỗi đề có từ 1 đến 5 câu hỏi cùng môn)
CREATE TABLE IF NOT EXISTS DeThi_CauHoi (
    maDe VARCHAR(20) NOT NULL,
    maCauHoi VARCHAR(20) NOT NULL,
    PRIMARY KEY (maDe, maCauHoi),
    FOREIGN KEY (maDe) REFERENCES DeThi(maDe) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (maCauHoi) REFERENCES CauHoi(maCauHoi) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 5. Bảng Lớp (Lop)
CREATE TABLE IF NOT EXISTS Lop (
    maLop VARCHAR(20) PRIMARY KEY,
    tenLop VARCHAR(100) NOT NULL
);

-- 6. Bảng Sinh Viên (SinhVien) - Thuộc về 1 Lớp
CREATE TABLE IF NOT EXISTS SinhVien (
    mssv VARCHAR(20) PRIMARY KEY,
    maLop VARCHAR(20) NOT NULL,
    hoTen VARCHAR(100) NOT NULL,
    FOREIGN KEY (maLop) REFERENCES Lop(maLop) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 7. Bảng Kết Quả Thi (KetQuaThi) - Ghi nhận chấm thi (QĐ3)
CREATE TABLE IF NOT EXISTS KetQuaThi (
    maDe VARCHAR(20) NOT NULL,
    mssv VARCHAR(20) NOT NULL,
    diemSo REAL NOT NULL CHECK (diemSo >= 0 AND diemSo <= 10),
    diemChu VARCHAR(5) NOT NULL CHECK (diemChu IN ('A', 'B', 'C', 'D', 'E', 'F')),
    ghiChu TEXT DEFAULT '',
    PRIMARY KEY (maDe, mssv),
    FOREIGN KEY (maDe) REFERENCES DeThi(maDe) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (mssv) REFERENCES SinhVien(mssv) ON UPDATE CASCADE ON DELETE CASCADE
);
