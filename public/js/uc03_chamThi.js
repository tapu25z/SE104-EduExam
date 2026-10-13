/**
 * Controller cho UC03: Ghi nhận chấm thi (BM3, QĐ3)
 * Giao diện trực quan với Avatar sinh viên, vòng tròn điểm chữ A-F
 */

class UC03Controller {
  constructor() {
    this.deThis = [];
    this.sinhViens = [];
    this.currentDe = null;
    this.currentLop = null;
  }

  async khoiTao() {
    await this.taiDanhSachDe();
    this.capNhatSelectLop();
  }

  async taiDanhSachDe() {
    try {
      const res = await fetch('/api/de-thi');
      const data = await res.json();
      if (data.success) {
        this.deThis = data.data;
      }
    } catch (err) {
      console.warn('Lỗi tải danh sách đề thi:', err);
    }
  }

  capNhatSelectLop() {
    const selLop = document.getElementById('ct-select-lop');
    if (!selLop) return;

    const currentVal = selLop.value;
    selLop.innerHTML = '<option value="">-- Chọn lớp học --</option>';

    window.app.lops.forEach(l => {
      const opt = document.createElement('option');
      opt.value = l.maLop;
      opt.textContent = `${l.maLop} - ${l.tenLop}`;
      selLop.appendChild(opt);
    });

    if (currentVal) selLop.value = currentVal;
  }

  onChonMon() {
    const maMon = document.getElementById('ct-select-mon')?.value;
    const selDe = document.getElementById('ct-select-de');
    if (!selDe) return;

    selDe.innerHTML = '<option value="">-- Chọn đề thi --</option>';

    if (!maMon) {
      selDe.setAttribute('disabled', 'true');
      this.clearExamInfo();
      this.taiDanhSachSinhVien();
      return;
    }

    const des = this.deThis.filter(d => d.maMon === maMon);
    if (des.length === 0) {
      selDe.innerHTML = '<option value="">(Chưa có đề thi nào cho môn này)</option>';
      selDe.setAttribute('disabled', 'true');
      this.clearExamInfo();
      this.taiDanhSachSinhVien();
      return;
    }

    des.forEach(d => {
      const opt = document.createElement('option');
      opt.value = d.maDe;
      opt.textContent = `${d.maDe} (${d.hocKy} - ${d.namHoc}, ${d.thoiLuong}p)`;
      selDe.appendChild(opt);
    });

    selDe.removeAttribute('disabled');
    this.clearExamInfo();
    this.taiDanhSachSinhVien();
  }

  onChonDe() {
    const maDe = document.getElementById('ct-select-de')?.value;
    this.currentDe = this.deThis.find(d => d.maDe === maDe) || null;

    const infoBox = document.getElementById('ct-exam-info');
    if (this.currentDe && infoBox) {
      document.getElementById('ct-info-mon').textContent = `Môn: ${this.currentDe.tenMon} (${this.currentDe.maMon})`;
      document.getElementById('ct-info-thoiluong').textContent = `Thời lượng: ${this.currentDe.thoiLuong} phút`;
      document.getElementById('ct-info-ngaythi').textContent = `Ngày thi: ${this.currentDe.ngayThi}`;
      document.getElementById('ct-info-hocky').textContent = `${this.currentDe.hocKy} • ${this.currentDe.namHoc}`;
      infoBox.classList.remove('hidden');
      infoBox.classList.add('flex');
    } else {
      this.clearExamInfo();
    }

    this.taiDanhSachSinhVien();
  }

  clearExamInfo() {
    const infoBox = document.getElementById('ct-exam-info');
    if (infoBox) {
      infoBox.classList.add('hidden');
      infoBox.classList.remove('flex');
    }
    this.currentDe = null;
  }

