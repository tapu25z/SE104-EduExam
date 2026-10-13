# HỆ THỐNG QUẢN LÝ VIỆC RA ĐỀ VÀ CHẤM THI CỦA GIẢNG VIÊN (EduExam)
### Đồ án môn học: Nhập môn Công nghệ Phần mềm (SE104.R13)
### Nhóm 30 - Trường Đại học Công nghệ Thông tin (UIT - ĐHQG-HCM)

---

## 👥 THÔNG TIN NHÓM THỰC HIỆN
* **Giảng viên hướng dẫn:** TS. Nguyễn Thị Thu Hương
* **Lớp sinh hoạt:** SE104.R13
* **Nhóm:** Nhóm 30
* **Thành viên:**
  1. **Bùi Huỳnh Tây** - MSSV: `24521589`
  2. **Phạm Ngọc Phú Thịnh** - MSSV: `24521703`
  3. **Lê Quang Huy** - MSSV: `24520669`

---

## 🚀 HƯỚNG DẪN KHỞI CHẠY (CHỈ 1 BƯỚC)

Hệ thống được thiết kế theo tiêu chí **End-to-End, đơn giản và dễ sử dụng**, sử dụng CSDL SQLite không cần cài đặt thêm MySQL hay SQL Server phức tạp.

### Bước 1: Mở terminal tại thư mục dự án và chạy:
```bash
npm start
```

