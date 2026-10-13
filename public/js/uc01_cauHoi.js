/**
 * Controller Quản lý Ngân hàng câu hỏi
 */

class UC01Controller {
  constructor() {
    this.danhSach = [];
    this.viewMode = 'card';
  }

  setViewMode(mode) {
    this.viewMode = mode;
    const cardBtn = document.getElementById('ch-view-card-btn');
    const tableBtn = document.getElementById('ch-view-table-btn');
    const cardContainer = document.getElementById('ch-card-container');
    const tableContainer = document.getElementById('ch-table-container');

    if (mode === 'card') {
      cardBtn.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg bg-white shadow-2xs text-blue-700';
      tableBtn.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg text-slate-600 hover:text-slate-900';
      cardContainer.classList.remove('hidden');
      tableContainer.classList.add('hidden');
    } else {
      tableBtn.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg bg-white shadow-2xs text-blue-700';
      cardBtn.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg text-slate-600 hover:text-slate-900';
      tableContainer.classList.remove('hidden');
      cardContainer.classList.add('hidden');
    }
    this.render();
  }

  async taiDanhSach() {
    const maMon = document.getElementById('ch-filter-mon')?.value || '';
    const doKho = document.getElementById('ch-filter-dokho')?.value || '';
    const tuKhoa = document.getElementById('ch-filter-search')?.value || '';

    const params = new URLSearchParams();
    if (maMon) params.append('maMon', maMon);
    if (doKho) params.append('doKho', doKho);
    if (tuKhoa) params.append('tuKhoa', tuKhoa);

    try {
      const res = await fetch(`/api/cau-hoi?${params.toString()}`);
      const data = await res.json();
      if (data.success) {
        this.danhSach = data.data;
        this.render();
      } else {
        window.app.toast(data.message, 'error');
      }
    } catch (err) {
      window.app.toast('Lỗi tải câu hỏi: ' + err.message, 'error');
    }
  }

  render() {
    const countEl = document.getElementById('ch-total-count');
    if (countEl) countEl.textContent = `Tổng cộng: ${this.danhSach.length} câu hỏi`;

    this.renderCards();
    this.renderTable();
  }

