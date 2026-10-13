const express = require('express');
const cors = require('cors');
const path = require('path');
const { initDatabase, seedDatabase } = require('./database/seedData');

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Phục vụ tệp tĩnh giao diện người dùng (Frontend)
app.use(express.static(path.join(__dirname, 'public')));

// Khởi tạo và nạp dữ liệu mẫu khi khởi động server
(async () => {
  try {
    await seedDatabase(false);
    console.log('📦 Cơ sở dữ liệu SQLite đã sẵn sàng hoạt động.');
  } catch (err) {
    console.error('❌ Lỗi khởi tạo cơ sở dữ liệu:', err);
  }
})();

// Đăng ký các Route API tương ứng với các Use Case trong Báo cáo Stage 1
const cauHoiRouter = require('./routes/cauHoi');
const deThiRouter = require('./routes/deThi');
const { router: chamThiRouter } = require('./routes/chamThi');
const baoCaoRouter = require('./routes/baoCao');
const metadataRouter = require('./routes/metadata');

app.use('/api/cau-hoi', cauHoiRouter);   // UC01: Soạn câu hỏi & QĐ1
app.use('/api/de-thi', deThiRouter);     // UC02: Soạn đề thi & QĐ2, UC04: Tra cứu đề thi (BM4)
app.use('/api/cham-thi', chamThiRouter); // UC03: Ghi nhận chấm thi (BM3) & QĐ3
app.use('/api/bao-cao', baoCaoRouter);   // UC05: Lập báo cáo năm (BM5)
app.use('/api/metadata', metadataRouter); // Danh mục Môn học, Lớp, Sinh viên, Reset CSDL

// Bất kỳ route nào không phải API thì trả về trang chủ Single Page App
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Khởi chạy máy chủ
app.listen(PORT, () => {
  console.log('================================================================');
  console.log(`🚀 HỆ THỐNG QUẢN LÝ VIỆC RA ĐỀ VÀ CHẤM THI CỦA GIẢNG VIÊN`);
  console.log(`🎓 Đồ án môn học: Nhập môn Công nghệ Phần mềm (SE104.R13) - Nhóm 30`);
  console.log(`🌐 Máy chủ đang chạy tại: http://localhost:${PORT}`);
  console.log('================================================================');
});