  async taiDanhSachSinhVien() {
    const maDe = document.getElementById('ct-select-de')?.value;
    const maLop = document.getElementById('ct-select-lop')?.value;
    const tbody = document.getElementById('ct-table-body');
    const countEl = document.getElementById('ct-student-count');
    if (!tbody) return;

    if (!maLop) {
      tbody.innerHTML = `
        <tr>
          <td colspan="7" class="py-12 text-center text-slate-400">
            <div class="w-36 h-28 mx-auto mb-2 opacity-90">
              <img src="assets/illustrations/grading.svg" alt="Grading" class="w-full h-full object-contain">
            </div>
            <p class="text-xs text-slate-500 font-medium">Vui lòng chọn <strong>Lớp học</strong> để hiển thị danh sách sinh viên và sổ điểm.</p>
          </td>
        </tr>
      `;
      if (countEl) countEl.textContent = 'Tổng số sinh viên: 0';
      return;
    }

    tbody.innerHTML = `
      <tr>
        <td colspan="7" class="py-8 text-center text-slate-400">Đang tải danh sách sinh viên lớp ${maLop}...</td>
      </tr>
    `;

    try {
      const url = `/api/cham-thi/sinh-vien-lop?maLop=${maLop}&maDe=${maDe || ''}`;
      const res = await fetch(url);
      const data = await res.json();
      if (data.success) {
        this.sinhViens = data.data.sinhViens;
        this.renderGradingTable();
      } else {
        window.app.toast(data.message, 'error');
      }
    } catch (err) {
      tbody.innerHTML = `<tr><td colspan="7" class="py-4 text-center text-red-500">Lỗi: ${err.message}</td></tr>`;
    }
  }

