const express = require('express');
const router = express.Router();
const { query, get, run } = require('../database/db');

/**
 * Hàm quy đổi điểm chữ theo Bảng 1.5 trong Báo cáo Stage 1:
 * - 9,0; 9,5; 10 -> A
 * - 8,0; 8,5     -> B
 * - 7,0; 7,5     -> C
 * - 6,0; 6,5     -> D
 * - 5,0; 5,5     -> E
 * - < 5          -> F
 */
function quyDoiDiemChu(diemSo) {
  if (diemSo >= 9.0) return 'A';
  if (diemSo >= 8.0) return 'B';
  if (diemSo >= 7.0) return 'C';
  if (diemSo >= 6.0) return 'D';
  if (diemSo >= 5.0) return 'E';
  return 'F';
}

/**
 * Kiểm tra tính hợp lệ của điểm số theo QĐ3:
 * - Nằm trong khoảng từ 0 đến 10
 * - Phải là bội số của 0,5
 * Trả về { isValid: boolean, message?: string }
 */
function kiemTraDiemQD3(diemSo) {
  if (typeof diemSo !== 'number' || isNaN(diemSo)) {
    return { isValid: false, message: 'Điểm số phải là một số hợp lệ!' };
  }
  if (diemSo < 0 || diemSo > 10) {
    return { isValid: false, message: `Điểm số ${diemSo} không hợp lệ! Điểm phải nằm trong khoảng từ 0 đến 10.` };
  }
  // Kiểm tra bội số của 0.5 (nhân 2 lên phải là số nguyên)
  const nhanHai = Math.round(diemSo * 10) / 10 * 2;
  if (Math.abs(nhanHai - Math.round(nhanHai)) > 1e-6) {
    return {
      isValid: false,
      message: `Điểm số phải là bội số của 0.5 (ví dụ: 7.0, 7.5, 8.0, 8.5...). Điểm ${diemSo} không hợp lệ, vui lòng làm tròn về 0.5 gần nhất trước khi nhập.`
    };
  }
  return { isValid: true };
}

/**
 * UC03: Lấy danh sách sinh viên của lớp và điểm số đã chấm (nếu có) theo đề thi
 */