  renderCards() {
    const container = document.getElementById('ch-card-container');
    if (!container) return;

    if (this.danhSach.length === 0) {
      container.innerHTML = `
        <div class="col-span-full py-12 text-center flex flex-col items-center justify-center">
          <div class="w-32 h-24 mb-2 opacity-80">
            <img src="assets/illustrations/quiz.svg" alt="Empty" class="w-full h-full object-contain">
          </div>
          <p class="text-xs text-slate-400 font-medium">Không tìm thấy câu hỏi nào phù hợp.</p>
        </div>
      `;
      return;
    }

    const subThemes = {
      'IT001': { border: 'border-t-4 border-t-blue-500', tagBg: 'bg-blue-50 text-blue-700 border-blue-200', glow: 'rgba(59, 130, 246, 0.22)' },
      'IT002': { border: 'border-t-4 border-t-purple-500', tagBg: 'bg-purple-50 text-purple-700 border-purple-200', glow: 'rgba(168, 85, 247, 0.22)' },
      'IT003': { border: 'border-t-4 border-t-emerald-500', tagBg: 'bg-emerald-50 text-emerald-700 border-emerald-200', glow: 'rgba(16, 185, 129, 0.22)' },
      'SE104': { border: 'border-t-4 border-t-amber-500', tagBg: 'bg-amber-50 text-amber-700 border-amber-200', glow: 'rgba(245, 158, 11, 0.22)' }
    };

    container.innerHTML = this.danhSach.map(item => {
      let badgeClass = 'badge-medium';
      if (item.doKho === 'Dễ') badgeClass = 'badge-easy';
      else if (item.doKho === 'Phức Tạp') badgeClass = 'badge-complex';
      else if (item.doKho === 'Khó') badgeClass = 'badge-hard';

      const isLocked = item.daDungTrongDe;
      const theme = subThemes[item.maMon] || { border: 'border-t-4 border-t-blue-500', tagBg: 'bg-blue-50 text-blue-700 border-blue-200', glow: 'rgba(59, 130, 246, 0.22)' };

      return `
        <div class="glass-card app-card-lift p-4 flex flex-col justify-between space-y-3 ${theme.border} relative overflow-hidden group">
          <div class="absolute -top-8 -right-8 w-28 h-28 rounded-full pointer-events-none opacity-50 blur-xl transition group-hover:opacity-85" style="background: ${theme.glow}"></div>
          <div>
            <!-- Header -->
            <div class="flex items-center justify-between mb-2.5">
              <div class="flex items-center space-x-1.5">
                <span class="font-mono font-bold text-xs ${theme.tagBg} px-2 py-0.5 rounded-lg border">${item.maCauHoi}</span>
                <span class="text-[11px] font-bold text-slate-500 font-mono">${item.maMon}</span>
              </div>
              <span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold ${badgeClass}">${item.doKho}</span>
            </div>

            <!-- Content -->
            <p class="text-xs text-slate-800 leading-relaxed font-medium line-clamp-4">
              ${this.escapeHtml(item.noiDung)}
            </p>
          </div>

          <!-- Footer -->
          <div class="pt-2.5 border-t border-slate-100/80 flex items-center justify-between">
            <div>
              ${isLocked ? `
                <span class="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-amber-500/10 text-amber-700 border border-amber-500/20" title="Đã có trong đề: ${item.danhSachMaDe}">
                  <i class="fa-solid fa-lock text-[9px]"></i>
                  <span>Đang dùng (${item.soLanDung} đề)</span>
                </span>
              ` : `
                <span class="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-700 border border-emerald-500/20">
                  <i class="fa-solid fa-check text-[9px]"></i>
                  <span>Sẵn sàng sử dụng</span>
                </span>
              `}
            </div>

            <div class="flex items-center space-x-1">
              ${isLocked ? `
                <button onclick="window.uc01.thongBaoKhoa('${item.maCauHoi}', '${item.danhSachMaDe}')" class="p-1.5 text-slate-400 hover:text-amber-600 rounded-lg transition" title="Không thể sửa vì đang dùng trong đề">
                  <i class="fa-solid fa-lock text-xs"></i>
                </button>
                <button onclick="window.uc01.thongBaoKhoa('${item.maCauHoi}', '${item.danhSachMaDe}')" class="p-1.5 text-slate-400 hover:text-amber-600 rounded-lg transition" title="Không thể xóa vì đang dùng trong đề">
                  <i class="fa-solid fa-trash-can text-xs opacity-50"></i>
                </button>
              ` : `
                <button onclick="window.uc01.openEditModal('${item.maCauHoi}')" class="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition" title="Sửa câu hỏi">
                  <i class="fa-solid fa-pen-to-square text-xs"></i>
                </button>
                <button onclick="window.uc01.xacNhanXoa('${item.maCauHoi}')" class="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg transition" title="Xóa câu hỏi">
                  <i class="fa-solid fa-trash-can text-xs"></i>
                </button>
              `}
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  renderTable() {
    const tbody = document.getElementById('ch-table-body');
    if (!tbody) return;

    if (this.danhSach.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="py-8 text-center text-slate-400">Không tìm thấy câu hỏi nào.</td></tr>';
      return;
    }

    tbody.innerHTML = this.danhSach.map((item, idx) => {
      let badgeClass = 'badge-medium';
      if (item.doKho === 'Dễ') badgeClass = 'badge-easy';
      else if (item.doKho === 'Phức Tạp') badgeClass = 'badge-complex';
      else if (item.doKho === 'Khó') badgeClass = 'badge-hard';

      const isLocked = item.daDungTrongDe;

      return `
        <tr class="hover:bg-slate-50/75 transition">
          <td class="py-3 px-4 text-center font-mono text-slate-400">${idx + 1}</td>
          <td class="py-3 px-4 font-mono font-bold text-slate-700">${item.maCauHoi}</td>
          <td class="py-3 px-4">
            <span class="font-semibold text-slate-800">${item.maMon}</span>
            <span class="text-[11px] text-slate-400 block">${item.tenMon}</span>
          </td>
          <td class="py-3 px-4">
            <span class="px-2 py-0.5 rounded text-[11px] font-bold ${badgeClass}">${item.doKho}</span>
          </td>
          <td class="py-3 px-4 text-slate-700 leading-relaxed font-normal">${this.escapeHtml(item.noiDung)}</td>
          <td class="py-3 px-4 text-center">
            ${isLocked ? `<span class="bg-amber-50 text-amber-700 text-[10px] px-2 py-0.5 rounded-full font-bold border border-amber-200">Đang dùng (${item.soLanDung})</span>` : `<span class="bg-emerald-50 text-emerald-700 text-[10px] px-2 py-0.5 rounded-full font-bold border border-emerald-200">Chưa dùng</span>`}
          </td>
          <td class="py-3 px-4 text-center">
            <div class="flex items-center justify-center space-x-1">
              ${isLocked ? `
                <button onclick="window.uc01.thongBaoKhoa('${item.maCauHoi}', '${item.danhSachMaDe}')" class="p-1 text-slate-400 hover:text-amber-600"><i class="fa-solid fa-lock text-xs"></i></button>
              ` : `
                <button onclick="window.uc01.openEditModal('${item.maCauHoi}')" class="p-1 text-blue-600 hover:text-blue-800"><i class="fa-solid fa-pen-to-square text-xs"></i></button>
                <button onclick="window.uc01.xacNhanXoa('${item.maCauHoi}')" class="p-1 text-rose-600 hover:text-rose-800"><i class="fa-solid fa-trash-can text-xs"></i></button>
              `}
            </div>
          </td>
        </tr>
      `;
    }).join('');
  }

  resetFilter() {
    const s = document.getElementById('ch-filter-search');
    const m = document.getElementById('ch-filter-mon');
    const d = document.getElementById('ch-filter-dokho');
    if (s) s.value = '';
    if (m) m.value = '';
    if (d) d.value = '';
    this.taiDanhSach();
  }

  openCreateModal() {
    document.getElementById('modal-ch-title').textContent = 'Soạn câu hỏi mới';
    document.getElementById('modal-ch-mode').value = 'create';
    document.getElementById('modal-ch-made').value = '';
    document.getElementById('modal-ch-made').removeAttribute('readonly');
    document.getElementById('modal-ch-mon').removeAttribute('disabled');
    document.getElementById('modal-ch-dokho').value = 'Trung Bình';
    document.getElementById('modal-ch-noidung').value = '';

    document.getElementById('modal-cauhoi').classList.remove('hidden');
  }

  async openEditModal(maCauHoi) {
    try {
      const res = await fetch(`/api/cau-hoi/${maCauHoi}`);
      const data = await res.json();
      if (!data.success) {
        window.app.toast(data.message, 'error');
        return;
      }

      const item = data.data;
      if (item.daDungTrongDe) {
        this.thongBaoKhoa(item.maCauHoi, item.danhSachMaDe);
        return;
      }

      document.getElementById('modal-ch-title').textContent = 'Chỉnh sửa câu hỏi';
      document.getElementById('modal-ch-mode').value = 'edit';
      document.getElementById('modal-ch-made').value = item.maCauHoi;
      document.getElementById('modal-ch-made').setAttribute('readonly', 'true');
      document.getElementById('modal-ch-mon').value = item.maMon;
      document.getElementById('modal-ch-dokho').value = item.doKho;
      document.getElementById('modal-ch-noidung').value = item.noiDung;

      document.getElementById('modal-cauhoi').classList.remove('hidden');
    } catch (err) {
      window.app.toast('Lỗi mở câu hỏi: ' + err.message, 'error');
    }
  }

  closeModal() {
    const modal = document.getElementById('modal-cauhoi');
    if (modal) modal.classList.add('hidden');
  }

  async submitForm(event) {
    event.preventDefault();
    const mode = document.getElementById('modal-ch-mode').value;
    const maCauHoi = document.getElementById('modal-ch-made').value.trim();
    const maMon = document.getElementById('modal-ch-mon').value;
    const doKho = document.getElementById('modal-ch-dokho').value;
    const noiDung = document.getElementById('modal-ch-noidung').value.trim();

    if (!maMon || !doKho || !noiDung) {
      window.app.toast('Vui lòng nhập đầy đủ các trường thông tin!', 'warning');
      return;
    }

    try {
      let res, result;
      if (mode === 'create') {
        res = await fetch('/api/cau-hoi', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ maCauHoi, maMon, doKho, noiDung })
        });
      } else {
        res = await fetch(`/api/cau-hoi/${maCauHoi}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ maMon, doKho, noiDung })
        });
      }

      result = await res.json();
      if (result.success) {
        window.app.toast(result.message, 'success');
        this.closeModal();
        this.taiDanhSach();
        window.app.taiDashboardStats();
      } else {
        window.app.toast(result.message, 'warning');
      }
    } catch (err) {
      window.app.toast('Lỗi gửi yêu cầu: ' + err.message, 'error');
    }
  }

  xacNhanXoa(maCauHoi) {
    window.app.confirm(
      'Xóa câu hỏi?',
      `Bạn có chắc chắn muốn xóa câu hỏi '${maCauHoi}' khỏi ngân hàng?`,
      async () => {
        try {
          const res = await fetch(`/api/cau-hoi/${maCauHoi}`, { method: 'DELETE' });
          const result = await res.json();
          if (result.success) {
            window.app.toast(result.message, 'success');
            this.taiDanhSach();
            window.app.taiDashboardStats();
          } else {
            window.app.toast(result.message, 'warning');
          }
        } catch (err) {
          window.app.toast('Lỗi xóa câu hỏi: ' + err.message, 'error');
        }
      }
    );
  }

  thongBaoKhoa(maCauHoi, danhSachDe) {
    window.app.toast(
      `Câu hỏi '${maCauHoi}' hiện đang nằm trong đề thi [${danhSachDe}]. Không thể sửa hoặc xóa để bảo toàn nội dung đề thi đã lập.`,
      'warning'
    );
  }

  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

window.uc01 = new UC01Controller();
