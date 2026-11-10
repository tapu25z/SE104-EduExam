const crypto = require('crypto');
const { get, run } = require('./database/db');
const sessions = new Map();

function hashPassword(password, salt = crypto.randomBytes(16).toString('hex')) {
  const digest = crypto.scryptSync(String(password), salt, 64).toString('hex');
  return { salt, digest, encoded: `${salt}:${digest}` };
}
function verifyPassword(password, encoded) {
  if (!encoded || !encoded.includes(':')) return false;
  const [salt, expectedHex] = encoded.split(':');
  const actual = crypto.scryptSync(String(password), salt, 64);
  const expected = Buffer.from(expectedHex, 'hex');
  return actual.length === expected.length && crypto.timingSafeEqual(actual, expected);
}
function requireAuth(req, res, next) {
  const token = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  const session = sessions.get(token);
  if (!session || session.expiresAt < Date.now()) {
    if (token) sessions.delete(token);
    return res.status(401).json({ success: false, message: 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.' });
  }
  req.user = session.user;
  next();
}
function requireAdmin(req, res, next) {
  if (req.user?.vaiTro !== 'admin') return res.status(403).json({ success: false, message: 'Chức năng này chỉ dành cho quản trị viên.' });
  next();
}
async function login(req, res) {
  const { tenDangNhap, matKhau } = req.body || {};
  if (!tenDangNhap || !matKhau) return res.status(400).json({ success: false, message: 'Nhập tên đăng nhập và mật khẩu.' });
  const account = await get('SELECT * FROM TaiKhoan WHERE tenDangNhap = ?', [tenDangNhap.trim()]);
  if (!account || account.trangThai !== 'active' || !verifyPassword(matKhau, account.matKhauHash)) {
    return res.status(401).json({ success: false, message: 'Tên đăng nhập hoặc mật khẩu không đúng, hoặc tài khoản đã bị khóa.' });
  }
  const token = crypto.randomBytes(32).toString('hex');
  const cleanHoTen = (account.hoTen || '').replace(/\s*demo\s*/gi, '').trim() || (account.vaiTro === 'admin' ? 'Quản trị viên' : 'Giảng viên');
  const user = { accountId: account.accountId, tenDangNhap: account.tenDangNhap, hoTen: cleanHoTen, vaiTro: account.vaiTro };
  sessions.set(token, { user, expiresAt: Date.now() + 8 * 60 * 60 * 1000 });
  res.json({ success: true, token, user });
}
async function register(req, res) {
  const { tenDangNhap, matKhau, hoTen } = req.body || {};
  if (!tenDangNhap?.trim() || !matKhau || matKhau.length < 6 || !hoTen?.trim()) {
    return res.status(400).json({ success: false, message: 'Vui lòng điền đầy đủ họ tên, tên đăng nhập và mật khẩu (tối thiểu 6 ký tự).' });
  }
  const cleanUsername = tenDangNhap.trim();
  const existing = await get('SELECT accountId FROM TaiKhoan WHERE tenDangNhap = ?', [cleanUsername]);
  if (existing) {
    return res.status(400).json({ success: false, message: 'Tên đăng nhập đã tồn tại. Vui lòng chọn tên đăng nhập khác.' });
  }
  const { encoded } = hashPassword(matKhau);
  const result = await run('INSERT INTO TaiKhoan (tenDangNhap, matKhauHash, hoTen, vaiTro, trangThai) VALUES (?, ?, ?, ?, ?)', [
    cleanUsername, encoded, hoTen.trim(), 'giangvien', 'active'
  ]);
  const token = crypto.randomBytes(32).toString('hex');
  const user = { accountId: result.lastID, tenDangNhap: cleanUsername, hoTen: hoTen.trim(), vaiTro: 'giangvien' };
  sessions.set(token, { user, expiresAt: Date.now() + 8 * 60 * 60 * 1000 });
  res.status(201).json({ success: true, message: 'Đăng ký tài khoản thành công.', token, user });
}

const router = require('express').Router();
router.post('/login', (req, res, next) => login(req, res).catch(next));
router.post('/register', (req, res, next) => register(req, res).catch(next));
router.get('/me', requireAuth, (req, res) => res.json({ success: true, data: req.user }));
router.post('/logout', requireAuth, (req, res) => {
  sessions.delete((req.headers.authorization || '').replace(/^Bearer\s+/i, ''));
  res.json({ success: true });
});

const accountsRouter = require('express').Router();
accountsRouter.use(requireAuth, requireAdmin);
accountsRouter.get('/', async (_req, res) => {
  const data = await require('./database/db').query('SELECT accountId, tenDangNhap, hoTen, vaiTro, trangThai, ngayTao FROM TaiKhoan ORDER BY accountId');
  res.json({ success: true, data });
});
accountsRouter.post('/', async (req, res) => {
  const { tenDangNhap, matKhau, hoTen } = req.body || {};
  if (!tenDangNhap?.trim() || !matKhau || matKhau.length < 8 || !hoTen?.trim()) return res.status(400).json({ success: false, message: 'Tên đăng nhập, họ tên và mật khẩu tối thiểu 8 ký tự là bắt buộc.' });
  try {
    const { encoded } = hashPassword(matKhau);
    const result = await run('INSERT INTO TaiKhoan (tenDangNhap, matKhauHash, hoTen, vaiTro) VALUES (?, ?, ?, ?)', [tenDangNhap.trim(), encoded, hoTen.trim(), 'giangvien']);
    res.status(201).json({ success: true, message: 'Đã tạo tài khoản giảng viên.', accountId: result.lastID });
  } catch (err) { res.status(400).json({ success: false, message: err.message.includes('UNIQUE') ? 'Tên đăng nhập đã được sử dụng.' : 'Không thể tạo tài khoản.' }); }
});
accountsRouter.put('/:id', async (req, res) => {
  const account = await get('SELECT * FROM TaiKhoan WHERE accountId = ?', [req.params.id]);
  if (!account || account.vaiTro !== 'giangvien') return res.status(404).json({ success: false, message: 'Không tìm thấy tài khoản giảng viên.' });
  const { hoTen, trangThai, matKhauMoi } = req.body || {};
  if (!['active', 'disabled'].includes(trangThai)) return res.status(400).json({ success: false, message: 'Trạng thái không hợp lệ.' });
  if (matKhauMoi && matKhauMoi.length < 8) return res.status(400).json({ success: false, message: 'Mật khẩu mới cần ít nhất 8 ký tự.' });
  if (matKhauMoi) {
    const { encoded } = hashPassword(matKhauMoi);
    await run('UPDATE TaiKhoan SET hoTen = ?, trangThai = ?, matKhauHash = ? WHERE accountId = ?', [hoTen?.trim() || account.hoTen, trangThai, encoded, account.accountId]);
  } else await run('UPDATE TaiKhoan SET hoTen = ?, trangThai = ? WHERE accountId = ?', [hoTen?.trim() || account.hoTen, trangThai, account.accountId]);
  for (const [token, session] of sessions) if (session.user.accountId === account.accountId) sessions.delete(token);
  res.json({ success: true, message: 'Đã cập nhật tài khoản. Các phiên đăng nhập cũ đã bị thu hồi.' });
});

module.exports = { router, accountsRouter, requireAuth, requireAdmin, hashPassword, verifyPassword };