### Bước 2: Mở trình duyệt web và truy cập:
👉 **[http://localhost:3000](http://localhost:3000)**

Hệ thống đã tự động tạo CSDL `database.sqlite` và nạp sẵn bộ dữ liệu mẫu đầy đủ (4 môn học, các câu hỏi theo 4 độ khó, đề thi, danh sách sinh viên nhóm 30 và bảng điểm) để sẵn sàng demo ngay lập tức!

---

## 🎨 ĐẶC ĐIỂM THIẾT KẾ GIAO DIỆN HIỆN ĐẠI (EDTECH SAAS)

1. **Thiết kế tối giản, ít chữ, nhiều hình đồ họa trực quan:**
   - Sử dụng đồ họa vector sắc nét (Hero Banner, linh vật môn học `IT001`, `IT002`, `IT003`, `SE104`, hình minh họa ngân hàng câu hỏi, đề thi và bảng điểm).
   - Sidebar trái hiện đại, điều hướng mượt mà, hỗ trợ chế độ xem **Thẻ (Card)** và **Bảng (Table)**.
   - Thang điểm chữ A, B, C, D, E, F hiển thị dạng huy hiệu màu sắc nổi bật với bóng đổ mềm.

2. **Giao diện như một ứng dụng web thực tế:**
   - Loại bỏ các mã kỹ thuật (`UC01..UC05`, `QĐ1..QĐ3`, `BM1..BM5`) khỏi mặt giao diện hằng ngày để đảm bảo tính tự nhiên, thẩm mỹ và thân thiện với người dùng.
   - Toàn bộ hồ sơ kỹ thuật phục vụ báo cáo với giảng viên được tích hợp tinh tế trong nút **"Sơ đồ & Kiến trúc"** ở sidebar. Bấm vào là mở đầy đủ bảng ma trận đối chiếu 5 Use Case, 5 Biểu mẫu, 3 Quy định và các sơ đồ UML/ERD độ phân giải cao trích từ file báo cáo.

---

## 🏛️ KIẾN TRÚC HỆ THỐNG (3 LỚP / 3-TIER ARCHITECTURE)

Khi giáo viên hỏi về kiến trúc phần mềm, nhóm trình bày:

1. **Tầng Giao diện (Presentation Layer - `public/`)**:
   - Web Single Page Application (SPA) thân thiện, responsive, chuẩn Tailwind CSS và phông chữ Plus Jakarta Sans.
   - Trực quan hóa dữ liệu bằng Chart.js (Biểu đồ tròn cơ cấu đề thi, biểu đồ cột bài chấm).
   - Thiết kế chuẩn hóa theo đúng 5 Biểu mẫu **BM1 đến BM5**. Hỗ trợ in đề thi và báo cáo chuẩn mẫu.

2. **Tầng Nghiệp vụ (Business Logic Layer - `routes/`)**:
   - Xây dựng dưới dạng RESTful API với **Node.js & Express.js**.
   - Cài đặt đầy đủ 5 Use Case (**UC01 đến UC05**).
   - Kiểm tra chặt chẽ 3 quy định cốt lõi (**QĐ1, QĐ2, QĐ3**) trước khi lưu xuống CSDL.

3. **Tầng Dữ liệu (Data Access Layer - `database/`)**:
   - Hệ quản trị CSDL quan hệ **SQLite** với 7 bảng ánh xạ chính xác 100% theo Biểu đồ thực thể liên kết (**ERD Hình 2.18**) và Biểu đồ lớp (**Hình 2.17**).

---

## 📋 ĐỐI CHIẾU 100% VỚI BÁO CÁO STAGE 1

| Use Case | Biểu mẫu | Quy định | Chức năng trong hệ thống | File mã nguồn xử lý |
| :--- | :---: | :---: | :--- | :--- |
| **UC01: Soạn câu hỏi** | **BM1** | **QĐ1** | Soạn, sửa, xóa câu hỏi theo 4 môn và 4 độ khó. **Chỉ sửa/xóa câu chưa vào đề**. | `routes/cauHoi.js` |
| **UC02: Soạn đề thi** | **BM2** | **QĐ2** | Lập đề từ 1–5 câu cùng môn, 30–180 phút. **Chỉ sửa/xóa đề chưa có kết quả chấm**. | `routes/deThi.js` |
| **UC03: Ghi nhận chấm thi** | **BM3** | **QĐ3** | Nhập điểm theo lớp, **kiểm tra điểm 0–10 bội số 0.5**, **tự động đổi điểm chữ A–F**. | `routes/chamThi.js` |
| **UC04: Tra cứu đề thi** | **BM4** | - | Tra cứu đa tiêu chí (mã đề, môn, học kỳ, năm học, ngày thi, thời lượng). Xem & in đề thi. | `routes/deThi.js` |
| **UC05: Lập báo cáo năm** | **BM5** | - | Thống kê số lượng đề, số bài chấm, **tính tỉ lệ theo công thức (1.1) và (1.2)**. | `routes/baoCao.js` |

---

## 🔍 CHI TIẾT 3 QUY ĐỊNH NGHIỆP VỤ (VỊ TRÍ CODE ĐỂ CHỈ CHO GIÁO VIÊN)

### 1. Quy định QĐ1 (Mục 1.2.1.1 trong Báo cáo)
* **Nghiệp vụ:** 
  - Hệ thống quản lý 4 môn: IT001, IT002, IT003, SE104.
  - 4 độ khó: Dễ, Trung Bình, Phức Tạp, Khó.
  - Giảng viên chỉ được sửa hoặc xóa câu hỏi khi câu hỏi **chưa thuộc đề thi**. Câu hỏi đã nằm trong đề được giữ nguyên để bảo toàn nội dung đề thi.
* **Code kiểm tra:** Xem file `routes/cauHoi.js` (dòng 170 và dòng 220):
  ```javascript
  const usedInExam = await get('SELECT maDe FROM DeThi_CauHoi WHERE maCauHoi = ? LIMIT 1', [maCauHoi]);
  if (usedInExam) {
    return res.status(400).json({
      success: false,
      ruleViolated: 'QĐ1',
      message: `Không thể chỉnh sửa: Câu hỏi '${maCauHoi}' hiện đang được sử dụng trong đề thi '${usedInExam.maDe}'...`
    });
  }
  ```

### 2. Quy định QĐ2 (Mục 1.2.1.2 trong Báo cáo)
* **Nghiệp vụ:**
  - Đề thi có từ 1 đến 5 câu.
  - Mọi câu hỏi của đề phải thuộc cùng môn thi với đề.
  - Thời lượng từ 30 đến 180 phút.
  - Giảng viên chỉ được sửa hoặc xóa đề khi đề **chưa có kết quả chấm**.
* **Code kiểm tra:** Xem file `routes/deThi.js` (dòng 168 - 208 và dòng 245 - 288):
  ```javascript
  // 1. Kiểm tra thời lượng 30 - 180 phút
  if (thoiLuong < 30 || thoiLuong > 180) throw Error('Thời lượng thi phải từ 30 đến 180 phút');
  // 2. Kiểm tra số câu hỏi 1 - 5 câu
  if (danhSachCauHoi.length < 1 || danhSachCauHoi.length > 5) throw Error('Đề thi phải có từ 1 đến 5 câu hỏi');
  // 3. Kiểm tra các câu hỏi cùng môn với đề
  if (cauHoi.maMon !== deThi.maMon) throw Error('Câu hỏi phải cùng môn với đề thi');
  // 4. Kiểm tra đề đã có kết quả chấm chưa khi sửa/xóa
  const daCham = await get('SELECT COUNT(*) as count FROM KetQuaThi WHERE maDe = ?', [maDe]);
  if (daCham.count > 0) throw Error('Đề thi đã có bài chấm, hệ thống khóa sửa/xóa');
  ```

### 3. Quy định QĐ3 (Mục 1.2.1.3 trong Báo cáo)
* **Nghiệp vụ:**
  - Điểm số nhập từ 0 đến 10 và là **bội số của 0.5**.
  - Giảng viên tự làm tròn về 0.5 gần nhất trước khi nhập; hệ thống kiểm tra tính hợp lệ, không tự làm tròn.
  - Hệ thống tự động quy đổi điểm chữ theo Bảng 1.5:
    * 9.0; 9.5; 10 -> **A**
    * 8.0; 8.5 -> **B**
    * 7.0; 7.5 -> **C**
    * 6.0; 6.5 -> **D**
    * 5.0; 5.5 -> **E**
    * < 5 -> **F**
* **Code kiểm tra:** Xem file `routes/chamThi.js` (dòng 11 - 45):
  ```javascript
  function quyDoiDiemChu(diemSo) {
    if (diemSo >= 9.0) return 'A';
    if (diemSo >= 8.0) return 'B';
    if (diemSo >= 7.0) return 'C';
    if (diemSo >= 6.0) return 'D';
    if (diemSo >= 5.0) return 'E';
    return 'F';
  }
  ```

---

## 🎯 KỊCH BẢN THUYẾT TRÌNH TRƯỚC GIÁO VIÊN (DEMO FLOW)

Khi đến lượt nhóm lên thuyết trình trước thầy/cô:

1. **Mở đầu (1 phút):**
   - Mở trang chủ (`http://localhost:3000`), giới thiệu hệ thống **EduExam** phục vụ Giảng viên ra đề và chấm thi của Nhóm 30.
   - Giới thiệu tổng quan hệ thống: Hero Banner, 4 chỉ số thống kê (Câu hỏi, Đề thi, Bài chấm, Sinh viên), 4 thẻ môn học và Widget tiến độ khảo thí.

2. **Cách mở hồ sơ kỹ thuật cho Giáo viên xem:**
   - Ở góc dưới sidebar bên trái, bấm vào nút **"Sơ đồ & Kiến trúc"**.
   - Bảng đối chiếu hiện ra với đầy đủ thông tin: đề tài, giảng viên hướng dẫn (TS. Nguyễn Thị Thu Hương), nhóm 30, bảng đối chiếu 5 Use Case, 5 Biểu mẫu BM1-BM5, 3 Quy định QĐ1-QĐ3.
   - Bấm vào các nút xem **Sơ đồ ERD (Hình 2.18)**, **Biểu đồ Lớp (Hình 2.17)**, **Biểu đồ Use Case (Hình 2.1)** để phóng to ảnh phân giải cao nếu thầy/cô yêu cầu đối chiếu.

3. **Demo Quản lý Câu hỏi (UC01 & QĐ1 - 2 phút):**
   - Bấm vào tab **Ngân hàng câu hỏi**.
   - Chuyển đổi giữa chế độ xem **Thẻ** và **Bảng**.
   - Bấm **Thêm câu hỏi**, soạn một câu hỏi mới môn `SE104`, độ khó `Trung Bình`.
   - **Điểm nhấn ràng buộc bảo toàn:** Chọn một câu hỏi có nhãn `Đang dùng` bấm nút Sửa/Xóa. Hệ thống sẽ giải thích lịch sự rằng câu hỏi đang nằm trong đề thi nên được bảo toàn.
   - Chọn câu hỏi có nhãn `Sẵn sàng sử dụng` để sửa và xóa thành công.

4. **Demo Soạn Đề thi (UC02 & QĐ2 - 2 phút):**
   - Bấm vào tab **Quản lý đề thi**.
   - Bấm **Tạo đề thi mới**:
     + Chọn môn `SE104`. Danh sách câu hỏi bên dưới tự động lọc đúng câu hỏi của môn `SE104`.
     + Tick chọn 3 câu hỏi (Huy hiệu hiển thị `Đã chọn: 3/5 câu`).
     + Nhập thời lượng `90` phút. Bấm lưu thành công.
   - **Điểm nhấn bảo vệ kết quả thi:** Chọn đề thi đã có bài chấm (biểu tượng ổ khóa), bấm nút Sửa hoặc Xóa. Hệ thống chặn lại và thông báo đề thi đã có kết quả chấm thi nên bị khóa để bảo toàn dữ liệu điểm của sinh viên.

5. **Demo Chấm điểm & Sổ điểm (UC03 & QĐ3 - 2 phút):**
   - Bấm vào tab **Chấm điểm & Sổ điểm**.
   - Chọn Môn `SE104` -> Chọn Đề thi `SE104_GK_2024` -> Chọn Lớp `SE104.R13`.
   - Bảng điểm của lớp hiện ra (thấy tên Bùi Huỳnh Tây, Phạm Ngọc Phú Thịnh, Lê Quang Huy...).
   - **Điểm nhấn thang điểm 0-10 & bước điểm 0.5:**
     + Thử nhập điểm `8.7`: Ô điểm báo lỗi ngay *"Bước điểm 0.5"*.
     + Sửa lại thành `9.0`: Ô điểm chuyển trạng thái hợp lệ, điểm chữ tự động nhảy thành **A**.
     + Nhập `8.5`: Điểm chữ tự động nhảy thành **B**.
     + Nhập `4.5`: Điểm chữ tự động nhảy thành **F**.
   - Bấm nút **Lưu kết quả chấm**.

6. **Demo Tra cứu & In đề thi (UC04 & BM2/BM4 - 1 phút):**
   - Tại Quản lý đề thi, bấm nút **Xem & in đề** tại bất kỳ đề thi nào.
   - Đề thi được trình bày trang trọng theo đúng mẫu chuẩn kết thúc học phần của Trường ĐH Công nghệ Thông tin - ĐHQG-HCM, có nút **In đề thi** trực tiếp ra file PDF hoặc máy in.

7. **Demo Báo cáo Thống kê (UC05 & BM5 - 1 phút):**
   - Bấm vào tab **Thống kê & Báo cáo**.
   - Chọn năm học `2024-2025` -> Bấm **Lập báo cáo**.
   - Bảng số liệu tổng hợp tính toán chuẩn xác tỉ lệ đề thi và tỉ lệ bài chấm theo đúng **công thức (1.1) và (1.2)** trong báo cáo.
   - Hai biểu đồ tương tác Chart.js (Biểu đồ tròn cơ cấu đề thi và Biểu đồ cột bài chấm) hiển thị sinh động, trực quan.

8. **Tính năng khôi phục dữ liệu mẫu:**
   - Bất kỳ lúc nào thầy cô yêu cầu thử nghiệm xóa, sửa dữ liệu, nhóm chỉ cần bấm nút **"Dữ liệu mẫu"** ở góc phải thanh tiêu đề. Hệ thống sẽ tự động nạp lại trạng thái ban đầu chỉ trong 1 giây!
