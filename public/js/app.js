/**
 * EduExam Application Controller
 * Quản lý Navigation, Toast Notifications, Confirm Dialog, Dashboard Data & Thông số Hệ thống
 */

class AppController {
  constructor() {
    this.currentTab = 'dashboard';
    this.monHocs = [];
    this.lops = [];
    this.user = null;
    this.token = localStorage.getItem('eduexam-token') || '';
    const nativeFetch = window.fetch.bind(window);
    window.fetch = (input, init = {}) => {
      const url = typeof input === 'string' ? input : input.url;
      if (!url.startsWith('/api/') || url.startsWith('/api/auth/login')) return nativeFetch(input, init);
      const headers = new Headers(init.headers || (input instanceof Request ? input.headers : undefined));
      if (this.token) headers.set('Authorization', `Bearer ${this.token}`);
      return nativeFetch(input, { ...init, headers }).then(response => {
        if (response.status === 401 && !url.startsWith('/api/auth/')) this.logout();
        return response;
      });
    };
    this.init();
  }

  async init() {
    console.log('🚀 Khởi động hệ thống EduExam...');
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
    if (this.token) {
      const res = await fetch('/api/auth/me');
      const result = await res.json().catch(() => ({}));
      if (result.success) await this.enterApp(result.data);
      else {
        this.token = '';
        localStorage.removeItem('eduexam-token');
        window.location.replace('/login');
      }
    } else {
      window.location.replace('/login');
    }
  }

  showLoginError(msg) {
    const error = document.getElementById('login-error');
    const errorText = document.getElementById('login-error-text');
    if (errorText) errorText.textContent = msg;
    else if (error) error.textContent = msg;
    if (error) {
      error.classList.remove('hidden');
      error.classList.remove('animate-shake');
      void error.offsetWidth;
      error.classList.add('animate-shake');
    }
  }

  hideLoginError() {
    const error = document.getElementById('login-error');
    if (error) error.classList.add('hidden');
  }

  togglePasswordVisibility(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    if (!input) return;
    if (input.type === 'password') {
      input.type = 'text';
      if (icon) {
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
      }
    } else {
      input.type = 'password';
      if (icon) {
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
      }
    }
  }

  switchAuthTab(tab) {
    const formLogin = document.getElementById('form-login');
    const formRegister = document.getElementById('form-register');
    const tabLogin = document.getElementById('auth-tab-login');
    const tabRegister = document.getElementById('auth-tab-register');
    this.hideLoginError();

    if (tab === 'login') {
      if (formLogin) formLogin.classList.remove('hidden');
      if (formRegister) formRegister.classList.add('hidden');
      if (tabLogin) {
        tabLogin.className = 'px-5 py-2 rounded-xl text-xs sm:text-sm font-bold text-slate-900 bg-white shadow-sm transition-all cursor-pointer';
      }
      if (tabRegister) {
        tabRegister.className = 'px-5 py-2 rounded-xl text-xs sm:text-sm font-semibold text-slate-500 hover:text-slate-800 transition-all cursor-pointer';
      }
    } else {
      if (formLogin) formLogin.classList.add('hidden');
      if (formRegister) formRegister.classList.remove('hidden');
      if (tabLogin) {
        tabLogin.className = 'px-5 py-2 rounded-xl text-xs sm:text-sm font-semibold text-slate-500 hover:text-slate-800 transition-all cursor-pointer';
      }
      if (tabRegister) {
        tabRegister.className = 'px-5 py-2 rounded-xl text-xs sm:text-sm font-bold text-slate-900 bg-white shadow-sm transition-all cursor-pointer';
      }
    }
  }

  quickFillDemo(username, password, autoLogin = false) {
    this.switchAuthTab('login');
    const uInput = document.getElementById('login-username');
    const pInput = document.getElementById('login-password');
    if (uInput) uInput.value = username;
    if (pInput) pInput.value = password;
    this.hideLoginError();
    if (autoLogin) {
      this.login({ preventDefault: () => {} });
    }
  }

  showForgotHint() {
    alert('💡 Thông tin đăng nhập thử nghiệm:\n\n• Giảng viên: giangvien (mật khẩu: gv123456)\n• Quản trị viên: admin (mật khẩu: admin123)\n\nNếu quên mật khẩu tài khoản cá nhân, vui lòng liên hệ Ban Quản trị hệ thống (admin) để được cấp lại.');
  }

  async login(event) {
    if (event?.preventDefault) event.preventDefault();
    this.hideLoginError();
    const btn = document.getElementById('login-submit-btn');
    const origHtml = btn ? btn.innerHTML : '';
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span>Đang xác thực...</span> <i class="fa-solid fa-circle-notch fa-spin text-sm"></i>';
    }

