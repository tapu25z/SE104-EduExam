import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

DOC_PATH = "Đồ án/report-chuong12.docx"
IMG_DIR = "Đồ án/rendered_images"

doc = docx.Document(DOC_PATH)

# Identify body elements
body = doc._body._body
ch2_start_idx = None

elements = list(body)
for idx, el in enumerate(elements):
    if el.tag.endswith('p'):
        p = docx.text.paragraph.Paragraph(el, doc)
        if "CHƯƠNG 2." in p.text:
            ch2_start_idx = idx
            break

if ch2_start_idx is None:
    raise ValueError("Could not find CHƯƠNG 2 in document!")

print(f"Trimming old Chapter 2 from index {ch2_start_idx} (out of {len(elements)} elements), preserving sectPr...")
to_remove = [el for el in elements[ch2_start_idx:] if not el.tag.endswith('sectPr')]
for el in to_remove:
    body.remove(el)

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

def add_h1(text):
    p = doc.add_paragraph(style='Heading 1')
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.bold = True
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

def add_img(img_name, caption_text, width_in=5.8):
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
    r1.font.size = Pt(12)
    r1.bold = True
    
    r2 = p_cap.add_run(parts[2] if len(parts) > 2 else "")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.italic = True

def style_cell(cell, text="", bold=False, italic=False, font_size=11, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=None):
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
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
    r2.italic = True

def create_table(headers, rows_data, col_widths=None):
    t = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_idx, h_text in enumerate(headers):
        style_cell(t.cell(0, c_idx), text=h_text, bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="EBF3FB")
    for r_idx, r_data in enumerate(rows_data):
        for c_idx, val in enumerate(r_data):
            cell_align = WD_ALIGN_PARAGRAPH.CENTER if (c_idx == 0 or (len(str(val)) <= 10 and not str(val).endswith('.'))) else WD_ALIGN_PARAGRAPH.LEFT
            style_cell(t.cell(r_idx + 1, c_idx), text=str(val), font_size=11, align=cell_align)
    if col_widths:
        for row in t.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)
    return t

