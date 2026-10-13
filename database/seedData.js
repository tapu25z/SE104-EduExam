const fs = require('fs');
const path = require('path');
const { exec, run, query } = require('./db');

async function initDatabase() {
  const schemaPath = path.join(__dirname, 'schema.sql');
  const schemaSql = fs.readFileSync(schemaPath, 'utf8');
  await exec(schemaSql);
  console.log('✅ Khởi tạo các bảng CSDL SQLite thành công!');
}

async function seedDatabase(force = false) {
  await initDatabase();

  const countRow = await query('SELECT COUNT(*) as count FROM MonHoc');
  if (countRow[0].count > 0 && !force) {
    console.log('ℹ️ CSDL đã có dữ liệu mẫu, không cần nạp lại.');
    return;
  }

  if (force) {
    console.log('🔄 Đang xóa sạch và nạp lại dữ liệu mẫu...');
    await exec(`
      DELETE FROM KetQuaThi;
      DELETE FROM DeThi_CauHoi;
      DELETE FROM DeThi;
      DELETE FROM CauHoi;
      DELETE FROM SinhVien;
      DELETE FROM Lop;
      DELETE FROM MonHoc;
    `);
  }

  // 1. Môn học (Theo QĐ1: 4 môn học)
  const monHocs = [
    { maMon: 'IT001', tenMon: 'Nhập môn lập trình' },
    { maMon: 'IT002', tenMon: 'Lập trình hướng đối tượng' },
    { maMon: 'IT003', tenMon: 'Cấu trúc dữ liệu và giải thuật' },
    { maMon: 'SE104', tenMon: 'Nhập môn công nghệ phần mềm' }
  ];
  for (const m of monHocs) {
    await run('INSERT INTO MonHoc (maMon, tenMon) VALUES (?, ?)', [m.maMon, m.tenMon]);
  }

  // 2. Lớp học
  const lops = [
    { maLop: 'SE104.R13', tenLop: 'Nhập môn CNPM - Lớp R13' },
    { maLop: 'IT001.N11', tenLop: 'Nhập môn Lập trình - Lớp N11' },
    { maLop: 'IT002.O12', tenLop: 'OOP - Lớp O12' },
    { maLop: 'IT003.P11', tenLop: 'CTDL & GT - Lớp P11' }
  ];
  for (const l of lops) {
    await run('INSERT INTO Lop (maLop, tenLop) VALUES (?, ?)', [l.maLop, l.tenLop]);
  }

  // 3. Sinh viên (Có thành viên Nhóm 30: Bùi Huỳnh Tây, Phạm Ngọc Phú Thịnh, Lê Quang Huy)
  const sinhViens = [
    // Lớp SE104.R13
    { mssv: '24521589', maLop: 'SE104.R13', hoTen: 'Bùi Huỳnh Tây' },
    { mssv: '24521703', maLop: 'SE104.R13', hoTen: 'Phạm Ngọc Phú Thịnh' },
    { mssv: '24520669', maLop: 'SE104.R13', hoTen: 'Lê Quang Huy' },
    { mssv: '24520112', maLop: 'SE104.R13', hoTen: 'Trần Bảo An' },
    { mssv: '24520334', maLop: 'SE104.R13', hoTen: 'Nguyễn Hoàng Dũng' },
    { mssv: '24520556', maLop: 'SE104.R13', hoTen: 'Võ Thuỳ Trang' },
    { mssv: '24520778', maLop: 'SE104.R13', hoTen: 'Đỗ Minh Khang' },
    { mssv: '24520990', maLop: 'SE104.R13', hoTen: 'Vũ Thị Mai Anh' },

    // Lớp IT001.N11
    { mssv: '24521001', maLop: 'IT001.N11', hoTen: 'Nguyễn Văn An' },
    { mssv: '24521002', maLop: 'IT001.N11', hoTen: 'Lê Thị Bích' },
    { mssv: '24521003', maLop: 'IT001.N11', hoTen: 'Trần Minh Chiến' },
    { mssv: '24521004', maLop: 'IT001.N11', hoTen: 'Phạm Quỳnh Dao' },
    { mssv: '24521005', maLop: 'IT001.N11', hoTen: 'Hoàng Quốc Đạt' },

    // Lớp IT002.O12
    { mssv: '24522001', maLop: 'IT002.O12', hoTen: 'Đinh Tiến Dũng' },
    { mssv: '24522002', maLop: 'IT002.O12', hoTen: 'Mai Phương Hoa' },
    { mssv: '24522003', maLop: 'IT002.O12', hoTen: 'Phan Hữu Lộc' },
    { mssv: '24522004', maLop: 'IT002.O12', hoTen: 'Ngô Thanh Tùng' },

    // Lớp IT003.P11
    { mssv: '24523001', maLop: 'IT003.P11', hoTen: 'Vũ Hải Yến' },
    { mssv: '24523002', maLop: 'IT003.P11', hoTen: 'Bùi Công Minh' },
    { mssv: '24523003', maLop: 'IT003.P11', hoTen: 'Trịnh Lan Anh' }
  ];
  for (const sv of sinhViens) {
    await run('INSERT INTO SinhVien (mssv, maLop, hoTen) VALUES (?, ?, ?)', [sv.mssv, sv.maLop, sv.hoTen]);
  }

  // 4. Câu hỏi (Có cả câu đã dùng trong đề và câu chưa dùng để demo QĐ1)
  const cauHois = [
    // SE104
    { maCauHoi: 'CH_SE104_01', maMon: 'SE104', doKho: 'Dễ', noiDung: 'Trình bày khái niệm vòng đời phát triển phần mềm (SDLC) và nêu các giai đoạn cơ bản.' },
    { maCauHoi: 'CH_SE104_02', maMon: 'SE104', doKho: 'Trung Bình', noiDung: 'Phân biệt sự khác nhau giữa biểu đồ Use Case và biểu đồ hoạt động (Activity Diagram).' },
    { maCauHoi: 'CH_SE104_03', maMon: 'SE104', doKho: 'Phức Tạp', noiDung: 'Vẽ biểu đồ lớp phân tích cho bài toán Quản lý bán hàng có áp dụng mẫu thiết kế Factory Pattern.' },
    { maCauHoi: 'CH_SE104_04', maMon: 'SE104', doKho: 'Khó', noiDung: 'Thiết kế kiến trúc vi dịch vụ (Microservices) chịu tải cao và giải thích cơ chế giải quyết xung đột dữ liệu.' },
    { maCauHoi: 'CH_SE104_05', maMon: 'SE104', doKho: 'Dễ', noiDung: 'Nêu các nguyên tắc cơ bản trong kiểm thử phần mềm Black-box và White-box. (Câu hỏi chưa đưa vào đề)' },
    { maCauHoi: 'CH_SE104_06', maMon: 'SE104', doKho: 'Trung Bình', noiDung: 'Giải thích quy tắc SOLID trong thiết kế phần mềm hướng đối tượng kèm ví dụ minh họa. (Câu hỏi chưa đưa vào đề)' },

    // IT001
    { maCauHoi: 'CH_IT001_01', maMon: 'IT001', doKho: 'Dễ', noiDung: 'Viết chương trình C++ tính tổng các số chẵn từ 1 đến N nhập từ bàn phím.' },
    { maCauHoi: 'CH_IT001_02', maMon: 'IT001', doKho: 'Trung Bình', noiDung: 'Viết hàm đệ quy tìm ước số chung lớn nhất (UCLN) của hai số nguyên dương a và b.' },
    { maCauHoi: 'CH_IT001_03', maMon: 'IT001', doKho: 'Phức Tạp', noiDung: 'Nhập mảng số nguyên một chiều. Hãy đếm số lượng phần tử là số nguyên tố.' },
    { maCauHoi: 'CH_IT001_04', maMon: 'IT001', doKho: 'Khó', noiDung: 'Thao tác với mảng 2 chiều: tìm đường đi có tổng lớn nhất từ góc trên-trái xuống góc dưới-phải.' },
    { maCauHoi: 'CH_IT001_05', maMon: 'IT001', doKho: 'Dễ', noiDung: 'Giải thích cú pháp và cách sử dụng con trỏ cơ bản trong C/C++. (Chưa đưa vào đề)' },

    // IT002
    { maCauHoi: 'CH_IT002_01', maMon: 'IT002', doKho: 'Dễ', noiDung: 'Nêu 4 tính chất cơ bản của lập trình hướng đối tượng (Đóng gói, Kế thừa, Đa hình, Trừu tượng).' },
    { maCauHoi: 'CH_IT002_02', maMon: 'IT002', doKho: 'Trung Bình', noiDung: 'Viết lớp PhanSo với các phương thức nạp chồng toán tử cộng, trừ, nhân, chia (+, -, *, /).' },
    { maCauHoi: 'CH_IT002_03', maMon: 'IT002', doKho: 'Khó', noiDung: 'Thiết kế hệ thống lớp kế thừa NhanVien, NhanVienSanXuat, NhanVienVanPhong sử dụng phương thức thuần ảo.' },
    { maCauHoi: 'CH_IT002_04', maMon: 'IT002', doKho: 'Phức Tạp', noiDung: 'Trình bày cách sử dụng Smart Pointers (unique_ptr, shared_ptr) trong C++. (Chưa đưa vào đề)' },

    // IT003
    { maCauHoi: 'CH_IT003_01', maMon: 'IT003', doKho: 'Dễ', noiDung: 'Trình bày giải thuật tìm kiếm nhị phân (Binary Search) và đánh giá độ phức tạp thời gian O(log n).' },
    { maCauHoi: 'CH_IT003_02', maMon: 'IT003', doKho: 'Trung Bình', noiDung: 'Cài đặt thao tác thêm và xóa một nút trên Cây nhị phân tìm kiếm (Binary Search Tree).' },
    { maCauHoi: 'CH_IT003_03', maMon: 'IT003', doKho: 'Khó', noiDung: 'Cài đặt thuật toán Dijkstra tìm đường đi ngắn nhất trên đồ thị có trọng số không âm.' },
    { maCauHoi: 'CH_IT003_04', maMon: 'IT003', doKho: 'Phức Tạp', noiDung: 'So sánh giải thuật Quick Sort và Merge Sort về độ phức tạp bộ nhớ và độ ổn định. (Chưa đưa vào đề)' }
  ];
  for (const ch of cauHois) {
    await run('INSERT INTO CauHoi (maCauHoi, maMon, doKho, noiDung) VALUES (?, ?, ?, ?)', [
      ch.maCauHoi, ch.maMon, ch.doKho, ch.noiDung
    ]);
  }

  // 5. Đề thi (Theo QĐ2: 1-5 câu, 30-180 phút, cùng môn)
  const deThis = [
    { maDe: 'SE104_K1_2425', maMon: 'SE104', hocKy: 'Học kỳ 1', namHoc: '2024-2025', ngayThi: '2024-12-15', thoiLuong: 90 },
    { maDe: 'SE104_K2_2425', maMon: 'SE104', hocKy: 'Học kỳ 2', namHoc: '2024-2025', ngayThi: '2025-05-20', thoiLuong: 60 },
    { maDe: 'IT001_K1_2425', maMon: 'IT001', hocKy: 'Học kỳ 1', namHoc: '2024-2025', ngayThi: '2024-12-18', thoiLuong: 90 },
    { maDe: 'IT002_K1_2425', maMon: 'IT002', hocKy: 'Học kỳ 1', namHoc: '2024-2025', ngayThi: '2024-12-20', thoiLuong: 75 },
    { maDe: 'IT003_K1_2425', maMon: 'IT003', hocKy: 'Học kỳ 1', namHoc: '2024-2025', ngayThi: '2024-12-22', thoiLuong: 90 },
    { maDe: 'SE104_K1_2324', maMon: 'SE104', hocKy: 'Học kỳ 1', namHoc: '2023-2024', ngayThi: '2023-12-14', thoiLuong: 90 },
    { maDe: 'IT001_K1_2324', maMon: 'IT001', hocKy: 'Học kỳ 1', namHoc: '2023-2024', ngayThi: '2023-12-16', thoiLuong: 60 }
  ];
  for (const dt of deThis) {
    await run('INSERT INTO DeThi (maDe, maMon, hocKy, namHoc, ngayThi, thoiLuong) VALUES (?, ?, ?, ?, ?, ?)', [
      dt.maDe, dt.maMon, dt.hocKy, dt.namHoc, dt.ngayThi, dt.thoiLuong
    ]);
  }

  // 6. Chi tiết Đề thi - Câu hỏi (DeThi_CauHoi)
  const deThiCauHois = [
    // SE104_K1_2425 (3 câu)
    { maDe: 'SE104_K1_2425', maCauHoi: 'CH_SE104_01' },
    { maDe: 'SE104_K1_2425', maCauHoi: 'CH_SE104_02' },
    { maDe: 'SE104_K1_2425', maCauHoi: 'CH_SE104_03' },

    // SE104_K2_2425 (2 câu - chưa có điểm chấm để demo sửa/xóa QĐ2)
    { maDe: 'SE104_K2_2425', maCauHoi: 'CH_SE104_01' },
    { maDe: 'SE104_K2_2425', maCauHoi: 'CH_SE104_04' },

    // IT001_K1_2425 (3 câu)
    { maDe: 'IT001_K1_2425', maCauHoi: 'CH_IT001_01' },
    { maDe: 'IT001_K1_2425', maCauHoi: 'CH_IT001_02' },
    { maDe: 'IT001_K1_2425', maCauHoi: 'CH_IT001_03' },

    // IT002_K1_2425 (3 câu)
    { maDe: 'IT002_K1_2425', maCauHoi: 'CH_IT002_01' },
    { maDe: 'IT002_K1_2425', maCauHoi: 'CH_IT002_02' },
    { maDe: 'IT002_K1_2425', maCauHoi: 'CH_IT002_03' },

    // IT003_K1_2425 (3 câu)
    { maDe: 'IT003_K1_2425', maCauHoi: 'CH_IT003_01' },
    { maDe: 'IT003_K1_2425', maCauHoi: 'CH_IT003_02' },
    { maDe: 'IT003_K1_2425', maCauHoi: 'CH_IT003_03' },

    // SE104_K1_2324 (2 câu)
    { maDe: 'SE104_K1_2324', maCauHoi: 'CH_SE104_01' },
    { maDe: 'SE104_K1_2324', maCauHoi: 'CH_SE104_02' },

    // IT001_K1_2324 (2 câu)
    { maDe: 'IT001_K1_2324', maCauHoi: 'CH_IT001_01' },
    { maDe: 'IT001_K1_2324', maCauHoi: 'CH_IT001_02' }
  ];
  for (const link of deThiCauHois) {
    await run('INSERT INTO DeThi_CauHoi (maDe, maCauHoi) VALUES (?, ?)', [link.maDe, link.maCauHoi]);
  }

  // 7. Kết quả thi (KetQuaThi) - QĐ3: Điểm từ 0-10, bội số 0.5, quy đổi A..F
  // Chấm cho đề SE104_K1_2425 - Lớp SE104.R13
  const ketQuas = [
    { maDe: 'SE104_K1_2425', mssv: '24521589', diemSo: 9.5, diemChu: 'A', ghiChu: 'Làm bài xuất sắc, biểu đồ rõ ràng' },
    { maDe: 'SE104_K1_2425', mssv: '24521703', diemSo: 9.0, diemChu: 'A', ghiChu: 'Trả lời đúng trọng tâm' },
    { maDe: 'SE104_K1_2425', mssv: '24520669', diemSo: 8.5, diemChu: 'B', ghiChu: 'Bài làm tốt, trình bày đẹp' },
    { maDe: 'SE104_K1_2425', mssv: '24520112', diemSo: 7.5, diemChu: 'C', ghiChu: 'Đạt yêu cầu' },
    { maDe: 'SE104_K1_2425', mssv: '24520334', diemSo: 6.5, diemChu: 'D', ghiChu: 'Cần bổ sung phần phân tích' },
    { maDe: 'SE104_K1_2425', mssv: '24520556', diemSo: 5.5, diemChu: 'E', ghiChu: 'Thiếu một số sơ đồ Use Case' },
    { maDe: 'SE104_K1_2425', mssv: '24520778', diemSo: 4.5, diemChu: 'F', ghiChu: 'Chưa đạt yêu cầu tối thiểu' },
    { maDe: 'SE104_K1_2425', mssv: '24520990', diemSo: 8.0, diemChu: 'B', ghiChu: 'Khá tốt' },

    // Chấm cho đề IT001_K1_2425 - Lớp IT001.N11
    { maDe: 'IT001_K1_2425', mssv: '24521001', diemSo: 9.0, diemChu: 'A', ghiChu: 'Code sạch, chạy đúng test case' },
    { maDe: 'IT001_K1_2425', mssv: '24521002', diemSo: 8.0, diemChu: 'B', ghiChu: 'Tốt' },
    { maDe: 'IT001_K1_2425', mssv: '24521003', diemSo: 7.0, diemChu: 'C', ghiChu: 'Khá' },

    // Chấm cho đề IT002_K1_2425 - Lớp IT002.O12
    { maDe: 'IT002_K1_2425', mssv: '24522001', diemSo: 9.5, diemChu: 'A', ghiChu: 'Thiết kế class hướng đối tượng rất chuẩn' },
    { maDe: 'IT002_K1_2425', mssv: '24522002', diemSo: 8.5, diemChu: 'B', ghiChu: 'Bài làm tốt' },

    // Chấm cho đề IT003_K1_2425 - Lớp IT003.P11
    { maDe: 'IT003_K1_2425', mssv: '24523001', diemSo: 8.0, diemChu: 'B', ghiChu: 'Giải thuật tối ưu' },
    { maDe: 'IT003_K1_2425', mssv: '24523002', diemSo: 6.0, diemChu: 'D', ghiChu: 'Cần chú ý trường hợp biên' },

    // Chấm cho năm 2023-2024
    { maDe: 'SE104_K1_2324', mssv: '24521589', diemSo: 9.0, diemChu: 'A', ghiChu: 'Năm học cũ 2023-2024' },
    { maDe: 'IT001_K1_2324', mssv: '24521001', diemSo: 8.5, diemChu: 'B', ghiChu: 'Năm học cũ 2023-2024' }
  ];
  for (const kq of ketQuas) {
    await run('INSERT INTO KetQuaThi (maDe, mssv, diemSo, diemChu, ghiChu) VALUES (?, ?, ?, ?, ?)', [
      kq.maDe, kq.mssv, kq.diemSo, kq.diemChu, kq.ghiChu
    ]);
  }

  console.log('✅ Đã nạp thành công bộ dữ liệu mẫu chuẩn theo Báo cáo Stage 1!');
}

module.exports = {
  initDatabase,
  seedDatabase
};