  getInitials(name) {
    if (!name) return 'SV';
    const parts = name.trim().split(/\s+/);
    if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  getAvatarColor(name) {
    const classes = [
      'avatar-grad-blue',
      'avatar-grad-purple',
      'avatar-grad-emerald',
      'avatar-grad-amber',
      'avatar-grad-rose',
      'avatar-grad-indigo',
      'avatar-grad-teal'
    ];
    let hash = 0;
    for (let i = 0; i < name.length; i++) hash += name.charCodeAt(i);
    return classes[hash % classes.length];
  }

  updateClassProgress() {
    const progressBox = document.getElementById('ct-progress-box');
    if (!progressBox) return;

    if (!this.sinhViens || this.sinhViens.length === 0) {
      progressBox.classList.add('hidden');
      return;
    }

    let gradedCount = 0;
    this.sinhViens.forEach(sv => {
      const input = document.getElementById(`diem-${sv.mssv}`);
      const val = input ? input.value.trim() : (sv.diemSo !== null && sv.diemSo !== undefined ? String(sv.diemSo) : '');
      if (val !== '') gradedCount++;
    });

    const totalCount = this.sinhViens.length;
    const pct = totalCount > 0 ? Math.round((gradedCount / totalCount) * 100) : 0;

    progressBox.innerHTML = `
      <div class="flex items-center justify-between text-xs mb-1.5">
        <span class="font-bold text-slate-700 flex items-center space-x-1.5">
          <i class="fa-solid fa-list-check text-indigo-600"></i>
          <span>Tiến độ vào điểm: <strong>${gradedCount}/${totalCount}</strong> sinh viên</span>
        </span>
        <span class="font-mono font-bold text-xs ${pct === 100 ? 'text-emerald-600' : 'text-indigo-600'}">${pct}%</span>
      </div>
      <div class="liquid-progress-bg h-2.5 w-full">
        <div class="liquid-progress-fill ${pct === 100 ? 'liquid-bar-emerald' : 'liquid-bar-blue'}" style="width: ${pct}%"></div>
      </div>
    `;
    progressBox.classList.remove('hidden');
  }

  renderGradingTable() {
    const tbody = document.getElementById('ct-table-body');
    const countEl = document.getElementById('ct-student-count');
    if (!tbody) return;

    if (this.sinhViens.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="7" class="py-8 text-center text-slate-400">
            Lớp học này chưa có sinh viên nào trong hệ thống.
          </td>
        </tr>
      `;
      if (countEl) countEl.textContent = 'Tổng số sinh viên: 0';
      this.updateClassProgress();
      return;
    }

    if (countEl) countEl.textContent = `Tổng số sinh viên: ${this.sinhViens.length}`;

    tbody.innerHTML = this.sinhViens.map((sv, idx) => {
      const diemVal = sv.diemSo !== null && sv.diemSo !== undefined ? sv.diemSo : '';
      const diemChuVal = sv.diemChu || '';
      const ghiChuVal = sv.ghiChu || '';
      const initials = this.getInitials(sv.hoTen);
      const avatarClass = this.getAvatarColor(sv.hoTen);

      const gradeBadge = diemChuVal
        ? `<span id="grade-badge-${sv.mssv}" class="grade-badge-gem grade-${diemChuVal}">${diemChuVal}</span>`
        : `<span id="grade-badge-${sv.mssv}" class="w-8 h-8 rounded-full border border-dashed border-slate-300 text-slate-300 inline-flex items-center justify-center font-mono text-xs">--</span>`;

      return `
        <tr class="hover:bg-slate-50/80 transition" id="row-${sv.mssv}">
          <td class="py-3 px-4 text-center font-mono text-slate-400">${idx + 1}</td>
          <td class="py-3 px-4 font-mono font-bold text-slate-800">${sv.mssv}</td>
          <td class="py-3 px-4">
            <div class="flex items-center space-x-3">
              <div class="avatar-circle ${avatarClass} shrink-0">${initials}</div>
              <span class="font-bold text-slate-800 text-xs">${sv.hoTen}</span>
            </div>
          </td>
          <td class="py-3 px-4">
            <div class="relative w-32">
              <input type="number" 
                     id="diem-${sv.mssv}" 
                     step="0.5" 
                     min="0" 
                     max="10" 
                     value="${diemVal}" 
                     placeholder="0 - 10"
                     oninput="window.uc03.onDiemChange('${sv.mssv}', this.value)"
                     class="w-full p-2.5 text-xs font-mono font-bold text-slate-800 bg-white/90 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none shadow-2xs">
              <div id="error-${sv.mssv}" class="text-[10px] text-red-600 hidden font-bold mt-0.5">Bội số của 0.5</div>
            </div>
          </td>
          <td class="py-3 px-4 text-center" id="container-grade-${sv.mssv}">
            ${gradeBadge}
          </td>
          <td class="py-3 px-4">
            <input type="text" 
                   id="ghichu-${sv.mssv}" 
                   value="${this.escapeHtml(ghiChuVal)}" 
                   placeholder="Nhận xét bài làm..." 
                   class="w-full p-2.5 text-xs text-slate-700 bg-white/80 border border-slate-200 rounded-xl focus:border-indigo-400 focus:outline-none">
          </td>
          <td class="py-3 px-4 text-center">
            ${diemVal !== '' ? `
              <button onclick="window.uc03.xoaDiemSinhVien('${sv.mssv}')" class="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition" title="Xóa điểm này">
                <i class="fa-solid fa-eraser text-xs"></i>
              </button>
            ` : `
              <span class="text-slate-300 text-xs">-</span>
            `}
          </td>
        </tr>
      `;
    }).join('');

    this.updateClassProgress();
  }

  onDiemChange(mssv, valStr) {
    const input = document.getElementById(`diem-${mssv}`);
    const errBox = document.getElementById(`error-${mssv}`);
    const gradeContainer = document.getElementById(`container-grade-${mssv}`);

    if (!valStr || valStr.trim() === '') {
      input.classList.remove('border-red-500');
      errBox.classList.add('hidden');
      gradeContainer.innerHTML = '<span class="w-8 h-8 rounded-full border border-dashed border-slate-300 text-slate-300 inline-flex items-center justify-center font-mono text-xs">--</span>';
      this.updateClassProgress();
      return;
    }

    const val = Number(valStr);

    const isOutOfRange = isNaN(val) || val < 0 || val > 10;
    const nhanHai = Math.round(val * 10) / 10 * 2;
    const isNotMultiple = Math.abs(nhanHai - Math.round(nhanHai)) > 1e-6;

    if (isOutOfRange || isNotMultiple) {
      input.classList.add('border-red-500', 'bg-red-50/50');
      errBox.classList.remove('hidden');
      errBox.textContent = isOutOfRange ? 'Từ 0 đến 10' : 'Bước điểm 0.5';
      gradeContainer.innerHTML = '<span class="text-red-500 font-bold text-[10px] font-mono">LỖI</span>';
      return;
    }

    input.classList.remove('border-red-500', 'bg-red-50/50');
    errBox.classList.add('hidden');

    let grade = 'F';
    if (val >= 9.0) grade = 'A';
    else if (val >= 8.0) grade = 'B';
    else if (val >= 7.0) grade = 'C';
    else if (val >= 6.0) grade = 'D';
    else if (val >= 5.0) grade = 'E';

    gradeContainer.innerHTML = `<span class="grade-badge-gem grade-${grade}">${grade}</span>`;
    this.updateClassProgress();
  }

  async luuBangDiem() {
    const maDe = document.getElementById('ct-select-de')?.value;
    const maLop = document.getElementById('ct-select-lop')?.value;

    if (!maDe) {
      window.app.toast('Vui lòng chọn Mã đề thi trước khi lưu điểm!', 'warning');
      return;
    }
    if (!maLop) {
      window.app.toast('Vui lòng chọn Lớp học trước khi lưu điểm!', 'warning');
      return;
    }

    const danhSachDiem = [];
    let hasError = false;

    for (const sv of this.sinhViens) {
      const diemInput = document.getElementById(`diem-${sv.mssv}`);
      const ghiChuInput = document.getElementById(`ghichu-${sv.mssv}`);
      const valStr = diemInput ? diemInput.value.trim() : '';

      if (valStr !== '') {
        const val = Number(valStr);
        if (isNaN(val) || val < 0 || val > 10) {
          window.app.toast(`Sinh viên ${sv.mssv}: Điểm phải nằm trong khoảng từ 0 đến 10!`, 'error');
          hasError = true;
          break;
        }
        const nhanHai = Math.round(val * 10) / 10 * 2;
        if (Math.abs(nhanHai - Math.round(nhanHai)) > 1e-6) {
          window.app.toast(`Sinh viên ${sv.mssv}: Điểm ${val} phải là bội số của 0.5 (ví dụ: 7.0, 7.5, 8.0)!`, 'error');
          hasError = true;
          break;
        }

        danhSachDiem.push({
          mssv: sv.mssv,
          diemSo: val,
          ghiChu: ghiChuInput ? ghiChuInput.value.trim() : ''
        });
      }
    }

    if (hasError) return;

    if (danhSachDiem.length === 0) {
      window.app.toast('Chưa có điểm nào được nhập vào bảng!', 'warning');
      return;
    }

    try {
      const res = await fetch('/api/cham-thi/luu', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ maDe, maLop, danhSachDiem })
      });

      const result = await res.json();
      if (result.success) {
        window.app.toast(result.message, 'success');
        await this.taiDanhSachDe();
        await this.taiDanhSachSinhVien();
        window.app.taiDashboardStats();
      } else {
        window.app.toast(result.message, result.ruleViolated ? 'error' : 'warning');
      }
    } catch (err) {
      window.app.toast('Lỗi lưu bảng điểm: ' + err.message, 'error');
    }
  }

  async xoaDiemSinhVien(mssv) {
    const maDe = document.getElementById('ct-select-de')?.value;
    if (!maDe) return;

    window.app.confirm(
      'Xóa điểm sinh viên?',
      `Bạn có chắc muốn xóa điểm của sinh viên ${mssv} trong đề thi ${maDe}?`,
      async () => {
        try {
          const res = await fetch(`/api/cham-thi/${maDe}/${mssv}`, { method: 'DELETE' });
          const result = await res.json();
          if (result.success) {
            window.app.toast(result.message, 'success');
            await this.taiDanhSachDe();
            await this.taiDanhSachSinhVien();
            window.app.taiDashboardStats();
          } else {
            window.app.toast(result.message, 'error');
          }
        } catch (err) {
          window.app.toast('Lỗi xóa điểm: ' + err.message, 'error');
        }
      }
    );
  }

  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

window.uc03 = new UC03Controller();
