/**
 * Controller cho UC04: Tra cứu đề thi (BM4) và xem chi tiết định dạng đề in (BM2)
 */

class UC04Controller {
  constructor() {
    this.ketQua = [];
  }

  async khoiTao() {
    await this.taiDanhSachNamHoc();
    this.traCuu();
  }

  async taiDanhSachNamHoc() {
    const sel = document.getElementById('tc-namhoc');
    if (!sel) return;

    try {
      const res = await fetch('/api/bao-cao/danh-sach-nam');
      const data = await res.json();
      if (data.success) {
        sel.innerHTML = '<option value="">Tất cả năm học</option>';
        data.data.forEach(nam => {
          const opt = document.createElement('option');
          opt.value = nam;
          opt.textContent = nam;
          sel.appendChild(opt);
        });
      }
    } catch (err) {
      console.warn('Lỗi tải năm học:', err);
    }
  }

  async traCuu() {
    const tuKhoa = document.getElementById('tc-keyword')?.value || '';
    const maMon = document.getElementById('tc-mon')?.value || '';
    const namHoc = document.getElementById('tc-namhoc')?.value || '';
    const hocKy = document.getElementById('tc-hocky')?.value || '';

    const params = new URLSearchParams();
    if (tuKhoa) params.append('tuKhoa', tuKhoa);
    if (maMon) params.append('maMon', maMon);
    if (namHoc) params.append('namHoc', namHoc);
    if (hocKy) params.append('hocKy', hocKy);

    const tbody = document.getElementById('tc-table-body');
    const countEl = document.getElementById('tc-result-count');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="8" class="py-8 text-center text-slate-400">Đang tìm kiếm đề thi...</td></tr>';

    try {
      const res = await fetch(`/api/de-thi?${params.toString()}`);
      const data = await res.json();
      if (data.success) {
        this.ketQua = data.data;
        this.renderTable();
      } else {
        window.app.toast(data.message, 'error');
      }
    } catch (err) {
      tbody.innerHTML = `<tr><td colspan="8" class="py-4 text-center text-red-500">Lỗi: ${err.message}</td></tr>`;
    }
  }

