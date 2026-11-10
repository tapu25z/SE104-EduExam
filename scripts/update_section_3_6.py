import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

DOC_PATH = "Đồ án/report--fifi.docx"
IMG_DIR = "Đồ án/rendered_images"

print(f"Loading document: {DOC_PATH}...")
doc = docx.Document(DOC_PATH)

body = doc._body._body
elements = list(body)

# Find start of section 3.6
p_start_idx = None
for idx, el in enumerate(elements):
    if el.tag.endswith('p'):
        p = docx.text.paragraph.Paragraph(el, doc)
        if p.text.strip().startswith("3.6.") and "Thiết kế giao diện" in p.text:
            p_start_idx = idx
            break

if p_start_idx is None:
    raise ValueError("Could not find section 3.6 in document!")

print(f"Found section 3.6 at body index {p_start_idx} (out of {len(elements)} elements).")

# Remove all elements from p_start_idx to end, except sectPr
to_remove = [el for el in elements[p_start_idx:] if not el.tag.endswith('sectPr')]
print(f"Removing {len(to_remove)} old elements of section 3.6...")
for el in to_remove:
    body.remove(el)

print(f"Body elements after removal: {len(list(body))}. Appending updated Section 3.6 with Home Screen & Direct Object Names...")

# Helper functions matching university guidelines
def add_p(text="", style='normal', bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=3, space_after=6):
    p = doc.add_paragraph(style=style)
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.bold = bold
        run.italic = italic
    return p

def add_h2(text):
    p = doc.add_paragraph(style='Heading 2')
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.bold = True
    return p

def add_h3(text):
    p = doc.add_paragraph(style='Heading 3')
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.bold = True
    return p

def add_h4(text):
    p = doc.add_paragraph(style='Heading 4')
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.bold = True
    run.italic = True
    return p

def add_img(img_name, caption_text, width_in=6.0):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(3)
    
    img_path = os.path.join(IMG_DIR, img_name)
    if os.path.exists(img_path):
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_in))
    else:
        print(f"WARNING: Image not found: {img_path}")
        
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    p_cap.paragraph_format.keep_with_next = True
    
    parts = caption_text.split(" ", 2)
    r1 = p_cap.add_run(f"{parts[0]} {parts[1]} ")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    r1.bold = True
    
    r2 = p_cap.add_run(parts[2] if len(parts) > 2 else "")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    r2.italic = True

def add_table_title(title_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    parts = title_text.split(" ", 2)
    r1 = p.add_run(f"{parts[0]} {parts[1]} ")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    r1.bold = True
    r2 = p.add_run(parts[2] if len(parts) > 2 else "")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)

def style_cell(cell, text="", bold=False, italic=False, font_size=11, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=None):
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2.5)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.1
    for r in p.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(font_size)
        r.bold = bold
        r.italic = italic
        
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}>\n'
                          f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                          f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                          f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                          f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                          f'</w:tcBorders>')
    tcPr.append(tcBorders)
    if bg_color:
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        tcPr.append(shd)

def create_styled_table(headers, rows_data, col_widths, align_cols=None):
    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Table borders & layout
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>\n'
                        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>\n'
                        f'</w:tblBorders>')
    tblPr.append(borders)
    
    # Header row
    for col_idx, header in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.width = col_widths[col_idx]
        style_cell(cell, header, bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="DCEAF7")
        
    # Data rows
    for row_idx, row_data in enumerate(rows_data):
        for col_idx, val in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.width = col_widths[col_idx]
            align = WD_ALIGN_PARAGRAPH.LEFT
            if align_cols and col_idx in align_cols:
                align = align_cols[col_idx]
            style_cell(cell, str(val), bold=False, font_size=10.5, align=align)
            
    # cantSplit & tblHeader
    for r in table.rows:
        trPr = r._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    header_trPr = table.rows[0]._tr.get_or_add_trPr()
    header_trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)
    return table

# ==============================================================================
# 3.6. THIẾT KẾ GIAO DIỆN
# ==============================================================================
add_h2("3.6. Thiết kế giao diện")

add_p("Giao diện người dùng của hệ thống Quản lý ra đề và chấm thi (EduExam) được thiết kế hiện đại, tối ưu hóa trải nghiệm sử dụng (UX/UI) theo mô hình ứng dụng web trang đơn đáp ứng (Responsive Single Page Application - SPA) kết hợp cổng thông tin Trang chủ (Landing Page) và mô-đun xác thực đa trang độc lập. Hệ thống xây dựng trên nền tảng HTML5, Tailwind CSS và Bootstrap 5 kết hợp JavaScript thuần hướng đối tượng, mang lại tốc độ phản hồi tức thì, mượt mà và không gây gián đoạn tải trang.")

add_p("Về ngôn ngữ thị giác, giao diện lấy tông màu xanh chàm học thuật (#4f46e5 / #3b82f6) làm sắc màu định danh chủ đạo kết hợp trên nền xám sáng thanh lịch (#f8fafc) và các thẻ bề mặt màu trắng tinh khiết (#ffffff). Bố cục giao diện phân định trực quan 3 vùng chức năng cốt lõi: Thanh điều hướng bên trái (Sidebar Navigation) phân cấp rõ ràng các phân hệ; Thanh tác vụ trên cùng (Header Actions) hiển thị thương hiệu, vai trò người dùng và lối thoát tài khoản; cùng Vùng làm việc trung tâm (Workspace Area) tập trung vào các bảng dữ liệu, biểu mẫu nghiệp vụ và đồ thị trực quan.")

add_p("Hệ thống tuân thủ chặt chẽ nguyên tắc phân lập dữ liệu học thuật riêng biệt cho từng tài khoản giảng viên và phân định quyền quản trị hệ thống rõ ràng cho Quản trị viên (Admin). Ngoài ra, giao diện được tối ưu đáp ứng hoàn hảo trên thiết bị di động (hệ thống tự động chuyển đổi thanh Sidebar thành thanh tác vụ đáy Bottom Navigation tiện lợi), tích hợp hệ thống thông báo trạng thái tức thời (Toast Notifications) và hộp thoại xác nhận an toàn (Confirm Dialog) nhằm triệt để ngăn ngừa sai sót khi xóa dữ liệu quan trọng.")

# 3.6.1 Sơ đồ liên kết các màn hình
add_h3("3.6.1. Sơ đồ liên kết các màn hình")

add_p("Sơ đồ liên kết các màn hình phản ánh toàn diện cấu trúc luồng di chuyển, các bước điều hướng và mối liên hệ nghiệp vụ chặt chẽ giữa các thành phần giao diện trong hệ thống EduExam. Toàn bộ luồng trải nghiệm người dùng được cấu trúc mạch lạc thành các luồng tương tác chính:")

add_p("1. Luồng tiếp cận & Cổng thông tin ban đầu: Người dùng khi truy cập địa chỉ gốc của hệ thống sẽ tiếp cận Màn hình Trang chủ (MH00). Trang chủ cung cấp cái nhìn tổng quan về nền tảng EduExam, các giải pháp số hóa khảo thí, công cụ quy đổi điểm tương tác và các nút điều hướng chuyển tiếp sang Màn hình Đăng nhập (MH01) hoặc Đăng ký tài khoản.")

add_p("2. Luồng xác thực tài khoản: Tại Màn hình Đăng nhập (MH01 - UC00), người dùng thực hiện đăng nhập danh tính. Sau khi hệ thống xác thực thành công qua API bảo mật, hệ thống sẽ lưu trữ phiên làm việc an toàn (Token) và điều hướng tự động vào Màn hình Tổng quan / Dashboard (MH02). Tại MH01, giảng viên chưa có tài khoản cũng có thể chuyển sang Tab Đăng ký để tự tạo tài khoản giảng viên mới.")

add_p("3. Luồng điều hướng giảng viên qua Dashboard: Màn hình Tổng quan (MH02) đóng vai trò là trạm trung chuyển (Navigation Hub). Từ thanh điều hướng Sidebar cũng như từ các thẻ chỉ số KPI và danh mục lối tắt trên Dashboard, Giảng viên có thể chuyển tiếp trực tiếp đến 6 màn hình nghiệp vụ chuyên môn gồm: Ngân hàng câu hỏi (MH03), Soạn đề thi (MH04), Ghi nhận chấm thi (MH05), Tra cứu đề thi (MH06), Báo cáo năm (MH07), và Quản lý lớp học (MH08).")

add_p("4. Luồng liên kết nghiệp vụ sâu giữa các phân hệ (Deep Navigation Actions):")
add_p("• Từ MH04 (Soạn đề thi) và MH06 (Tra cứu đề thi): Giảng viên có thể nhấn nút tác vụ \"Chấm thi ngay\" trên từng đề thi cụ thể để hệ thống lập tức chuyển thẳng sang MH05 (Ghi nhận chấm thi) với thông tin môn thi và đề thi đã được chọn sẵn tự động, rút ngắn thao tác và hạn chế chọn nhầm.")
add_p("• Từ MH06 (Tra cứu đề thi): Giảng viên nhấn nút \"Xem chi tiết\" để mở Hộp thoại Modal bản in đề thi chuẩn (BM4) hỗ trợ in trực tiếp ra giấy qua lệnh in trình duyệt.")
add_p("• Từ MH03 (Ngân hàng câu hỏi) và MH08 (Quản lý lớp học): Giảng viên mở các Hộp thoại Modal chuyên dụng để biên soạn câu hỏi (BM1) hoặc cập nhật danh sách sinh viên theo lớp (BM7).")

add_p("5. Luồng phân quyền Quản trị viên: Đối với tài khoản có vai trò Quản trị viên (Admin), thanh Sidebar và Dashboard sẽ hiển thị thêm mục Quản lý tài khoản (MH09 - UC06), cho phép quản lý hồ sơ, cấp phát, khóa/mở khóa tài khoản giảng viên toàn trường.")

