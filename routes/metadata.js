const express = require('express');
const router = express.Router();
const { query } = require('../database/db');
const { seedDatabase } = require('../database/seedData');

/**
 * Lấy danh sách Môn học (MonHoc)
 */
router.get('/mon-hoc', async (req, res) => {
  try {
    const list = await query('SELECT * FROM MonHoc ORDER BY maMon ASC');
    res.json({ success: true, data: list });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi tải danh mục môn học: ' + err.message });
  }
});

/**
 * Lấy danh sách Lớp học (Lop)
 */
router.get('/lop', async (req, res) => {
  try {
    const list = await query(`
      SELECT l.*, COUNT(sv.mssv) AS soSinhVien
      FROM Lop l
      LEFT JOIN SinhVien sv ON l.maLop = sv.maLop
      GROUP BY l.maLop
      ORDER BY l.maLop ASC
    `);
    res.json({ success: true, data: list });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi tải danh mục lớp học: ' + err.message });
  }
});

/**
 * Lấy danh sách Sinh viên (SinhVien)
 */
router.get('/sinh-vien', async (req, res) => {
  try {
    const { maLop } = req.query;
    let sql = `
      SELECT sv.*, l.tenLop
      FROM SinhVien sv
      JOIN Lop l ON sv.maLop = l.maLop
    `;
    const params = [];
    if (maLop) {
      sql += ' WHERE sv.maLop = ?';
      params.push(maLop);
    }
    sql += ' ORDER BY sv.maLop, sv.mssv ASC';

    const list = await query(sql, params);
    res.json({ success: true, data: list });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi tải danh sách sinh viên: ' + err.message });
  }
});

/**
 * Thống kê tổng quan hệ thống cho Dashboard
 */
router.get('/thong-ke-dashboard', async (req, res) => {
  try {
    const [cauHoiRow] = await query('SELECT COUNT(*) AS total FROM CauHoi');
    const [deThiRow] = await query('SELECT COUNT(*) AS total FROM DeThi');
    const [baiChamRow] = await query('SELECT COUNT(*) AS total FROM KetQuaThi');
    const [sinhVienRow] = await query('SELECT COUNT(*) AS total FROM SinhVien');
    const [lopRow] = await query('SELECT COUNT(*) AS total FROM Lop');
    const [monHocRow] = await query('SELECT COUNT(*) AS total FROM MonHoc');

    res.json({
      success: true,
      data: {
        tongCauHoi: cauHoiRow.total,
        tongDeThi: deThiRow.total,
        tongBaiCham: baiChamRow.total,
        tongSinhVien: sinhVienRow.total,
        tongLop: lopRow.total,
        tongMonHoc: monHocRow.total
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi lấy thống kê: ' + err.message });
  }
});

/**
 * Đặt lại CSDL về trạng thái dữ liệu mẫu chuẩn (Seed Data)
 * Rất tiện lợi khi sinh viên trình diễn demo trước giáo viên!
 */
router.post('/reset-data', async (req, res) => {
  try {
    await seedDatabase(true);
    res.json({
      success: true,
      message: 'Đã khôi phục toàn bộ cơ sở dữ liệu về bộ dữ liệu mẫu chuẩn của Đồ án SE104!'
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi khôi phục dữ liệu: ' + err.message });
  }
});

module.exports = router;