  renderTable() {
    const tbody = document.getElementById('tc-table-body');
    const countEl = document.getElementById('tc-result-count');
    if (!tbody) return;

    if (this.ketQua.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" class="py-12 text-center text-slate-400">
            <div class="w-32 h-24 mx-auto mb-2 opacity-80">
              <img src="assets/illustrations/empty-state.svg" alt="Empty" class="w-full h-full object-contain">
            </div>
            <p class="text-xs text-slate-500 font-medium">Không tìm thấy đề thi nào phù hợp với các tiêu chí tìm kiếm.</p>
          </td>
        </tr>
      `;
      if (countEl) countEl.textContent = 'Tìm thấy: 0 đề thi';
      return;
    }

    if (countEl) countEl.textContent = `Tìm thấy: ${this.ketQua.length} đề thi`;

    tbody.innerHTML = this.ketQua.map((dt, idx) => {
      const gradedBadge = dt.soBaiCham > 0
        ? `<span class="bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-full font-bold text-[10px] border border-emerald-200">
             ${dt.soBaiCham} bài đã chấm
           </span>`
        : `<span class="bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full text-[10px]">
             Chưa chấm
           </span>`;

      return `
        <tr class="hover:bg-slate-50/75 transition">
          <td class="py-3 px-4 text-center font-mono text-slate-400">${idx + 1}</td>
          <td class="py-3 px-4 font-mono font-bold text-blue-700">${dt.maDe}</td>
          <td class="py-3 px-4">
            <span class="font-bold text-slate-800">${dt.tenMon}</span>
            <span class="text-[11px] text-slate-400 block">${dt.maMon} • ${dt.hocKy} • ${dt.namHoc}</span>
          </td>
          <td class="py-3 px-4 text-center font-mono font-semibold text-slate-700">${dt.thoiLuong} phút</td>
          <td class="py-3 px-4 text-center font-mono text-slate-600">${dt.ngayThi}</td>
          <td class="py-3 px-4 text-center font-bold text-slate-700">${dt.soCauHoi}/5 câu</td>
          <td class="py-3 px-4 text-center">${gradedBadge}</td>
          <td class="py-3 px-4 text-center">
            <div class="flex items-center justify-center space-x-2">
              <button onclick="window.uc04.xemChiTietDe('${dt.maDe}')" class="bg-blue-50 hover:bg-blue-100 text-blue-700 px-2.5 py-1 rounded-lg text-xs font-bold transition border border-blue-200 flex items-center space-x-1">
                <i class="fa-solid fa-eye text-[11px]"></i>
                <span>Xem đề</span>
              </button>
              <button onclick="window.uc04.chuyenSangChamThi('${dt.maMon}', '${dt.maDe}')" class="bg-emerald-50 hover:bg-emerald-100 text-emerald-700 px-2.5 py-1 rounded-lg text-xs font-bold transition border border-emerald-200 flex items-center space-x-1" title="Nhập điểm cho đề này">
                <i class="fa-solid fa-square-check text-[11px]"></i>
                <span>Chấm</span>
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join('');
  }

  resetFilter() {
    const k = document.getElementById('tc-keyword');
    const m = document.getElementById('tc-mon');
    const n = document.getElementById('tc-namhoc');
    const h = document.getElementById('tc-hocky');
    if (k) k.value = '';
    if (m) m.value = '';
    if (n) n.value = '';
    if (h) h.value = '';
    this.traCuu();
  }

  async xemChiTietDe(maDe) {
    try {
      const res = await fetch(`/api/de-thi/${maDe}`);
      const data = await res.json();
      if (!data.success) {
        window.app.toast(data.message, 'error');
        return;
      }

      const dt = data.data;
      const content = document.getElementById('preview-dethi-content');
      if (!content) return;

      const questionsHtml = dt.cauHois.map((q, idx) => `
        <div class="mb-5 pb-4 border-b border-slate-200/60 last:border-0">
          <div class="flex items-center justify-between mb-1.5">
          <h5 class="font-bold text-slate-900 text-sm">Câu ${idx + 1} (${q.doKho}, ${Number(q.diemToiDa).toFixed(1)} điểm):</h5>
            <span class="text-xs text-slate-400 font-mono">${q.maCauHoi}</span>
          </div>
          <p class="text-slate-800 leading-relaxed text-sm whitespace-pre-line">${q.noiDung}</p>
        </div>
      `).join('');

      const classesGradedHtml = dt.cacLopDaCham && dt.cacLopDaCham.length > 0
        ? dt.cacLopDaCham.map(l => `<span class="bg-slate-100 px-2 py-0.5 rounded text-xs text-slate-700 font-sans border border-slate-200">${l.tenLop} (${l.soSinhVienCham} bài)</span>`).join(' ')
        : '<span class="text-slate-400 text-xs italic font-sans">Chưa có lớp nào được chấm điểm</span>';

      content.innerHTML = `
        <div class="border-b-2 border-slate-900 pb-4 mb-6 text-center">
          <div class="flex justify-between items-start text-xs text-slate-600 mb-3 uppercase tracking-wider font-sans">
            <div>
              <p class="font-bold text-slate-800">ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH</p>
              <p class="font-bold text-blue-900">TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN</p>
            </div>
            <div class="text-right">
              <p class="font-bold text-slate-800">ĐỀ THI KẾT THÚC HỌC PHẦN</p>
              <p class="font-mono text-slate-500">Mã đề: ${dt.maDe}</p>
            </div>
          </div>

          <h3 class="text-xl font-bold uppercase text-slate-900 tracking-wide mt-2">
            ĐỀ THI MÔN: ${dt.tenMon} (${dt.maMon})
          </h3>
          <p class="text-xs text-slate-600 font-sans mt-1">
            ${dt.hocKy} • Năm học: ${dt.namHoc} • Thời lượng: <strong>${dt.thoiLuong} phút</strong> • Ngày thi: ${dt.ngayThi}
          </p>
          <p class="text-[11px] text-slate-500 italic mt-1 font-sans">
            (Sinh viên không được sử dụng tài liệu trừ khi có thông báo riêng của đề thi)
          </p>
        </div>

        <div class="space-y-4 mb-8">
          ${questionsHtml}
        </div>

        <div class="text-center font-bold text-xs uppercase tracking-widest text-slate-400 my-6">
          --- HẾT ---
        </div>

        <div class="mt-8 pt-4 border-t border-slate-200 bg-slate-50 p-4 rounded-2xl no-print font-sans">
          <h6 class="text-xs font-bold text-slate-700 uppercase mb-2">Trạng thái chấm thi:</h6>
          <div class="flex flex-wrap items-center gap-2 mb-2">
            ${classesGradedHtml}
          </div>
          <p class="text-[11px] text-slate-500">
            Tổng cộng: <strong>${dt.soBaiCham} bài chấm</strong>. 
            ${dt.daCoKetQuaCham ? '<span class="text-amber-700 font-bold">Đề thi đã có kết quả chấm (Đã khóa chức năng sửa/xóa để bảo toàn kết quả thi).</span>' : '<span class="text-emerald-700 font-bold">Đề thi chưa có bài chấm (Có thể chỉnh sửa hoặc xóa bình thường).</span>'}
          </p>
        </div>
      `;

      document.getElementById('modal-preview-dethi').classList.remove('hidden');
    } catch (err) {
      window.app.toast('Lỗi xem đề thi: ' + err.message, 'error');
    }
  }

  closePreviewModal() {
    const modal = document.getElementById('modal-preview-dethi');
    if (modal) modal.classList.add('hidden');
  }

  chuyenSangChamThi(maMon, maDe) {
    window.app.switchTab('chamthi');
    setTimeout(() => {
      const selMon = document.getElementById('ct-select-mon');
      if (selMon) {
        selMon.value = maMon;
        window.uc03.onChonMon();
        const selDe = document.getElementById('ct-select-de');
        if (selDe) {
          selDe.value = maDe;
          window.uc03.onChonDe();
        }
      }
    }, 200);
  }
}

window.uc04 = new UC04Controller();
