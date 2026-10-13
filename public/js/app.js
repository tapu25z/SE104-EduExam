/**
 * EduExam Application Controller
 * Quản lý Navigation, Toast Notifications, Confirm Dialog, Dashboard Data & Hồ sơ Đồ án SE104
 */

class AppController {
  constructor() {
    this.currentTab = 'dashboard';
    this.monHocs = [];
    this.lops = [];
    this.init();
  }

  async init() {
    console.log('🚀 Khởi động hệ thống EduExam...');
    await this.taiMetadata();
    await this.taiDashboardStats();

    // Lắng nghe phím ESC để đóng modal
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        window.uc01?.closeModal();
        window.uc02?.closeModal();
        window.uc04?.closePreviewModal();
        this.closeDiagramModal();
        this.closeProjectSpecModal();
        this.closeConfirmModal();
      }
    });
  }

  async taiMetadata() {
    try {
      const resMon = await fetch('/api/metadata/mon-hoc');
      const dataMon = await resMon.json();
      if (dataMon.success) {
        this.monHocs = dataMon.data;
        this.capNhatSelectMonHoc();
      }

      const resLop = await fetch('/api/metadata/lop');
      const dataLop = await resLop.json();
      if (dataLop.success) {
        this.lops = dataLop.data;
      }
    } catch (err) {
      this.toast('Không thể tải dữ liệu danh mục: ' + err.message, 'error');
    }
  }

  capNhatSelectMonHoc() {
    const selects = [
      document.getElementById('ch-filter-mon'),
      document.getElementById('modal-ch-mon'),
      document.getElementById('modal-dt-mon'),
      document.getElementById('ct-select-mon')
    ];

    selects.forEach(sel => {
      if (!sel) return;
      const isFilter = sel.id.includes('filter');
      const currentVal = sel.value;
      sel.innerHTML = isFilter ? '<option value="">Tất cả môn học</option>' : '<option value="">-- Chọn môn học --</option>';

      this.monHocs.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m.maMon;
        opt.textContent = `${m.maMon} - ${m.tenMon}`;
        sel.appendChild(opt);
      });

      if (currentVal) sel.value = currentVal;
    });
  }

  switchTab(tabName) {
    this.currentTab = tabName;

    // Cập nhật sidebar active item
    document.querySelectorAll('.nav-item').forEach(btn => {
      const isTarget = btn.getAttribute('data-tab') === tabName;
      if (isTarget) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // Cập nhật tiêu đề Topbar
    const titles = {
      'dashboard': 'Tổng quan hệ thống',
      'cauhoi': 'Ngân hàng câu hỏi',
      'dethi': 'Quản lý đề thi',
      'chamthi': 'Chấm điểm & Sổ điểm',
      'baocao': 'Thống kê & Báo cáo khảo thí'
    };
    const titleEl = document.getElementById('topbar-title');
    if (titleEl) {
      titleEl.textContent = titles[tabName] || 'Hệ thống Khảo thí';
    }

    // Ẩn tất cả views và mở view mục tiêu
    document.querySelectorAll('.tab-view').forEach(view => {
      view.classList.add('hidden');
    });

    const targetView = document.getElementById(`view-${tabName}`);
    if (targetView) {
      targetView.classList.remove('hidden');
    }

    if (tabName === 'dashboard') {
      this.taiDashboardStats();
    } else if (tabName === 'cauhoi') {
      window.uc01?.taiDanhSach();
    } else if (tabName === 'dethi') {
      window.uc02?.taiDanhSach();
    } else if (tabName === 'chamthi') {
      window.uc03?.khoiTao();
    } else if (tabName === 'baocao') {
      window.uc05?.khoiTao();
    }
  }

  async taiDashboardStats() {
    try {
      const res = await fetch('/api/metadata/thong-ke-dashboard');
      const data = await res.json();
      if (data.success) {
        const d = data.data;
        document.getElementById('dash-cauhoi').textContent = d.tongCauHoi || 0;
        document.getElementById('dash-dethi').textContent = d.tongDeThi || 0;
        document.getElementById('dash-baicham').textContent = d.tongBaiCham || 0;
        document.getElementById('dash-sinhvien').textContent = d.tongSinhVien || 0;
      }

      // Đếm số lượng theo môn học
      const resCh = await fetch('/api/cau-hoi');
      const dataCh = await resCh.json();
      const resDt = await fetch('/api/de-thi');
      const dataDt = await resDt.json();

      if (dataCh.success && dataDt.success) {
        const chList = dataCh.data;
        const dtList = dataDt.data;

        ['IT001', 'IT002', 'IT003', 'SE104'].forEach(maMon => {
          const countCh = chList.filter(c => c.maMon === maMon).length;
          const countDt = dtList.filter(d => d.maMon === maMon).length;
          const el = document.getElementById(`dash-count-${maMon.toLowerCase()}`);
          if (el) el.textContent = `${countCh} câu hỏi • ${countDt} đề`;
        });
      }
    } catch (err) {
      console.warn('Lỗi tải thống kê dashboard:', err);
    }
  }

  locTheoMon(maMon) {
    this.switchTab('cauhoi');
    setTimeout(() => {
      const sel = document.getElementById('ch-filter-mon');
      if (sel) {
        sel.value = maMon;
        window.uc01?.taiDanhSach();
      }
    }, 120);
  }

  openQuickCreate() {
    if (this.currentTab === 'dethi') {
      window.uc02?.openCreateModal();
    } else {
      window.uc01?.openCreateModal();
    }
  }

  openProjectSpecModal() {
    const modal = document.getElementById('modal-project-spec');
    if (modal) modal.classList.remove('hidden');
  }

  closeProjectSpecModal() {
    const modal = document.getElementById('modal-project-spec');
    if (modal) modal.classList.add('hidden');
  }

  openDiagramModal(diagKey = 'erd') {
    const modal = document.getElementById('modal-diagram-viewer');
    if (!modal) return;

    const diagrams = {
      'erd': {
        src: 'assets/diagrams/erd.png',
        title: 'Biểu đồ Thực thể Liên kết (ERD - Hình 2.18)',
        caption: 'Mô hình dữ liệu quan hệ 7 bảng (MonHoc, CauHoi, DeThi, DeThi_CauHoi, Lop, SinhVien, KetQuaThi)'
      },
      'class-diagram': {
        src: 'assets/diagrams/class-diagram.png',
        title: 'Biểu đồ Lớp Phân Tích (Hình 2.17)',
        caption: 'Biểu đồ lớp phân tích bài toán Quản lý ra đề và chấm thi'
      },
      'usecase-overview': {
        src: 'assets/diagrams/usecase-overview.png',
        title: 'Biểu đồ Use Case Tổng Quan (Hình 2.1)',
        caption: '5 Use Case chức năng phục vụ Giảng viên'
      }
    };

    const target = diagrams[diagKey] || diagrams['erd'];
    document.getElementById('modal-diag-img').src = target.src;
    document.getElementById('modal-diag-title').textContent = target.title;
    document.getElementById('modal-diag-caption').textContent = target.caption;

    modal.classList.remove('hidden');
  }

  closeDiagramModal() {
    const modal = document.getElementById('modal-diagram-viewer');
    if (modal) modal.classList.add('hidden');
  }

  async resetSampleData() {
    this.confirm(
      'Khôi phục dữ liệu mẫu?',
      'Hệ thống sẽ tải lại dữ liệu mẫu chuẩn (môn học, ngân hàng câu hỏi, đề thi và bảng điểm).',
      async () => {
        try {
          const res = await fetch('/api/metadata/reset-data', { method: 'POST' });
          const result = await res.json();
          if (result.success) {
            this.toast(result.message, 'success');
            await this.taiMetadata();
            this.switchTab(this.currentTab);
          } else {
            this.toast('Lỗi: ' + result.message, 'error');
          }
        } catch (err) {
          this.toast('Không thể nạp lại dữ liệu: ' + err.message, 'error');
        }
      }
    );
  }

  toast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');

    const config = {
      success: { bg: 'bg-emerald-600', icon: 'fa-circle-check', title: 'Thành công' },
      error: { bg: 'bg-rose-600', icon: 'fa-circle-exmark', title: 'Thông báo' },
      warning: { bg: 'bg-amber-600', icon: 'fa-triangle-exclamation', title: 'Lưu ý' },
      info: { bg: 'bg-blue-600', icon: 'fa-circle-info', title: 'Thông báo' }
    }[type] || { bg: 'bg-slate-700', icon: 'fa-bell', title: 'Thông báo' };

    toast.className = `toast ${config.bg} text-white px-4 py-3 rounded-2xl shadow-xl flex items-start space-x-3 text-xs border border-white/20`;
    toast.innerHTML = `
      <div class="text-sm mt-0.5"><i class="fa-solid ${config.icon}"></i></div>
      <div class="flex-1">
        <div class="font-bold mb-0.5">${config.title}</div>
        <div class="leading-relaxed opacity-95">${message}</div>
      </div>
      <button onclick="this.parentElement.remove()" class="text-white/70 hover:text-white text-xs ml-2">
        <i class="fa-solid fa-xmark"></i>
      </button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-10px)';
      setTimeout(() => toast.remove(), 250);
    }, 4000);
  }

  confirm(title, message, onConfirm) {
    const modal = document.getElementById('modal-confirm');
    document.getElementById('modal-confirm-title').textContent = title;
    document.getElementById('modal-confirm-message').textContent = message;

    const btnOk = document.getElementById('modal-confirm-ok');
    const btnCancel = document.getElementById('modal-confirm-cancel');

    const newBtnOk = btnOk.cloneNode(true);
    const newBtnCancel = btnCancel.cloneNode(true);
    btnOk.parentNode.replaceChild(newBtnOk, btnOk);
    btnCancel.parentNode.replaceChild(newBtnCancel, btnCancel);

    newBtnOk.onclick = () => {
      modal.classList.add('hidden');
      if (onConfirm) onConfirm();
    };

    newBtnCancel.onclick = () => {
      modal.classList.add('hidden');
    };

    modal.classList.remove('hidden');
  }

  closeConfirmModal() {
    const modal = document.getElementById('modal-confirm');
    if (modal) modal.classList.add('hidden');
  }
}

window.app = new AppController();