    const tenDangNhap = document.getElementById('login-username')?.value?.trim();
    const matKhau = document.getElementById('login-password')?.value;

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tenDangNhap, matKhau })
      });
      const result = await res.json();
      if (!result.success) {
        this.showLoginError(result.message || 'Tên đăng nhập hoặc mật khẩu không đúng.');
        if (btn) { btn.disabled = false; btn.innerHTML = origHtml; }
        return;
      }
      this.token = result.token;
      localStorage.setItem('eduexam-token', this.token);
      this.toast(`Đăng nhập thành công! Chào mừng ${result.user.hoTen}`, 'success');
      await this.enterApp(result.user);
    } catch (_err) {
      this.showLoginError('Không kết nối được máy chủ.');
      if (btn) { btn.disabled = false; btn.innerHTML = origHtml; }
    }
  }

  async register(event) {
    if (event?.preventDefault) event.preventDefault();
    this.hideLoginError();
    const btn = document.getElementById('register-submit-btn');
    const origHtml = btn ? btn.innerHTML : '';
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span>Đang tạo tài khoản...</span> <i class="fa-solid fa-circle-notch fa-spin text-sm"></i>';
    }

    const hoTen = document.getElementById('reg-fullname')?.value?.trim();
    const tenDangNhap = document.getElementById('reg-username')?.value?.trim();
    const matKhau = document.getElementById('reg-password')?.value;

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hoTen, tenDangNhap, matKhau })
      });
      const result = await res.json();
      if (!result.success) {
        this.showLoginError(result.message || 'Không thể tạo tài khoản.');
        if (btn) { btn.disabled = false; btn.innerHTML = origHtml; }
        return;
      }
      this.token = result.token;
      localStorage.setItem('eduexam-token', this.token);
      this.toast(`Tạo tài khoản thành công! Chào mừng ${result.user.hoTen}`, 'success');
      await this.enterApp(result.user);
    } catch (_err) {
      this.showLoginError('Không thể kết nối đến máy chủ.');
      if (btn) { btn.disabled = false; btn.innerHTML = origHtml; }
    }
  }

  async enterApp(user) {
    this.user = user;
    const cleanName = (user.hoTen || '').replace(/\s*demo\s*/gi, '').trim() || (user.vaiTro === 'admin' ? 'Quản trị viên' : 'Giảng viên');
    document.getElementById('login-screen').classList.add('hidden');
    document.getElementById('user-name').textContent = cleanName;
    const dashboardName = document.getElementById('dashboard-name');
    if (dashboardName) dashboardName.textContent = cleanName;
    const title = document.getElementById('topbar-title');
    if (title) title.textContent = 'Tổng quan';
    document.querySelectorAll('.mobile-bottom-nav button[data-tab]').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === 'dashboard'));
    document.getElementById('user-role').textContent = user.vaiTro === 'admin' ? 'Quản trị viên' : 'Giảng viên';
    document.querySelectorAll('[data-admin-only]').forEach(el => el.classList.toggle('hidden', user.vaiTro !== 'admin'));
    await this.taiMetadata();
    await this.taiDashboardStats();
  }

  async logout() {
    try { await fetch('/api/auth/logout', {method:'POST'}); } catch (_err) {}
    this.token = '';
    this.user = null;
    localStorage.removeItem('eduexam-token');
    window.location.href = '/login';
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
      document.getElementById('ct-select-mon'),
      document.getElementById('tc-mon')
    ];

    selects.forEach(sel => {
      if (!sel) return;
      const isFilter = sel.id.includes('filter') || sel.id === 'tc-mon';
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
    document.getElementById('mobile-more-menu')?.classList.add('hidden');
    if (tabName === 'taikhoan' && this.user?.vaiTro !== 'admin') return this.toast('Chỉ quản trị viên được quản lý tài khoản.', 'error');
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
    document.querySelectorAll('.mobile-bottom-nav button[data-tab]').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tabName));

    // Cập nhật tiêu đề Topbar
    const titles = {
      'dashboard': 'Tổng quan',
      'cauhoi': 'Câu hỏi',
      'dethi': 'Đề thi',
      'chamthi': 'Chấm thi',
      'tracuu': 'Tra cứu đề thi',
      'lophoc': 'Lớp học',
      'taikhoan': 'Tài khoản',
      'baocao': 'Báo cáo'
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
    } else if (tabName === 'tracuu') {
      window.uc04?.khoiTao();
    } else if (tabName === 'lophoc') {
      window.uc07?.load();
    } else if (tabName === 'taikhoan' && this.user?.vaiTro === 'admin') {
      window.uc06?.load();
    } else if (tabName === 'baocao') {
      window.uc05?.khoiTao();
    }
  }

  toggleMobileMenu() {
    const menu = document.getElementById('mobile-more-menu');
    if (menu) menu.classList.toggle('hidden');
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
    this.toast('Dữ liệu được phân lập theo tài khoản; chức năng đặt lại toàn bộ dữ liệu đã tắt để tránh xóa dữ liệu của giảng viên khác.', 'info');
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
