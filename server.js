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

// Route Trang chủ (Landing page EduExam)
app.get(['/', '/home', '/home.html'], (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'home.html'));
});

// Route Màn hình Đăng nhập riêng biệt (Dedicated Login Screen)
app.get(['/login', '/login.html'], (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// Route Cổng ứng dụng khảo thí (Management App)
app.get(['/app', '/app.html'], (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

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
const lopRouter = require('./routes/lop');
const { router: authRouter, accountsRouter, requireAuth } = require('./middleware_auth');

app.use('/api/auth', authRouter);
app.use('/api/accounts', accountsRouter);
app.use('/api', requireAuth);

app.use('/api/cau-hoi', cauHoiRouter);   // UC01: Soạn câu hỏi & QĐ1
app.use('/api/de-thi', deThiRouter);     // UC02: Soạn đề thi & QĐ2, UC04: Tra cứu đề thi (BM4)
app.use('/api/cham-thi', chamThiRouter); // UC03: Ghi nhận chấm thi (BM3) & QĐ3
app.use('/api/bao-cao', baoCaoRouter);   // UC05: Lập báo cáo năm (BM5)
app.use('/api/metadata', metadataRouter); // Danh mục Môn học, Lớp, Sinh viên, Reset CSDL
app.use('/api/lop', lopRouter); // UC07: Quản lý lớp và sinh viên theo QĐ5

// Bất kỳ route nào không phải API thì trả về trang chủ Single Page App
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Khởi chạy máy chủ
app.listen(PORT, () => {
  console.log('================================================================');
  console.log(`🚀 EduExam — Nền tảng Quản lý Khảo thí & Chấm thi Trực tuyến`);
  console.log(`🌐 Máy chủ đang hoạt động tại: http://localhost:${PORT}`);
  console.log('================================================================');
});
