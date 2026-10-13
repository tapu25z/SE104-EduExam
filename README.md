# EduExam - Hệ thống Quản lý Ra đề & Chấm thi Giảng viên

Đồ án môn học: **Nhập môn Công nghệ Phần mềm (SE104.R13)**  
Khoa Kỹ thuật Phần mềm, Trường Đại học Công nghệ Thông tin - ĐHQG-HCM  
Giảng viên hướng dẫn: **TS. Nguyễn Thị Thu Hương**

---

## 1. Giới thiệu

EduExam là hệ thống web hỗ trợ giảng viên trong công tác quản lý khảo thí nội bộ bộ môn, bao gồm việc quản lý ngân hàng câu hỏi, biên soạn đề thi chuẩn hóa, ghi nhận kết quả chấm thi theo lớp học và tổng hợp báo cáo khảo thí định kỳ.

Hệ thống được thiết kế theo mô hình kiến trúc 3 lớp (3-tier architecture), đáp ứng đầy đủ các yêu cầu nghiệp vụ và quy định ràng buộc được đặc tả trong Báo cáo Đồ án Stage 1 của Nhóm 30.

## 2. Thông tin nhóm thực hiện

* **Lớp sinh hoạt:** SE104.R13
* **Nhóm:** 30
* **Thành viên:**
  * Bùi Huỳnh Tây - MSSV: 24521589
  * Phạm Ngọc Phú Thịnh - MSSV: 24521703
  * Lê Quang Huy - MSSV: 24520669

## 3. Công nghệ sử dụng

* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript, Chart.js
* **Backend:** Node.js, Express.js (RESTful API)
* **Database:** SQLite3
* **Kiến trúc:** 3-Tier Architecture (Presentation, Business Logic, Data Access)

## 4. Hướng dẫn cài đặt và khởi chạy

### Yêu cầu môi trường
* Node.js (phiên bản 16.x trở lên)
* npm (đi kèm với Node.js)

### Các bước thực hiện

1. Clone repository về máy:
```bash
git clone https://github.com/tapu25z/SE104-EduExam.git
cd SE104-EduExam
```

2. Cài đặt các gói phụ thuộc:
```bash
npm install
```

3. Khởi động server:
```bash
npm start
```

4. Truy cập hệ thống trên trình duyệt:
```
http://localhost:3000
```

> **Lưu ý:** Khi khởi động lần đầu, hệ thống sẽ tự động khởi tạo cơ sở dữ liệu SQLite (`database/database.sqlite`) và nạp sẵn bộ dữ liệu mẫu phục vụ kiểm thử.

## 5. Danh mục chức năng và Ràng buộc nghiệp vụ

### 5.1. Bảng đối chiếu Use Case và Biểu mẫu

| STT | Use Case | Biểu mẫu | Quy định | Mô tả xử lý | Module phụ trách |
| :---: | :--- | :---: | :---: | :--- | :--- |
| 1 | **UC01: Soạn câu hỏi** | BM1 | QĐ1 | Quản lý ngân hàng câu hỏi theo môn học và độ khó. Bảo toàn câu hỏi đã thuộc đề thi. | `routes/cauHoi.js` |
| 2 | **UC02: Soạn đề thi** | BM2 | QĐ2 | Lập đề thi chuẩn hóa, giới hạn 1–5 câu cùng môn, thời lượng 30–180 phút. Bảo toàn đề đã có bài chấm. | `routes/deThi.js` |
| 3 | **UC03: Ghi nhận chấm thi** | BM3 | QĐ3 | Nhập điểm theo lớp, kiểm tra bước điểm 0.5, tự động quy đổi thang điểm chữ A–F. | `routes/chamThi.js` |
| 4 | **UC04: Tra cứu đề thi** | BM4 | - | Tra cứu đa tiêu chí, xem trước và in đề thi theo biểu mẫu chuẩn kết thúc học phần. | `routes/deThi.js` |
| 5 | **UC05: Lập báo cáo năm** | BM5 | - | Tổng hợp số lượng đề thi và bài chấm theo môn, tính tỷ lệ theo công thức (1.1) và (1.2). | `routes/baoCao.js` |

