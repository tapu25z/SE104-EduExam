const express = require('express');
const { query, get, run } = require('../database/db');
const router = express.Router();

router.get('/', async (req, res) => {
  const rows = await query(`SELECT l.*, COUNT(sv.mssv) AS soSinhVien FROM Lop l
    LEFT JOIN SinhVien sv ON sv.maLop = l.maLop WHERE l.accountId = ?
    GROUP BY l.maLop ORDER BY l.maLop`, [req.user.accountId]);
  res.json({ success: true, data: rows });
});
router.post('/', async (req, res) => {
  const { maLop, tenLop, sinhViens = [] } = req.body || {};
  if (!maLop?.trim() || !tenLop?.trim() || !Array.isArray(sinhViens)) return res.status(400).json({ success: false, message: 'Mã lớp, tên lớp và danh sách sinh viên hợp lệ là bắt buộc.' });
  const normalizedStudents = sinhViens.map(sv => ({mssv:sv.mssv?.trim(),hoTen:sv.hoTen?.trim()}));
  if (normalizedStudents.some(sv => !sv.mssv || !sv.hoTen) || new Set(normalizedStudents.map(sv=>sv.mssv)).size !== normalizedStudents.length) return res.status(400).json({ success: false, message: 'Mỗi sinh viên cần MSSV và họ tên; không được trùng MSSV.' });
  let classCreated = false;
  try {
    await run('INSERT INTO Lop (maLop, tenLop, accountId) VALUES (?, ?, ?)', [maLop.trim(), tenLop.trim(), req.user.accountId]);
    classCreated = true;
    for (const sv of normalizedStudents) await run('INSERT INTO SinhVien (mssv, maLop, hoTen) VALUES (?, ?, ?)', [sv.mssv, maLop.trim(), sv.hoTen]);
    res.status(201).json({ success: true, message: 'Đã tạo lớp học.' });
  } catch (err) {
    if (classCreated) {
      await run('DELETE FROM SinhVien WHERE maLop = ?', [maLop.trim()]).catch(() => {});
      await run('DELETE FROM Lop WHERE maLop = ? AND accountId = ?', [maLop.trim(), req.user.accountId]).catch(() => {});
    }
    res.status(400).json({ success: false, message: err.message.includes('UNIQUE') ? 'Mã lớp hoặc MSSV đã tồn tại.' : 'Không thể lưu lớp học.' });
  }
});
router.put('/:maLop', async (req, res) => {
  const current = await get('SELECT * FROM Lop WHERE maLop = ? AND accountId = ?', [req.params.maLop, req.user.accountId]);
  if (!current) return res.status(404).json({ success: false, message: 'Không tìm thấy lớp thuộc tài khoản.' });
  const { tenLop } = req.body || {};
  if (!tenLop?.trim()) return res.status(400).json({ success: false, message: 'Tên lớp không được để trống.' });
  await run('UPDATE Lop SET tenLop = ? WHERE maLop = ? AND accountId = ?', [tenLop.trim(), current.maLop, req.user.accountId]);
  res.json({ success: true, message: 'Đã cập nhật lớp học.' });
});
router.delete('/:maLop', async (req, res) => {
  const current = await get('SELECT * FROM Lop WHERE maLop = ? AND accountId = ?', [req.params.maLop, req.user.accountId]);
  if (!current) return res.status(404).json({ success: false, message: 'Không tìm thấy lớp thuộc tài khoản.' });
  const graded = await get('SELECT COUNT(*) AS n FROM KetQuaThi k JOIN SinhVien s ON s.mssv = k.mssv WHERE s.maLop = ?', [current.maLop]);
  if (graded.n) return res.status(400).json({ success: false, ruleViolated: 'QĐ5', message: 'Không thể xóa lớp đã có kết quả chấm thi.' });
  await run('DELETE FROM SinhVien WHERE maLop = ?', [current.maLop]);
  await run('DELETE FROM Lop WHERE maLop = ? AND accountId = ?', [current.maLop, req.user.accountId]);
  res.json({ success: true, message: 'Đã xóa lớp học.' });
});
router.get('/:maLop/sinh-vien', async (req, res) => {
  const lop = await get('SELECT * FROM Lop WHERE maLop = ? AND accountId = ?', [req.params.maLop, req.user.accountId]);
  if (!lop) return res.status(404).json({ success: false, message: 'Không tìm thấy lớp.' });
  const sinhViens = await query('SELECT * FROM SinhVien WHERE maLop = ? ORDER BY mssv', [lop.maLop]);
  res.json({ success: true, data: { lop, sinhViens } });
});
router.post('/:maLop/sinh-vien', async (req, res) => {
  const lop = await get('SELECT * FROM Lop WHERE maLop = ? AND accountId = ?', [req.params.maLop, req.user.accountId]);
  if (!lop) return res.status(404).json({ success: false, message: 'Không tìm thấy lớp.' });
  const { mssv, hoTen } = req.body || {};
  if (!mssv?.trim() || !hoTen?.trim()) return res.status(400).json({ success: false, message: 'MSSV và họ tên là bắt buộc.' });
  try { await run('INSERT INTO SinhVien (mssv, maLop, hoTen) VALUES (?, ?, ?)', [mssv.trim(), lop.maLop, hoTen.trim()]); res.status(201).json({ success: true, message: 'Đã thêm sinh viên.' }); }
  catch (_err) { res.status(400).json({ success: false, message: 'MSSV đã tồn tại.' }); }
});
router.delete('/:maLop/sinh-vien/:mssv', async (req, res) => {
  const student = await get(`SELECT s.mssv FROM SinhVien s JOIN Lop l ON l.maLop=s.maLop
    WHERE s.mssv=? AND l.maLop=? AND l.accountId=?`, [req.params.mssv, req.params.maLop, req.user.accountId]);
  if (!student) return res.status(404).json({ success: false, message: 'Không tìm thấy sinh viên trong lớp.' });
  const graded = await get('SELECT COUNT(*) AS n FROM KetQuaThi WHERE mssv = ?', [student.mssv]);
  if (graded.n) return res.status(400).json({ success: false, ruleViolated: 'QĐ5', message: 'Không thể xóa sinh viên đã có kết quả chấm thi.' });
  await run('DELETE FROM SinhVien WHERE mssv = ?', [student.mssv]);
  res.json({ success: true, message: 'Đã xóa sinh viên khỏi lớp.' });
});
module.exports = router;
