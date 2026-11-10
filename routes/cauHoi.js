const express = require('express');
const router = express.Router();
const { query, get, run } = require('../database/db');
const DO_KHO_HOP_LE = ['Dễ', 'Trung Bình', 'Phức Tạp', 'Khó'];

router.get('/', async (req, res) => {
  try {
    const { maMon, doKho, tuKhoa } = req.query;
    let sql = `SELECT ch.maCauHoi,ch.maMon,mh.tenMon,ch.doKho,ch.noiDung,ch.dapAn,
      COUNT(dtch.maDe) AS soLanDung,GROUP_CONCAT(dtch.maDe, ', ') AS danhSachMaDe
      FROM CauHoi ch JOIN MonHoc mh ON mh.maMon=ch.maMon
      LEFT JOIN DeThi_CauHoi dtch ON dtch.maCauHoi=ch.maCauHoi
      WHERE ch.accountId=?`;
    const params = [req.user.accountId];
    if (maMon) { sql += ' AND ch.maMon=?'; params.push(maMon); }
    if (doKho) { sql += ' AND ch.doKho=?'; params.push(doKho); }
    if (tuKhoa) { sql += ' AND (ch.noiDung LIKE ? OR ch.maCauHoi LIKE ?)'; params.push(`%${tuKhoa}%`,`%${tuKhoa}%`); }
    sql += ' GROUP BY ch.maCauHoi ORDER BY ch.maMon,ch.maCauHoi';
    const data = await query(sql, params);
    res.json({ success:true, data:data.map(x=>({...x, daDungTrongDe:x.soLanDung>0})) });
  } catch (err) { res.status(500).json({success:false,message:'Lỗi tải câu hỏi: '+err.message}); }
});
router.get('/:maCauHoi', async (req,res)=>{
  const item=await get(`SELECT ch.*,mh.tenMon,COUNT(dtch.maDe) AS soLanDung,GROUP_CONCAT(dtch.maDe, ', ') AS danhSachMaDe
    FROM CauHoi ch JOIN MonHoc mh ON mh.maMon=ch.maMon LEFT JOIN DeThi_CauHoi dtch ON dtch.maCauHoi=ch.maCauHoi
    WHERE ch.maCauHoi=? AND ch.accountId=? GROUP BY ch.maCauHoi`,[req.params.maCauHoi,req.user.accountId]);
  if(!item)return res.status(404).json({success:false,message:'Không tìm thấy câu hỏi trong tài khoản.'});
  res.json({success:true,data:{...item,daDungTrongDe:item.soLanDung>0}});
});
router.post('/', async(req,res)=>{
  let {maCauHoi,maMon,doKho,noiDung,dapAn}=req.body||{};
  if(!maMon||!DO_KHO_HOP_LE.includes(doKho)||!noiDung?.trim()||!dapAn?.trim())return res.status(400).json({success:false,message:'Môn học, độ khó, nội dung và đáp án đúng là bắt buộc.'});
  if(!(await get('SELECT maMon FROM MonHoc WHERE maMon=?',[maMon])))return res.status(400).json({success:false,message:'Môn học không tồn tại.'});
  if(!maCauHoi?.trim()){
    const last=await get('SELECT maCauHoi FROM CauHoi WHERE maMon=? AND accountId=? ORDER BY maCauHoi DESC LIMIT 1',[maMon,req.user.accountId]);
    const n=last?((parseInt(last.maCauHoi.split('_').pop(),10)||0)+1):1;
    maCauHoi=`CH_${maMon}_${String(n).padStart(2,'0')}`;
  }
  maCauHoi=maCauHoi.trim();
  try{await run('INSERT INTO CauHoi(maCauHoi,maMon,doKho,noiDung,dapAn,accountId) VALUES(?,?,?,?,?,?)',[maCauHoi,maMon,doKho,noiDung.trim(),dapAn.trim(),req.user.accountId]);res.status(201).json({success:true,message:'Đã lưu câu hỏi và đáp án đúng.',data:{maCauHoi}});}
  catch(err){res.status(400).json({success:false,message:err.message.includes('UNIQUE')?'Mã câu hỏi đã tồn tại.':'Không thể lưu câu hỏi.'});}
});
router.put('/:maCauHoi',async(req,res)=>{
  const {maMon,doKho,noiDung,dapAn}=req.body||{}; const id=req.params.maCauHoi;
  const current=await get('SELECT * FROM CauHoi WHERE maCauHoi=? AND accountId=?',[id,req.user.accountId]);
  if(!current)return res.status(404).json({success:false,message:'Không tìm thấy câu hỏi trong tài khoản.'});
  if(!maMon||!DO_KHO_HOP_LE.includes(doKho)||!noiDung?.trim()||!dapAn?.trim())return res.status(400).json({success:false,message:'Môn học, độ khó, nội dung và đáp án đúng là bắt buộc.'});
  await run('UPDATE CauHoi SET maMon=?,doKho=?,noiDung=?,dapAn=? WHERE maCauHoi=? AND accountId=?',[maMon,doKho,noiDung.trim(),dapAn.trim(),id,req.user.accountId]);
  res.json({success:true,message:'Đã cập nhật câu hỏi.'});
});
router.delete('/:maCauHoi',async(req,res)=>{
  const id=req.params.maCauHoi;const current=await get('SELECT maCauHoi FROM CauHoi WHERE maCauHoi=? AND accountId=?',[id,req.user.accountId]);
  if(!current)return res.status(404).json({success:false,message:'Không tìm thấy câu hỏi trong tài khoản.'});
  const used=await get('SELECT dtch.maDe FROM DeThi_CauHoi dtch JOIN DeThi dt ON dt.maDe=dtch.maDe WHERE dtch.maCauHoi=? AND dt.accountId=? LIMIT 1',[id,req.user.accountId]);
  if(used)return res.status(400).json({success:false,ruleViolated:'QĐ1',message:`Câu hỏi đã được dùng trong đề ${used.maDe}.`});
  await run('DELETE FROM CauHoi WHERE maCauHoi=? AND accountId=?',[id,req.user.accountId]);res.json({success:true,message:'Đã xóa câu hỏi.'});
});
module.exports=router;
