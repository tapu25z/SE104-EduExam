const express = require('express');
const router = express.Router();
const { query, get, run } = require('../database/db');

/**
 * UC04: Tra cứu đề thi (BM4)
 * Hỗ trợ lọc đa tiêu chí: mã đề, môn học, học kỳ, năm học, ngày thi, thời lượng, từ khóa
 */
router.get('/', async (req, res) => {
  try {
    const {
      maMon,
      hocKy,
      namHoc,
      tuKhoa,
      ngayThiTu,
      ngayThiDen,
      thoiLuongTu,
      thoiLuongDen
    } = req.query;

    let sql = `
      SELECT dt.maDe, dt.maMon, mh.tenMon, dt.hocKy, dt.namHoc, dt.ngayThi, dt.thoiLuong,
             COUNT(DISTINCT dtch.maCauHoi) AS soCauHoi,
             COUNT(DISTINCT kqt.mssv) AS soBaiCham
      FROM DeThi dt
      JOIN MonHoc mh ON dt.maMon = mh.maMon
      LEFT JOIN DeThi_CauHoi dtch ON dt.maDe = dtch.maDe
      LEFT JOIN KetQuaThi kqt ON dt.maDe = kqt.maDe
      WHERE 1=1
    `;
    const params = [];

    if (maMon) {
      sql += ' AND dt.maMon = ?';
      params.push(maMon);
    }
    if (hocKy) {
      sql += ' AND dt.hocKy = ?';
      params.push(hocKy);
    }
    if (namHoc) {
      sql += ' AND dt.namHoc = ?';
      params.push(namHoc);
    }
    if (tuKhoa) {
      sql += ' AND (dt.maDe LIKE ? OR mh.tenMon LIKE ?)';
      params.push(`%${tuKhoa}%`, `%${tuKhoa}%`);
    }
    if (ngayThiTu) {
      sql += ' AND dt.ngayThi >= ?';
      params.push(ngayThiTu);
    }
    if (ngayThiDen) {
      sql += ' AND dt.ngayThi <= ?';
      params.push(ngayThiDen);
    }
    if (thoiLuongTu) {
      sql += ' AND dt.thoiLuong >= ?';
      params.push(Number(thoiLuongTu));
    }
    if (thoiLuongDen) {
      sql += ' AND dt.thoiLuong <= ?';
      params.push(Number(thoiLuongDen));
    }

    sql += ' GROUP BY dt.maDe ORDER BY dt.namHoc DESC, dt.ngayThi DESC';

    const danhSach = await query(sql, params);
    res.json({
      success: true,
      data: danhSach.map(dt => ({
        ...dt,
        daCoKetQuaCham: dt.soBaiCham > 0
      }))
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi tra cứu đề thi: ' + err.message });
  }
});

/**
 * Lấy chi tiết 1 đề thi (gồm danh sách câu hỏi và trạng thái chấm thi)
 */
router.get('/:maDe', async (req, res) => {
  try {
    const { maDe } = req.params;

    const deThi = await get(`
      SELECT dt.*, mh.tenMon,
             COUNT(DISTINCT kqt.mssv) AS soBaiCham
      FROM DeThi dt
      JOIN MonHoc mh ON dt.maMon = mh.maMon
      LEFT JOIN KetQuaThi kqt ON dt.maDe = kqt.maDe
      WHERE dt.maDe = ?
      GROUP BY dt.maDe
    `, [maDe]);

    if (!deThi) {
      return res.status(404).json({ success: false, message: 'Không tìm thấy đề thi với mã ' + maDe });
    }

    // Lấy danh sách câu hỏi trong đề
    const cauHois = await query(`
      SELECT ch.maCauHoi, ch.maMon, ch.doKho, ch.noiDung
      FROM DeThi_CauHoi dtch
      JOIN CauHoi ch ON dtch.maCauHoi = ch.maCauHoi
      WHERE dtch.maDe = ?
      ORDER BY ch.maCauHoi
    `, [maDe]);

    // Lấy các lớp đã có kết quả chấm của đề thi này
    const cacLopDaCham = await query(`
      SELECT DISTINCT l.maLop, l.tenLop, COUNT(kqt.mssv) AS soSinhVienCham
      FROM KetQuaThi kqt
      JOIN SinhVien sv ON kqt.mssv = sv.mssv
      JOIN Lop l ON sv.maLop = l.maLop
      WHERE kqt.maDe = ?
      GROUP BY l.maLop
    `, [maDe]);

    res.json({
      success: true,
      data: {
        ...deThi,
        daCoKetQuaCham: deThi.soBaiCham > 0,
        cauHois,
        cacLopDaCham
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi lấy chi tiết đề thi: ' + err.message });
  }
});

/**
 * UC02: Soạn đề thi mới (BM2, QĐ2)
 * Kiểm tra các ràng buộc:
 * - 1 <= Số câu hỏi <= 5
 * - 30 <= Thời lượng <= 180 phút
 * - Mọi câu hỏi phải cùng môn thi với đề
 */
router.post('/', async (req, res) => {
  try {
    const { maDe, maMon, hocKy, namHoc, ngayThi, thoiLuong, danhSachCauHoi } = req.body;

    // 1. Kiểm tra thông tin bắt buộc
    if (!maDe || !maDe.trim() || !maMon || !hocKy || !namHoc || !ngayThi || thoiLuong === undefined) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng nhập đầy đủ: Mã đề, Môn thi, Học kỳ, Năm học, Ngày thi và Thời lượng!'
      });
    }

    const trimmedMaDe = maDe.trim();

    // 2. Kiểm tra mã đề đã tồn tại chưa
    const existing = await get('SELECT maDe FROM DeThi WHERE maDe = ?', [trimmedMaDe]);
    if (existing) {
      return res.status(400).json({
        success: false,
        message: `Mã đề thi '${trimmedMaDe}' đã tồn tại! Vui lòng chọn mã khác.`
      });
    }

    // Kiểm tra thời lượng thi từ 30 đến 180 phút
    const thoiLuongNum = Number(thoiLuong);
    if (isNaN(thoiLuongNum) || thoiLuongNum < 30 || thoiLuongNum > 180) {
      return res.status(400).json({
        success: false,
        ruleViolated: 'QĐ2',
        message: `Thời lượng thi phải nằm trong khoảng từ 30 đến 180 phút (hiện tại: ${thoiLuong} phút).`
      });
    }

    // Kiểm tra số câu hỏi từ 1 đến 5 câu
    if (!Array.isArray(danhSachCauHoi) || danhSachCauHoi.length < 1 || danhSachCauHoi.length > 5) {
      return res.status(400).json({
        success: false,
        ruleViolated: 'QĐ2',
        message: `Mỗi đề thi cần có từ 1 đến 5 câu hỏi (hiện đã chọn: ${danhSachCauHoi ? danhSachCauHoi.length : 0} câu).`
      });
    }

    // Kiểm tra các câu hỏi cùng môn thi với đề
    const placeholders = danhSachCauHoi.map(() => '?').join(',');
    const selectedQuestions = await query(
      `SELECT maCauHoi, maMon FROM CauHoi WHERE maCauHoi IN (${placeholders})`,
      danhSachCauHoi
    );

    if (selectedQuestions.length !== danhSachCauHoi.length) {
      return res.status(400).json({
        success: false,
        message: 'Một số câu hỏi được chọn không còn tồn tại trong ngân hàng câu hỏi.'
      });
    }

    for (const q of selectedQuestions) {
      if (q.maMon !== maMon) {
        return res.status(400).json({
          success: false,
          ruleViolated: 'QĐ2',
          message: `Câu hỏi '${q.maCauHoi}' thuộc môn '${q.maMon}', không thể gán vào đề thi môn '${maMon}'.`
        });
      }
    }

    // 6. Thực hiện lưu Đề thi và liên kết các câu hỏi
    await run(
      `INSERT INTO DeThi (maDe, maMon, hocKy, namHoc, ngayThi, thoiLuong)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [trimmedMaDe, maMon, hocKy, namHoc, ngayThi, thoiLuongNum]
    );

    for (const maCauHoi of danhSachCauHoi) {
      await run('INSERT INTO DeThi_CauHoi (maDe, maCauHoi) VALUES (?, ?)', [trimmedMaDe, maCauHoi]);
    }

    res.status(201).json({
      success: true,
      message: `Soạn và lưu đề thi '${trimmedMaDe}' thành công với ${danhSachCauHoi.length} câu hỏi!`,
      data: { maDe: trimmedMaDe }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi tạo đề thi: ' + err.message });
  }
});

/**
 * UC02: Cập nhật đề thi (BM2, QĐ2)
 * RÀNG BUỘC QĐ2: Giảng viên chỉ được sửa hoặc xóa đề khi đề CHƯA có kết quả chấm!
 */
router.put('/:maDe', async (req, res) => {
  try {
    const { maDe } = req.params;
    const { maMon, hocKy, namHoc, ngayThi, thoiLuong, danhSachCauHoi } = req.body;

    const existing = await get('SELECT * FROM DeThi WHERE maDe = ?', [maDe]);
    if (!existing) {
      return res.status(404).json({ success: false, message: 'Không tìm thấy đề thi với mã ' + maDe });
    }

    // Kiểm tra đề thi đã có kết quả chấm chưa
    const daCham = await get('SELECT COUNT(*) as count FROM KetQuaThi WHERE maDe = ?', [maDe]);
    if (daCham && daCham.count > 0) {
      return res.status(400).json({
        success: false,
        ruleViolated: 'QĐ2',
        message: `Không thể chỉnh sửa: Đề thi '${maDe}' đã có ${daCham.count} bài thi được chấm điểm. Dữ liệu đề thi được khóa để bảo vệ điểm của sinh viên.`
      });
    }

    // Kiểm tra thời lượng
    const thoiLuongNum = Number(thoiLuong);
    if (isNaN(thoiLuongNum) || thoiLuongNum < 30 || thoiLuongNum > 180) {
      return res.status(400).json({
        success: false,
        ruleViolated: 'QĐ2',
        message: `Thời lượng thi phải nằm trong khoảng từ 30 đến 180 phút (hiện tại: ${thoiLuong} phút).`
      });
    }

    // Kiểm tra số câu hỏi
    if (!Array.isArray(danhSachCauHoi) || danhSachCauHoi.length < 1 || danhSachCauHoi.length > 5) {
      return res.status(400).json({
        success: false,
        ruleViolated: 'QĐ2',
        message: `Đề thi phải có từ 1 đến 5 câu hỏi (hiện tại đã chọn: ${danhSachCauHoi ? danhSachCauHoi.length : 0} câu).`
      });
    }

    // Kiểm tra các câu hỏi cùng môn với đề
    const placeholders = danhSachCauHoi.map(() => '?').join(',');
    const selectedQuestions = await query(
      `SELECT maCauHoi, maMon FROM CauHoi WHERE maCauHoi IN (${placeholders})`,
      danhSachCauHoi
    );

    for (const q of selectedQuestions) {
      if (q.maMon !== maMon) {
        return res.status(400).json({
          success: false,
          ruleViolated: 'QĐ2',
          message: `Câu hỏi '${q.maCauHoi}' thuộc môn '${q.maMon}', không thể gán vào đề thi môn '${maMon}'.`
        });
      }
    }

    // Cập nhật thông tin đề thi
    await run(
      `UPDATE DeThi
       SET maMon = ?, hocKy = ?, namHoc = ?, ngayThi = ?, thoiLuong = ?
       WHERE maDe = ?`,
      [maMon, hocKy, namHoc, ngayThi, thoiLuongNum, maDe]
    );

    // Cập nhật danh sách câu hỏi
    await run('DELETE FROM DeThi_CauHoi WHERE maDe = ?', [maDe]);
    for (const maCauHoi of danhSachCauHoi) {
      await run('INSERT INTO DeThi_CauHoi (maDe, maCauHoi) VALUES (?, ?)', [maDe, maCauHoi]);
    }

    res.json({
      success: true,
      message: `Cập nhật đề thi '${maDe}' thành công!`
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi cập nhật đề thi: ' + err.message });
  }
});

/**
 * UC02: Xóa đề thi (BM2, QĐ2)
 * RÀNG BUỘC QĐ2: Giảng viên chỉ được sửa hoặc xóa đề khi đề CHƯA có kết quả chấm!
 */
router.delete('/:maDe', async (req, res) => {
  try {
    const { maDe } = req.params;

    const existing = await get('SELECT * FROM DeThi WHERE maDe = ?', [maDe]);
    if (!existing) {
      return res.status(404).json({ success: false, message: 'Không tìm thấy đề thi với mã ' + maDe });
    }

    // Kiểm tra đề thi đã có kết quả chấm chưa
    const daCham = await get('SELECT COUNT(*) as count FROM KetQuaThi WHERE maDe = ?', [maDe]);
    if (daCham && daCham.count > 0) {
      return res.status(400).json({
        success: false,
        ruleViolated: 'QĐ2',
        message: `Không thể xóa: Đề thi '${maDe}' đã có ${daCham.count} bài thi được chấm điểm. Dữ liệu đề thi được bảo vệ an toàn.`
      });
    }

    // Xóa liên kết câu hỏi và đề thi
    await run('DELETE FROM DeThi_CauHoi WHERE maDe = ?', [maDe]);
    await run('DELETE FROM DeThi WHERE maDe = ?', [maDe]);

    res.json({
      success: true,
      message: `Đã xóa thành công đề thi '${maDe}'!`
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi xóa đề thi: ' + err.message });
  }
});

module.exports = router;
