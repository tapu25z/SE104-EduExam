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
      WHERE l.accountId = ?
      GROUP BY l.maLop
      ORDER BY l.maLop ASC
    `, [req.user.accountId]);
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
    const params = [req.user.accountId];
    sql += ' WHERE l.accountId = ?';
    if (maLop) {
      sql += ' AND sv.maLop = ?';
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
    const [cauHoiRow] = await query('SELECT COUNT(*) AS total FROM CauHoi WHERE accountId = ?', [req.user.accountId]);
    const [deThiRow] = await query('SELECT COUNT(*) AS total FROM DeThi WHERE accountId = ?', [req.user.accountId]);
    const [baiChamRow] = await query('SELECT COUNT(*) AS total FROM KetQuaThi k JOIN DeThi d ON d.maDe = k.maDe WHERE d.accountId = ?', [req.user.accountId]);
    const [sinhVienRow] = await query('SELECT COUNT(*) AS total FROM SinhVien s JOIN Lop l ON l.maLop = s.maLop WHERE l.accountId = ?', [req.user.accountId]);
    const [lopRow] = await query('SELECT COUNT(*) AS total FROM Lop WHERE accountId = ?', [req.user.accountId]);
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
    return res.status(410).json({ success: false, message: 'Khôi phục toàn bộ dữ liệu mẫu đã được tắt để bảo vệ dữ liệu nhiều tài khoản.' });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi khôi phục dữ liệu: ' + err.message });
  }
});

module.exports = router;
