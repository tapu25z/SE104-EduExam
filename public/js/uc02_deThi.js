/**
 * Controller cho UC02: Soạn, sửa, xóa đề thi (BM2, QĐ2)
 * Hỗ trợ chuyển đổi Dạng Thẻ (Card View) & Dạng Bảng (Table View)
 */

class UC02Controller {
  constructor() {
    this.danhSach = [];
    this.cauHoiTheoMon = [];
    this.cauHoiDaChon = new Set();
    this.viewMode = 'card';
  }

  setViewMode(mode) {
    this.viewMode = mode;
    const cardBtn = document.getElementById('dt-view-card-btn');
    const tableBtn = document.getElementById('dt-view-table-btn');
    const cardContainer = document.getElementById('dt-card-container');
    const tableContainer = document.getElementById('dt-table-container');

    if (mode === 'card') {
      cardBtn.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg bg-white shadow-2xs text-blue-700 transition';
      tableBtn.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg text-slate-600 hover:text-slate-900 transition';
      cardContainer.classList.remove('hidden');
      tableContainer.classList.add('hidden');
    } else {
      tableBtn.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg bg-white shadow-2xs text-blue-700 transition';
      cardBtn.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg text-slate-600 hover:text-slate-900 transition';
      tableContainer.classList.remove('hidden');
      cardContainer.classList.add('hidden');
    }
    this.render();
  }

  async taiDanhSach() {
    try {
      const res = await fetch('/api/de-thi');
      const data = await res.json();
      if (data.success) {
        this.danhSach = data.data;
        this.render();
      } else {
        window.app.toast(data.message, 'error');
      }
    } catch (err) {
      window.app.toast('Lỗi tải danh sách đề thi: ' + err.message, 'error');
    }
  }

  render() {
    const countEl = document.getElementById('dt-total-count');
    if (countEl) countEl.textContent = `Tổng cộng: ${this.danhSach.length} đề thi`;

    this.renderCards();
    this.renderTable();
  }

