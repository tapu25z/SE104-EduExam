const express = require('express');
const router = express.Router();
const { query } = require('../database/db');

/**
 * Lấy danh sách các năm học hiện có trong hệ thống
 */
router.get('/danh-sach-nam', async (req, res) => {
  try {
    const rows = await query(`
      SELECT DISTINCT namHoc 
      FROM DeThi WHERE accountId = ?
      ORDER BY namHoc DESC
    `, [req.user.accountId]);
    const danhSach = rows.map(r => r.namHoc);
    // Nếu chưa có năm nào, cung cấp các năm học mặc định
    if (danhSach.length === 0) {
      danhSach.push('2024-2025', '2023-2024');
    }
    res.json({ success: true, data: danhSach });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi lấy danh sách năm học: ' + err.message });
  }
});

/**
 * UC05: Lập báo cáo năm học (BM5)
 * Áp dụng công thức (1.1) và (1.2) trong Báo cáo Stage 1:
 * - Tỷ lệ đề thi môn = Số đề môn / Tổng số đề thi năm học * 100%
 * - Tỷ lệ bài chấm môn = Số bài chấm môn / Tổng số bài chấm năm học * 100%
 * - Nếu mẫu số = 0 thì tỷ lệ hiển thị 0%
 */
router.get('/', async (req, res) => {
  try {
    const { namHoc } = req.query;

    if (!namHoc) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng chọn năm học cần lập báo cáo thống kê!'
      });
    }

    // 1. Tính tổng số đề thi của năm học đã chọn
    const tongDeRow = await query(`
      SELECT COUNT(*) AS tongDe
      FROM DeThi
      WHERE namHoc = ? AND accountId = ?
    `, [namHoc, req.user.accountId]);
    const tongSoDeThi = tongDeRow[0].tongDe || 0;

    // 2. Tính tổng số bài chấm gắn với các đề thuộc năm học đó
    const tongBaiChamRow = await query(`
      SELECT COUNT(kqt.mssv) AS tongBaiCham
      FROM KetQuaThi kqt
      JOIN DeThi dt ON kqt.maDe = dt.maDe
      WHERE dt.namHoc = ? AND dt.accountId = ?
    `, [namHoc, req.user.accountId]);
    const tongSoBaiCham = tongBaiChamRow[0].tongBaiCham || 0;

    // 3. Thống kê chi tiết theo từng môn học (bao gồm tất cả môn học trong bảng MonHoc)
    const thongKeMon = await query(`
      SELECT 
        mh.maMon,
        mh.tenMon,
        COUNT(DISTINCT dt.maDe) AS soLuongDeThi,
        COUNT(kqt.mssv) AS soLuongBaiCham
      FROM MonHoc mh
      LEFT JOIN DeThi dt ON mh.maMon = dt.maMon AND dt.namHoc = ? AND dt.accountId = ?
      LEFT JOIN KetQuaThi kqt ON dt.maDe = kqt.maDe
      GROUP BY mh.maMon, mh.tenMon
      ORDER BY mh.maMon ASC
    `, [namHoc, req.user.accountId]);

    // 4. Áp dụng công thức (1.1) và (1.2) để tính tỉ lệ phần trăm
    const chiTietMon = thongKeMon.map((item, index) => {
      const soDe = Number(item.soLuongDeThi) || 0;
      const soBai = Number(item.soLuongBaiCham) || 0;

      // Công thức (1.1): Tỷ lệ đề thi môn = Số đề môn / Tổng số đề thi năm học * 100%
      const tiLeDeThi = tongSoDeThi > 0 ? (soDe / tongSoDeThi) * 100 : 0;

      // Công thức (1.2): Tỷ lệ bài chấm môn = Số bài chấm môn / Tổng số bài chấm năm học * 100%
      const tiLeBaiCham = tongSoBaiCham > 0 ? (soBai / tongSoBaiCham) * 100 : 0;

      return {
        stt: index + 1,
        maMon: item.maMon,
        tenMon: item.tenMon,
        soLuongDeThi: soDe,
        soLuongBaiCham: soBai,
        tiLeDeThi: Number(tiLeDeThi.toFixed(2)),
        tiLeBaiCham: Number(tiLeBaiCham.toFixed(2)),
        tiLeDeThiText: `${tiLeDeThi.toFixed(1)}%`,
        tiLeBaiChamText: `${tiLeBaiCham.toFixed(1)}%`
      };
    });

    res.json({
      success: true,
      data: {
        namHoc,
        tongSoDeThi,
        tongSoBaiCham,
        chiTiet: chiTietMon
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi lập báo cáo năm: ' + err.message });
  }
});

module.exports = router;
