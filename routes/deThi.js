const express = require('express');
const { query, get, run } = require('../database/db');
const router = express.Router();
const normalizeQuestions = list => Array.isArray(list) ? list.map(x => typeof x === 'string' ? {maCauHoi:x, diemToiDa:0} : ({maCauHoi:x.maCauHoi,diemToiDa:Number(x.diemToiDa)})) : [];
async function validateQuestionSet(list, maMon, accountId) {
  if (list.length < 1 || list.length > 5) return 'Mỗi đề thi cần từ 1 đến 5 câu hỏi.';
  if (list.some(q => !Number.isFinite(q.diemToiDa) || q.diemToiDa <= 0 || Math.abs(q.diemToiDa*2-Math.round(q.diemToiDa*2)) > 1e-7)) return 'Điểm mỗi câu phải lớn hơn 0 và là bội số của 0,5.';
  const total = list.reduce((n,q)=>n+q.diemToiDa,0);
  if (Math.abs(total-10)>1e-7) return `Tổng điểm đề phải bằng 10 (hiện tại ${total.toFixed(1)}).`;
  const ids=list.map(q=>q.maCauHoi); if(new Set(ids).size!==ids.length)return 'Không chọn trùng câu hỏi.';
  const marks=ids.map(()=>'?').join(',');
  const found=await query(`SELECT maCauHoi,maMon FROM CauHoi WHERE accountId=? AND maCauHoi IN (${marks})`,[accountId,...ids]);
  if(found.length!==ids.length)return 'Có câu hỏi không thuộc tài khoản hoặc không còn tồn tại.';
  if(found.some(q=>q.maMon!==maMon))return 'Tất cả câu hỏi phải thuộc cùng môn với đề thi.';
  return null;
}
router.get('/',async(req,res)=>{
  try {
    const { maMon, hocKy, namHoc, tuKhoa } = req.query;
    let sql = `SELECT dt.maDe,dt.maMon,mh.tenMon,dt.hocKy,dt.namHoc,dt.ngayThi,dt.thoiLuong,
    COUNT(DISTINCT dtch.maCauHoi) AS soCauHoi,COUNT(DISTINCT kqt.mssv) AS soBaiCham
    FROM DeThi dt JOIN MonHoc mh ON mh.maMon=dt.maMon LEFT JOIN DeThi_CauHoi dtch ON dtch.maDe=dt.maDe
    LEFT JOIN KetQuaThi kqt ON kqt.maDe=dt.maDe WHERE dt.accountId=?`;
    const params = [req.user.accountId];
    if (maMon) { sql += ' AND dt.maMon=?'; params.push(maMon); }
    if (hocKy) { sql += ' AND dt.hocKy=?'; params.push(hocKy); }
    if (namHoc) { sql += ' AND dt.namHoc=?'; params.push(namHoc); }
    if (tuKhoa) { sql += ' AND (dt.maDe LIKE ? OR mh.tenMon LIKE ?)'; params.push(`%${tuKhoa}%`, `%${tuKhoa}%`); }
    sql += ' GROUP BY dt.maDe ORDER BY dt.namHoc DESC,dt.ngayThi DESC';
    const rows=await query(sql,params);
    res.json({success:true,data:rows.map(x=>({...x,daCoKetQuaCham:x.soBaiCham>0}))});
  }
  catch(err){res.status(500).json({success:false,message:'Lỗi tải đề thi: '+err.message});}
});
router.get('/:maDe',async(req,res)=>{
  const dt=await get(`SELECT dt.*,mh.tenMon,COUNT(DISTINCT k.mssv) AS soBaiCham FROM DeThi dt JOIN MonHoc mh ON mh.maMon=dt.maMon
    LEFT JOIN KetQuaThi k ON k.maDe=dt.maDe WHERE dt.maDe=? AND dt.accountId=? GROUP BY dt.maDe`,[req.params.maDe,req.user.accountId]);
  if(!dt)return res.status(404).json({success:false,message:'Không tìm thấy đề thi trong tài khoản.'});
  const cauHois=await query(`SELECT ch.maCauHoi,ch.maMon,ch.doKho,ch.noiDung,ch.dapAn,dtch.diemToiDa
    FROM DeThi_CauHoi dtch JOIN CauHoi ch ON ch.maCauHoi=dtch.maCauHoi WHERE dtch.maDe=? ORDER BY ch.maCauHoi`,[dt.maDe]);
  const cacLopDaCham=await query(`SELECT l.maLop,l.tenLop,COUNT(k.mssv) AS soSinhVienCham FROM KetQuaThi k JOIN SinhVien s ON s.mssv=k.mssv
    JOIN Lop l ON l.maLop=s.maLop WHERE k.maDe=? AND l.accountId=? GROUP BY l.maLop`,[dt.maDe,req.user.accountId]);
  res.json({success:true,data:{...dt,daCoKetQuaCham:dt.soBaiCham>0,cauHois,cacLopDaCham}});
});
router.post('/',async(req,res)=>{
  const {maDe,maMon,hocKy,namHoc,ngayThi,thoiLuong}=req.body||{};const questions=normalizeQuestions(req.body?.danhSachCauHoi);
  if(!maDe?.trim()||!maMon||!hocKy||!namHoc||!ngayThi)return res.status(400).json({success:false,message:'Vui lòng nhập đủ thông tin đề thi.'});
  const duration=Number(thoiLuong);if(!Number.isInteger(duration)||duration<30||duration>180)return res.status(400).json({success:false,ruleViolated:'QĐ2',message:'Thời lượng phải từ 30 đến 180 phút.'});
  const err=await validateQuestionSet(questions,maMon,req.user.accountId);if(err)return res.status(400).json({success:false,ruleViolated:'QĐ2',message:err});
  let examCreated = false;
  try{
    await run('INSERT INTO DeThi(maDe,maMon,hocKy,namHoc,ngayThi,thoiLuong,accountId) VALUES(?,?,?,?,?,?,?)',[maDe.trim(),maMon,hocKy,namHoc.trim(),ngayThi,duration,req.user.accountId]);
    examCreated = true;
    for(const q of questions)await run('INSERT INTO DeThi_CauHoi(maDe,maCauHoi,diemToiDa) VALUES(?,?,?)',[maDe.trim(),q.maCauHoi,q.diemToiDa]);
    res.status(201).json({success:true,message:`Đã tạo đề thi ${maDe.trim()} với tổng điểm 10.`,data:{maDe:maDe.trim()}});
  }catch(e){
    if(examCreated){await run('DELETE FROM DeThi_CauHoi WHERE maDe=?',[maDe.trim()]).catch(()=>{});await run('DELETE FROM DeThi WHERE maDe=? AND accountId=?',[maDe.trim(),req.user.accountId]).catch(()=>{});}
    res.status(400).json({success:false,message:e.message.includes('UNIQUE')?'Mã đề đã tồn tại.':'Không thể lưu đề thi.'});
  }
});
router.put('/:maDe',async(req,res)=>{
  const id=req.params.maDe;const dt=await get('SELECT * FROM DeThi WHERE maDe=? AND accountId=?',[id,req.user.accountId]);
  if(!dt)return res.status(404).json({success:false,message:'Không tìm thấy đề thi trong tài khoản.'});
  if((await get('SELECT COUNT(*) AS n FROM KetQuaThi WHERE maDe=?',[id])).n)return res.status(400).json({success:false,ruleViolated:'QĐ2',message:'Đề đã có kết quả chấm và được khóa.'});
  const {maMon,hocKy,namHoc,ngayThi}=req.body||{};const duration=Number(req.body?.thoiLuong),questions=normalizeQuestions(req.body?.danhSachCauHoi);
  if(!maMon||!hocKy||!namHoc||!ngayThi||!Number.isInteger(duration)||duration<30||duration>180)return res.status(400).json({success:false,ruleViolated:'QĐ2',message:'Thông tin đề hoặc thời lượng chưa hợp lệ.'});
  const err=await validateQuestionSet(questions,maMon,req.user.accountId);if(err)return res.status(400).json({success:false,ruleViolated:'QĐ2',message:err});
  const oldQuestions=await query('SELECT maCauHoi,diemToiDa FROM DeThi_CauHoi WHERE maDe=?',[id]);
  try {
    await run('UPDATE DeThi SET maMon=?,hocKy=?,namHoc=?,ngayThi=?,thoiLuong=? WHERE maDe=? AND accountId=?',[maMon,hocKy,namHoc.trim(),ngayThi,duration,id,req.user.accountId]);
    await run('DELETE FROM DeThi_CauHoi WHERE maDe=?',[id]);for(const q of questions)await run('INSERT INTO DeThi_CauHoi(maDe,maCauHoi,diemToiDa) VALUES(?,?,?)',[id,q.maCauHoi,q.diemToiDa]);
    res.json({success:true,message:'Đã cập nhật đề thi.'});
  } catch (err) {
    await run('DELETE FROM DeThi_CauHoi WHERE maDe=?',[id]).catch(()=>{});
    await run('UPDATE DeThi SET maMon=?,hocKy=?,namHoc=?,ngayThi=?,thoiLuong=? WHERE maDe=? AND accountId=?',[dt.maMon,dt.hocKy,dt.namHoc,dt.ngayThi,dt.thoiLuong,id,req.user.accountId]).catch(()=>{});
    for(const q of oldQuestions)await run('INSERT INTO DeThi_CauHoi(maDe,maCauHoi,diemToiDa) VALUES(?,?,?)',[id,q.maCauHoi,q.diemToiDa]).catch(()=>{});
    res.status(400).json({success:false,message:err.message.includes('UNIQUE')?'Mã câu hỏi trong đề bị trùng.':'Không thể cập nhật đề thi.'});
  }
});
router.delete('/:maDe',async(req,res)=>{
  const id=req.params.maDe;if(!(await get('SELECT maDe FROM DeThi WHERE maDe=? AND accountId=?',[id,req.user.accountId])))return res.status(404).json({success:false,message:'Không tìm thấy đề thi trong tài khoản.'});
  if((await get('SELECT COUNT(*) AS n FROM KetQuaThi WHERE maDe=?',[id])).n)return res.status(400).json({success:false,ruleViolated:'QĐ2',message:'Đề đã có kết quả chấm và được khóa.'});
  await run('DELETE FROM DeThi_CauHoi WHERE maDe=?',[id]);await run('DELETE FROM DeThi WHERE maDe=? AND accountId=?',[id,req.user.accountId]);res.json({success:true,message:'Đã xóa đề thi.'});
});
module.exports=router;
