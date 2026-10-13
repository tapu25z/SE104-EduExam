const express = require('express');
const router = express.Router();
const { query, get, run } = require('../database/db');

// Danh sách độ khó hợp lệ theo QĐ1
const DO_KHO_HOP_LE = ['Dễ', 'Trung Bình', 'Phức Tạp', 'Khó'];

/**
 * UC01: Lấy danh sách câu hỏi (hỗ trợ lọc theo môn học, độ khó, từ khóa)
 * Kèm thông tin kiểm tra câu hỏi đã thuộc đề thi nào chưa (để phục vụ QĐ1)
 */
router.get('/', async (req, res) => {
  try {
    const { maMon, doKho, tuKhoa } = req.query;

    let sql = `
      SELECT ch.maCauHoi, ch.maMon, mh.tenMon, ch.doKho, ch.noiDung,
             COUNT(dtch.maDe) AS soLanDung,
             GROUP_CONCAT(dtch.maDe, ', ') AS danhSachMaDe
      FROM CauHoi ch
      JOIN MonHoc mh ON ch.maMon = mh.maMon
      LEFT JOIN DeThi_CauHoi dtch ON ch.maCauHoi = dtch.maCauHoi
      WHERE 1=1
    `;
    const params = [];

    if (maMon) {
      sql += ' AND ch.maMon = ?';
      params.push(maMon);
    }
    if (doKho) {
      sql += ' AND ch.doKho = ?';
      params.push(doKho);
    }
    if (tuKhoa) {
      sql += ' AND (ch.noiDung LIKE ? OR ch.maCauHoi LIKE ?)';
      params.push(`%${tuKhoa}%`, `%${tuKhoa}%`);
    }

    sql += ' GROUP BY ch.maCauHoi ORDER BY ch.maMon, ch.maCauHoi';

    const danhSach = await query(sql, params);
    res.json({
      success: true,
      data: danhSach.map(item => ({
        ...item,
        daDungTrongDe: item.soLanDung > 0
      }))
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi máy chủ: ' + err.message });
  }
});

/**
 * Lấy chi tiết 1 câu hỏi theo mã
 */
router.get('/:maCauHoi', async (req, res) => {
  try {
    const { maCauHoi } = req.params;
    const cauHoi = await get(`
      SELECT ch.*, mh.tenMon,
             COUNT(dtch.maDe) AS soLanDung,
             GROUP_CONCAT(dtch.maDe, ', ') AS danhSachMaDe
      FROM CauHoi ch
      JOIN MonHoc mh ON ch.maMon = mh.maMon
      LEFT JOIN DeThi_CauHoi dtch ON ch.maCauHoi = dtch.maCauHoi
      WHERE ch.maCauHoi = ?
      GROUP BY ch.maCauHoi
    `, [maCauHoi]);

    if (!cauHoi) {
      return res.status(404).json({ success: false, message: 'Không tìm thấy câu hỏi với mã ' + maCauHoi });
    }

    res.json({
      success: true,
      data: {
        ...cauHoi,
        daDungTrongDe: cauHoi.soLanDung > 0
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi máy chủ: ' + err.message });
  }
});

/**
 * UC01: Thêm mới câu hỏi (BM1)
 */
router.post('/', async (req, res) => {
  try {
    let { maCauHoi, maMon, doKho, noiDung } = req.body;

    if (!maMon || !doKho || !noiDung || !noiDung.trim()) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng điền đầy đủ các thông tin bắt buộc: Môn học, Độ khó và Nội dung câu hỏi!'
      });
    }

    // Kiểm tra độ khó hợp lệ
    if (!DO_KHO_HOP_LE.includes(doKho)) {
      return res.status(400).json({
        success: false,
        message: `Độ khó không hợp lệ! Phải là một trong: ${DO_KHO_HOP_LE.join(', ')}`
      });
    }

    // Kiểm tra môn học có tồn tại
    const monHoc = await get('SELECT * FROM MonHoc WHERE maMon = ?', [maMon]);
    if (!monHoc) {
      return res.status(400).json({ success: false, message: 'Môn học không tồn tại trong hệ thống!' });
    }

    // Tự động sinh mã câu hỏi nếu không cung cấp
    if (!maCauHoi || !maCauHoi.trim()) {
      const lastRow = await get(`
        SELECT maCauHoi FROM CauHoi 
        WHERE maMon = ? 
        ORDER BY maCauHoi DESC LIMIT 1
      `, [maMon]);

      let stt = 1;
      if (lastRow && lastRow.maCauHoi) {
        const parts = lastRow.maCauHoi.split('_');
        const num = parseInt(parts[parts.length - 1], 10);
        if (!isNaN(num)) stt = num + 1;
      }
      maCauHoi = `CH_${maMon}_${String(stt).padStart(2, '0')}`;
    } else {
      maCauHoi = maCauHoi.trim();
      // Kiểm tra trùng mã
      const existing = await get('SELECT maCauHoi FROM CauHoi WHERE maCauHoi = ?', [maCauHoi]);
      if (existing) {
        return res.status(400).json({ success: false, message: `Mã câu hỏi '${maCauHoi}' đã tồn tại! Vui lòng chọn mã khác.` });
      }
    }

    await run(`
      INSERT INTO CauHoi (maCauHoi, maMon, doKho, noiDung)
      VALUES (?, ?, ?, ?)
    `, [maCauHoi, maMon, doKho, noiDung.trim()]);

    res.status(201).json({
      success: true,
      message: 'Soạn và lưu câu hỏi mới thành công!',
      data: { maCauHoi, maMon, doKho, noiDung: noiDung.trim() }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi lưu câu hỏi: ' + err.message });
  }
});

/**
 * UC01: Cập nhật câu hỏi (BM1, QĐ1)
 * RÀNG BUỘC QĐ1: Giảng viên chỉ được sửa hoặc xóa câu hỏi khi câu hỏi CHƯA thuộc đề thi!
 */
router.put('/:maCauHoi', async (req, res) => {
  try {
    const { maCauHoi } = req.params;
    const { maMon, doKho, noiDung } = req.body;

    const existing = await get('SELECT * FROM CauHoi WHERE maCauHoi = ?', [maCauHoi]);
    if (!existing) {
      return res.status(404).json({ success: false, message: 'Không tìm thấy câu hỏi có mã ' + maCauHoi });
    }

    // Kiểm tra câu hỏi đã thuộc đề thi chưa (Ràng buộc bảo toàn đề thi)
    const usedInExam = await get('SELECT maDe FROM DeThi_CauHoi WHERE maCauHoi = ? LIMIT 1', [maCauHoi]);
    if (usedInExam) {
      return res.status(400).json({
        success: false,
        ruleViolated: 'QĐ1',
        message: `Không thể chỉnh sửa: Câu hỏi '${maCauHoi}' hiện đang được sử dụng trong đề thi '${usedInExam.maDe}'. Dữ liệu được bảo toàn để không ảnh hưởng đến đề thi đã lập.`
      });
    }

    if (!maMon || !doKho || !noiDung || !noiDung.trim()) {
      return res.status(400).json({ success: false, message: 'Vui lòng nhập đầy đủ Môn học, Độ khó và Nội dung!' });
    }

    if (!DO_KHO_HOP_LE.includes(doKho)) {
      return res.status(400).json({
        success: false,
        message: `Độ khó không hợp lệ! Phải là một trong: ${DO_KHO_HOP_LE.join(', ')}`
      });
    }

    await run(`
      UPDATE CauHoi
      SET maMon = ?, doKho = ?, noiDung = ?
      WHERE maCauHoi = ?
    `, [maMon, doKho, noiDung.trim(), maCauHoi]);

    res.json({
      success: true,
      message: 'Cập nhật câu hỏi thành công!',
      data: { maCauHoi, maMon, doKho, noiDung: noiDung.trim() }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi cập nhật câu hỏi: ' + err.message });
  }
});

/**
 * UC01: Xóa câu hỏi (BM1, QĐ1)
 * RÀNG BUỘC QĐ1: Giảng viên chỉ được sửa hoặc xóa câu hỏi khi câu hỏi CHƯA thuộc đề thi!
 */
router.delete('/:maCauHoi', async (req, res) => {
  try {
    const { maCauHoi } = req.params;

    const existing = await get('SELECT * FROM CauHoi WHERE maCauHoi = ?', [maCauHoi]);
    if (!existing) {
      return res.status(404).json({ success: false, message: 'Không tìm thấy câu hỏi có mã ' + maCauHoi });
    }

    // Kiểm tra câu hỏi đã thuộc đề thi chưa (Ràng buộc bảo toàn đề thi)
    const usedInExam = await get('SELECT maDe FROM DeThi_CauHoi WHERE maCauHoi = ? LIMIT 1', [maCauHoi]);
    if (usedInExam) {
      return res.status(400).json({
        success: false,
        ruleViolated: 'QĐ1',
        message: `Không thể xóa: Câu hỏi '${maCauHoi}' hiện đang nằm trong đề thi '${usedInExam.maDe}'. Dữ liệu được bảo toàn để không làm rỗng đề thi đã lập.`
      });
    }

    await run('DELETE FROM CauHoi WHERE maCauHoi = ?', [maCauHoi]);

    res.json({
      success: true,
      message: `Đã xóa thành công câu hỏi '${maCauHoi}'!`
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi xóa câu hỏi: ' + err.message });
  }
});

module.exports = router;