router.get('/sinh-vien-lop', async (req, res) => {
  try {
    const { maDe, maLop } = req.query;

    if (!maLop) {
      return res.status(400).json({ success: false, message: 'Vui lòng cung cấp mã lớp (maLop)!' });
    }

    // Lấy thông tin lớp
    const lop = await get('SELECT * FROM Lop WHERE maLop = ? AND accountId = ?', [maLop, req.user.accountId]);
    if (!lop) {
      return res.status(404).json({ success: false, message: 'Lớp học không tồn tại!' });
    }

    // Lấy thông tin đề thi nếu có
    let deThi = null;
    if (maDe) {
      deThi = await get(`
        SELECT dt.*, mh.tenMon 
        FROM DeThi dt 
        JOIN MonHoc mh ON dt.maMon = mh.maMon 
        WHERE dt.maDe = ? AND dt.accountId = ?
      `, [maDe, req.user.accountId]);
    }

    // Lấy danh sách sinh viên của lớp kèm kết quả chấm thi tương ứng với đề này
    const danhSachSinhVien = await query(`
      SELECT sv.mssv, sv.hoTen, sv.maLop,
             kqt.diemSo, kqt.diemChu, kqt.ghiChu
      FROM SinhVien sv
      LEFT JOIN KetQuaThi kqt ON sv.mssv = kqt.mssv AND kqt.maDe = ?
      WHERE sv.maLop = ? AND EXISTS (SELECT 1 FROM Lop l WHERE l.maLop=sv.maLop AND l.accountId = ?)
      ORDER BY sv.mssv ASC
    `, [maDe || '', maLop, req.user.accountId]);

    res.json({
      success: true,
      data: {
        lop,
        deThi,
        sinhViens: danhSachSinhVien
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi tải danh sách sinh viên: ' + err.message });
  }
});

/**
 * UC03: Ghi nhận kết quả chấm thi (BM3, QĐ3)
 * Nhận vào:
 * - maDe
 * - maLop
 * - danhSachDiem: Array<{ mssv: string, diemSo: number | null, ghiChu: string }>
 */
router.post('/luu', async (req, res) => {
  try {
    const { maDe, maLop, danhSachDiem } = req.body;

    if (!maDe || !maLop || !Array.isArray(danhSachDiem) || danhSachDiem.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'Vui lòng chọn Mã đề thi, Lớp học và nhập điểm cho sinh viên!'
      });
    }

    const lop = await get('SELECT maLop FROM Lop WHERE maLop = ? AND accountId = ?', [maLop, req.user.accountId]);
    if (!lop) return res.status(404).json({ success: false, message: 'Lớp không thuộc tài khoản.' });

    // Kiểm tra đề thi tồn tại
    const deThi = await get('SELECT * FROM DeThi WHERE maDe = ? AND accountId = ?', [maDe, req.user.accountId]);
    if (!deThi) {
      return res.status(404).json({ success: false, message: `Đề thi '${maDe}' không tồn tại trong tài khoản.` });
    }

    // Kiểm tra dữ liệu từng sinh viên trước khi lưu
    const hopLeList = [];
    for (const item of danhSachDiem) {
      // Nếu không nhập điểm (null hoặc '') thì bỏ qua
      if (item.diemSo === null || item.diemSo === undefined || item.diemSo === '') {
        continue;
      }

      const student = await get('SELECT mssv FROM SinhVien WHERE mssv = ? AND maLop = ?', [item.mssv, maLop]);
      if (!student) return res.status(400).json({ success: false, message: `MSSV ${item.mssv} không thuộc lớp đã chọn.` });
      const diemNum = Number(item.diemSo);
      const checkResult = kiemTraDiemQD3(diemNum);
      if (!checkResult.isValid) {
        return res.status(400).json({
          success: false,
          ruleViolated: 'QĐ3',
          mssv: item.mssv,
          message: `Sinh viên MSSV [${item.mssv}]: ${checkResult.message}`
        });
      }

      const diemChu = quyDoiDiemChu(diemNum);
      hopLeList.push({
        mssv: item.mssv,
        diemSo: diemNum,
        diemChu,
        ghiChu: item.ghiChu ? item.ghiChu.trim() : ''
      });
    }

    if (hopLeList.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'Không có điểm sinh viên nào được nhập để lưu!'
      });
    }

    // Lưu vào CSDL (nếu đã có thì UPDATE, chưa có thì INSERT)
    for (const sv of hopLeList) {
      const existing = await get('SELECT * FROM KetQuaThi WHERE maDe = ? AND mssv = ?', [maDe, sv.mssv]);
      if (existing) {
        await run(`
          UPDATE KetQuaThi
          SET diemSo = ?, diemChu = ?, ghiChu = ?
          WHERE maDe = ? AND mssv = ?
        `, [sv.diemSo, sv.diemChu, sv.ghiChu, maDe, sv.mssv]);
      } else {
        await run(`
          INSERT INTO KetQuaThi (maDe, mssv, diemSo, diemChu, ghiChu)
          VALUES (?, ?, ?, ?, ?)
        `, [maDe, sv.mssv, sv.diemSo, sv.diemChu, sv.ghiChu]);
      }
    }

    res.json({
      success: true,
      message: `Đã lưu thành công kết quả chấm thi cho ${hopLeList.length} sinh viên lớp ${maLop} vào đề thi ${maDe}!`,
      soLuongLuu: hopLeList.length
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi lưu kết quả chấm thi: ' + err.message });
  }
});

/**
 * Xóa điểm của một sinh viên trong đề thi
 */
router.delete('/:maDe/:mssv', async (req, res) => {
  try {
    const { maDe, mssv } = req.params;
    const owned = await get('SELECT maDe FROM DeThi WHERE maDe = ? AND accountId = ?', [maDe, req.user.accountId]);
    if (!owned) return res.status(404).json({ success: false, message: 'Không tìm thấy đề thi trong tài khoản.' });
    await run('DELETE FROM KetQuaThi WHERE maDe = ? AND mssv = ?', [maDe, mssv]);
    res.json({ success: true, message: `Đã xóa kết quả thi của sinh viên ${mssv} trong đề ${maDe}!` });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Lỗi xóa điểm: ' + err.message });
  }
});

module.exports = {
  router,
  quyDoiDiemChu,
  kiemTraDiemQD3
};