### 5.2. Chi tiết các quy định nghiệp vụ cốt lõi

* **Quy định 1 (QĐ1 - Bảo toàn câu hỏi):**
  * Quản lý 4 môn học: `IT001`, `IT002`, `IT003`, `SE104`.
  * 4 mức độ khó: Dễ, Trung Bình, Phức Tạp, Khó.
  * Giảng viên chỉ được phép sửa hoặc xóa câu hỏi khi câu hỏi **chưa thuộc bất kỳ đề thi nào**. Câu hỏi đã được đưa vào đề thi sẽ bị khóa nhằm đảm bảo tính toàn vẹn của đề thi.

* **Quy định 2 (QĐ2 - Cấu trúc đề thi & Bảo toàn kết quả chấm):**
  * Mỗi đề thi có từ 1 đến 5 câu hỏi.
  * Tất cả các câu hỏi trong đề phải thuộc cùng môn thi với đề.
  * Thời lượng làm bài từ 30 đến 180 phút.
  * Giảng viên chỉ được phép sửa hoặc xóa đề thi khi đề **chưa có kết quả chấm**. Khi đề đã có bài thi được ghi nhận điểm, hệ thống khóa thao tác sửa/xóa để bảo toàn kết quả thi của sinh viên.

* **Quy định 3 (QĐ3 - Thang điểm và Quy đổi điểm chữ):**
  * Điểm số nhập vào từ 0.0 đến 10.0 và phải là **bội số của 0.5**.
  * Hệ thống tự động quy đổi điểm số sang điểm chữ:
    * 9.0 – 10.0: **A**
    * 8.0 – 8.5: **B**
    * 7.0 – 7.5: **C**
    * 6.0 – 6.5: **D**
    * 5.0 – 5.5: **E**
    * < 5.0: **F**

## 6. Cấu trúc thư mục dự án

```text
SE104-EduExam/
├── database/               # Cấu hình CSDL và dữ liệu mẫu
│   ├── database.sqlite     # File CSDL SQLite cục bộ
│   ├── db.js               # Wrapper truy vấn SQLite (Promise-based)
│   ├── schema.sql          # DDL định nghĩa 7 bảng quan hệ (ERD)
│   └── seedData.js         # Script khởi tạo dữ liệu mẫu
├── public/                 # Giao diện người dùng (Client-side)
│   ├── assets/             # Hình ảnh minh họa, logo UIT, sơ đồ hệ thống
│   ├── css/                # Stylesheet và giao diện Glassmorphism
│   ├── js/                 # Logic client theo từng phân hệ
│   │   ├── app.js          # Điều hướng tab, toast, modal
│   │   ├── uc01_cauHoi.js  # Phân hệ Quản lý câu hỏi
│   │   ├── uc02_deThi.js   # Phân hệ Quản lý đề thi
│   │   ├── uc03_chamThi.js # Phân hệ Chấm thi & Sổ điểm
│   │   ├── uc04_traCuu.js  # Phân hệ Tra cứu & In đề thi
│   │   └── uc05_baoCao.js  # Phân hệ Báo cáo thống kê
│   └── index.html          # Trang chủ ứng dụng (Single Page Application)
├── routes/                 # API Controllers (Server-side)
│   ├── baoCao.js           # API báo cáo thống kê
│   ├── cauHoi.js           # API câu hỏi và kiểm tra ràng buộc QĐ1
│   ├── chamThi.js          # API chấm thi và kiểm tra ràng buộc QĐ3
│   ├── deThi.js            # API đề thi và kiểm tra ràng buộc QĐ2
│   └── metadata.js         # API danh mục môn học, lớp, sinh viên
├── Đồ án/                 # Tài liệu Báo cáo Stage 1 và file đặc tả
├── package.json            # Khai báo dependencies dự án
├── server.js               # Khởi tạo Express server
└── README.md               # Tài liệu hướng dẫn dự án
```

## 7. Bản quyền & Mục đích sử dụng

Dự án được xây dựng phục vụ mục đích học tập và báo cáo đồ án môn học Nhập môn Công nghệ Phần mềm tại Trường Đại học Công nghệ Thông tin - ĐHQG-HCM.