add_p("6. Luồng đăng xuất: Tại bất kỳ màn hình nào trong khu vực làm việc SPA, người dùng có thể kích hoạt nút \"Đăng xuất\" trên thanh tiêu đề để hủy Token phiên làm việc và trở về màn hình Đăng nhập (MH01) hoặc Trang chủ (MH00).")

add_img("screen_00_navigation.png", "Hình 3.3. Sơ đồ liên kết các màn hình hệ thống EduExam", width_in=6.2)

# 3.6.2 Danh sách các màn hình
add_h3("3.6.2. Danh sách các màn hình")
add_p("Hệ thống EduExam được thiết kế gồm 10 màn hình chức năng chính như được tổng hợp trong Bảng 3.12 dưới đây:")

add_table_title("Bảng 3.12 Danh sách các màn hình giao diện hệ thống EduExam")
screens_headers = ["STT", "Mã MH", "Tên màn hình", "Loại màn hình", "Chức năng nghiệp vụ chính", "Mã UC"]
screens_widths = [Inches(0.45), Inches(0.65), Inches(1.3), Inches(1.1), Inches(2.2), Inches(0.5)]
screens_data = [
    ["1", "MH00", "Màn hình Trang chủ", "Cổng thông tin (Landing Page)", "Giới thiệu nền tảng EduExam, các tính năng nổi bật, công cụ quy đổi điểm tương tác và các nút dẫn đến đăng nhập/đăng ký.", "N/A"],
    ["2", "MH01", "Màn hình Đăng nhập", "Biểu mẫu xác thực (Auth Form)", "Xác thực danh tính tài khoản, phân quyền Giảng viên / Quản trị viên, chuyển đổi tab đăng ký tài khoản mới.", "UC00"],
    ["3", "MH02", "Màn hình Tổng quan", "Bảng điều khiển (Dashboard)", "Tổng hợp 4 chỉ số KPI quan trọng, biểu đồ phân bố ngân hàng đề 4 môn học, cung cấp lối tắt điều hướng.", "N/A"],
    ["4", "MH03", "Màn hình Quản lý câu hỏi", "Danh sách & Modal (BM1)", "Tìm kiếm, lọc câu hỏi theo môn và độ khó, xem dạng lưới/bảng; thêm/sửa/xóa câu hỏi kèm đáp án chuẩn (QĐ1).", "UC01"],
    ["5", "MH04", "Màn hình Soạn đề thi", "Danh sách & Modal (BM2)", "Biên soạn đề thi, chọn 1–5 câu cùng môn, gán điểm từng câu đảm bảo tổng bằng 10, thời lượng 30–180 phút (QĐ2).", "UC02"],
    ["6", "MH05", "Màn hình Ghi nhận chấm thi", "Biểu mẫu & Bảng nhập tương tác", "Chọn môn, đề thi, lớp học (BM3); bảng nhập điểm sinh viên bước nhảy 0.5, tự động đổi điểm chữ A–F (QĐ3).", "UC03"],
    ["7", "MH06", "Màn hình Tra cứu đề thi", "Bộ lọc & Bảng kết quả (BM4)", "Tra cứu đề thi đa tiêu chí theo từ khóa, môn, kỳ, năm; xem bản in đề thi chuẩn và chuyển nhanh sang chấm thi.", "UC04"],
    ["8", "MH07", "Màn hình Báo cáo năm", "Biểu đồ & Bảng tổng hợp (BM5)", "Lập báo cáo năm học, vẽ 2 biểu đồ cột so sánh đề thi và bài chấm giữa các môn, tính tỷ lệ % chuẩn (1.1, 1.2).", "UC05"],
    ["9", "MH08", "Màn hình Quản lý lớp học", "Danh sách thẻ & Modal (BM7)", "Quản lý danh sách lớp học phụ trách, xem và cập nhật danh sách sinh viên lớp, bảo vệ dữ liệu đã chấm (QĐ5).", "UC07"],
    ["10", "MH09", "Màn hình Quản lý tài khoản", "Bảng dữ liệu & Modal (BM6)", "Dành riêng cho Quản trị viên: quản lý danh sách tài khoản giảng viên, cấp mới, khóa/mở khóa và đặt lại mật khẩu.", "UC06"]
]
create_styled_table(screens_headers, screens_data, screens_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 1: WD_ALIGN_PARAGRAPH.CENTER, 5: WD_ALIGN_PARAGRAPH.CENTER})

# 3.6.3 Mô tả chi tiết các màn hình
add_h3("3.6.3. Mô tả chi tiết các màn hình")
add_p("Phần này trình bày đặc tả chi tiết về bố cục không gian giao diện, bảng danh mục các đối tượng trên màn hình (được định danh trực tiếp bằng tên tiếng Việt rõ ràng) và bảng danh mục các biến cố kèm quy trình xử lý tương ứng của toàn bộ 10 màn hình trong hệ thống.")