def add_spec_table(title, rows_data):
    add_table_title(title)
    headers = ["Nội dung", "Mô tả"]
    t = doc.add_table(rows=len(rows_data) + 1, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_idx, h_text in enumerate(headers):
        style_cell(t.cell(0, c_idx), text=h_text, bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER, bg_color="EBF3FB")
    for r_idx, (col1, col2) in enumerate(rows_data):
        style_cell(t.cell(r_idx + 1, 0), text=col1, bold=True, font_size=11, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color="F8FAFC")
        style_cell(t.cell(r_idx + 1, 1), text=col2, font_size=11, align=WD_ALIGN_PARAGRAPH.LEFT)
    for row in t.rows:
        row.cells[0].width = Inches(1.8)
        row.cells[1].width = Inches(4.3)
    return t

print("Start appending Chapter 2 content...")

# ============================================================
# CHƯƠNG 2. ĐẶC TẢ VÀ PHÂN TÍCH YÊU CẦU
# ============================================================
add_h1("CHƯƠNG 2. ĐẶC TẢ VÀ PHÂN TÍCH YÊU CẦU")

# 2.1 Các tác nhân của hệ thống
add_h2("2.1. Các tác nhân của hệ thống")
add_p("Hệ thống Quản lý ra đề và chấm thi (EduExam) được thiết kế nhằm hỗ trợ giảng viên trong công tác quản lý khảo thí nội bộ bộ môn và cung cấp công cụ quản trị tài khoản người dùng cho quản trị viên. Dựa trên các yêu cầu nghiệp vụ đã khảo sát tại Chương 1, các đối tượng tương tác trực tiếp với hệ thống được mô hình hóa thành 3 tác nhân chính, bao gồm một tác nhân tổng quát và hai tác nhân cụ thể:")
add_p("1. Người dùng (User): Là tác nhân tổng quát đại diện cho bất kỳ cá nhân nào được cấp tài khoản để truy nhập vào hệ thống. Tác nhân này thực hiện các hành động cơ bản như đăng nhập, xác thực danh tính, duy trì phiên làm việc theo vai trò và đăng xuất.")
add_p("2. Giảng viên: Là tác nhân nghiệp vụ cốt lõi của hệ thống, kế thừa từ tác nhân Người dùng. Giảng viên trực tiếp thực hiện các nghiệp vụ chuyên môn gồm: biên soạn, sửa, xóa câu hỏi và đáp án đúng (BM1, QĐ1); khởi tạo, chỉnh sửa đề thi kết thúc học phần và phân bổ điểm cho từng câu hỏi (BM2, QĐ2); ghi nhận điểm thi theo lớp học, tự động quy đổi thang điểm chữ (BM3, QĐ3); tra cứu thông tin đề thi đa tiêu chí (BM4); lập báo cáo tổng hợp theo năm học (BM5); và quản lý lớp học cùng danh sách sinh viên phụ trách (BM7, QĐ5). Dữ liệu học thuật của từng giảng viên được phân quyền và bảo mật theo tài khoản cá nhân.")
add_p("3. Quản trị viên (Admin): Là tác nhân kỹ thuật, kế thừa từ tác nhân Người dùng. Quản trị viên chịu trách nhiệm quản lý tài khoản người dùng của giảng viên (BM6, QĐ4), bao gồm cấp mới tài khoản, cập nhật thông tin hồ sơ, kích hoạt, khóa tài khoản hoặc đặt lại mật khẩu đăng nhập. Quản trị viên không can thiệp, không xem và không chỉnh sửa dữ liệu học thuật hay kết quả chấm thi của giảng viên.")
add_p("Lưu ý: Đối tượng Sinh viên không có tài khoản đăng nhập vào hệ thống mà chỉ đóng vai trò là thực thể dữ liệu được lưu trữ và quản lý trong danh sách sinh viên của từng lớp học phục vụ cho việc nhập và lưu kết quả chấm thi.")

add_table_title("Bảng 2.1 Tác nhân của hệ thống")
t_actors_data = [
    ["1", "Người dùng (User)", "Tác nhân cơ sở/tổng quát. Có tài khoản hợp lệ, thực hiện xác thực đăng nhập, duy trì phiên làm việc và đăng xuất."],
    ["2", "Giảng viên", "Tác nhân nghiệp vụ chính (kế thừa từ Người dùng). Quản lý câu hỏi, soạn đề thi, ghi nhận điểm chấm thi, tra cứu, lập báo cáo và quản lý lớp học trong phạm vi tài khoản được cấp."],
    ["3", "Quản trị viên", "Tác nhân quản trị hệ thống (kế thừa từ Người dùng). Quản lý tài khoản giảng viên, phân quyền truy cập, kích hoạt, khóa hoặc đặt lại mật khẩu tài khoản."]
]
create_table(["STT", "Tên tác nhân", "Mô tả tác nhân"], t_actors_data, [0.6, 1.8, 3.8])

# 2.2 Bảng các use case của hệ thống và đặt mã các use case
add_h2("2.2. Bảng các use case của hệ thống và đặt mã các use case")
add_p("Mỗi yêu cầu chức năng nghiệp vụ được xác định ở Chương 1 (Bảng 1.1) được chuyển hóa thành một Use Case cụ thể trong hệ thống. Hệ thống bao gồm 8 Use Case chính được đặt mã từ UC00 đến UC07. Bảng 2.2 trình bày danh sách Use Case, tác nhân tương tác chính và mức độ phức tạp định tính tương ứng:")

add_table_title("Bảng 2.2 Danh sách Use Case của hệ thống")
t_ucs_data = [
    ["1", "UC00", "Đăng nhập / đăng xuất", "Xác thực tài khoản người dùng, khởi tạo và hủy phiên làm việc theo vai trò.", "Người dùng", "Thấp"],
    ["2", "UC01", "Quản lý câu hỏi và nhập đáp án", "Tạo mới, sửa nội dung, xóa câu hỏi và lưu đáp án đúng theo môn học, độ khó (QĐ1).", "Giảng viên", "Trung bình"],
    ["3", "UC02", "Soạn đề thi và phân bổ điểm", "Khởi tạo, sửa, xóa đề thi; chọn 1–5 câu cùng môn và gán điểm sao cho tổng bằng 10 (QĐ2).", "Giảng viên", "Phức tạp"],
    ["4", "UC03", "Ghi nhận chấm thi", "Chọn đề và lớp, nhập điểm số (bội số 0.5), tự động quy đổi điểm chữ A–F và lưu kết quả (QĐ3).", "Giảng viên", "Phức tạp"],
    ["5", "UC04", "Tra cứu đề thi", "Tìm kiếm đề thi đa tiêu chí trong phạm vi dữ liệu thuộc tài khoản giảng viên (BM4).", "Giảng viên", "Thấp"],
    ["6", "UC05", "Lập báo cáo năm", "Thống kê số lượng đề thi, số bài chấm và tính tỷ lệ theo từng môn học trong năm học (BM5).", "Giảng viên", "Trung bình"],
    ["7", "UC06", "Quản lý tài khoản giảng viên", "Tạo tài khoản, cập nhật hồ sơ, kích hoạt, khóa tài khoản hoặc đặt lại mật khẩu (BM6, QĐ4).", "Quản trị viên", "Trung bình"],
    ["8", "UC07", "Quản lý lớp học", "Khởi tạo lớp học mới, sửa thông tin lớp, cập nhật danh sách sinh viên hoặc xóa lớp (BM7, QĐ5).", "Giảng viên", "Trung bình"]
]
create_table(["STT", "Mã UC", "Tên Use Case", "Mô tả Use Case", "Tác nhân", "Độ phức tạp"], t_ucs_data, [0.5, 0.7, 1.6, 2.0, 0.9, 0.8])

# 2.3 Biểu đồ use case
add_h2("2.3. Biểu đồ use case")
add_p("Biểu đồ Use Case mô tả góc nhìn chức năng bên ngoài của hệ thống, thể hiện sự tương tác giữa các tác nhân và các ca sử dụng nằm trong ranh giới hệ thống.")

add_h3("2.3.1. Biểu đồ Use Case tổng quan")
add_p("Biểu đồ Use Case tổng quan (Hình 2.1) thể hiện ranh giới hệ thống Quản lý ra đề và chấm thi (EduExam), các tác nhân tham gia cùng toàn bộ 8 Use Case chính. Giảng viên và Quản trị viên kế thừa quan hệ từ Người dùng để cùng sử dụng chức năng xác thực UC00. Các chức năng chuyên môn học thuật (UC01–UC05 và UC07) được gắn trực tiếp với Giảng viên, trong khi chức năng quản trị tài khoản (UC06) thuộc đặc quyền của Quản trị viên.")
add_img("usecase_overview.png", "Hình 2.1 Biểu đồ Use Case tổng quan", width_in=5.8)

add_h3("2.3.2. Biểu đồ phân rã Use Case")
add_p("Nhằm làm rõ các hành vi và chức năng chi tiết bên trong từng phân hệ, các Use Case từ UC01 đến UC07 được phân rã thành các biểu đồ con tương ứng từ Hình 2.2 đến Hình 2.8.")

add_h4("2.3.2.1. UC01 - Quản lý câu hỏi và nhập đáp án")
add_p("Biểu đồ phân rã UC01 (Hình 2.2) thể hiện các thao tác: Xem danh sách, Thêm câu hỏi, Sửa nội dung câu hỏi và Xóa câu hỏi. Thao tác thêm hoặc sửa luôn bao gồm (<<include>>) thao tác 'Nhập đáp án đúng'. Thao tác sửa hoặc xóa câu hỏi luôn bao gồm bước kiểm tra điều kiện quy định QĐ1: câu hỏi phải chưa thuộc bất kỳ đề thi nào mới được phép thao tác.")
add_img("usecase_uc01.png", "Hình 2.2 Biểu đồ Use Case phân rã UC01 - Quản lý câu hỏi và đáp án", width_in=5.4)

add_h4("2.3.2.2. UC02 - Soạn đề thi và phân bổ điểm")
add_p("Biểu đồ phân rã UC02 (Hình 2.3) thể hiện các thao tác: Tạo đề thi mới, Sửa thông tin đề thi và Xóa đề thi. Khi tạo mới hoặc sửa đề, hệ thống bắt buộc bao gồm (<<include>>) việc chọn từ 1 đến 5 câu hỏi cùng môn thi và phân bổ điểm cho từng câu sao cho tổng điểm bằng 10. Thao tác sửa và xóa đề luôn bao gồm bước kiểm tra quy định QĐ2: đề thi chưa có kết quả chấm thi nào được ghi nhận.")
add_img("usecase_uc02.png", "Hình 2.3 Biểu đồ Use Case phân rã UC02 - Soạn đề và phân bổ điểm", width_in=5.5)

add_h4("2.3.2.3. UC03 - Ghi nhận chấm thi")
add_p("Biểu đồ phân rã UC03 (Hình 2.4) thể hiện các bước: Chọn đề thi và lớp học, Xem danh sách sinh viên lớp, Nhập điểm số sinh viên và Lưu kết quả. Quá trình nhập điểm số bắt buộc bao gồm việc tự động kiểm tra bước điểm 0.5 và quy đổi sang điểm chữ tương ứng từ A đến F theo quy định QĐ3.")
add_img("usecase_uc03.png", "Hình 2.4 Biểu đồ Use Case phân rã UC03 - Ghi nhận chấm thi", width_in=5.3)

add_h4("2.3.2.4. UC04 - Tra cứu đề thi")
add_p("Biểu đồ phân rã UC04 (Hình 2.5) thể hiện các thao tác: Nhập tiêu chí tra cứu, Lọc danh sách đề thi trong phạm vi tài khoản, Xem chi tiết nội dung đề thi và In đề thi theo biểu mẫu chuẩn kết thúc học phần.")
add_img("usecase_uc04.png", "Hình 2.5 Biểu đồ Use Case phân rã UC04 - Tra cứu đề thi", width_in=5.2)

add_h4("2.3.2.5. UC05 - Lập báo cáo năm")
add_p("Biểu đồ phân rã UC05 (Hình 2.6) thể hiện các bước: Chọn năm học báo cáo, Tổng hợp số lượng đề thi và bài chấm theo từng môn, Tự động tính toán các tỷ lệ theo công thức (1.1) và (1.2), và Xuất hiển thị biểu mẫu báo cáo năm BM5.")
add_img("usecase_uc05.png", "Hình 2.6 Biểu đồ Use Case phân rã UC05 - Lập báo cáo năm", width_in=5.3)

add_h4("2.3.2.6. UC06 - Quản lý tài khoản giảng viên")
add_p("Biểu đồ phân rã UC06 (Hình 2.7) thể hiện các quyền năng của Quản trị viên gồm: Xem danh sách tài khoản, Tạo tài khoản giảng viên mới (BM6), Cập nhật thông tin giảng viên, Kích hoạt hoặc khóa tài khoản, và Đặt lại mật khẩu tài khoản theo quy định QĐ4.")
add_img("usecase_uc06.png", "Hình 2.7 Biểu đồ Use Case phân rã UC06 - Quản lý tài khoản giảng viên", width_in=5.3)

add_h4("2.3.2.7. UC07 - Quản lý lớp học")
add_p("Biểu đồ phân rã UC07 (Hình 2.8) thể hiện các thao tác do Giảng viên thực hiện: Xem danh sách lớp học phụ trách, Khởi tạo lớp học mới (BM7), Sửa thông tin lớp, Quản lý thêm/xóa sinh viên trong lớp theo MSSV và Họ tên, và Xóa lớp học (chỉ được thực hiện khi lớp chưa có kết quả chấm thi theo QĐ5).")
add_img("usecase_uc07.png", "Hình 2.8 Biểu đồ Use Case phân rã UC07 - Quản lý lớp học", width_in=5.4)

# 2.4 Đặc tả và phân tích các yêu cầu phần mềm
add_h2("2.4. Đặc tả và phân tích các yêu cầu phần mềm")
add_p("Mục này trình bày chi tiết về đặc tả kịch bản Use Case, mô hình hành vi thông qua biểu đồ hoạt động (Activity Diagram), mô hình tương tác thông qua biểu đồ tuần tự (Sequence Diagram), và biểu đồ lớp phân tích (Analysis Class Diagram) theo đúng kiến trúc Boundary - Control - Entity (ECB).")

add_h3("2.4.1. Đặc tả use case")
add_p("Các Bảng từ 2.3 đến 2.10 trình bày đặc tả cấu trúc của 8 Use Case từ UC00 đến UC07:")

# Bảng 2.3 UC00
add_spec_table("Bảng 2.3 Đặc tả UC00 - Đăng nhập và đăng xuất", [
    ("Mã UC", "UC00"),
    ("Tên UC", "Đăng nhập / đăng xuất"),
    ("Mô tả tóm tắt", "Xác thực danh tính người dùng và khởi tạo phiên làm việc tương ứng với vai trò Giảng viên hoặc Quản trị viên."),
    ("Tác nhân tham gia", "Người dùng (Giảng viên hoặc Quản trị viên)"),
    ("Sự kiện kích hoạt", "Người dùng chọn chức năng 'Đăng nhập' trên giao diện chính."),
    ("Luồng sự kiện chính", "1. Người dùng nhập Tên đăng nhập và Mật khẩu.\n2. Hệ thống kiểm tra thông tin tài khoản và trạng thái hoạt động.\n3. Hệ thống xác định vai trò, khởi tạo phiên làm việc (Session) và hiển thị menu chức năng tương ứng.\n4. Khi người dùng chọn 'Đăng xuất', hệ thống hủy phiên làm việc và trở về màn hình đăng nhập."),
    ("Luồng sự kiện phụ", "Nếu tên đăng nhập không tồn tại, sai mật khẩu hoặc tài khoản đang bị vô hiệu hóa (khóa), hệ thống hiển thị thông báo lỗi và cho phép nhập lại."),
    ("Yêu cầu trước", "Tài khoản người dùng đã được tạo và đang ở trạng thái Hoạt động."),
    ("Yêu cầu sau", "Phiên làm việc được tạo lập với quyền truy cập tương ứng hoặc kết thúc an toàn."),
    ("Yêu cầu phi chức năng", "Mật khẩu được mã hóa băm an toàn; thời gian xác thực dưới 1 giây.")
])

# Bảng 2.4 UC01
add_spec_table("Bảng 2.4 Đặc tả UC01 - Quản lý câu hỏi và nhập đáp án", [
    ("Mã UC", "UC01"),
    ("Tên UC", "Quản lý câu hỏi và nhập đáp án"),
    ("Mô tả tóm tắt", "Giảng viên thêm mới, cập nhật nội dung, xóa câu hỏi và lưu đáp án đúng theo môn học và độ khó."),
    ("Tác nhân tham gia", "Giảng viên đã đăng nhập"),
    ("Sự kiện kích hoạt", "Giảng viên chọn menu 'Quản lý câu hỏi'."),
    ("Luồng sự kiện chính", "1. Giảng viên chọn Môn học và Độ khó (Dễ, Trung Bình, Phức Tạp, Khó).\n2. Nhập nội dung câu hỏi và đáp án đúng.\n3. Nhấn 'Lưu'.\n4. Hệ thống kiểm tra tính hợp lệ dữ liệu và quyền sở hữu tài khoản.\n5. Hệ thống lưu câu hỏi cùng đáp án vào CSDL và cập nhật danh sách hiển thị."),
    ("Luồng sự kiện phụ", "Giảng viên có thể chọn sửa hoặc xóa câu hỏi của mình. Nếu câu hỏi đã thuộc về một đề thi nào đó, hệ thống từ chối xóa/sửa và thông báo lỗi vi phạm quy định QĐ1."),
    ("Yêu cầu trước", "Giảng viên đã đăng nhập; danh mục môn học và độ khó đã có sẵn."),
    ("Yêu cầu sau", "Câu hỏi cùng đáp án được lưu mới, cập nhật hoặc xóa khỏi ngân hàng câu hỏi."),
    ("Yêu cầu phi chức năng", "Thời gian lưu/cập nhật dưới 1 giây; chỉ thao tác trên câu hỏi do chính tài khoản tạo.")
])

# Bảng 2.5 UC02
add_spec_table("Bảng 2.5 Đặc tả UC02 - Soạn đề thi và phân bổ điểm", [
    ("Mã UC", "UC02"),
    ("Tên UC", "Soạn đề thi và phân bổ điểm"),
    ("Mô tả tóm tắt", "Giảng viên khởi tạo, chỉnh sửa hoặc xóa đề thi kết thúc học phần, chọn câu hỏi cùng môn và phân bổ điểm."),
    ("Tác nhân tham gia", "Giảng viên đã đăng nhập"),
    ("Sự kiện kích hoạt", "Giảng viên chọn menu 'Soạn đề thi'."),
    ("Luồng sự kiện chính", "1. Giảng viên nhập Mã đề, Môn thi, Học kỳ, Năm học, Ngày thi và Thời lượng làm bài.\n2. Chọn từ 1 đến 5 câu hỏi từ ngân hàng câu hỏi thuộc cùng môn thi.\n3. Nhập điểm số tối đa cho từng câu hỏi.\n4. Nhấn 'Lưu đề thi'.\n5. Hệ thống kiểm tra: thời lượng 30–180 phút, số lượng 1–5 câu cùng môn và tổng điểm bằng 10.\n6. Hệ thống lưu đề thi và chi tiết phân bổ điểm vào CSDL."),
    ("Luồng sự kiện phụ", "Giảng viên có thể sửa hoặc xóa đề thi. Nếu đề thi đã có kết quả chấm thi được ghi nhận, hệ thống từ chối xóa/sửa và thông báo lỗi vi phạm quy định QĐ2."),
    ("Yêu cầu trước", "Đã có sẵn các câu hỏi cùng môn thi thuộc tài khoản giảng viên."),
    ("Yêu cầu sau", "Đề thi và phân bổ điểm chi tiết được lưu trữ thành công."),
    ("Yêu cầu phi chức năng", "Kiểm tra tổng điểm bằng 10 chính xác trước khi ghi dữ liệu.")
])

# Bảng 2.6 UC03
add_spec_table("Bảng 2.6 Đặc tả UC03 - Ghi nhận chấm thi", [
    ("Mã UC", "UC03"),
    ("Tên UC", "Ghi nhận chấm thi"),
    ("Mô tả tóm tắt", "Giảng viên ghi nhận điểm số thi kết thúc học phần cho sinh viên theo đề thi và lớp học."),
    ("Tác nhân tham gia", "Giảng viên đã đăng nhập"),
    ("Sự kiện kích hoạt", "Giảng viên chọn menu 'Ghi nhận chấm thi'."),
    ("Luồng sự kiện chính", "1. Giảng viên chọn Đề thi và Lớp học cần nhập điểm.\n2. Hệ thống hiển thị danh sách sinh viên của lớp.\n3. Giảng viên nhập điểm số (đã tự làm tròn về 0.5) và ghi chú cho sinh viên.\n4. Nhấn 'Lưu kết quả'.\n5. Hệ thống kiểm tra điểm nằm trong khoảng 0 đến 10 và là bội số của 0.5.\n6. Hệ thống tự động quy đổi điểm chữ (A, B, C, D, E, F theo QĐ3) và lưu vào CSDL."),
    ("Luồng sự kiện phụ", "Nếu điểm số nhập vào không nằm trong khoảng 0–10 hoặc không phải bội số của 0.5, hệ thống hiển thị thông báo lỗi và yêu cầu chỉnh sửa."),
    ("Yêu cầu trước", "Đề thi và lớp học đã được tạo trước đó."),
    ("Yêu cầu sau", "Kết quả chấm thi gồm điểm số, điểm chữ và ghi chú được lưu an toàn."),
    ("Yêu cầu phi chức năng", "Đảm bảo tính toán quy đổi điểm chữ chính xác 100%.")
])

# Bảng 2.7 UC04
add_spec_table("Bảng 2.7 Đặc tả UC04 - Tra cứu đề thi", [
    ("Mã UC", "UC04"),
    ("Tên UC", "Tra cứu đề thi"),
    ("Mô tả tóm tắt", "Giảng viên tra cứu danh sách đề thi theo một hoặc nhiều tiêu chí trong phạm vi tài khoản."),
    ("Tác nhân tham gia", "Giảng viên đã đăng nhập"),
    ("Sự kiện kích hoạt", "Giảng viên chọn menu 'Tra cứu đề thi'."),
    ("Luồng sự kiện chính", "1. Giảng viên nhập một hoặc kết hợp nhiều tiêu chí: Mã đề, Môn học, Học kỳ, Năm học.\n2. Nhấn 'Tra cứu'.\n3. Hệ thống lọc và hiển thị danh sách đề thi thỏa mãn (BM4).\n4. Giảng viên có thể chọn xem chi tiết nội dung đề thi hoặc in đề thi theo biểu mẫu chuẩn."),
    ("Luồng sự kiện phụ", "Nếu không tìm thấy đề thi thỏa mãn tiêu chí, hệ thống hiển thị thông báo 'Không tìm thấy kết quả phù hợp'."),
    ("Yêu cầu trước", "Dữ liệu đề thi đã được tạo lập trong hệ thống."),
    ("Yêu cầu sau", "Danh sách đề thi phù hợp được hiển thị trên giao diện."),
    ("Yêu cầu phi chức năng", "Tốc độ phản hồi tra cứu dưới 1 giây.")
])

# Bảng 2.8 UC05
add_spec_table("Bảng 2.8 Đặc tả UC05 - Lập báo cáo năm", [
    ("Mã UC", "UC05"),
    ("Tên UC", "Lập báo cáo năm"),
    ("Mô tả tóm tắt", "Giảng viên tổng hợp tình hình ra đề và chấm thi theo từng môn học trong một năm học."),
    ("Tác nhân tham gia", "Giảng viên đã đăng nhập"),
    ("Sự kiện kích hoạt", "Giảng viên chọn menu 'Lập báo cáo năm'."),
    ("Luồng sự kiện chính", "1. Giảng viên chọn Năm học cần báo cáo.\n2. Nhấn 'Lập báo cáo'.\n3. Hệ thống tổng hợp số lượng đề thi và số bài chấm của tài khoản theo từng môn.\n4. Hệ thống tính tỷ lệ đề thi (công thức 1.1) và tỷ lệ bài chấm (công thức 1.2).\n5. Hệ thống hiển thị bảng báo cáo hoàn chỉnh theo biểu mẫu BM5."),
    ("Luồng sự kiện phụ", "Nếu năm học chưa có dữ liệu đề thi hoặc bài chấm, tỷ lệ tương ứng hiển thị 0% và hệ thống vẫn hiển thị bảng báo cáo."),
    ("Yêu cầu trước", "Năm học được chọn hợp lệ."),
    ("Yêu cầu sau", "Báo cáo tổng hợp năm được hiển thị đầy đủ và có thể xuất in."),
    ("Yêu cầu phi chức năng", "Tính toán số liệu và tỷ lệ phần trăm chính xác theo công thức quy định.")
])

# Bảng 2.9 UC06
add_spec_table("Bảng 2.9 Đặc tả UC06 - Quản lý tài khoản giảng viên", [
    ("Mã UC", "UC06"),
    ("Tên UC", "Quản lý tài khoản giảng viên"),
    ("Mô tả tóm tắt", "Quản trị viên quản lý danh sách tài khoản, hồ sơ giảng viên và phân quyền trạng thái hoạt động."),
    ("Tác nhân tham gia", "Quản trị viên"),
    ("Sự kiện kích hoạt", "Quản trị viên chọn menu 'Quản lý tài khoản'."),
    ("Luồng sự kiện chính", "1. Quản trị viên xem danh sách tài khoản giảng viên (BM6).\n2. Chọn Tạo tài khoản mới hoặc Sửa thông tin tài khoản đã có.\n3. Nhập Tên đăng nhập, Mật khẩu, Họ và tên giảng viên và Trạng thái.\n4. Nhấn 'Lưu'.\n5. Hệ thống kiểm tra tên đăng nhập duy nhất (QĐ4) và lưu thay đổi."),
    ("Luồng sự kiện phụ", "Nếu tên đăng nhập đã tồn tại, hệ thống báo lỗi trùng lặp. Khi tài khoản đã có dữ liệu tham chiếu (câu hỏi, đề thi, lớp học), hệ thống không cho phép xóa cứng mà chỉ hỗ trợ vô hiệu hóa (khóa) theo QĐ4."),
    ("Yêu cầu trước", "Quản trị viên đã đăng nhập thành công vào hệ thống."),
    ("Yêu cầu sau", "Tài khoản giảng viên được tạo mới hoặc cập nhật trạng thái."),
    ("Yêu cầu phi chức năng", "Chỉ quản trị viên mới có quyền thao tác trên Use Case này.")
])

# Bảng 2.10 UC07
add_spec_table("Bảng 2.10 Đặc tả UC07 - Quản lý lớp học", [
    ("Mã UC", "UC07"),
    ("Tên UC", "Quản lý lớp học"),
    ("Mô tả tóm tắt", "Giảng viên khởi tạo lớp học mới, cập nhật danh sách sinh viên phụ trách hoặc xóa lớp học."),
    ("Tác nhân tham gia", "Giảng viên đã đăng nhập"),
    ("Sự kiện kích hoạt", "Giảng viên chọn menu 'Quản lý lớp học'."),
    ("Luồng sự kiện chính", "1. Giảng viên nhập Mã lớp duy nhất và Tên lớp (BM7).\n2. Cập nhật danh sách sinh viên gồm Họ tên và MSSV.\n3. Nhấn 'Lưu lớp học'.\n4. Hệ thống kiểm tra tính duy nhất của Mã lớp và tính hợp lệ của MSSV.\n5. Hệ thống lưu lớp học cùng danh sách sinh viên vào CSDL."),
    ("Luồng sự kiện phụ", "Giảng viên có thể sửa thông tin lớp hoặc xóa lớp. Nếu lớp học đã có dữ liệu kết quả chấm thi, hệ thống từ chối xóa và hiển thị thông báo lỗi vi phạm quy định QĐ5."),
    ("Yêu cầu trước", "Giảng viên đã đăng nhập vào hệ thống."),
    ("Yêu cầu sau", "Lớp học và danh sách sinh viên được lưu trữ hoặc cập nhật thành công."),
    ("Yêu cầu phi chức năng", "Dữ liệu lớp học được quản lý phân lập theo tài khoản giảng viên.")
])

# 2.4.2 Biểu đồ hoạt động
add_h3("2.4.2. Biểu đồ hoạt động")
add_p("Biểu đồ hoạt động (Activity Diagram) tập trung mô tả luồng điều khiển và quy trình xử lý dữ liệu của từng chức năng. Các biểu đồ sử dụng ký pháp chuẩn gồm: 2 làn bơi (Swimlanes) phân định trách nhiệm của Tác nhân và Hệ thống; Nút bắt đầu (Initial state); Các hoạt động (Activity); Nút quyết định rẽ nhánh điều kiện (Decision) kèm nhãn điều kiện (Guard); và Nút kết thúc (Final state).")
add_p("Từ Hình 2.9 đến Hình 2.16 thể hiện biểu đồ hoạt động của toàn bộ 8 Use Case từ UC00 đến UC07:")

add_h4("2.4.2.1. UC00 - Đăng nhập và đăng xuất")
add_p("Hình 2.9 mô tả quy trình đăng nhập hệ thống: người dùng nhập thông tin xác thực, hệ thống kiểm tra mật khẩu băm và trạng thái hoạt động. Nếu hợp lệ, hệ thống khởi tạo phiên làm việc và phân quyền chức năng; nếu không hợp lệ, hệ thống thông báo lỗi và yêu cầu nhập lại.")
add_img("activity_uc00.png", "Hình 2.9 Biểu đồ hoạt động UC00 - Đăng nhập và đăng xuất", width_in=5.4)

add_h4("2.4.2.2. UC01 - Quản lý câu hỏi và nhập đáp án")
add_p("Hình 2.10 mô tả quy trình quản lý câu hỏi: giảng viên thực hiện tạo mới, sửa hoặc xóa câu hỏi. Hệ thống kiểm tra tính hợp lệ dữ liệu và kiểm tra ràng buộc QĐ1 (câu hỏi chưa thuộc đề thi nào).")
add_img("activity_uc01.png", "Hình 2.10 Biểu đồ hoạt động UC01 - Quản lý câu hỏi và nhập đáp án", width_in=5.4)

add_h4("2.4.2.3. UC02 - Soạn đề thi và phân bổ điểm")
add_p("Hình 2.11 mô tả quy trình soạn đề thi: giảng viên nhập thông tin đề, chọn câu hỏi cùng môn và phân bổ điểm. Hệ thống kiểm tra thời lượng 30–180 phút, số lượng 1–5 câu, tổng điểm bằng 10 và đề chưa có kết quả chấm theo quy định QĐ2.")
add_img("activity_uc02.png", "Hình 2.11 Biểu đồ hoạt động UC02 - Soạn đề thi và phân bổ điểm", width_in=5.4)

add_h4("2.4.2.4. UC03 - Ghi nhận chấm thi")
add_p("Hình 2.12 mô tả quy trình chấm thi: giảng viên chọn đề và lớp học, nhập điểm số cho sinh viên. Hệ thống kiểm tra thang điểm 0–10, bước điểm 0.5 và tự động quy đổi thang điểm chữ A–F theo quy định QĐ3.")
add_img("activity_uc03.png", "Hình 2.12 Biểu đồ hoạt động UC03 - Ghi nhận chấm thi", width_in=5.4)

add_h4("2.4.2.5. UC04 - Tra cứu đề thi")
add_p("Hình 2.13 mô tả quy trình tra cứu đề thi: giảng viên nhập tiêu chí tìm kiếm, hệ thống truy vấn và hiển thị danh sách đề thi thuộc phạm vi tài khoản, cho phép xem chi tiết hoặc in đề thi.")
add_img("activity_uc04.png", "Hình 2.13 Biểu đồ hoạt động UC04 - Tra cứu đề thi", width_in=5.4)

add_h4("2.4.2.6. UC05 - Lập báo cáo năm")
add_p("Hình 2.14 mô tả quy trình lập báo cáo: giảng viên chọn năm học, hệ thống tự động tổng hợp số lượng đề thi, bài chấm theo môn và tính các tỷ lệ theo công thức (1.1) và (1.2) để hiển thị biểu mẫu BM5.")
add_img("activity_uc05.png", "Hình 2.14 Biểu đồ hoạt động UC05 - Lập báo cáo năm", width_in=5.4)

add_h4("2.4.2.7. UC06 - Quản lý tài khoản giảng viên")
add_p("Hình 2.15 mô tả quy trình quản trị tài khoản: quản trị viên nhập thông tin tài khoản giảng viên, hệ thống kiểm tra tên đăng nhập duy nhất và kiểm tra không xóa cứng tài khoản đã có dữ liệu theo quy định QĐ4.")
add_img("activity_uc06.png", "Hình 2.15 Biểu đồ hoạt động UC06 - Quản lý tài khoản giảng viên", width_in=5.4)

add_h4("2.4.2.8. UC07 - Quản lý lớp học")
add_p("Hình 2.16 mô tả quy trình quản lý lớp học: giảng viên tạo lớp mới, cập nhật danh sách sinh viên hoặc xóa lớp. Hệ thống kiểm tra tính duy nhất của mã lớp và kiểm tra lớp chưa có kết quả chấm thi theo quy định QĐ5.")
add_img("activity_uc07.png", "Hình 2.16 Biểu đồ hoạt động UC07 - Quản lý lớp học", width_in=5.4)

# 2.4.3 Biểu đồ tuần tự
add_h3("2.4.3. Biểu đồ tuần tự")
add_p("Biểu đồ tuần tự (Sequence Diagram) mô tả chi tiết sự tương tác động theo thời gian giữa các đối tượng tham gia thực hiện ca sử dụng. Mỗi biểu đồ bao gồm 4 đường đời (Lifelines): Tác nhân người dùng, Lớp giao tiếp (:GiaoDien), Lớp điều khiển (:BoXuLy) và Lớp thực thể/CSDL (:CoSoDuLieu), kết hợp cùng khung điều kiện tương tác (Alt Frame) biểu diễn luồng thực thi thành công và luồng xử lý ngoại lệ vi phạm quy định.")
add_p("Từ Hình 2.17 đến Hình 2.24 thể hiện biểu đồ tuần tự đầy đủ của 8 Use Case từ UC00 đến UC07:")

add_h4("2.4.3.1. UC00 - Đăng nhập và đăng xuất")
add_p("Hình 2.17 mô tả trình tự tương tác đăng nhập: thông tin tài khoản được gửi từ giao diện đến bộ xử lý để xác thực với CSDL, trả về phiên làm việc hợp lệ hoặc hiển thị thông báo lỗi.")
add_img("sequence_uc00.png", "Hình 2.17 Biểu đồ tuần tự UC00 - Đăng nhập và đăng xuất", width_in=5.5)

add_h4("2.4.3.2. UC01 - Quản lý câu hỏi và nhập đáp án")
add_p("Hình 2.18 mô tả trình tự lưu hoặc xóa câu hỏi: bộ xử lý kiểm tra tình trạng sử dụng của câu hỏi trong các đề thi trước khi cho phép ghi nhận thay đổi vào CSDL.")
add_img("sequence_uc01.png", "Hình 2.18 Biểu đồ tuần tự UC01 - Quản lý câu hỏi và nhập đáp án", width_in=5.5)

add_h4("2.4.3.3. UC02 - Soạn đề thi và phân bổ điểm")
add_p("Hình 2.19 mô tả trình tự lưu đề thi: bộ xử lý kiểm tra các ràng buộc thời lượng, số câu, tổng điểm 10 và tình trạng chấm thi của đề trước khi ghi dữ liệu.")
add_img("sequence_uc02.png", "Hình 2.19 Biểu đồ tuần tự UC02 - Soạn đề thi và phân bổ điểm", width_in=5.5)

add_h4("2.4.3.4. UC03 - Ghi nhận chấm thi")
add_p("Hình 2.20 mô tả trình tự chấm thi: bộ xử lý tiếp nhận bảng điểm, kiểm tra bước điểm 0.5, thực hiện quy đổi điểm chữ A–F và lưu kết quả vào CSDL.")
add_img("sequence_uc03.png", "Hình 2.20 Biểu đồ tuần tự UC03 - Ghi nhận chấm thi", width_in=5.5)

add_h4("2.4.3.5. UC04 - Tra cứu đề thi")
add_p("Hình 2.21 mô tả trình tự tra cứu đề thi: giao diện gửi tiêu chí tìm kiếm kèm ID tài khoản đăng nhập để bộ xử lý truy vấn danh sách đề tương ứng từ CSDL.")
add_img("sequence_uc04.png", "Hình 2.21 Biểu đồ tuần tự UC04 - Tra cứu đề thi", width_in=5.5)

add_h4("2.4.3.6. UC05 - Lập báo cáo năm")
add_p("Hình 2.22 mô tả trình tự lập báo cáo năm: bộ xử lý lấy số liệu đề thi và bài chấm từ CSDL, tính toán các tổng số và tỷ lệ phần trăm theo công thức (1.1), (1.2) để trả về giao diện.")
add_img("sequence_uc05.png", "Hình 2.22 Biểu đồ tuần tự UC05 - Lập báo cáo năm", width_in=5.5)

add_h4("2.4.3.7. UC06 - Quản lý tài khoản giảng viên")
add_p("Hình 2.23 mô tả trình tự quản lý tài khoản: quản trị viên gửi thông tin cập nhật tài khoản, bộ xử lý kiểm tra tính duy nhất của tên đăng nhập trước khi ghi vào CSDL.")
add_img("sequence_uc06.png", "Hình 2.23 Biểu đồ tuần tự UC06 - Quản lý tài khoản giảng viên", width_in=5.5)

add_h4("2.4.3.8. UC07 - Quản lý lớp học")
add_p("Hình 2.24 mô tả trình tự quản lý lớp học: giảng viên gửi thông tin lớp và DSSV, bộ xử lý kiểm tra mã lớp duy nhất và kiểm tra lớp chưa có kết quả chấm trước khi lưu hoặc xóa.")
add_img("sequence_uc07.png", "Hình 2.24 Biểu đồ tuần tự UC07 - Quản lý lớp học", width_in=5.5)

# 2.4.4 Biểu đồ lớp phân tích theo Use Case
add_h3("2.4.4. Biểu đồ lớp phân tích theo Use Case")
add_p("Biểu đồ lớp phân tích áp dụng mô hình kiến trúc phân tích Hướng đối tượng tiêu chuẩn gồm 3 loại lớp: Lớp giao tiếp (<<boundary>>), Lớp điều khiển (<<control>>) và Lớp thực thể (<<entity>>). Mỗi lớp được thể hiện đầy đủ tên lớp, thuộc tính chính kèm kiểu dữ liệu, các phương thức nghiệp vụ và bản số quan hệ (Multiplicity).")
add_p("Từ Hình 2.25 đến Hình 2.32 thể hiện biểu đồ lớp phân tích của 8 Use Case từ UC00 đến UC07:")

add_h4("2.4.4.1. UC00 - Đăng nhập và phân quyền truy cập")
add_p("Hình 2.25 biểu diễn lớp giao diện FormDangNhap, lớp điều khiển DangNhapController và lớp thực thể TaiKhoan.")
add_img("class_uc00.png", "Hình 2.25 Biểu đồ lớp phân tích UC00 - Đăng nhập và phân quyền truy cập", width_in=5.5)

add_h4("2.4.4.2. UC01 - Quản lý câu hỏi và nhập đáp án")
add_p("Hình 2.26 biểu diễn FormQuanLyCauHoi, CauHoiController cùng hai thực thể CauHoi và MonHoc.")
add_img("class_uc01.png", "Hình 2.26 Biểu đồ lớp phân tích UC01 - Quản lý câu hỏi và nhập đáp án", width_in=5.5)

add_h4("2.4.4.3. UC02 - Soạn đề thi và phân bổ điểm")
add_p("Hình 2.27 biểu diễn FormSoanDeThi, DeThiController cùng các thực thể DeThi và DeThi_CauHoi.")
add_img("class_uc02.png", "Hình 2.27 Biểu đồ lớp phân tích UC02 - Soạn đề thi và phân bổ điểm", width_in=5.5)

add_h4("2.4.4.4. UC03 - Ghi nhận chấm thi")
add_p("Hình 2.28 biểu diễn FormGhiNhanChamThi, ChamThiController cùng các thực thể KetQuaThi và SinhVien.")
add_img("class_uc03.png", "Hình 2.28 Biểu đồ lớp phân tích UC03 - Ghi nhận chấm thi", width_in=5.5)

add_h4("2.4.4.5. UC04 - Tra cứu đề thi")
add_p("Hình 2.29 biểu diễn FormTraCuuDeThi, TraCuuController và thực thể DeThi.")
add_img("class_uc04.png", "Hình 2.29 Biểu đồ lớp phân tích UC04 - Tra cứu đề thi", width_in=5.5)

add_h4("2.4.4.6. UC05 - Lập báo cáo năm")
add_p("Hình 2.30 biểu diễn FormBaoCaoNam, BaoCaoController cùng các thực thể DeThi và KetQuaThi phục vụ thống kê.")
add_img("class_uc05.png", "Hình 2.30 Biểu đồ lớp phân tích UC05 - Lập báo cáo năm", width_in=5.5)

add_h4("2.4.4.7. UC06 - Quản lý tài khoản giảng viên")
add_p("Hình 2.31 biểu diễn FormQuanLyTaiKhoan, TaiKhoanController và thực thể TaiKhoan phục vụ quản trị viên.")
add_img("class_uc06.png", "Hình 2.31 Biểu đồ lớp phân tích UC06 - Quản lý tài khoản giảng viên", width_in=5.5)

add_h4("2.4.4.8. UC07 - Quản lý lớp học")
add_p("Hình 2.32 biểu diễn FormQuanLyLopHoc, LopHocController cùng các thực thể Lop và SinhVien do giảng viên quản lý.")
add_img("class_uc07.png", "Hình 2.32 Biểu đồ lớp phân tích UC07 - Quản lý lớp học", width_in=5.5)

# 2.5 Xây dựng biểu đồ thực thể liên kết (ERD)
add_h2("2.5. Xây dựng biểu đồ thực thể liên kết (ERD)")
add_p("Biểu đồ thực thể liên kết (Entity-Relationship Diagram - ERD) thể hiện cấu trúc dữ liệu quan hệ hoàn chỉnh của hệ thống, khớp 100% với 7 biểu mẫu nghiệp vụ (BM1–BM7) ở Chương 1 và cơ sở dữ liệu vật lý. Hệ thống gồm 8 thực thể dữ liệu chính:")
add_p("1. TaiKhoan: Lưu trữ thông tin tài khoản người dùng gồm mã định danh id (PK), tên đăng nhập tenDangNhap, mật khẩu đã mã hóa băm matKhauHash, họ tên người dùng hoTen, vai trò vaiTro (Giảng viên/Quản trị viên) và trạng thái tài khoản trangThai (Hoạt động/Khóa).")
add_p("2. MonHoc: Lưu trữ danh mục môn học gồm mã môn maMon (PK) và tên môn học tenMon (4 môn học theo QĐ1: IT001, IT002, IT003, SE104).")
add_p("3. CauHoi: Lưu trữ ngân hàng câu hỏi gồm mã câu hỏi maCauHoi (PK), mã môn maMon (FK), độ khó doKho (Dễ, Trung Bình, Phức Tạp, Khó theo QĐ1), nội dung câu hỏi noiDung, đáp án đúng dapAn, và tài khoản sở hữu taiKhoanId (FK).")
add_p("4. DeThi: Lưu trữ đề thi gồm mã đề thi maDe (PK), mã môn thi maMon (FK), học kỳ hocKy, năm học namHoc, ngày thi ngayThi, thời lượng thi thoiLuong (30–180 phút theo QĐ2), tổng điểm tối đa tongDiem (= 10), và tài khoản sở hữu taiKhoanId (FK).")
add_p("5. DeThi_CauHoi: Thực thể kết hợp biểu diễn mối quan hệ nhiều-nhiều (N-N) giữa Đề thi và Câu hỏi. Khóa chính phức hợp gồm (maDe, maCauHoi) vừa là PK vừa là FK. Mỗi bản ghi lưu số thứ tự câu hỏi thuTu và số điểm tối đa phân bổ cho câu hỏi diem (tổng điểm các câu thuộc đề luôn bằng 10 theo QĐ2).")
add_p("6. Lop: Lưu trữ thông tin lớp học gồm mã lớp maLop (PK), tên lớp tenLop, và tài khoản giảng viên phụ trách taiKhoanId (FK) theo BM7 và QĐ5.")
add_p("7. SinhVien: Lưu trữ thông tin sinh viên thuộc lớp gồm mã số sinh viên mssv (PK), mã lớp maLop (FK), và họ tên sinh viên hoTen.")
add_p("8. KetQuaThi: Lưu trữ kết quả chấm thi kết thúc học phần gồm mã định danh id (PK), mã đề thi maDe (FK), mã sinh viên mssv (FK), điểm số diemSo (0–10, bội số 0.5 theo QĐ3), điểm chữ quy đổi diemChu (A, B, C, D, E, F theo QĐ3), ghi chú ghiChu, và thời gian ghi nhận điểm ngayCham.")

add_p("Mối quan hệ giữa các thực thể:")
add_p("- MonHoc liên kết 1–N với CauHoi: Một môn học có thể có nhiều câu hỏi; mỗi câu hỏi thuộc về duy nhất một môn học.")
add_p("- MonHoc liên kết 1–N với DeThi: Một môn học có thể có nhiều đề thi; mỗi đề thi được biên soạn cho duy nhất một môn thi.")
add_p("- DeThi và CauHoi liên kết N–N thông qua thực thể kết hợp DeThi_CauHoi: Một đề thi có từ 1 đến 5 câu hỏi; một câu hỏi có thể được sử dụng trong nhiều đề thi khác nhau.")
add_p("- Lop liên kết 1–N với SinhVien: Một lớp học có nhiều sinh viên; mỗi sinh viên thuộc về một lớp học cụ thể.")
add_p("- DeThi và SinhVien liên kết 1–N với KetQuaThi: Mỗi kết quả chấm thi gắn liền với một đề thi cụ thể và một sinh viên cụ thể.")
add_p("- TaiKhoan liên kết 1–N với CauHoi, DeThi, Lop: Đảm bảo phân lập và bảo mật dữ liệu học thuật riêng biệt theo từng tài khoản giảng viên.")

add_img("erd_system.png", "Hình 2.33 Biểu đồ thực thể liên kết (ERD) toàn hệ thống", width_in=6.0)

doc.save(DOC_PATH)
print("SUCCESS: Updated Chapter 2 in report-chuong12.docx!")
