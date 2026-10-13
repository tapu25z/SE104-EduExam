/**
 * Controller cho UC05: Lập báo cáo năm học (BM5) & Biểu đồ thống kê
 */

class UC05Controller {
  constructor() {
    this.chartDeThi = null;
    this.chartBaiCham = null;
  }

  async khoiTao() {
    await this.taiDanhSachNam();
    this.lapBaoCao();
  }

  async taiDanhSachNam() {
    const sel = document.getElementById('bc-select-nam');
    if (!sel) return;

    try {
      const res = await fetch('/api/bao-cao/danh-sach-nam');
      const data = await res.json();
      if (data.success && data.data.length > 0) {
        sel.innerHTML = '';
        data.data.forEach((nam, idx) => {
          const opt = document.createElement('option');
          opt.value = nam;
          opt.textContent = nam;
          if (idx === 0) opt.selected = true;
          sel.appendChild(opt);
        });
      }
    } catch (err) {
      console.warn('Lỗi tải danh sách năm:', err);
    }
  }

  async lapBaoCao() {
    const namHoc = document.getElementById('bc-select-nam')?.value;
    if (!namHoc) {
      window.app.toast('Vui lòng chọn năm học!', 'warning');
      return;
    }

    try {
      const res = await fetch(`/api/bao-cao?namHoc=${namHoc}`);
      const data = await res.json();
      if (data.success) {
        this.renderBaoCao(data.data);
      } else {
        window.app.toast(data.message, 'error');
      }
    } catch (err) {
      window.app.toast('Lỗi lập báo cáo: ' + err.message, 'error');
    }
  }

  renderBaoCao(reportData) {
    const { namHoc, tongSoDeThi, tongSoBaiCham, chiTiet } = reportData;

    document.getElementById('bc-table-subtitle').textContent = 
      `Năm học: ${namHoc} • Tổng số đề: ${tongSoDeThi} • Tổng số bài chấm: ${tongSoBaiCham}`;

    const tbody = document.getElementById('bc-table-body');
    if (tbody) {
      tbody.innerHTML = chiTiet.map(item => `
        <tr class="hover:bg-slate-50 transition">
          <td class="py-3 px-4 text-center font-mono text-slate-400">${item.stt}</td>
          <td class="py-3 px-4">
            <span class="font-bold text-slate-800">${item.tenMon}</span>
            <span class="text-[11px] text-slate-400 block font-mono">${item.maMon}</span>
          </td>
          <td class="py-3 px-4 text-center font-bold text-blue-700">${item.soLuongDeThi}</td>
          <td class="py-3 px-4 text-center font-bold text-emerald-700">${item.soLuongBaiCham}</td>
          <td class="py-3 px-4 min-w-[140px]">
            <div class="flex items-center space-x-2">
              <div class="flex-1 liquid-progress-bg h-2.5">
                <div class="liquid-progress-fill liquid-bar-blue" style="width: ${item.tiLeDeThi}%"></div>
              </div>
              <span class="font-mono font-bold text-xs text-blue-700 shrink-0 w-12 text-right">
                ${item.tiLeDeThiText}
              </span>
            </div>
          </td>
          <td class="py-3 px-4 min-w-[140px]">
            <div class="flex items-center space-x-2">
              <div class="flex-1 liquid-progress-bg h-2.5">
                <div class="liquid-progress-fill liquid-bar-emerald" style="width: ${item.tiLeBaiCham}%"></div>
              </div>
              <span class="font-mono font-bold text-xs text-emerald-700 shrink-0 w-12 text-right">
                ${item.tiLeBaiChamText}
              </span>
            </div>
          </td>
        </tr>
      `).join('');
    }

    this.renderCharts(chiTiet);
  }

  renderCharts(chiTiet) {
    const labels = chiTiet.map(c => `${c.maMon}`);
    const dataDeThi = chiTiet.map(c => c.soLuongDeThi);
    const dataBaiCham = chiTiet.map(c => c.soLuongBaiCham);

    const colors = ['#2563eb', '#8b5cf6', '#10b981', '#f59e0b'];

    // 1. Chart Đề thi (Doughnut)
    const ctxDe = document.getElementById('chart-de-thi')?.getContext('2d');
    if (ctxDe) {
      if (this.chartDeThi) this.chartDeThi.destroy();
      this.chartDeThi = new Chart(ctxDe, {
        type: 'doughnut',
        data: {
          labels: chiTiet.map(c => `${c.maMon} (${c.tenMon})`),
          datasets: [{
            data: dataDeThi,
            backgroundColor: colors,
            borderWidth: 3,
            borderColor: '#ffffff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { boxWidth: 12, font: { size: 11, family: 'Plus Jakarta Sans' } }
            }
          }
        }
      });
    }

    // 2. Chart Bài chấm (Bar)
    const ctxBai = document.getElementById('chart-bai-cham')?.getContext('2d');
    if (ctxBai) {
      if (this.chartBaiCham) this.chartBaiCham.destroy();
      this.chartBaiCham = new Chart(ctxBai, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Số lượng bài chấm',
            data: dataBaiCham,
            backgroundColor: '#0d9488',
            borderRadius: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1, font: { size: 11 } }
            },
            x: {
              ticks: { font: { size: 11, weight: 'bold' } }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }
  }
}

window.uc05 = new UC05Controller();