  renderCards() {
    const container = document.getElementById('dt-card-container');
    if (!container) return;

    if (this.danhSach.length === 0) {
      container.innerHTML = `
        <div class="col-span-full py-12 text-center flex flex-col items-center justify-center">
          <div class="w-36 h-28 mb-3">
            <img src="assets/illustrations/exam.svg" alt="Empty" class="w-full h-full object-contain">
          </div>
          <p class="text-xs text-slate-500 font-medium">Chưa có đề thi nào trong hệ thống.</p>
        </div>
      `;
      return;
    }

    const subThemes = {
      'IT001': { 
        img: 'assets/illustrations/sub-it001.svg', 
        border: 'border-t-4 border-t-blue-500', 
        badge: 'bg-blue-500/10 text-blue-700 border-blue-500/20',
        glow: 'rgba(59, 130, 246, 0.25)'
      },
      'IT002': { 
        img: 'assets/illustrations/sub-it002.svg', 
        border: 'border-t-4 border-t-purple-500', 
        badge: 'bg-purple-500/10 text-purple-700 border-purple-500/20',
        glow: 'rgba(168, 85, 247, 0.25)'
      },
      'IT003': { 
        img: 'assets/illustrations/sub-it003.svg', 
        border: 'border-t-4 border-t-emerald-500', 
        badge: 'bg-emerald-500/10 text-emerald-700 border-emerald-500/20',
        glow: 'rgba(16, 185, 129, 0.25)'
      },
      'SE104': { 
        img: 'assets/illustrations/sub-se104.svg', 
        border: 'border-t-4 border-t-amber-500', 
        badge: 'bg-amber-500/10 text-amber-700 border-amber-500/20',
        glow: 'rgba(245, 158, 11, 0.25)'
      }
    };

    container.innerHTML = this.danhSach.map(item => {
      const isGraded = item.daCoKetQuaCham;
      const theme = subThemes[item.maMon] || { 
        img: 'assets/illustrations/exam.svg', 
        border: 'border-t-4 border-t-blue-500', 
        badge: 'bg-blue-500/10 text-blue-700 border-blue-500/20',
        glow: 'rgba(59, 130, 246, 0.25)'
      };

      return `
        <div class="glass-card app-card-lift ${theme.border} p-5 rounded-2xl flex flex-col justify-between space-y-4 relative overflow-hidden group">
          
          <!-- Background Ambient Glow -->
          <div class="absolute -top-10 -right-10 w-36 h-36 rounded-full pointer-events-none opacity-60 blur-2xl transition group-hover:opacity-95" style="background: ${theme.glow}"></div>

          <div>
            <!-- Card Header: Code + Date + Time Badge -->
            <div class="flex items-start justify-between gap-2 mb-3">
              <div class="flex items-center space-x-2.5">
                <div class="w-11 h-11 rounded-2xl overflow-hidden bg-white/80 p-1.5 shrink-0 shadow-2xs border border-white/90">
                  <img src="${theme.img}" alt="${item.maMon}" class="w-full h-full object-contain">
                </div>
                <div>
                  <span class="font-mono font-bold text-xs ${theme.badge} px-2.5 py-0.5 rounded-lg border backdrop-blur-md">${item.maDe}</span>
                  <p class="text-[10px] text-slate-400 mt-0.5 font-medium">${item.hocKy} • ${item.namHoc}</p>
                </div>
              </div>

              <!-- Thời lượng thi (iOS Time Pill) -->
              <div class="glass-pill px-2.5 py-1 rounded-full text-xs font-bold text-slate-700 flex items-center space-x-1 shrink-0 shadow-2xs">
                <i class="fa-regular fa-clock text-blue-500 text-[11px]"></i>
                <span>${item.thoiLuong}p</span>
              </div>
            </div>

            <!-- Subject Title -->
            <h4 class="font-extrabold text-sm text-slate-800 leading-snug mb-3">
              ${item.tenMon}
            </h4>

            <!-- Stats & Trạng thái chấm điểm -->
            <div class="flex flex-wrap items-center gap-2 text-xs">
              <!-- Số câu hỏi -->
              <span class="glass-pill px-2.5 py-0.5 rounded-full text-[11px] font-bold text-slate-600 flex items-center space-x-1">
                <i class="fa-solid fa-list-check text-slate-400 text-[10px]"></i>
                <span>${item.soCauHoi}/5 câu</span>
              </span>

              <!-- Trạng thái chấm điểm -->
              ${isGraded ? `
                <span class="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/10 text-emerald-700 border border-emerald-500/25 backdrop-blur-md">
                  <i class="fa-solid fa-circle-check text-[10px] text-emerald-600"></i>
                  <span>${item.soBaiCham} bài đã chấm</span>
                </span>
              ` : `
                <span class="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-slate-500/10 text-slate-500 border border-slate-500/15 backdrop-blur-md">
                  <i class="fa-regular fa-clock text-[10px] text-slate-400"></i>
                  <span>Chưa chấm điểm</span>
                </span>
              `}
            </div>
          </div>

          <!-- Card Footer Actions -->
          <div class="pt-3 border-t border-slate-100/80 flex items-center justify-between">
            <button onclick="window.uc04.xemChiTietDe('${item.maDe}')" class="text-xs font-bold text-blue-600 hover:text-white bg-blue-50 hover:bg-blue-600 px-3.5 py-1.5 rounded-xl transition flex items-center space-x-1.5 shadow-2xs">
              <i class="fa-solid fa-eye text-xs"></i>
              <span>Xem & In đề</span>
            </button>

            <div class="flex items-center space-x-1">
              ${isGraded ? `
                <button onclick="window.uc02.thongBaoKhoaQD2('${item.maDe}', ${item.soBaiCham})" class="p-2 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-xl transition" title="Đã có bài thi được chấm (Khóa chỉnh sửa)">
                  <i class="fa-solid fa-lock text-xs"></i>
                </button>
                <button onclick="window.uc02.thongBaoKhoaQD2('${item.maDe}', ${item.soBaiCham})" class="p-2 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-xl transition" title="Đã có bài thi được chấm (Khóa xóa)">
                  <i class="fa-solid fa-trash-can text-xs opacity-50"></i>
                </button>
              ` : `
                <button onclick="window.uc02.openEditModal('${item.maDe}')" class="p-2 text-blue-600 hover:bg-blue-50 rounded-xl transition" title="Sửa đề thi">
                  <i class="fa-solid fa-pen-to-square text-xs"></i>
                </button>
                <button onclick="window.uc02.xacNhanXoa('${item.maDe}')" class="p-2 text-rose-600 hover:bg-rose-50 rounded-xl transition" title="Xóa đề thi">
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
    const tbody = document.getElementById('dt-table-body');
    if (!tbody) return;

    if (this.danhSach.length === 0) {
      tbody.innerHTML = '<tr><td colspan="9" class="py-8 text-center text-slate-400">Chưa có đề thi nào.</td></tr>';
      return;
    }

    tbody.innerHTML = this.danhSach.map((item, idx) => {
      const isGraded = item.daCoKetQuaCham;

      return `
        <tr class="hover:bg-slate-50/75 transition">
          <td class="py-3 px-4 text-center font-mono text-slate-400">${idx + 1}</td>
          <td class="py-3 px-4 font-mono font-bold text-slate-800">${item.maDe}</td>
          <td class="py-3 px-4">
            <span class="font-semibold text-slate-800">${item.maMon}</span>
            <span class="text-[11px] text-slate-500 block">${item.tenMon}</span>
          </td>
          <td class="py-3 px-4 text-center">
            <span class="text-slate-700 font-medium">${item.hocKy}</span>
            <span class="text-[11px] text-slate-400 block">${item.namHoc}</span>
          </td>
          <td class="py-3 px-4 text-center text-slate-600 font-mono">${item.ngayThi}</td>
          <td class="py-3 px-4 text-center font-bold font-mono text-blue-700">${item.thoiLuong}p</td>
          <td class="py-3 px-4 text-center font-bold text-slate-700">${item.soCauHoi}/5</td>
          <td class="py-3 px-4 text-center">
            ${isGraded ? `<span class="bg-emerald-50 text-emerald-700 text-[10px] px-2 py-0.5 rounded-full font-bold border border-emerald-200">Đã chấm (${item.soBaiCham})</span>` : `<span class="bg-slate-100 text-slate-500 text-[10px] px-2 py-0.5 rounded-full font-medium">Chưa chấm</span>`}
          </td>
          <td class="py-3 px-4 text-center">
            <div class="flex items-center justify-center space-x-1">
              <button onclick="window.uc04.xemChiTietDe('${item.maDe}')" class="p-1 text-indigo-600 hover:text-indigo-800" title="Xem đề"><i class="fa-solid fa-eye text-xs"></i></button>
              ${isGraded ? `
                <button onclick="window.uc02.thongBaoKhoaQD2('${item.maDe}', ${item.soBaiCham})" class="p-1 text-slate-400 hover:text-amber-600"><i class="fa-solid fa-lock text-xs"></i></button>
              ` : `
                <button onclick="window.uc02.openEditModal('${item.maDe}')" class="p-1 text-blue-600 hover:text-blue-800"><i class="fa-solid fa-pen-to-square text-xs"></i></button>
                <button onclick="window.uc02.xacNhanXoa('${item.maDe}')" class="p-1 text-rose-600 hover:text-rose-800"><i class="fa-solid fa-trash-can text-xs"></i></button>
              `}
            </div>
          </td>
        </tr>
      `;
    }).join('');
  }

  async openCreateModal() {
    document.getElementById('modal-dt-title').innerHTML = '<i class="fa-solid fa-plus text-blue-600"></i><span>Tạo đề thi mới</span>';
    document.getElementById('modal-dt-mode').value = 'create';
    document.getElementById('modal-dt-made').value = '';
    document.getElementById('modal-dt-made').removeAttribute('readonly');
    document.getElementById('modal-dt-mon').removeAttribute('disabled');
    document.getElementById('modal-dt-thoiluong').value = '90';
    document.getElementById('modal-dt-hocky').value = 'Học kỳ 1';
    document.getElementById('modal-dt-namhoc').value = '2024-2025';

    const today = new Date().toISOString().split('T')[0];
    document.getElementById('modal-dt-ngaythi').value = today;

    this.cauHoiDaChon.clear();
    this.updateCountPill();

    const selMon = document.getElementById('modal-dt-mon');
    if (selMon && !selMon.value && window.app.monHocs.length > 0) {
      selMon.value = window.app.monHocs[0].maMon;
    }
    await this.onMonChange();

    document.getElementById('modal-dethi').classList.remove('hidden');
  }

  async openEditModal(maDe) {
    try {
      const res = await fetch(`/api/de-thi/${maDe}`);
      const data = await res.json();
      if (!data.success) {
        window.app.toast(data.message, 'error');
        return;
      }

      const item = data.data;
      if (item.daCoKetQuaCham) {
        this.thongBaoKhoaQD2(item.maDe, item.soBaiCham);
        return;
      }

      document.getElementById('modal-dt-title').innerHTML = '<i class="fa-solid fa-pen-to-square text-blue-600"></i><span>Chỉnh sửa đề thi</span>';
      document.getElementById('modal-dt-mode').value = 'edit';
      document.getElementById('modal-dt-made').value = item.maDe;
      document.getElementById('modal-dt-made').setAttribute('readonly', 'true');
      document.getElementById('modal-dt-mon').value = item.maMon;
      document.getElementById('modal-dt-hocky').value = item.hocKy;
      document.getElementById('modal-dt-namhoc').value = item.namHoc;
      document.getElementById('modal-dt-ngaythi').value = item.ngayThi;
      document.getElementById('modal-dt-thoiluong').value = item.thoiLuong;

      this.cauHoiDaChon = new Set(item.cauHois.map(c => c.maCauHoi));
      await this.onMonChange();

      document.getElementById('modal-dethi').classList.remove('hidden');
    } catch (err) {
      window.app.toast('Lỗi mở đề thi: ' + err.message, 'error');
    }
  }

  closeModal() {
    const modal = document.getElementById('modal-dethi');
    if (modal) modal.classList.add('hidden');
  }

  async onMonChange() {
    const maMon = document.getElementById('modal-dt-mon')?.value;
    const container = document.getElementById('modal-dt-questions-list');
    if (!container) return;

    if (!maMon) {
      container.innerHTML = '<div class="text-xs text-slate-400 py-3 text-center">Vui lòng chọn môn thi.</div>';
      return;
    }

    container.innerHTML = '<div class="text-xs text-slate-400 py-3 text-center">Đang tải câu hỏi...</div>';

    try {
      const res = await fetch(`/api/cau-hoi?maMon=${maMon}`);
      const data = await res.json();
      if (data.success) {
        this.cauHoiTheoMon = data.data;
        this.renderQuestionPicker();
      }
    } catch (err) {
      container.innerHTML = '<div class="text-xs text-red-500 py-2">Lỗi: ' + err.message + '</div>';
    }
  }

  renderQuestionPicker() {
    const container = document.getElementById('modal-dt-questions-list');
    if (!container) return;

    if (this.cauHoiTheoMon.length === 0) {
      container.innerHTML = `
        <div class="text-xs text-amber-600 bg-amber-50 p-3 rounded-xl border border-amber-200">
          Chưa có câu hỏi nào thuộc môn này! Hãy chuyển sang <strong>Ngân hàng câu hỏi</strong> để thêm câu hỏi trước.
        </div>
      `;
      this.updateCountPill();
      return;
    }

    container.innerHTML = this.cauHoiTheoMon.map(ch => {
      const isChecked = this.cauHoiDaChon.has(ch.maCauHoi);
      let badgeClass = 'badge-medium';
      if (ch.doKho === 'Dễ') badgeClass = 'badge-easy';
      else if (ch.doKho === 'Phức Tạp') badgeClass = 'badge-complex';
      else if (ch.doKho === 'Khó') badgeClass = 'badge-hard';

      return `
        <label class="flex items-start space-x-2.5 p-2 rounded-xl border transition cursor-pointer ${
          isChecked ? 'bg-blue-50/80 border-blue-300' : 'bg-white border-slate-200 hover:border-slate-300'
        }">
          <input type="checkbox" value="${ch.maCauHoi}" ${isChecked ? 'checked' : ''} onchange="window.uc02.toggleQuestion('${ch.maCauHoi}', this.checked)" class="mt-1 text-blue-600 rounded focus:ring-blue-500">
          <div class="flex-1 text-xs">
            <div class="flex items-center space-x-2 mb-1">
              <span class="font-mono font-bold text-slate-800">${ch.maCauHoi}</span>
              <span class="px-1.5 py-0.2 rounded text-[10px] font-bold ${badgeClass}">${ch.doKho}</span>
            </div>
            <p class="text-slate-600 leading-relaxed">${ch.noiDung}</p>
          </div>
        </label>
      `;
    }).join('');

    this.updateCountPill();
  }

  toggleQuestion(maCauHoi, checked) {
    if (checked) {
      if (this.cauHoiDaChon.size >= 5) {
        window.app.toast('Mỗi đề thi chỉ được chọn tối đa 5 câu hỏi!', 'warning');
        const input = document.querySelector(`input[type="checkbox"][value="${maCauHoi}"]`);
        if (input) input.checked = false;
        return;
      }
      this.cauHoiDaChon.add(maCauHoi);
    } else {
      this.cauHoiDaChon.delete(maCauHoi);
    }
    this.renderQuestionPicker();
  }

  updateCountPill() {
    const pill = document.getElementById('modal-dt-count-pill');
    if (!pill) return;
    const count = this.cauHoiDaChon.size;
    pill.textContent = `Đã chọn: ${count}/5 câu`;

    if (count >= 1 && count <= 5) {
      pill.className = 'text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300';
    } else {
      pill.className = 'text-xs font-bold px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-800 border border-rose-300';
    }
  }

  async submitForm(event) {
    event.preventDefault();
    const mode = document.getElementById('modal-dt-mode').value;
    const maDe = document.getElementById('modal-dt-made').value.trim();
    const maMon = document.getElementById('modal-dt-mon').value;
    const hocKy = document.getElementById('modal-dt-hocky').value;
    const namHoc = document.getElementById('modal-dt-namhoc').value.trim();
    const ngayThi = document.getElementById('modal-dt-ngaythi').value;
    const thoiLuong = Number(document.getElementById('modal-dt-thoiluong').value);
    const danhSachCauHoi = Array.from(this.cauHoiDaChon);

    if (isNaN(thoiLuong) || thoiLuong < 30 || thoiLuong > 180) {
      window.app.toast('Thời lượng thi hợp lệ là từ 30 đến 180 phút!', 'error');
      return;
    }

    if (danhSachCauHoi.length < 1 || danhSachCauHoi.length > 5) {
      window.app.toast(`Đề thi phải có từ 1 đến 5 câu hỏi (hiện tại đã chọn: ${danhSachCauHoi.length} câu)!`, 'error');
      return;
    }

    try {
      let res, result;
      if (mode === 'create') {
        res = await fetch('/api/de-thi', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ maDe, maMon, hocKy, namHoc, ngayThi, thoiLuong, danhSachCauHoi })
        });
      } else {
        res = await fetch(`/api/de-thi/${maDe}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ maMon, hocKy, namHoc, ngayThi, thoiLuong, danhSachCauHoi })
        });
      }

      result = await res.json();
      if (result.success) {
        window.app.toast(result.message, 'success');
        this.closeModal();
        this.taiDanhSach();
        window.app.taiDashboardStats();
      } else {
        window.app.toast(result.message, result.ruleViolated ? 'error' : 'warning');
      }
    } catch (err) {
      window.app.toast('Lỗi lưu đề thi: ' + err.message, 'error');
    }
  }

  xacNhanXoa(maDe) {
    window.app.confirm(
      'Xóa đề thi?',
      `Bạn có chắc chắn muốn xóa đề thi '${maDe}'?`,
      async () => {
        try {
          const res = await fetch(`/api/de-thi/${maDe}`, { method: 'DELETE' });
          const result = await res.json();
          if (result.success) {
            window.app.toast(result.message, 'success');
            this.taiDanhSach();
            window.app.taiDashboardStats();
          } else {
            window.app.toast(result.message, result.ruleViolated ? 'error' : 'warning');
          }
        } catch (err) {
          window.app.toast('Lỗi xóa đề thi: ' + err.message, 'error');
        }
      }
    );
  }

  thongBaoKhoaQD2(maDe, soBai) {
    window.app.toast(
      `Đề thi '${maDe}' đã có kết quả chấm thi (${soBai} bài chấm). Hệ thống khóa chức năng sửa/xóa để bảo toàn kết quả thi của sinh viên!`,
      'error'
    );
  }
}

window.uc02 = new UC02Controller();