# ------------------------------------------------------------------------------
# 3.6.3.1. MH00 - Màn hình Trang chủ
# ------------------------------------------------------------------------------
add_h4("3.6.3.1. Màn hình Trang chủ (MH00 - Landing Page)")
add_p("a. Giao diện")
add_p("Màn hình Trang chủ là cổng thông tin tiếp đón người dùng và giới thiệu giải pháp tổng thể EduExam. Phần Header bố trí thanh điều hướng dính (Sticky Navbar) với logo thương hiệu, các liên kết cuộn trang nhanh (Tính năng, Giải pháp, Trải nghiệm, Hỗ trợ) và hai nút thao tác Đăng nhập, Đăng ký. Phần Hero Section nổi bật với thông điệp định vị giá trị, nút hành động chính \"Bắt đầu ngay\", nút \"Khám phá tính năng\", cùng khung xem trước giao diện ứng dụng số hóa. Bên dưới là khu vực giới thiệu 4 giải pháp trụ cột và công cụ tương tác mô phỏng quy đổi thang điểm chữ (A, B, C, D, E, F) tức thì theo quy chế đào tạo.")
add_img("screen_00_home.png", "Hình 3.4. Giao diện Màn hình Trang chủ (MH00)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.13 Danh sách các đối tượng trên Màn hình Trang chủ")
obj_headers = ["STT", "Tên đối tượng", "Kiểu đối tượng", "Ràng buộc / Miền giá trị", "Chức năng / Diễn giải nghiệp vụ"]
obj_widths = [Inches(0.45), Inches(1.4), Inches(1.1), Inches(1.3), Inches(1.95)]
mh00_objs = [
    ["1", "Logo EduExam", "Image / Link", "Tệp ảnh logo hệ thống", "Hiển thị biểu trưng thương hiệu; click để cuộn về đầu trang chủ."],
    ["2", "Liên kết Tính năng", "Nav Link", "N/A", "Cuộn trang mượt đến phần giới thiệu các tính năng khảo thí."],
    ["3", "Liên kết Giải pháp", "Nav Link", "N/A", "Cuộn trang đến phần giải pháp số hóa quy trình ra đề & chấm thi."],
    ["4", "Liên kết Trải nghiệm", "Nav Link", "N/A", "Cuộn trang đến khu vực công cụ thử nghiệm quy đổi điểm số."],
    ["5", "Liên kết Hỗ trợ", "Nav Link", "N/A", "Cuộn trang đến chân trang chứa thông tin liên hệ và trợ giúp."],
    ["6", "Nút Đăng nhập (Header)", "Button / Link", "N/A", "Chuyển hướng người dùng sang Màn hình Đăng nhập (MH01)."],
    ["7", "Nút Đăng ký (Header)", "Button / Link", "N/A", "Chuyển hướng sang MH01 và tự động mở Tab Đăng ký tài khoản."],
    ["8", "Nút Bắt đầu ngay (Hero CTA)", "Action Button", "N/A", "Kiểm tra phiên đăng nhập: nếu đã có phiên thì vào thẳng Dashboard, nếu chưa thì mở Đăng nhập."],
    ["9", "Nút Khám phá tính năng", "Button / Link", "N/A", "Cuộn trang nhanh xuống khu vực trải nghiệm công cụ."],
    ["10", "Khung xem trước ứng dụng", "Interactive Mockup", "Hình ảnh / Giao diện mẫu", "Mô phỏng trực quan không gian làm việc số và các số liệu mẫu."],
    ["11", "Thanh trượt điểm số mô phỏng", "Range Slider", "Thực: 0.0 đến 10.0", "Cho phép người dùng kéo thử điểm số để xem quy đổi điểm chữ tức thì."],
    ["12", "Huy hiệu Điểm chữ tương tác", "Badge / Text", "A, B, C, D, E, F", "Hiển thị điểm chữ tương ứng theo đúng quy tắc QĐ3 khi kéo thanh trượt."]
]
create_styled_table(obj_headers, mh00_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.14 Danh sách các biến cố và xử lý trên Màn hình Trang chủ")
evt_headers = ["STT", "Tên biến cố / Thao tác người dùng", "Quy trình xử lý tương ứng của hệ thống"]
evt_widths = [Inches(0.45), Inches(1.8), Inches(3.95)]
mh00_evts = [
    ["1", "Khởi tạo Trang chủ (Page Load)", "Kiểm tra trạng thái phiên làm việc trong localStorage. Nếu người dùng đã đăng nhập từ trước, tự động chuyển đổi nút \"Đăng nhập\" trên Header thành \"Vào ứng dụng\" và đổi nút CTA thành \"Tiếp tục làm việc\"."],
    ["2", "Nhấn nút \"Đăng nhập\" hoặc \"Đăng ký\" trên Header", "Điều hướng trình duyệt sang trang /login hoặc /login?tab=register tương ứng."],
    ["3", "Nhấn nút \"Bắt đầu ngay\" (Hero CTA)", "Kích hoạt hàm handleHeroStart(): Kiểm tra token; nếu đã có token hợp lệ, chuyển thẳng vào /app (MH02); nếu chưa có token, chuyển hướng sang /login (MH01)."],
    ["4", "Kéo thanh trượt hoặc nhấn chọn điểm mẫu trên công cụ tính điểm", "Bắt biến cố oninput của thanh trượt calcSlider: Lấy giá trị điểm số hiện tại, áp dụng logic quy đổi điểm chữ theo QĐ3 (>=8.5: A; >=7.0: B; >=5.5: C; >=4.0: D; <4.0: F), cập nhật huy hiệu điểm chữ calcLetterBadge và hiển thị diễn giải xếp loại học lực tương ứng."],
    ["5", "Nhấn các liên kết điều hướng trên Navbar", "Kích hoạt hành vi cuộn mượt (smooth scrolling) đến đúng tọa độ của phân đoạn nội dung được chỉ định trên trang."]
]
create_styled_table(evt_headers, mh00_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

# ------------------------------------------------------------------------------
# 3.6.3.2. MH01 - Màn hình Đăng nhập
# ------------------------------------------------------------------------------
add_h4("3.6.3.2. Màn hình Đăng nhập (MH01 - UC00)")
add_p("a. Giao diện")
add_p("Màn hình Đăng nhập được thiết kế theo phong cách khung thẻ trung tâm (Floating Card) nổi bật trên nền hoa văn kỹ thuật số sang trọng. Khung thẻ chứa logo EduExam, tiêu đề chào đón và 2 tab chuyển đổi linh hoạt: \"Đăng nhập\" và \"Đăng ký\". Form đăng nhập trang bị các ô nhập liệu hiện đại với biểu tượng trực quan, nút ẩn/hiện mật khẩu tức thời, checkbox ghi nhớ đăng nhập, hộp cảnh báo lỗi tự động và nút bấm xác nhận có hiệu ứng phản hồi.")
add_img("screen_01_login.png", "Hình 3.5. Giao diện Màn hình Đăng nhập (MH01)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.15 Danh sách các đối tượng trên Màn hình Đăng nhập")
mh01_objs = [
    ["1", "Tab Đăng nhập", "Tab Button", "N/A", "Kích hoạt chuyển sang chế độ biểu mẫu đăng nhập hệ thống."],
    ["2", "Tab Đăng ký", "Tab Button", "N/A", "Kích hoạt chuyển sang chế độ biểu mẫu đăng ký tài khoản giảng viên."],
    ["3", "Tên đăng nhập", "Textbox", "Bắt buộc, không dấu cách", "Tiếp nhận tên đăng nhập của tài khoản (VD: giangvien, admin)."],
    ["4", "Mật khẩu", "Password Box", "Bắt buộc, tối thiểu 6 ký tự", "Tiếp nhận mật khẩu xác thực của tài khoản."],
    ["5", "Nút Ẩn/Hiện mật khẩu", "Icon Button", "N/A", "Chuyển đổi trạng thái hiển thị mật khẩu giữa dạng ẩn (dấu chấm) và rõ."],
    ["6", "Tùy chọn Ghi nhớ đăng nhập", "Checkbox", "Checked / Unchecked", "Tùy chọn lưu giữ phiên làm việc lâu dài trên trình duyệt."],
    ["7", "Nút Đăng nhập", "Button", "Trạng thái sẵn sàng / Loading", "Gửi dữ liệu biểu mẫu đăng nhập để hệ thống thực hiện xác thực."],
    ["8", "Hộp thông báo lỗi xác thực", "Alert Box", "Hiển thị / Ẩn tự động", "Hiển thị thông điệp cảnh báo màu đỏ chi tiết khi xác thực thất bại."],
    ["9", "Họ và tên giảng viên", "Textbox", "Bắt buộc, độ dài 2–100 ký tự", "Tiếp nhận họ và tên đầy đủ của giảng viên khi đăng ký mới."],
    ["10", "Tên đăng nhập đăng ký", "Textbox", "Bắt buộc, duy nhất toàn trường", "Tiếp nhận tên đăng nhập mong muốn cho tài khoản đăng ký mới."],
    ["11", "Mật khẩu đăng ký", "Password Box", "Bắt buộc, tối thiểu 6 ký tự", "Tiếp nhận mật khẩu khởi tạo cho tài khoản mới đăng ký."],
    ["12", "Nút Đăng ký tài khoản", "Button", "Trạng thái sẵn sàng / Loading", "Gửi yêu cầu tạo tài khoản giảng viên mới lên máy chủ."]
]
create_styled_table(obj_headers, mh01_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.16 Danh sách các biến cố và xử lý trên Màn hình Đăng nhập")
mh01_evts = [
    ["1", "Khởi tạo màn hình (Page Load)", "Kiểm tra token phiên làm việc hiện có trong localStorage. Nếu token hợp lệ và còn hiệu lực, tự động chuyển hướng thẳng vào Màn hình Tổng quan (MH02). Nếu chưa có hoặc đã hết hạn, tập trung con trỏ chuột vào ô Tên đăng nhập."],
    ["2", "Nhấn nút \"Đăng nhập\" hoặc nhấn Enter tại ô Mật khẩu", "1. Kiểm tra tính hợp lệ dữ liệu đầu vào: Tên đăng nhập và Mật khẩu không được để trống.\n2. Gửi yêu cầu POST /api/auth/login kèm tên đăng nhập và mật khẩu.\n3. Máy chủ kiểm tra trong bảng TaiKhoan, kiểm tra trạng thái hoạt động (active) và so khớp mật khẩu băm scrypt.\n4. Nếu xác thực thành công: Lưu trữ JWT Token, vai trò người dùng vào localStorage, hiển thị thông báo thành công và điều hướng sang MH02.\n5. Nếu sai thông tin: Hiển thị cảnh báo lỗi màu đỏ tại Hộp thông báo lỗi xác thực."],
    ["3", "Nhấn nút chuyển đổi Tab \"Đăng ký\"", "Ẩn biểu mẫu đăng nhập, xóa các cảnh báo lỗi cũ, hiển thị biểu mẫu đăng ký và tập trung con trỏ vào ô Họ và tên giảng viên."],
    ["4", "Nhấn nút \"Đăng ký tài khoản\"", "1. Kiểm tra tính hợp lệ: họ tên, tên đăng nhập không rỗng, mật khẩu đủ từ 6 ký tự.\n2. Gửi yêu cầu POST /api/auth/register lên máy chủ.\n3. Máy chủ kiểm tra tính duy nhất của tên đăng nhập trong CSDL. Nếu đã tồn tại, trả về lỗi trùng lặp.\n4. Nếu hợp lệ, tự động mã hóa mật khẩu và tạo mới bản ghi TaiKhoan với vaiTro='giangvien'.\n5. Hiển thị thông báo đăng ký thành công, tự động chuyển về Tab Đăng nhập để giảng viên đăng nhập."],
    ["5", "Nhấn nút Ẩn/Hiện mật khẩu", "Chuyển đổi thuộc tính type của ô nhập liệu giữa 'password' và 'text', đồng thời hoán đổi biểu tượng mắt mở / mắt đóng."]
]
create_styled_table(evt_headers, mh01_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

# ------------------------------------------------------------------------------
# 3.6.3.3. MH02 - Màn hình Tổng quan (Dashboard)
# ------------------------------------------------------------------------------
add_h4("3.6.3.3. Màn hình Tổng quan - Dashboard (MH02)")
add_p("a. Giao diện")
add_p("Màn hình Tổng quan là trung tâm điều khiển chính của hệ thống EduExam. Phía trên cùng hiển thị lời chào mừng cá nhân hóa kèm họ tên người dùng đang đăng nhập. Khu vực trung tâm gồm 4 thẻ chỉ số KPI nổi bật (Tổng số câu hỏi, Tổng số đề thi, Tổng số bài chấm, Tổng số sinh viên phụ trách) kèm biểu tượng và hiệu ứng màu riêng biệt. Phía dưới là Thẻ phân tích phân bố ngân hàng đề thi theo 4 môn học (QĐ1) kèm các nút lối tắt thao tác nhanh và bảng tóm tắt cấu hình hệ thống.")
add_img("screen_02_dashboard.png", "Hình 3.6. Giao diện Màn hình Tổng quan (Dashboard - MH02)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.17 Danh sách các đối tượng trên Màn hình Tổng quan")
mh02_objs = [
    ["1", "Tiêu đề chào mừng người dùng", "Label / Text", "Họ tên người dùng", "Hiển thị tên người dùng và vai trò đăng nhập hiện tại."],
    ["2", "Thẻ Thống kê tổng số câu hỏi", "Stat Card / Button", "Số nguyên không âm", "Hiển thị tổng số câu hỏi do giảng viên tạo; click để mở MH03."],
    ["3", "Thẻ Thống kê tổng số đề thi", "Stat Card / Button", "Số nguyên không âm", "Hiển thị tổng số đề thi giảng viên đã soạn; click để mở MH04."],
    ["4", "Thẻ Thống kê tổng số bài chấm", "Stat Card / Button", "Số nguyên không âm", "Hiển thị tổng số bài thi sinh viên đã chấm; click để mở MH05."],
    ["5", "Thẻ Thống kê tổng số sinh viên", "Stat Card / Button", "Số nguyên không âm", "Hiển thị tổng số sinh viên thuộc các lớp phụ trách; click mở MH08."],
    ["6", "Huy hiệu số câu hỏi IT001", "Badge / Counter", "Số câu hỏi môn IT001", "Hiển thị số câu hỏi thuộc môn Nhập môn lập trình (QĐ1)."],
    ["7", "Huy hiệu số câu hỏi IT002", "Badge / Counter", "Số câu hỏi môn IT002", "Hiển thị số câu hỏi thuộc môn Lập trình hướng đối tượng (QĐ1)."],
    ["8", "Huy hiệu số câu hỏi IT003", "Badge / Counter", "Số câu hỏi môn IT003", "Hiển thị số câu hỏi thuộc môn Cấu trúc dữ liệu và giải thuật."],
    ["9", "Huy hiệu số câu hỏi SE104", "Badge / Counter", "Số câu hỏi môn SE104", "Hiển thị số câu hỏi thuộc môn Nhập môn CNPM (QĐ1)."],
    ["10", "Thanh menu điều hướng Sidebar", "Nav Menu", "Danh sách các phân hệ", "Thanh điều hướng chuyển đổi qua lại giữa tất cả các màn hình SPA."],
    ["11", "Nút Đăng xuất", "Action Button", "N/A", "Nút thoát phiên làm việc của người dùng hiện tại."]
]
create_styled_table(obj_headers, mh02_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.18 Danh sách các biến cố và xử lý trên Màn hình Tổng quan")
mh02_evts = [
    ["1", "Kích hoạt mở Dashboard (View Init)", "1. Gọi đồng thời các API dữ liệu: /api/metadata, /api/cauhoi, /api/dethi, /api/chamthi/summary, /api/lop.\n2. Tổng hợp và điền các giá trị đếm số lượng vào 4 thẻ KPI Câu hỏi, Đề thi, Bài chấm, Sinh viên.\n3. Phân loại danh sách câu hỏi theo 4 mã môn để hiển thị số lượng tương ứng lên các huy hiệu môn học.\n4. Cập nhật họ tên giảng viên lên tiêu đề chào mừng."],
    ["2", "Nhấn vào bất kỳ Thẻ chỉ số KPI", "Hệ thống xác định loại thẻ được nhấn và gọi hàm app.switchTab(tabId) để chuyển ngay vùng làm việc sang phân hệ tương ứng (ví dụ: click Thẻ Câu hỏi -> chuyển sang MH03; click Thẻ Đề thi -> chuyển sang MH04)."],
    ["3", "Nhấn chọn phân hệ trên Sidebar điều hướng", "Đổi trạng thái active cho mục menu được chọn, ẩn phân hệ hiện tại và hiển thị phân hệ mới theo mô hình SPA, cập nhật thanh tiêu đề tương ứng."],
    ["4", "Nhấn nút \"Đăng xuất\" trên thanh Header", "Mở Hộp thoại xác nhận modal-confirm. Nếu người dùng xác nhận: Xóa bỏ token và thông tin cá nhân trong localStorage, gọi hàm app.logout() và điều hướng trở lại Màn hình Đăng nhập (MH01)."]
]
create_styled_table(evt_headers, mh02_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

# ------------------------------------------------------------------------------
# 3.6.3.4. MH03 - Màn hình Quản lý câu hỏi
# ------------------------------------------------------------------------------
add_h4("3.6.3.4. Màn hình Quản lý câu hỏi (MH03 - UC01)")
add_p("a. Giao diện")
add_p("Màn hình Quản lý câu hỏi cung cấp không gian biên soạn và tổ chức ngân hàng câu hỏi học thuật. Phía trên bố trí thanh công cụ tìm kiếm tức thời theo từ khóa, bộ chọn môn học (4 môn theo QĐ1), bộ chọn độ khó (4 cấp độ theo QĐ1), nút bấm chuyển đổi kiểu hiển thị (dạng thẻ bài Card trực quan hoặc bảng chi tiết Table), và nút \"Thêm câu hỏi mới\" nổi bật. Khu vực chính hiển thị danh sách các câu hỏi kèm nhãn mã môn, nhãn độ khó, nội dung, đáp án chuẩn, cùng các nút thao tác Sửa/Xóa. Khi thêm hoặc sửa câu hỏi, Hộp thoại Modal hiện lên với đầy đủ các trường nhập liệu theo biểu mẫu BM1.")
add_img("screen_03_cauhoi.png", "Hình 3.7. Giao diện Màn hình Ngân hàng câu hỏi (MH03)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.19 Danh sách các đối tượng trên Màn hình Quản lý câu hỏi")
mh03_objs = [
    ["1", "Ô tìm kiếm từ khóa câu hỏi", "Search Box", "Chuỗi ký tự tùy ý", "Nhập từ khóa tìm kiếm trong nội dung hoặc đáp án câu hỏi."],
    ["2", "Hộp chọn lọc Môn học", "Combobox", "Tất cả / 4 môn học (QĐ1)", "Lọc danh sách câu hỏi theo môn học lựa chọn."],
    ["3", "Hộp chọn lọc Độ khó", "Combobox", "Tất cả / 4 mức độ khó (QĐ1)", "Lọc danh sách câu hỏi theo độ khó (Dễ, Trung bình, Phức tạp, Khó)."],
    ["4", "Nút Xem dạng thẻ lưới (Card)", "Toggle Button", "Active / Inactive", "Chuyển giao diện sang chế độ hiển thị lưới các thẻ bài (Card)."],
    ["5", "Nút Xem dạng bảng (Table)", "Toggle Button", "Active / Inactive", "Chuyển giao diện sang chế độ hiển thị bảng danh sách (Table)."],
    ["6", "Nút Thêm câu hỏi mới", "Button", "N/A", "Mở hộp thoại Modal biên soạn câu hỏi mới theo mẫu BM1."],
    ["7", "Huy hiệu Tổng số câu hỏi", "Badge / Counter", "Số nguyên không âm", "Hiển thị tổng số câu hỏi thỏa mãn điều kiện lọc."],
    ["8", "Hộp thoại Modal Soạn câu hỏi", "Modal Dialog", "Hiển thị / Ẩn", "Hộp thoại nhập thông tin tạo mới hoặc chỉnh sửa câu hỏi."],
    ["9", "Ô nhập Mã câu hỏi", "Textbox", "Bắt buộc, duy nhất (PK)", "Nhập mã định danh câu hỏi (tự sinh hoặc người dùng nhập)."],
    ["10", "Hộp chọn Môn học (Modal)", "Combobox", "Bắt buộc, 1 trong 4 môn", "Chọn môn học của câu hỏi theo danh mục quy định QĐ1."],
    ["11", "Hộp chọn Độ khó (Modal)", "Combobox", "Bắt buộc, 1 trong 4 mức", "Chọn độ khó cho câu hỏi (Dễ, Trung bình, Phức tạp, Khó)."],
    ["12", "Ô nhập Nội dung câu hỏi", "Textarea", "Bắt buộc, không để trống", "Nhập nội dung đề dẫn chi tiết của câu hỏi."],
    ["13", "Ô nhập Đáp án chuẩn", "Textarea", "Bắt buộc với câu hỏi mới", "Nhập đáp án chuẩn và thang điểm mẫu của câu hỏi."],
    ["14", "Nút Lưu câu hỏi", "Button", "Trạng thái sẵn sàng", "Lưu dữ liệu câu hỏi vào cơ sở dữ liệu."],
    ["15", "Nút Sửa câu hỏi", "Icon Button", "N/A", "Mở modal chỉnh sửa nội dung câu hỏi tương ứng."],
    ["16", "Nút Xóa câu hỏi", "Icon Button", "N/A", "Kích hoạt quy trình kiểm tra và xóa câu hỏi theo QĐ1."]
]
create_styled_table(obj_headers, mh03_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.20 Danh sách các biến cố và xử lý trên Màn hình Quản lý câu hỏi")
mh03_evts = [
    ["1", "Khởi tạo màn hình Quản lý câu hỏi", "Gọi API GET /api/cauhoi để tải toàn bộ danh sách câu hỏi do giảng viên hiện tại tạo; đồng thời nạp danh mục 4 môn học và 4 mức độ khó vào các combobox lọc."],
    ["2", "Nhập từ khóa tìm kiếm hoặc thay đổi bộ lọc Môn/Độ khó", "Thực hiện lọc danh sách câu hỏi trong bộ nhớ theo từ khóa, mã môn và độ khó (áp dụng kỹ thuật debounce 300ms). Cập nhật số đếm Huy hiệu Tổng số câu hỏi và kết xuất lại giao diện dạng Card hoặc Table tương ứng."],
    ["3", "Nhấn nút \"Thêm câu hỏi mới\"", "Mở Hộp thoại Modal Soạn câu hỏi ở chế độ tạo mới: Tự động khởi tạo mã câu hỏi gợi ý, xóa trống nội dung và đáp án, gán mặc định môn học đầu tiên và độ khó \"Dễ\"."],
    ["4", "Nhấn nút \"Lưu câu hỏi\"", "1. Kiểm tra tính hợp lệ client-side: Môn học, độ khó, nội dung câu hỏi và đáp án chuẩn không được để trống.\n2. Nếu tạo mới: Gửi POST /api/cauhoi kèm accountId của giảng viên.\n3. Nếu chỉnh sửa: Gửi PUT /api/cauhoi/:maCauHoi.\n4. Máy chủ kiểm tra ràng buộc QĐ1, lưu vào bảng CauHoi.\n5. Đóng modal, hiển thị Toast thông báo thành công và làm mới danh sách câu hỏi."],
    ["5", "Nhấn nút \"Sửa câu hỏi\" trên từng dòng", "Gọi API hoặc lấy bản ghi câu hỏi hiện tại, mở modal ở chế độ cập nhật, khóa trường mã câu hỏi (không cho đổi mã) và điền sẵn nội dung, môn, độ khó, đáp án hiện hữu."],
    ["6", "Nhấn nút \"Xóa câu hỏi\" trên từng dòng", "1. Kiểm tra ràng buộc QĐ1: Giảng viên chỉ được xóa câu hỏi chưa thuộc bất kỳ đề thi nào.\n2. Gửi yêu cầu DELETE /api/cauhoi/:maCauHoi lên máy chủ.\n3. Máy chủ truy vấn bảng ChiTietDeThi; nếu câu hỏi đã được sử dụng trong đề thi, từ chối xóa và trả về thông báo vi phạm QĐ1.\n4. Nếu câu hỏi chưa thuộc đề thi nào: Mở hộp thoại xác nhận, sau khi xác nhận thì xóa khỏi CSDL và cập nhật giao diện."]
]
create_styled_table(evt_headers, mh03_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

# ------------------------------------------------------------------------------
# 3.6.3.5. MH04 - Màn hình Soạn đề thi
# ------------------------------------------------------------------------------
add_h4("3.6.3.5. Màn hình Soạn đề thi (MH04 - UC02)")
add_p("a. Giao diện")
add_p("Màn hình Soạn đề thi cho phép giảng viên quản lý danh mục đề thi đã lập và khởi tạo đề thi mới đáp ứng quy chuẩn QĐ2. Màn hình hiển thị danh sách các đề thi với đầy đủ thông tin: Mã đề, Tên môn thi, Học kỳ, Năm học, Thời lượng, Số lượng câu hỏi, Tổng điểm và trạng thái đề thi (Đã có bài chấm / Chưa có bài chấm). Mỗi dòng đề thi có các nút chức năng: Chấm thi ngay, Sửa đề, Xóa đề. Nút \"Soạn đề thi mới\" kích hoạt Hộp thoại Modal Soạn đề thi (BM2) tích hợp bộ chọn câu hỏi trực quan cùng thanh tính tổng điểm tự động.")
add_img("screen_04_dethi.png", "Hình 3.8. Giao diện Màn hình Soạn đề thi (MH04)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.21 Danh sách các đối tượng trên Màn hình Soạn đề thi")
mh04_objs = [
    ["1", "Nút Soạn đề thi mới", "Button", "N/A", "Mở Hộp thoại Modal soạn đề thi mới theo biểu mẫu BM2."],
    ["2", "Nút Xem dạng thẻ lưới (Card)", "Toggle Button", "Active / Inactive", "Chuyển chế độ hiển thị danh sách đề thi dạng lưới thẻ Card."],
    ["3", "Nút Xem dạng bảng (Table)", "Toggle Button", "Active / Inactive", "Chuyển chế độ hiển thị danh sách đề thi dạng bảng chi tiết."],
    ["4", "Huy hiệu Tổng số đề thi", "Badge / Counter", "Số nguyên không âm", "Hiển thị tổng số lượng đề thi do giảng viên khởi tạo."],
    ["5", "Nút Chấm thi ngay", "Button / Link", "N/A", "Nút tác vụ nhanh: chuyển thẳng sang MH05 để chấm thi cho đề này."],
    ["6", "Hộp thoại Modal Soạn đề thi", "Modal Dialog", "Hiển thị / Ẩn", "Hộp thoại biên soạn thông tin chung và chi tiết câu hỏi đề thi."],
    ["7", "Ô nhập Mã đề thi", "Textbox", "Bắt buộc, duy nhất (PK)", "Nhập mã định danh đề thi (VD: SE104-GK1, IT001-CK)."],
    ["8", "Hộp chọn Môn thi", "Combobox", "Bắt buộc, 1 trong 4 môn", "Chọn môn thi; hệ thống tự động lọc danh sách câu hỏi theo môn."],
    ["9", "Ô nhập Học kỳ", "Textbox / Select", "1 / 2 / 3", "Nhập học kỳ diễn ra kỳ thi."],
    ["10", "Ô nhập Năm học", "Textbox", "Định dạng YYYY-YYYY", "Nhập năm học diễn ra kỳ thi (VD: 2023-2024)."],
    ["11", "Hộp chọn Ngày thi", "Date Picker", "Định dạng YYYY-MM-DD", "Chọn ngày tổ chức thi kết thúc môn học."],
    ["12", "Ô nhập Thời lượng thi", "Number Box", "Số nguyên: 30–180 phút", "Thời lượng làm bài theo quy định QĐ2 (từ 30 đến 180 phút)."],
    ["13", "Huy hiệu Số câu đã chọn", "Badge", "Hiển thị \"X / 5 câu\"", "Hiển thị số lượng câu hỏi đã chọn trong đề (QĐ2: 1 đến 5 câu)."],
    ["14", "Huy hiệu Tổng điểm đề thi", "Badge / Alert", "Bắt buộc bằng 10.0 điểm", "Hiển thị tổng số điểm đã gán cho các câu hỏi (xanh khi = 10, đỏ khi != 10)."],
    ["15", "Danh sách câu hỏi cùng môn", "Container / List", "Danh sách câu hỏi cùng môn", "Vùng hiển thị danh sách câu hỏi kèm checkbox chọn và ô gán điểm."],
    ["16", "Nút Lưu đề thi", "Button", "Sẵn sàng khi tổng điểm = 10", "Lưu thông tin đề thi và chi tiết phân bổ điểm vào CSDL."]
]
create_styled_table(obj_headers, mh04_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.22 Danh sách các biến cố và xử lý trên Màn hình Soạn đề thi")
mh04_evts = [
    ["1", "Khởi tạo màn hình Soạn đề thi", "Gọi API GET /api/dethi để nạp danh sách đề thi của giảng viên. Đối với mỗi đề thi, kiểm tra số lượng bài thi đã chấm để thiết lập trạng thái và hiển thị nút thao tác tương ứng."],
    ["2", "Nhấn nút \"Soạn đề thi mới\"", "Mở Hộp thoại Modal Soạn đề thi ở chế độ tạo mới: Khởi tạo giá trị mặc định cho năm học hiện tại, học kỳ 1, thời lượng 60 phút; đồng thời tải danh sách câu hỏi thuộc môn thi đang được chọn."],
    ["3", "Thay đổi lựa chọn Môn thi trong Modal", "Cập nhật lại danh sách câu hỏi trong Modal: Chỉ tải các câu hỏi thuộc đúng môn thi vừa chọn; xóa bỏ các câu hỏi môn cũ đã chọn trước đó và đặt lại tổng điểm về 0."],
    ["4", "Tích chọn/Bỏ chọn câu hỏi và nhập điểm", "1. Kiểm tra số lượng câu hỏi được chọn: Nếu đã đủ 5 câu mà tiếp tục chọn thêm câu thứ 6, hệ thống cảnh báo và ngăn chặn theo quy định QĐ2.\n2. Khi người dùng nhập điểm phân bổ cho từng câu hỏi, tự động cộng dồn và cập nhật lên Huy hiệu Tổng điểm đề thi. Nếu tổng điểm = 10.0, badge chuyển màu xanh lá hợp lệ; nếu khác 10.0, badge hiển thị cảnh báo màu đỏ."],
    ["5", "Nhấn nút \"Lưu đề thi\"", "1. Kiểm tra toàn bộ quy định QĐ2: Thời lượng thi thuộc đoạn [30; 180] phút, số lượng câu từ 1 đến 5 câu, các câu hỏi phải cùng một môn, tổng điểm các câu hỏi phải chính xác bằng 10.0 điểm.\n2. Gửi yêu cầu POST /api/dethi lên máy chủ.\n3. Máy chủ thực hiện giao dịch (transaction) thêm bản ghi DeThi và các bản ghi ChiTietDeThi tương ứng.\n4. Đóng modal, hiển thị Toast thành công và làm mới danh sách đề thi."],
    ["6", "Nhấn nút \"Xóa đề thi\"", "1. Kiểm tra quy định QĐ2: Giảng viên chỉ được xóa đề thi khi chưa có kết quả chấm thi.\n2. Gọi API DELETE /api/dethi/:maDe; máy chủ kiểm tra bảng KetQuaCham, nếu đã có bài chấm sẽ từ chối xóa và trả về thông báo vi phạm QĐ2.\n3. Nếu chưa có bài chấm: Mở modal-confirm, xóa đề thi sau khi người dùng xác nhận."],
    ["7", "Nhấn nút \"Chấm thi ngay\" trên dòng đề thi", "Lưu mã đề thi vào bộ nhớ tạm, tự động kích hoạt hàm chuyển tab sang MH05 (Ghi nhận chấm thi) và chọn sẵn đề thi này trên giao diện chấm."]
]
create_styled_table(evt_headers, mh04_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

# ------------------------------------------------------------------------------
# 3.6.3.6. MH05 - Màn hình Ghi nhận chấm thi
# ------------------------------------------------------------------------------
add_h4("3.6.3.6. Màn hình Ghi nhận chấm thi (MH05 - UC03)")
add_p("a. Giao diện")
add_p("Màn hình Ghi nhận chấm thi được thiết kế tối ưu hóa tốc độ nhập liệu điểm số cho giảng viên. Phía trên gồm bộ ba combobox chọn liên hoàn: Môn học → Đề thi → Lớp học (theo BM3). Kế tiếp là Hộp tóm tắt thông số đề thi (Môn thi, Thời lượng, Ngày thi, Học kỳ) và Thanh tiến độ hoàn thành chấm thi trực quan. Vùng trung tâm là Bảng điểm sinh viên tương tác trực tiếp với các cột: STT, Mã số sinh viên, Họ và tên, Điểm số (ô nhập liệu trực tiếp), Điểm chữ (badge quy đổi tự động A, B, C, D, E, F theo QĐ3), Ô nhập ghi chú và Trạng thái lưu.")
add_img("screen_05_chamthi.png", "Hình 3.9. Giao diện Màn hình Ghi nhận chấm thi (MH05)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.23 Danh sách các đối tượng trên Màn hình Ghi nhận chấm thi")
mh05_objs = [
    ["1", "Hộp chọn Môn học", "Combobox", "Bắt buộc, 1 trong 4 môn", "Chọn môn học cần tiến hành chấm điểm."],
    ["2", "Hộp chọn Đề thi", "Combobox", "Bắt buộc, theo môn đã chọn", "Chọn đề thi áp dụng để chấm điểm cho sinh viên."],
    ["3", "Hộp chọn Lớp học", "Combobox", "Bắt buộc, lớp giảng viên phụ trách", "Chọn lớp học cần nhập kết quả điểm thi."],
    ["4", "Khung tóm tắt thông số đề thi", "Info Container", "Thông tin đề thi đã chọn", "Hộp hiển thị tóm tắt môn thi, thời lượng, ngày thi và học kỳ."],
    ["5", "Thanh tiến độ chấm thi", "Progress Bar", "Phần trăm từ 0% đến 100%", "Thanh tiến độ hiển thị trực quan tỷ lệ bài thi đã được nhập điểm."],
    ["6", "Huy hiệu đếm số sinh viên đã chấm", "Badge / Counter", "Hiển thị \"Đã chấm X / Y SV\"", "Bộ đếm chi tiết số lượng sinh viên đã có điểm trong lớp."],
    ["7", "Bảng điểm sinh viên", "Interactive Table", "Danh sách sinh viên lớp", "Bảng tương tác hiển thị danh sách sinh viên lớp được chọn."],
    ["8", "Ô nhập Điểm số", "Number Box", "Thực: 0.0–10.0, bước 0.5 (QĐ3)", "Ô nhập điểm số trực tiếp cho từng sinh viên."],
    ["9", "Huy hiệu Điểm chữ tự động", "Badge", "A, B, C, D, E, F", "Huy hiệu tự động hiển thị điểm chữ quy đổi tức thời theo QĐ3."],
    ["10", "Ô nhập Ghi chú", "Textbox", "Chuỗi ký tự tùy chọn", "Ô nhập ghi chú đánh giá của giảng viên cho bài thi sinh viên."],
    ["11", "Nút Lưu bảng điểm", "Button", "Sẵn sàng lưu", "Lưu toàn bộ bảng điểm của lớp vào cơ sở dữ liệu."],
    ["12", "Nút Hủy / Nhập lại", "Button", "N/A", "Xóa toàn bộ điểm đang nhập dở để nạp lại điểm gốc từ CSDL."]
]
create_styled_table(obj_headers, mh05_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.24 Danh sách các biến cố và xử lý trên Màn hình Ghi nhận chấm thi")
mh05_evts = [
    ["1", "Thay đổi lựa chọn Hộp chọn Môn học", "Hệ thống lọc danh mục đề thi thuộc môn vừa chọn và cập nhật lại Hộp chọn Đề thi; làm trống bảng điểm và hộp thông tin đề."],
    ["2", "Chọn Đề thi và Lớp học cụ thể", "1. Hiển thị thông số chi tiết của đề thi lên Khung tóm tắt thông số đề thi.\n2. Gọi API GET /api/chamthi?maDe=...&maLop=... để tải danh sách sinh viên của lớp kèm kết quả chấm đã có (nếu có).\n3. Kết xuất bảng điểm lên Bảng điểm sinh viên, tự động hiển thị điểm chữ tương ứng.\n4. Cập nhật thanh tiến độ và bộ đếm sinh viên đã chấm."],
    ["3", "Nhập điểm số tại Ô nhập Điểm số trên từng dòng", "Bắt biến cố oninput / onchange thời gian thực:\n1. Kiểm tra giá trị điểm thuộc khoảng [0.0; 10.0] và phải là bội số của 0.5 theo quy định QĐ3 (hợp lệ: 0.0, 0.5, 1.0, ..., 9.5, 10.0).\n2. Nếu vi phạm: Đổi màu viền ô nhập sang đỏ, hiển thị cảnh báo lỗi.\n3. Nếu hợp lệ: Tự động tính toán và đổi Huy hiệu Điểm chữ tự động tức thời theo thang điểm chữ QĐ3 (8.5–10: A, 7.0–8.0: B, 5.5–6.5: C, 4.0–5.0: D, Dưới 4.0: F).\n4. Cập nhật lại thanh tiến độ chấm thi của lớp."],
    ["4", "Nhấn nút \"Lưu bảng điểm\"", "1. Kiểm tra tính hợp lệ toàn bộ các ô điểm trên bảng (không có ô bị lỗi vi phạm QĐ3).\n2. Thu thập danh sách các bản ghi điểm và ghi chú, gửi yêu cầu POST /api/chamthi/bulk lên máy chủ.\n3. Máy chủ thực hiện giao dịch ghi nhận/cập nhật đồng loạt vào bảng KetQuaCham kèm thời gian chấm.\n4. Hiển thị Toast thông báo thành công và đánh dấu trạng thái đã lưu cho từng dòng."]
]
create_styled_table(evt_headers, mh05_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

# ------------------------------------------------------------------------------
# 3.6.3.7. MH06 - Màn hình Tra cứu đề thi
# ------------------------------------------------------------------------------
add_h4("3.6.3.7. Màn hình Tra cứu đề thi (MH06 - UC04)")
add_p("a. Giao diện")
add_p("Màn hình Tra cứu đề thi phục vụ nhu cầu tìm kiếm nhanh chóng và xem chi tiết cấu trúc đề thi theo biểu mẫu BM4. Phía trên bố trí vùng lọc tích hợp gồm ô tìm kiếm từ khóa đa năng, 3 combobox lựa chọn (Môn học, Học kỳ, Năm học) và nút đặt lại bộ lọc. Phía dưới là bảng kết quả hiển thị thông tin tổng hợp của các đề thi phù hợp (Mã đề, Môn học, Học kỳ, Năm học, Thời lượng, Số câu, Tổng điểm, Trạng thái bài chấm) cùng 2 nút hành động tiện lợi: \"Xem chi tiết\" (mở Modal bản in đề thi chuẩn BM4) và \"Chấm thi\" (chuyển nhanh sang phân hệ chấm).")
add_img("screen_06_tracuu.png", "Hình 3.10. Giao diện Màn hình Tra cứu đề thi (MH06)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.25 Danh sách các đối tượng trên Màn hình Tra cứu đề thi")
mh06_objs = [
    ["1", "Ô tìm kiếm từ khóa đề thi", "Search Box", "Chuỗi ký tự tùy ý", "Nhập từ khóa tìm kiếm theo mã đề hoặc thông tin ghi chú đề thi."],
    ["2", "Hộp chọn lọc Môn học", "Combobox", "Tất cả môn / 4 môn học", "Lọc kết quả đề thi theo môn học chỉ định."],
    ["3", "Hộp chọn lọc Học kỳ", "Combobox", "Tất cả học kỳ / HK1, HK2, HK3", "Lọc kết quả đề thi theo học kỳ tổ chức."],
    ["4", "Hộp chọn lọc Năm học", "Combobox", "Tất cả năm / Danh sách năm học", "Lọc kết quả đề thi theo năm học biên soạn."],
    ["5", "Nút Đặt lại bộ lọc", "Button", "N/A", "Đặt lại toàn bộ các tiêu chí lọc về trạng thái mặc định ban đầu."],
    ["6", "Huy hiệu Số lượng kết quả", "Badge / Counter", "Số nguyên không âm", "Hiển thị số lượng đề thi tìm thấy thỏa mãn tiêu chí."],
    ["7", "Bảng kết quả tra cứu đề thi", "Table View", "Danh sách đề thi kết quả", "Bảng kết quả tra cứu hiển thị thông tin tổng hợp các đề thi."],
    ["8", "Nút Xem chi tiết bản in", "Icon Button", "N/A", "Mở Hộp thoại Modal xem bản in chi tiết đề thi chuẩn BM4."],
    ["9", "Nút Chấm thi cho đề", "Icon Button", "N/A", "Chuyển tiếp nhanh sang MH05 để chấm thi cho đề thi này."],
    ["10", "Hộp thoại Modal Xem bản in đề thi", "Modal Dialog", "Hiển thị / Ẩn", "Hộp thoại xem trước toàn văn đề thi theo biểu mẫu BM4."],
    ["11", "Nút In đề thi (Print)", "Button", "N/A", "Kích hoạt lệnh in đề thi ra máy in hoặc xuất tệp PDF."]
]
create_styled_table(obj_headers, mh06_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.26 Danh sách các biến cố và xử lý trên Màn hình Tra cứu đề thi")
mh06_evts = [
    ["1", "Khởi tạo màn hình Tra cứu đề thi", "Tải danh mục đề thi từ API GET /api/dethi, đồng thời nạp danh sách các giá trị môn học, học kỳ, năm học hiện có vào các combobox lựa chọn; kết xuất toàn bộ danh sách đề thi ban đầu."],
    ["2", "Thay đổi từ khóa tìm kiếm hoặc các tiêu chí combobox", "Thực hiện lọc kết hợp đa tiêu chí (Multi-criteria Filter) trên tập dữ liệu đề thi: So khớp từ khóa với mã đề/môn, kiểm tra giá trị môn học, học kỳ và năm học. Cập nhật Huy hiệu Số lượng kết quả và làm mới bảng kết quả."],
    ["3", "Nhấn nút \"Xem chi tiết bản in\" trên dòng đề thi", "1. Gọi API GET /api/dethi/:maDe để lấy toàn bộ thông tin đề thi và danh sách câu hỏi kèm đáp án chuẩn và điểm số chi tiết từng câu.\n2. Điền dữ liệu vào khung biểu mẫu in BM4 trong Hộp thoại Modal Xem bản in đề thi.\n3. Hiển thị modal để người dùng xem trước đề thi trước khi in."],
    ["4", "Nhấn nút \"In đề thi\" trong Modal Preview", "Kích hoạt lệnh in trình duyệt window.print() với định dạng CSS trang in ấn chuyên nghiệp (ẩn toàn bộ thanh điều hướng, nút bấm, lề trang chuẩn A4)."],
    ["5", "Nhấn nút \"Chấm thi cho đề\" trên dòng kết quả tra cứu", "Tự động kích hoạt chuyển hướng sang Màn hình Ghi nhận chấm thi (MH05) và chọn sẵn đề thi này trong bộ chọn."]
]
create_styled_table(evt_headers, mh06_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

# ------------------------------------------------------------------------------
# 3.6.3.8. MH07 - Màn hình Báo cáo tổng hợp năm
# ------------------------------------------------------------------------------
add_h4("3.6.3.8. Màn hình Báo cáo tổng hợp năm (MH07 - UC05)")
add_p("a. Giao diện")
add_p("Màn hình Báo cáo tổng hợp năm phục vụ công tác thống kê, giám sát và đánh giá hiệu quả ra đề, chấm thi theo từng năm học (biểu mẫu BM5). Phía trên gồm combobox chọn Năm học cần báo cáo và nút \"Lập báo cáo\". Khu vực trực quan hóa trung tâm bố trí 2 đồ thị dạng cột so sánh trực quan giữa 4 môn học: Đồ thị Số lượng đề thi đã soạn và Đồ thị Số lượng bài thi đã chấm. Phía dưới là Bảng số liệu chi tiết theo biểu mẫu BM5 (Mã môn, Tên môn, Số đề thi, Tỷ lệ đề thi %, Số bài chấm, Tỷ lệ bài chấm %) cùng dòng Tổng cộng toàn trường đạt 100.0%.")
add_img("screen_07_baocao.png", "Hình 3.11. Giao diện Màn hình Báo cáo tổng hợp năm (MH07)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.27 Danh sách các đối tượng trên Màn hình Báo cáo tổng hợp năm")
mh07_objs = [
    ["1", "Hộp chọn Năm học", "Combobox", "Bắt buộc, danh sách năm học", "Chọn năm học cần lập báo cáo thống kê số liệu (VD: 2023-2024)."],
    ["2", "Nút Lập báo cáo", "Button", "N/A", "Kích hoạt tính toán và kết xuất báo cáo thống kê cho năm học đã chọn."],
    ["3", "Biểu đồ cột Số lượng đề thi", "Bar Chart / Canvas", "Biểu đồ cột so sánh", "Biểu đồ cột trực quan hiển thị số lượng đề thi biên soạn theo 4 môn."],
    ["4", "Biểu đồ cột Số lượng bài chấm", "Bar Chart / Canvas", "Biểu đồ cột so sánh", "Biểu đồ cột trực quan hiển thị số lượng bài thi sinh viên đã chấm."],
    ["5", "Tiêu đề bảng số liệu báo cáo", "Label / Text", "Năm học được lập", "Nhãn hiển thị ngữ cảnh năm học đang được phân tích số liệu."],
    ["6", "Bảng số liệu thống kê chi tiết (BM5)", "Report Table (BM5)", "4 dòng môn học + 1 dòng Tổng", "Bảng dữ liệu chi tiết thống kê số lượng và tỷ lệ % theo biểu mẫu BM5."],
    ["7", "Ô hiển thị Tổng số đề thi", "Table Cell / Bold", "Số nguyên không âm", "Hiển thị tổng số lượng đề thi của toàn trường trong năm học."],
    ["8", "Ô hiển thị Tổng số bài chấm", "Table Cell / Bold", "Số nguyên không âm", "Hiển thị tổng số bài thi đã chấm của toàn trường trong năm học."]
]
create_styled_table(obj_headers, mh07_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.28 Danh sách các biến cố và xử lý trên Màn hình Báo cáo tổng hợp năm")
mh07_evts = [
    ["1", "Khởi tạo màn hình Báo cáo năm", "Hệ thống tự động chọn năm học gần nhất hiện có (mặc định '2023-2024') và tự động kích hoạt lập báo cáo ban đầu để hiển thị ngay số liệu cho người dùng."],
    ["2", "Chọn Năm học và Nhấn nút \"Lập báo cáo\"", "1. Lấy giá trị năm học từ Hộp chọn Năm học, gửi yêu cầu GET /api/baocao/nam?namHoc=... lên máy chủ.\n2. Máy chủ truy vấn CSDL, tổng hợp số đề thi và số bài thi đã chấm của từng môn học trong năm đó, tính tổng số toàn trường.\n3. Áp dụng công thức (1.1) và (1.2) để tính tỷ lệ phần trăm số đề thi và số bài chấm cho từng môn học, làm tròn chính xác 1 chữ số thập phân.\n4. Trả về tập dữ liệu JSON tổng hợp về máy khách."],
    ["3", "Kết xuất biểu đồ và bảng dữ liệu BM5", "1. Cập nhật số liệu vẽ lại 2 biểu đồ cột Biểu đồ cột Số lượng đề thi và Biểu đồ cột Số lượng bài chấm với thang đo tỷ lệ chuẩn.\n2. Điền số liệu từng môn vào Bảng số liệu thống kê chi tiết, hiển thị tỷ lệ % kèm ký hiệu phần trăm.\n3. Tính tổng dòng cuối: Tổng số đề, tỷ lệ đề = 100.0%, Tổng số bài chấm, tỷ lệ chấm = 100.0%."]
]
create_styled_table(evt_headers, mh07_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

# ------------------------------------------------------------------------------
# 3.6.3.9. MH08 - Màn hình Quản lý lớp học
# ------------------------------------------------------------------------------
add_h4("3.6.3.9. Màn hình Quản lý lớp học (MH08 - UC07)")
add_p("a. Giao diện")
add_p("Màn hình Quản lý lớp học thể hiện danh sách các lớp học thuộc quyền phụ trách của giảng viên theo biểu mẫu BM7. Các lớp học được hiển thị dạng thẻ bài Card trực quan với Mã lớp nổi bật, Tên lớp, Sĩ số sinh viên hiện tại, cùng 2 nút hành động: \"Danh sách SV\" và \"Xóa lớp\". Phía trên có nút \"Tạo lớp học mới\" mở Modal thêm lớp (BM7). Nút \"Danh sách SV\" mở Modal quản lý chuyên sâu cho phép xem danh sách sinh viên hiện có, thêm sinh viên mới theo mã số MSSV và họ tên, hoặc xóa sinh viên khỏi lớp kèm ràng buộc bảo vệ dữ liệu QĐ5.")
add_img("screen_08_lophoc.png", "Hình 3.12. Giao diện Màn hình Quản lý lớp học (MH08)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.29 Danh sách các đối tượng trên Màn hình Quản lý lớp học")
mh08_objs = [
    ["1", "Nút Tạo lớp học mới", "Button", "N/A", "Mở Hộp thoại Modal tạo lớp học mới theo biểu mẫu BM7."],
    ["2", "Danh sách thẻ bài lớp học phụ trách", "Container / Cards", "Danh sách lớp học phụ trách", "Khu vực hiển thị danh sách các thẻ bài lớp học của giảng viên."],
    ["3", "Nút Xem danh sách sinh viên", "Button", "N/A", "Mở Hộp thoại Modal quản lý danh sách sinh viên của lớp học tương ứng."],
    ["4", "Nút Xóa lớp học", "Button", "N/A", "Kích hoạt kiểm tra và xóa lớp học theo quy định QĐ5."],
    ["5", "Hộp thoại Modal Tạo lớp học", "Modal Dialog", "Hiển thị / Ẩn", "Hộp thoại nhập thông tin khởi tạo lớp học mới."],
    ["6", "Ô nhập Mã lớp học", "Textbox", "Bắt buộc, duy nhất (PK)", "Nhập mã lớp học (VD: SE104.R13, IT001.N11)."],
    ["7", "Ô nhập Tên lớp học", "Textbox", "Bắt buộc, độ dài 2–100 ký tự", "Nhập tên diễn giải đầy đủ của lớp học."],
    ["8", "Nút Lưu lớp học", "Button", "Trạng thái sẵn sàng", "Lưu thông tin lớp học mới vào cơ sở dữ liệu."],
    ["9", "Hộp thoại Modal Quản lý sinh viên", "Modal Dialog", "Hiển thị / Ẩn", "Hộp thoại quản lý danh sách sinh viên theo lớp học chỉ định."],
    ["10", "Ô nhập Mã số sinh viên (MSSV)", "Textbox", "Bắt buộc, 8 chữ số", "Nhập mã số sinh viên cần thêm vào lớp học."],
    ["11", "Ô nhập Họ và tên sinh viên", "Textbox", "Bắt buộc, độ dài 2–100 ký tự", "Nhập họ và tên đầy đủ của sinh viên cần thêm."],
    ["12", "Nút Thêm sinh viên", "Button", "N/A", "Thêm sinh viên mới vào danh sách lớp học hiện tại."],
    ["13", "Bảng danh sách sinh viên của lớp", "Table View", "Danh sách sinh viên lớp", "Bảng hiển thị STT, MSSV, Họ tên và nút xóa từng sinh viên."],
    ["14", "Nút Xóa sinh viên khỏi lớp", "Icon Button", "N/A", "Xóa sinh viên ra khỏi danh sách lớp học theo ràng buộc QĐ5."]
]
create_styled_table(obj_headers, mh08_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.30 Danh sách các biến cố và xử lý trên Màn hình Quản lý lớp học")
mh08_evts = [
    ["1", "Khởi tạo màn hình Quản lý lớp học", "Gửi yêu cầu GET /api/lop để lấy danh sách toàn bộ các lớp học do tài khoản giảng viên hiện tại phụ trách kèm sĩ số sinh viên; kết xuất ra danh sách thẻ card."],
    ["2", "Nhấn nút \"Tạo lớp học mới\"", "Mở Hộp thoại Modal Tạo lớp học, xóa trống các ô nhập liệu, đưa con trỏ chuột vào ô mã lớp."],
    ["3", "Nhấn nút \"Lưu lớp học\"", "1. Kiểm tra tính hợp lệ: Mã lớp và tên lớp không được để trống.\n2. Gửi yêu cầu POST /api/lop kèm accountId giảng viên.\n3. Máy chủ kiểm tra tính duy nhất của Mã lớp trong CSDL; nếu đã tồn tại thì báo lỗi trùng lặp.\n4. Nếu hợp lệ, lưu lớp mới vào bảng Lop, đóng modal, hiển thị Toast thành công và làm mới danh sách lớp."],
    ["4", "Nhấn nút \"Xem danh sách sinh viên\" trên thẻ lớp", "1. Mở Hộp thoại Modal Quản lý sinh viên, hiển thị tiêu đề mã lớp và tên lớp tương ứng.\n2. Gọi API GET /api/lop/:maLop/sinhvien để lấy toàn bộ danh sách sinh viên thuộc lớp đó và kết xuất lên Bảng danh sách sinh viên."],
    ["5", "Nhập MSSV, Họ tên và Nhấn nút \"Thêm sinh viên\"", "1. Kiểm tra MSSV và họ tên hợp lệ.\n2. Gửi POST /api/lop/:maLop/sinhvien.\n3. Máy chủ kiểm tra tính duy nhất của MSSV trong lớp, lưu vào bảng SinhVien.\n4. Làm mới bảng danh sách sinh viên trong modal và cập nhật lại sĩ số trên thẻ lớp."],
    ["6", "Nhấn nút \"Xóa sinh viên khỏi lớp\" hoặc \"Xóa lớp học\"", "1. Kiểm tra ràng buộc bảo vệ toàn vẹn dữ liệu QĐ5: Hệ thống kiểm tra xem sinh viên hoặc lớp học đã phát sinh dữ liệu chấm thi trong bảng KetQuaCham hay chưa.\n2. Nếu đã có dữ liệu chấm thi: Hệ thống lập tức từ chối thao tác và hiển thị thông báo lỗi \"Không thể xóa lớp học hoặc sinh viên đã có kết quả chấm thi theo QĐ5!\".\n3. Nếu chưa có dữ liệu chấm thi: Mở hộp thoại xác nhận modal-confirm, thực hiện xóa sau khi người dùng xác nhận."]
]
create_styled_table(evt_headers, mh08_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

# ------------------------------------------------------------------------------
# 3.6.3.10. MH09 - Màn hình Quản lý tài khoản
# ------------------------------------------------------------------------------
add_h4("3.6.3.10. Màn hình Quản lý tài khoản giảng viên (MH09 - UC06)")
add_p("a. Giao diện")
add_p("Màn hình Quản lý tài khoản là phân hệ quản trị hệ thống đặc quyền dành riêng cho tài khoản có vai trò Quản trị viên (Admin). Giao diện thể hiện bảng danh sách toàn bộ tài khoản người dùng trong hệ thống theo biểu mẫu BM6 với các cột: Mã tài khoản, Tên đăng nhập, Họ và tên giảng viên, Vai trò hệ thống, Trạng thái hoạt động (badge xanh lá \"Hoạt động\" / badge đỏ \"Đã khóa\") và các nút tác vụ quản trị. Phía trên có nút \"Thêm tài khoản mới\" mở Hộp thoại Modal cấp phát tài khoản. Tại mỗi dòng, Quản trị viên có thể bấm nút Khóa / Mở khóa tài khoản hoặc nút Đặt lại mật khẩu về mặc định.")
add_img("screen_09_taikhoan.png", "Hình 3.13. Giao diện Màn hình Quản lý tài khoản giảng viên (MH09)", width_in=5.8)

add_p("b. Mô tả các đối tượng trên màn hình")
add_table_title("Bảng 3.31 Danh sách các đối tượng trên Màn hình Quản lý tài khoản")
mh09_objs = [
    ["1", "Nút Thêm tài khoản mới", "Button", "N/A", "Mở Hộp thoại Modal cấp phát tài khoản giảng viên mới (BM6)."],
    ["2", "Bảng danh sách tài khoản giảng viên (BM6)", "Table Body", "Danh sách tài khoản", "Bảng hiển thị danh sách các tài khoản người dùng toàn hệ thống."],
    ["3", "Huy hiệu Trạng thái tài khoản", "Badge", "Hoạt động / Đã khóa", "Huy hiệu màu phản ánh trạng thái kích hoạt của tài khoản."],
    ["4", "Nút Khóa / Mở khóa tài khoản", "Button", "Khóa / Mở khóa", "Chuyển đổi trạng thái hoạt động của tài khoản giữa active và disabled."],
    ["5", "Nút Đặt lại mật khẩu", "Button", "N/A", "Khôi phục mật khẩu tài khoản về mật khẩu mặc định của nhà trường."],
    ["6", "Hộp thoại Modal Tạo tài khoản mới", "Modal Dialog", "Hiển thị / Ẩn", "Hộp thoại khởi tạo tài khoản giảng viên mới của Quản trị viên."],
    ["7", "Ô nhập Tên đăng nhập", "Textbox", "Bắt buộc, duy nhất (PK)", "Nhập tên đăng nhập hệ thống cho giảng viên mới."],
    ["8", "Ô nhập Họ và tên giảng viên", "Textbox", "Bắt buộc, độ dài 2–100 ký tự", "Nhập họ và tên đầy đủ của giảng viên."],
    ["9", "Ô nhập Mật khẩu ban đầu", "Password Box", "Bắt buộc, tối thiểu 6 ký tự", "Nhập mật khẩu khởi tạo ban đầu cho tài khoản."],
    ["10", "Nút Lưu tài khoản", "Button", "Trạng thái sẵn sàng", "Gửi lệnh tạo tài khoản giảng viên lên máy chủ."]
]
create_styled_table(obj_headers, mh09_objs, obj_widths, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

add_p("c. Danh sách các biến cố và xử lý")
add_table_title("Bảng 3.32 Danh sách các biến cố và xử lý trên Màn hình Quản lý tài khoản")
mh09_evts = [
    ["1", "Kiểm tra quyền truy cập khi mở màn hình", "Kiểm tra vai trò người dùng trong phiên làm việc. Nếu vaiTro !== 'admin', hệ thống từ chối hiển thị màn hình và thông báo lỗi truy cập trái phép. Nếu là admin, gọi API GET /api/admin/accounts."],
    ["2", "Khởi tạo bảng danh sách tài khoản", "Nhận danh sách tài khoản từ máy chủ, kết xuất lên Bảng danh sách tài khoản giảng viên với đầy đủ thông tin định danh, trạng thái và các nút chức năng quản trị tương ứng."],
    ["3", "Nhấn nút \"Thêm tài khoản mới\"", "Mở Hộp thoại Modal Tạo tài khoản mới, xóa trống các trường thông tin và chuẩn bị tạo tài khoản giảng viên."],
    ["4", "Nhấn nút \"Lưu tài khoản\"", "1. Kiểm tra tính hợp lệ: Tên đăng nhập không rỗng, họ tên hợp lệ, mật khẩu tối thiểu 6 ký tự.\n2. Gửi POST /api/admin/accounts.\n3. Máy chủ kiểm tra tính duy nhất của tên đăng nhập, băm mật khẩu bảo mật và lưu vào bảng TaiKhoan với vaiTro='giangvien', trangThai='active'.\n4. Đóng modal, hiển thị Toast thành công và cập nhật lại bảng tài khoản."],
    ["5", "Nhấn nút \"Khóa / Mở khóa tài khoản\"", "1. Mở modal-confirm yêu cầu Quản trị viên xác nhận thao tác.\n2. Khi xác nhận, gửi PUT /api/admin/accounts/:id/toggle-status.\n3. Máy chủ đảo trạng thái trangThai giữa 'active' và 'disabled'. Giảng viên có tài khoản bị khóa sẽ không thể đăng nhập vào hệ thống ở MH01.\n4. Cập nhật lại huy hiệu trạng thái trên giao diện."],
    ["6", "Nhấn nút \"Đặt lại mật khẩu\"", "1. Mở modal-confirm yêu cầu xác nhận đặt lại mật khẩu về mặc định (gv123456).\n2. Khi xác nhận, gửi PUT /api/admin/accounts/:id/reset-password.\n3. Máy chủ cập nhật matKhauHash của tài khoản về mật khẩu chuẩn.\n4. Hiển thị thông báo thành công cho Quản trị viên."]
]
create_styled_table(evt_headers, mh09_evts, evt_widths, {0: WD_ALIGN_PARAGRAPH.CENTER})

print(f"Saving updated document to {DOC_PATH}...")
doc.save(DOC_PATH)

# Also save to new copy
NEW_PATH = "Đồ án/report--fifi-new.docx"
doc.save(NEW_PATH)

print("SUCCESS: Section 3.6 has been completely updated with Home Screen & Direct Object Names!")
