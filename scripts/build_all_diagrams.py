import os
import xml.etree.ElementTree as ET

DRAWIO_DIR = "Đồ án/drawio"
os.makedirs(DRAWIO_DIR, exist_ok=True)

FONT = "fontFamily=Times New Roman;"
S_ACTOR = f"shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;strokeColor=#000000;fillColor=#FFFFFF;fontColor=#000000;{FONT}fontSize=14;fontStyle=1;"
S_UC = f"ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;{FONT}fontSize=13;fontStyle=0;"
S_BOUND = f"swimlane;startSize=32;horizontal=1;html=1;fillColor=#F8FAFC;swimlaneFillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;{FONT}fontSize=15;fontStyle=1;"
S_SWIM = f"swimlane;startSize=35;horizontal=1;html=1;fillColor=#F1F5F9;swimlaneFillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;{FONT}fontSize=15;fontStyle=1;"
S_START = "ellipse;fillColor=#000000;strokeColor=#000000;html=1;"
S_END = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;"
S_ACTION = f"rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;{FONT}fontSize=13;arcSize=20;"
S_DECISION = f"rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;{FONT}fontSize=12;"
S_FLOW = f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#000000;endArrow=block;endFill=1;fontColor=#000000;{FONT}fontSize=12;"
S_LINE = f"edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#000000;endArrow=none;fontColor=#000000;{FONT}fontSize=12;"
S_GEN = f"edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#000000;endArrow=block;endFill=0;fontColor=#000000;{FONT}fontSize=12;"
S_INC = f"edgeStyle=orthogonalEdgeStyle;html=1;strokeColor=#000000;dashed=1;endArrow=open;endFill=0;fontColor=#000000;{FONT}fontSize=11;"
S_LIFE = f"shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;outlineConnect=0;size=40;strokeColor=#000000;fillColor=#F8FAFC;fontColor=#000000;{FONT}fontSize=13;fontStyle=1;"
S_SYNC = f"edgeStyle=none;html=1;strokeColor=#000000;endArrow=block;endFill=1;fontColor=#000000;{FONT}fontSize=12;"
S_RET = f"edgeStyle=none;html=1;strokeColor=#000000;endArrow=open;endFill=0;dashed=1;fontColor=#000000;{FONT}fontSize=12;"
S_ALT = f"shape=umlFrame;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontColor=#000000;{FONT}fontSize=12;"
S_CLASS = f"swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;html=1;fillColor=#EFF6FF;strokeColor=#000000;fontColor=#000000;{FONT}fontSize=13;"
S_SEC = f"text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=6;spacingRight=4;overflow=hidden;rotatable=0;{FONT}fontSize=11;fontColor=#000000;"
S_ERD = f"swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;html=1;fillColor=#F8FAFC;strokeColor=#000000;fontColor=#000000;{FONT}fontSize=13;"

def cell(cid, val, style, vertex="1", parent="1", x=0, y=0, w=100, h=50, edge=None, source=None, target=None, points=None):
    attribs = {"id": str(cid), "value": str(val), "style": style, "parent": str(parent)}
    if edge:
        attribs["edge"] = "1"
        if source: attribs["source"] = str(source)
        if target: attribs["target"] = str(target)
    else:
        attribs["vertex"] = str(vertex)
    el = ET.Element("mxCell", attribs)
    if not edge:
        ET.SubElement(el, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), attrib={"as": "geometry"})
    else:
        geom = ET.SubElement(el, "mxGeometry", relative="1", attrib={"as": "geometry"})
        if points:
            arr = ET.SubElement(geom, "Array", attrib={"as": "points"})
            for px, py in points:
                ET.SubElement(arr, "mxPoint", x=str(px), y=str(py))
    return el

all_diagrams = {}

def add_diag(name, cells):
    all_diagrams[name] = cells

# ==========================================
# 1. BIỂU ĐỒ USE CASE TỔNG QUAN (Hình 2.1)
# ==========================================
c_uc00 = [
    cell("user", "Người dùng", S_ACTOR, x=80, y=140, w=45, h=80),
    cell("gv", "Giảng viên", S_ACTOR, x=80, y=430, w=45, h=80),
    cell("admin", "Quản trị viên", S_ACTOR, x=80, y=780, w=45, h=80),
    cell("gen_gv", "", S_GEN, edge=1, source="gv", target="user"),
    cell("gen_admin", "", S_GEN, edge=1, source="admin", target="user"),
    cell("sys", "Hệ thống Quản lý ra đề và chấm thi (EduExam)", S_BOUND, x=260, y=40, w=580, h=860),
    cell("u0", "UC00: Đăng nhập / đăng xuất", S_UC, x=420, y=90, w=260, h=55),
    cell("u1", "UC01: Quản lý câu hỏi và nhập đáp án", S_UC, x=420, y=190, w=260, h=55),
    cell("u2", "UC02: Soạn đề thi và phân bổ điểm", S_UC, x=420, y=285, w=260, h=55),
    cell("u3", "UC03: Ghi nhận chấm thi", S_UC, x=420, y=380, w=260, h=55),
    cell("u4", "UC04: Tra cứu đề thi", S_UC, x=420, y=475, w=260, h=55),
    cell("u5", "UC05: Lập báo cáo năm", S_UC, x=420, y=570, w=260, h=55),
    cell("u7", "UC07: Quản lý lớp học", S_UC, x=420, y=665, w=260, h=55),
    cell("u6", "UC06: Quản lý tài khoản giảng viên", S_UC, x=420, y=785, w=260, h=55),
    cell("l0", "", S_LINE, edge=1, source="user", target="u0"),
    cell("l1", "", S_LINE, edge=1, source="gv", target="u1"),
    cell("l2", "", S_LINE, edge=1, source="gv", target="u2"),
    cell("l3", "", S_LINE, edge=1, source="gv", target="u3"),
    cell("l4", "", S_LINE, edge=1, source="gv", target="u4"),
    cell("l5", "", S_LINE, edge=1, source="gv", target="u5"),
    cell("l7", "", S_LINE, edge=1, source="gv", target="u7"),
    cell("l6", "", S_LINE, edge=1, source="admin", target="u6")
]
add_diag("Hình 2.1 Biểu đồ Use Case tổng quan", c_uc00)

# ==========================================
# 2. BIỂU ĐỒ PHÂN RÃ UC01 (Hình 2.2)
# ==========================================
c_uc01 = [
    cell("gv", "Giảng viên", S_ACTOR, x=60, y=220, w=45, h=80),
    cell("sys", "Phân hệ Quản lý câu hỏi (UC01)", S_BOUND, x=230, y=40, w=560, h=470),
    cell("u1_1", "Xem danh sách câu hỏi", S_UC, x=370, y=75, w=230, h=50),
    cell("u1_2", "Thêm câu hỏi mới", S_UC, x=370, y=155, w=230, h=50),
    cell("u1_3", "Sửa nội dung câu hỏi", S_UC, x=370, y=240, w=230, h=50),
    cell("u1_4", "Xóa câu hỏi", S_UC, x=370, y=325, w=230, h=50),
    cell("u1_5", "Nhập đáp án đúng", S_UC, x=510, y=415, w=200, h=50),
    cell("u1_6", "Kiểm tra chưa thuộc đề thi (QĐ1)", S_UC, x=270, y=415, w=210, h=50),
    cell("l1", "", S_LINE, edge=1, source="gv", target="u1_1"),
    cell("l2", "", S_LINE, edge=1, source="gv", target="u1_2"),
    cell("l3", "", S_LINE, edge=1, source="gv", target="u1_3"),
    cell("l4", "", S_LINE, edge=1, source="gv", target="u1_4"),
    cell("inc1", "&laquo;include&raquo;", S_INC, edge=1, source="u1_2", target="u1_5"),
    cell("inc2", "&laquo;include&raquo;", S_INC, edge=1, source="u1_3", target="u1_5"),
    cell("inc3", "&laquo;include&raquo;", S_INC, edge=1, source="u1_3", target="u1_6"),
    cell("inc4", "&laquo;include&raquo;", S_INC, edge=1, source="u1_4", target="u1_6")
]
add_diag("Hình 2.2 Biểu đồ Use Case phân rã UC01", c_uc01)

# ==========================================
# 3. BIỂU ĐỒ PHÂN RÃ UC02 (Hình 2.3)
# ==========================================
c_uc02 = [
    cell("gv", "Giảng viên", S_ACTOR, x=60, y=230, w=45, h=80),
    cell("sys", "Phân hệ Soạn đề thi và phân bổ điểm (UC02)", S_BOUND, x=230, y=40, w=580, h=490),
    cell("u2_1", "Tạo đề thi mới", S_UC, x=370, y=75, w=240, h=50),
    cell("u2_2", "Sửa thông tin đề thi", S_UC, x=370, y=165, w=240, h=50),
    cell("u2_3", "Xóa đề thi", S_UC, x=370, y=255, w=240, h=50),
    cell("u2_4", "Chọn câu hỏi cùng môn (1–5 câu)", S_UC, x=510, y=355, w=220, h=50),
    cell("u2_5", "Phân bổ điểm (tổng = 10, QĐ2)", S_UC, x=510, y=440, w=220, h=50),
    cell("u2_6", "Kiểm tra chưa có điểm chấm (QĐ2)", S_UC, x=260, y=390, w=220, h=50),
    cell("l1", "", S_LINE, edge=1, source="gv", target="u2_1"),
    cell("l2", "", S_LINE, edge=1, source="gv", target="u2_2"),
    cell("l3", "", S_LINE, edge=1, source="gv", target="u2_3"),
    cell("inc1", "&laquo;include&raquo;", S_INC, edge=1, source="u2_1", target="u2_4"),
    cell("inc2", "&laquo;include&raquo;", S_INC, edge=1, source="u2_1", target="u2_5"),
    cell("inc3", "&laquo;include&raquo;", S_INC, edge=1, source="u2_2", target="u2_4"),
    cell("inc4", "&laquo;include&raquo;", S_INC, edge=1, source="u2_2", target="u2_5"),
    cell("inc5", "&laquo;include&raquo;", S_INC, edge=1, source="u2_2", target="u2_6"),
    cell("inc6", "&laquo;include&raquo;", S_INC, edge=1, source="u2_3", target="u2_6")
]
add_diag("Hình 2.3 Biểu đồ Use Case phân rã UC02", c_uc02)

# ==========================================
# 4. BIỂU ĐỒ PHÂN RÃ UC03 (Hình 2.4)
# ==========================================
c_uc03 = [
    cell("gv", "Giảng viên", S_ACTOR, x=60, y=200, w=45, h=80),
    cell("sys", "Phân hệ Ghi nhận chấm thi (UC03)", S_BOUND, x=230, y=40, w=540, h=410),
    cell("u3_1", "Chọn đề thi và lớp học", S_UC, x=370, y=75, w=250, h=50),
    cell("u3_2", "Xem danh sách sinh viên lớp", S_UC, x=370, y=155, w=250, h=50),
    cell("u3_3", "Nhập điểm số (0–10, bước 0.5)", S_UC, x=370, y=240, w=250, h=50),
    cell("u3_4", "Tự động quy đổi điểm chữ A–F (QĐ3)", S_UC, x=470, y=330, w=240, h=50),
    cell("u3_5", "Lưu kết quả chấm thi", S_UC, x=260, y=330, w=180, h=50),
    cell("l1", "", S_LINE, edge=1, source="gv", target="u3_1"),
    cell("l2", "", S_LINE, edge=1, source="gv", target="u3_2"),
    cell("l3", "", S_LINE, edge=1, source="gv", target="u3_3"),
    cell("l5", "", S_LINE, edge=1, source="gv", target="u3_5"),
    cell("inc1", "&laquo;include&raquo;", S_INC, edge=1, source="u3_3", target="u3_4")
]
add_diag("Hình 2.4 Biểu đồ Use Case phân rã UC03", c_uc03)

# ==========================================
# 5. BIỂU ĐỒ PHÂN RÃ UC04 (Hình 2.5)
# ==========================================
c_uc04 = [
    cell("gv", "Giảng viên", S_ACTOR, x=60, y=180, w=45, h=80),
    cell("sys", "Phân hệ Tra cứu đề thi (UC04)", S_BOUND, x=230, y=40, w=520, h=360),
    cell("u4_1", "Nhập tiêu chí tra cứu", S_UC, x=360, y=75, w=260, h=50),
    cell("u4_2", "Lọc đề trong phạm vi tài khoản", S_UC, x=360, y=155, w=260, h=50),
    cell("u4_3", "Xem chi tiết đề thi", S_UC, x=360, y=235, w=260, h=50),
    cell("u4_4", "In đề thi theo biểu mẫu chuẩn", S_UC, x=360, y=305, w=260, h=50),
    cell("l1", "", S_LINE, edge=1, source="gv", target="u4_1"),
    cell("l3", "", S_LINE, edge=1, source="gv", target="u4_3"),
    cell("l4", "", S_LINE, edge=1, source="gv", target="u4_4"),
    cell("inc1", "&laquo;include&raquo;", S_INC, edge=1, source="u4_1", target="u4_2")
]
add_diag("Hình 2.5 Biểu đồ Use Case phân rã UC04", c_uc04)

# ==========================================
# 6. BIỂU ĐỒ PHÂN RÃ UC05 (Hình 2.6)
# ==========================================
c_uc05 = [
    cell("gv", "Giảng viên", S_ACTOR, x=60, y=200, w=45, h=80),
    cell("sys", "Phân hệ Báo cáo thống kê (UC05)", S_BOUND, x=230, y=40, w=550, h=400),
    cell("u5_1", "Chọn năm học báo cáo", S_UC, x=360, y=75, w=260, h=50),
    cell("u5_2", "Tổng hợp số lượng đề theo môn", S_UC, x=360, y=155, w=260, h=50),
    cell("u5_3", "Tổng hợp số lượng bài chấm theo môn", S_UC, x=360, y=235, w=260, h=50),
    cell("u5_4", "Tính tỷ lệ đề & bài chấm (1.1, 1.2)", S_UC, x=470, y=325, w=240, h=50),
    cell("u5_5", "Xuất / Hiển thị báo cáo năm (BM5)", S_UC, x=260, y=325, w=180, h=50),
    cell("l1", "", S_LINE, edge=1, source="gv", target="u5_1"),
    cell("l5", "", S_LINE, edge=1, source="gv", target="u5_5"),
    cell("inc1", "&laquo;include&raquo;", S_INC, edge=1, source="u5_2", target="u5_4"),
    cell("inc2", "&laquo;include&raquo;", S_INC, edge=1, source="u5_3", target="u5_4")
]
add_diag("Hình 2.6 Biểu đồ Use Case phân rã UC05", c_uc05)

# ==========================================
# 7. BIỂU ĐỒ PHÂN RÃ UC06 (Hình 2.7)
# ==========================================
c_uc06 = [
    cell("admin", "Quản trị viên", S_ACTOR, x=60, y=220, w=45, h=80),
    cell("sys", "Phân hệ Quản lý tài khoản giảng viên (UC06)", S_BOUND, x=230, y=40, w=540, h=430),
    cell("u6_1", "Xem danh sách tài khoản giảng viên", S_UC, x=360, y=75, w=270, h=50),
    cell("u6_2", "Tạo tài khoản giảng viên mới (BM6, QĐ4)", S_UC, x=360, y=155, w=270, h=50),
    cell("u6_3", "Cập nhật thông tin giảng viên", S_UC, x=360, y=235, w=270, h=50),
    cell("u6_4", "Kích hoạt / Khóa tài khoản", S_UC, x=360, y=315, w=270, h=50),
    cell("u6_5", "Đặt lại mật khẩu tài khoản", S_UC, x=360, y=385, w=270, h=50),
    cell("l1", "", S_LINE, edge=1, source="admin", target="u6_1"),
    cell("l2", "", S_LINE, edge=1, source="admin", target="u6_2"),
    cell("l3", "", S_LINE, edge=1, source="admin", target="u6_3"),
    cell("l4", "", S_LINE, edge=1, source="admin", target="u6_4"),
    cell("l5", "", S_LINE, edge=1, source="admin", target="u6_5")
]
add_diag("Hình 2.7 Biểu đồ Use Case phân rã UC06", c_uc06)

# ==========================================
# 8. BIỂU ĐỒ PHÂN RÃ UC07 (Hình 2.8)
# ==========================================
c_uc07 = [
    cell("gv", "Giảng viên", S_ACTOR, x=60, y=230, w=45, h=80),
    cell("sys", "Phân hệ Quản lý lớp học (UC07)", S_BOUND, x=230, y=40, w=560, h=450),
    cell("u7_1", "Xem danh sách lớp học", S_UC, x=370, y=75, w=250, h=50),
    cell("u7_2", "Khởi tạo lớp học mới (BM7, QĐ5)", S_UC, x=370, y=155, w=250, h=50),
    cell("u7_3", "Sửa thông tin lớp học", S_UC, x=370, y=235, w=250, h=50),
    cell("u7_4", "Xóa lớp học", S_UC, x=370, y=315, w=250, h=50),
    cell("u7_5", "Quản lý danh sách sinh viên (Họ tên, MSSV)", S_UC, x=480, y=395, w=240, h=50),
    cell("u7_6", "Kiểm tra chưa có điểm chấm (QĐ5)", S_UC, x=250, y=395, w=210, h=50),
    cell("l1", "", S_LINE, edge=1, source="gv", target="u7_1"),
    cell("l2", "", S_LINE, edge=1, source="gv", target="u7_2"),
    cell("l3", "", S_LINE, edge=1, source="gv", target="u7_3"),
    cell("l4", "", S_LINE, edge=1, source="gv", target="u7_4"),
    cell("inc1", "&laquo;include&raquo;", S_INC, edge=1, source="u7_2", target="u7_5"),
    cell("inc2", "&laquo;include&raquo;", S_INC, edge=1, source="u7_3", target="u7_5"),
    cell("inc3", "&laquo;include&raquo;", S_INC, edge=1, source="u7_4", target="u7_6")
]
add_diag("Hình 2.8 Biểu đồ Use Case phân rã UC07", c_uc07)

# Helper for Activity Diagram
def make_activity(title, actor_name, act_steps):
    # act_steps is a list of tuples: (id, text, lane, type, guard, target_id)
    # lane: 'actor' (x=50..390) or 'sys' (x=390..790)
    cells = [
        cell("l_act", actor_name, S_SWIM, x=40, y=40, w=340, h=700),
        cell("l_sys", "Hệ thống", S_SWIM, x=380, y=40, w=430, h=700)
    ]
    return cells

# ==========================================
# 9. HOẠT ĐỘNG UC00 (Hình 2.9)
# ==========================================
c_act00 = [
    cell("l_act", "Người dùng", S_SWIM, x=40, y=40, w=340, h=700),
    cell("l_sys", "Hệ thống", S_SWIM, x=380, y=40, w=430, h=700),
    cell("start", "", S_START, x=190, y=90, w=30, h=30),
    cell("a1", "Chọn chức năng ĐĂNG NHẬP", S_ACTION, x=105, y=150, w=200, h=45),
    cell("a2", "Nhập Tên đăng nhập và Mật khẩu", S_ACTION, x=95, y=225, w=220, h=45),
    cell("a3", "Nhấn nút 'Đăng nhập'", S_ACTION, x=115, y=300, w=180, h=45),
    cell("s1", "Tiếp nhận thông tin xác thực", S_ACTION, x=480, y=300, w=220, h=45),
    cell("s2", "Kiểm tra tài khoản, mật khẩu băm\nvà trạng thái hoạt động", S_ACTION, x=470, y=375, w=240, h=50),
    cell("d1", "Hợp lệ?", S_DECISION, x=550, y=455, w=80, h=50),
    cell("s_err", "Báo lỗi đăng nhập không đúng\nhoặc tài khoản bị khóa", S_ACTION, x=470, y=535, w=240, h=45),
    cell("s_ok", "Khởi tạo phiên làm việc\nvà phân quyền theo vai trò", S_ACTION, x=470, y=605, w=240, h=50),
    cell("a_ok", "Truy cập giao diện chức năng\ntương ứng với vai trò", S_ACTION, x=95, y=605, w=220, h=50),
    cell("end", "", S_END, x=190, y=685, w=30, h=30),
    cell("f0", "", S_FLOW, edge=1, source="start", target="a1"),
    cell("f1", "", S_FLOW, edge=1, source="a1", target="a2"),
    cell("f2", "", S_FLOW, edge=1, source="a2", target="a3"),
    cell("f3", "", S_FLOW, edge=1, source="a3", target="s1"),
    cell("f4", "", S_FLOW, edge=1, source="s1", target="s2"),
    cell("f5", "", S_FLOW, edge=1, source="s2", target="d1"),
    cell("f_fail", "[Không]", S_FLOW, edge=1, source="d1", target="s_err"),
    cell("f_retry", "", S_FLOW, edge=1, source="s_err", target="a2", points=[(730, 557), (730, 247)]),
    cell("f_pass", "[Hợp lệ]", S_FLOW, edge=1, source="d1", target="s_ok"),
    cell("f_view", "", S_FLOW, edge=1, source="s_ok", target="a_ok"),
    cell("f_end", "", S_FLOW, edge=1, source="a_ok", target="end")
]
add_diag("Hình 2.9 Biểu đồ hoạt động UC00", c_act00)

# ==========================================
# 10. HOẠT ĐỘNG UC01 (Hình 2.10)
# ==========================================
c_act01 = [
    cell("l_act", "Giảng viên", S_SWIM, x=40, y=40, w=340, h=720),
    cell("l_sys", "Hệ thống", S_SWIM, x=380, y=40, w=430, h=720),
    cell("start", "", S_START, x=190, y=85, w=30, h=30),
    cell("a1", "Chọn chức năng QUẢN LÝ CÂU HỎI", S_ACTION, x=95, y=140, w=220, h=45),
    cell("a2", "Chọn thao tác (Tạo mới / Sửa / Xóa)", S_ACTION, x=95, y=215, w=220, h=45),
    cell("a3", "Nhập thông tin câu hỏi & đáp án\nhoặc chọn câu hỏi cần xóa", S_ACTION, x=95, y=290, w=220, h=45),
    cell("a4", "Nhấn nút 'Lưu' hoặc xác nhận Xóa", S_ACTION, x=95, y=365, w=220, h=45),
    cell("s1", "Kiểm tra dữ liệu bắt buộc,\nmôn học và độ khó (QĐ1)", S_ACTION, x=470, y=365, w=240, h=45),
    cell("s2", "Kiểm tra câu hỏi đã thuộc đề thi chưa?", S_ACTION, x=470, y=440, w=240, h=45),
    cell("d1", "Hợp lệ & Chưa dùng?", S_DECISION, x=540, y=515, w=100, h=50),
    cell("s_err", "Báo lỗi vi phạm QĐ1\n(Khóa sửa/xóa câu hỏi trong đề)", S_ACTION, x=470, y=590, w=240, h=45),
    cell("s_ok", "Lưu mới / Cập nhật / Xóa câu hỏi\ntrong phạm vi tài khoản", S_ACTION, x=470, y=660, w=240, h=45),
    cell("a_ok", "Nhận thông báo kết quả thành công", S_ACTION, x=95, y=660, w=220, h=45),
    cell("end", "", S_END, x=45, y=667, w=30, h=30),
    cell("f0", "", S_FLOW, edge=1, source="start", target="a1"),
    cell("f1", "", S_FLOW, edge=1, source="a1", target="a2"),
    cell("f2", "", S_FLOW, edge=1, source="a2", target="a3"),
    cell("f3", "", S_FLOW, edge=1, source="a3", target="a4"),
    cell("f4", "", S_FLOW, edge=1, source="a4", target="s1"),
    cell("f5", "", S_FLOW, edge=1, source="s1", target="s2"),
    cell("f6", "", S_FLOW, edge=1, source="s2", target="d1"),
    cell("f_fail", "[Không]", S_FLOW, edge=1, source="d1", target="s_err"),
    cell("f_back", "", S_FLOW, edge=1, source="s_err", target="a3", points=[(730, 612), (730, 312)]),
    cell("f_pass", "[Hợp lệ]", S_FLOW, edge=1, source="d1", target="s_ok"),
    cell("f_notify", "", S_FLOW, edge=1, source="s_ok", target="a_ok"),
    cell("f_end", "", S_FLOW, edge=1, source="a_ok", target="end")
]
add_diag("Hình 2.10 Biểu đồ hoạt động UC01", c_act01)

# ==========================================
# 11. HOẠT ĐỘNG UC02 (Hình 2.11)
# ==========================================
c_act02 = [
    cell("l_act", "Giảng viên", S_SWIM, x=40, y=40, w=340, h=720),
    cell("l_sys", "Hệ thống", S_SWIM, x=380, y=40, w=430, h=720),
    cell("start", "", S_START, x=190, y=85, w=30, h=30),
    cell("a1", "Chọn chức năng SOẠN ĐỀ THI", S_ACTION, x=95, y=140, w=220, h=45),
    cell("a2", "Nhập thông tin đề: Mã đề, Môn thi,\nHọc kỳ, Năm học, Thời lượng", S_ACTION, x=95, y=215, w=220, h=50),
    cell("a3", "Chọn 1–5 câu hỏi cùng môn thi\nvà gán điểm cho từng câu", S_ACTION, x=95, y=295, w=220, h=45),
    cell("a4", "Nhấn nút 'Lưu đề thi'", S_ACTION, x=115, y=370, w=180, h=45),
    cell("s1", "Kiểm tra thời lượng (30–180 phút)\nvà số câu hỏi (1–5 câu)", S_ACTION, x=470, y=370, w=240, h=45),
    cell("s2", "Kiểm tra tổng điểm các câu = 10\nvà đề chưa có kết quả chấm (QĐ2)", S_ACTION, x=470, y=445, w=240, h=50),
    cell("d1", "Hợp lệ QĐ2?", S_DECISION, x=550, y=525, w=80, h=50),
    cell("s_err", "Báo lỗi vi phạm quy định QĐ2\n(Sai thời lượng / số câu / điểm != 10)", S_ACTION, x=470, y=600, w=240, h=45),
    cell("s_ok", "Lưu đề thi và chi tiết phân bổ điểm\nvào cơ sở dữ liệu", S_ACTION, x=470, y=665, w=240, h=45),
    cell("a_ok", "Nhận thông báo lưu đề thành công", S_ACTION, x=95, y=665, w=220, h=45),
    cell("end", "", S_END, x=45, y=672, w=30, h=30),
    cell("f0", "", S_FLOW, edge=1, source="start", target="a1"),
    cell("f1", "", S_FLOW, edge=1, source="a1", target="a2"),
    cell("f2", "", S_FLOW, edge=1, source="a2", target="a3"),
    cell("f3", "", S_FLOW, edge=1, source="a3", target="a4"),
    cell("f4", "", S_FLOW, edge=1, source="a4", target="s1"),
    cell("f5", "", S_FLOW, edge=1, source="s1", target="s2"),
    cell("f6", "", S_FLOW, edge=1, source="s2", target="d1"),
    cell("f_fail", "[Không]", S_FLOW, edge=1, source="d1", target="s_err"),
    cell("f_back", "", S_FLOW, edge=1, source="s_err", target="a3", points=[(730, 622), (730, 317)]),
    cell("f_pass", "[Hợp lệ]", S_FLOW, edge=1, source="d1", target="s_ok"),
    cell("f_notify", "", S_FLOW, edge=1, source="s_ok", target="a_ok"),
    cell("f_end", "", S_FLOW, edge=1, source="a_ok", target="end")
]
add_diag("Hình 2.11 Biểu đồ hoạt động UC02", c_act02)

# ==========================================
# 12. HOẠT ĐỘNG UC03 (Hình 2.12)
# ==========================================
c_act03 = [
    cell("l_act", "Giảng viên", S_SWIM, x=40, y=40, w=340, h=710),
    cell("l_sys", "Hệ thống", S_SWIM, x=380, y=40, w=430, h=710),
    cell("start", "", S_START, x=190, y=85, w=30, h=30),
    cell("a1", "Chọn chức năng GHI NHẬN CHẤM THI", S_ACTION, x=95, y=140, w=220, h=45),
    cell("a2", "Chọn Đề thi và chọn Lớp học", S_ACTION, x=105, y=215, w=200, h=45),
    cell("s1", "Tải và hiển thị danh sách sinh viên\ncủa lớp học đã chọn", S_ACTION, x=470, y=215, w=240, h=45),
    cell("a3", "Nhập điểm số (0–10, bội số 0.5)\nvà ghi chú cho sinh viên", S_ACTION, x=95, y=295, w=220, h=45),
    cell("a4", "Nhấn nút 'Lưu bảng điểm'", S_ACTION, x=115, y=370, w=180, h=45),
    cell("s2", "Kiểm tra thang điểm (0 <= điểm <= 10\nvà bước điểm = 0.5 theo QĐ3)", S_ACTION, x=470, y=370, w=240, h=45),
    cell("d1", "Điểm hợp lệ?", S_DECISION, x=550, y=445, w=80, h=50),
    cell("s_err", "Báo lỗi điểm không hợp lệ theo QĐ3", S_ACTION, x=470, y=525, w=240, h=45),
    cell("s_conv", "Tự động quy đổi sang điểm chữ\n(A, B, C, D, E, F theo QĐ3)", S_ACTION, x=470, y=595, w=240, h=45),
    cell("s_ok", "Lưu kết quả chấm thi vào CSDL", S_ACTION, x=470, y=660, w=240, h=40),
    cell("a_ok", "Xem kết quả chấm thi đã cập nhật", S_ACTION, x=95, y=660, w=220, h=40),
    cell("end", "", S_END, x=45, y=665, w=30, h=30),
    cell("f0", "", S_FLOW, edge=1, source="start", target="a1"),
    cell("f1", "", S_FLOW, edge=1, source="a1", target="a2"),
    cell("f2", "", S_FLOW, edge=1, source="a2", target="s1"),
    cell("f3", "", S_FLOW, edge=1, source="s1", target="a3"),
    cell("f4", "", S_FLOW, edge=1, source="a3", target="a4"),
    cell("f5", "", S_FLOW, edge=1, source="a4", target="s2"),
    cell("f6", "", S_FLOW, edge=1, source="s2", target="d1"),
    cell("f_fail", "[Không]", S_FLOW, edge=1, source="d1", target="s_err"),
    cell("f_back", "", S_FLOW, edge=1, source="s_err", target="a3", points=[(730, 547), (730, 317)]),
    cell("f_pass", "[Hợp lệ]", S_FLOW, edge=1, source="d1", target="s_conv"),
    cell("f_save", "", S_FLOW, edge=1, source="s_conv", target="s_ok"),
    cell("f_view", "", S_FLOW, edge=1, source="s_ok", target="a_ok"),
    cell("f_end", "", S_FLOW, edge=1, source="a_ok", target="end")
]
add_diag("Hình 2.12 Biểu đồ hoạt động UC03", c_act03)

# ==========================================
# 13. HOẠT ĐỘNG UC04 (Hình 2.13)
# ==========================================
c_act04 = [
    cell("l_act", "Giảng viên", S_SWIM, x=40, y=40, w=340, h=620),
    cell("l_sys", "Hệ thống", S_SWIM, x=380, y=40, w=430, h=620),
    cell("start", "", S_START, x=190, y=85, w=30, h=30),
    cell("a1", "Chọn chức năng TRA CỨU ĐỀ THI", S_ACTION, x=95, y=140, w=220, h=45),
    cell("a2", "Nhập tiêu chí tra cứu\n(Mã đề, Môn học, Học kỳ, Năm học)", S_ACTION, x=95, y=215, w=220, h=45),
    cell("a3", "Nhấn nút 'Tra cứu'", S_ACTION, x=125, y=290, w=160, h=45),
    cell("s1", "Truy vấn danh sách đề thi theo tiêu chí\ntrong phạm vi tài khoản giảng viên", S_ACTION, x=470, y=290, w=240, h=45),
    cell("d1", "Có kết quả?", S_DECISION, x=550, y=365, w=80, h=50),
    cell("s_none", "Thông báo không tìm thấy đề thi", S_ACTION, x=470, y=445, w=240, h=45),
    cell("s_show", "Hiển thị danh sách đề thi (BM4)\nkèm tổng điểm tối đa", S_ACTION, x=470, y=515, w=240, h=45),
    cell("a_view", "Xem chi tiết hoặc in đề thi", S_ACTION, x=105, y=515, w=200, h=45),
    cell("end", "", S_END, x=190, y=580, w=30, h=30),
    cell("f0", "", S_FLOW, edge=1, source="start", target="a1"),
    cell("f1", "", S_FLOW, edge=1, source="a1", target="a2"),
    cell("f2", "", S_FLOW, edge=1, source="a2", target="a3"),
    cell("f3", "", S_FLOW, edge=1, source="a3", target="s1"),
    cell("f4", "", S_FLOW, edge=1, source="s1", target="d1"),
    cell("f_fail", "[Không]", S_FLOW, edge=1, source="d1", target="s_none"),
    cell("f_pass", "[Có]", S_FLOW, edge=1, source="d1", target="s_show"),
    cell("f_view", "", S_FLOW, edge=1, source="s_show", target="a_view"),
    cell("f_end1", "", S_FLOW, edge=1, source="a_view", target="end"),
    cell("f_end2", "", S_FLOW, edge=1, source="s_none", target="end", points=[(590, 595)])
]
add_diag("Hình 2.13 Biểu đồ hoạt động UC04", c_act04)

# ==========================================
# 14. HOẠT ĐỘNG UC05 (Hình 2.14)
# ==========================================
c_act05 = [
    cell("l_act", "Giảng viên", S_SWIM, x=40, y=40, w=340, h=620),
    cell("l_sys", "Hệ thống", S_SWIM, x=380, y=40, w=430, h=620),
    cell("start", "", S_START, x=190, y=85, w=30, h=30),
    cell("a1", "Chọn chức năng LẬP BÁO CÁO NĂM", S_ACTION, x=95, y=140, w=220, h=45),
    cell("a2", "Chọn Năm học cần báo cáo", S_ACTION, x=105, y=215, w=200, h=45),
    cell("a3", "Nhấn nút 'Lập báo cáo'", S_ACTION, x=125, y=290, w=160, h=45),
    cell("s1", "Lấy dữ liệu đề thi và bài chấm\nthuộc tài khoản trong năm học", S_ACTION, x=470, y=290, w=240, h=45),
    cell("s2", "Tính tổng số đề, tổng số bài chấm\nvà tỷ lệ từng môn theo CT (1.1) & (1.2)", S_ACTION, x=470, y=365, w=240, h=50),
    cell("s3", "Hiển thị bảng báo cáo tổng hợp (BM5)", S_ACTION, x=470, y=445, w=240, h=45),
    cell("a_view", "Xem báo cáo hoặc xuất in", S_ACTION, x=105, y=445, w=200, h=45),
    cell("end", "", S_END, x=190, y=530, w=30, h=30),
    cell("f0", "", S_FLOW, edge=1, source="start", target="a1"),
    cell("f1", "", S_FLOW, edge=1, source="a1", target="a2"),
    cell("f2", "", S_FLOW, edge=1, source="a2", target="a3"),
    cell("f3", "", S_FLOW, edge=1, source="a3", target="s1"),
    cell("f4", "", S_FLOW, edge=1, source="s1", target="s2"),
    cell("f5", "", S_FLOW, edge=1, source="s2", target="s3"),
    cell("f6", "", S_FLOW, edge=1, source="s3", target="a_view"),
    cell("f7", "", S_FLOW, edge=1, source="a_view", target="end")
]
add_diag("Hình 2.14 Biểu đồ hoạt động UC05", c_act05)

# ==========================================
# 15. HOẠT ĐỘNG UC06 (Hình 2.15)
# ==========================================
c_act06 = [
    cell("l_act", "Quản trị viên", S_SWIM, x=40, y=40, w=340, h=660),
    cell("l_sys", "Hệ thống", S_SWIM, x=380, y=40, w=430, h=660),
    cell("start", "", S_START, x=190, y=85, w=30, h=30),
    cell("a1", "Chọn chức năng QUẢN LÝ TÀI KHOẢN", S_ACTION, x=95, y=140, w=220, h=45),
    cell("a2", "Chọn thao tác: Tạo mới / Cập nhật /\nKhóa-Kích hoạt / Đặt lại mật khẩu", S_ACTION, x=95, y=215, w=220, h=50),
    cell("a3", "Nhập thông tin tài khoản (BM6, QĐ4)\nhoặc chọn tài khoản cần xử lý", S_ACTION, x=95, y=295, w=220, h=45),
    cell("a4", "Nhấn nút 'Lưu thay đổi'", S_ACTION, x=115, y=370, w=180, h=45),
    cell("s1", "Kiểm tra tính duy nhất của Tên đăng nhập\nvà kiểm tra không xóa cứng (QĐ4)", S_ACTION, x=470, y=370, w=240, h=45),
    cell("d1", "Hợp lệ QĐ4?", S_DECISION, x=550, y=445, w=80, h=50),
    cell("s_err", "Báo lỗi trùng tên đăng nhập\nhoặc dữ liệu không hợp lệ", S_ACTION, x=470, y=525, w=240, h=45),
    cell("s_ok", "Lưu thông tin tài khoản / đổi trạng thái\nvào cơ sở dữ liệu", S_ACTION, x=470, y=595, w=240, h=45),
    cell("a_ok", "Nhận thông báo cập nhật thành công", S_ACTION, x=95, y=595, w=220, h=45),
    cell("end", "", S_END, x=45, y=602, w=30, h=30),
    cell("f0", "", S_FLOW, edge=1, source="start", target="a1"),
    cell("f1", "", S_FLOW, edge=1, source="a1", target="a2"),
    cell("f2", "", S_FLOW, edge=1, source="a2", target="a3"),
    cell("f3", "", S_FLOW, edge=1, source="a3", target="a4"),
    cell("f4", "", S_FLOW, edge=1, source="a4", target="s1"),
    cell("f5", "", S_FLOW, edge=1, source="s1", target="d1"),
    cell("f_fail", "[Không]", S_FLOW, edge=1, source="d1", target="s_err"),
    cell("f_back", "", S_FLOW, edge=1, source="s_err", target="a3", points=[(730, 547), (730, 317)]),
    cell("f_pass", "[Hợp lệ]", S_FLOW, edge=1, source="d1", target="s_ok"),
    cell("f_view", "", S_FLOW, edge=1, source="s_ok", target="a_ok"),
    cell("f_end", "", S_FLOW, edge=1, source="a_ok", target="end")
]
add_diag("Hình 2.15 Biểu đồ hoạt động UC06", c_act06)

# ==========================================
# 16. HOẠT ĐỘNG UC07 (Hình 2.16 - QUẢN LÝ LỚP HỌC)
# ==========================================
c_act07 = [
    cell("l_act", "Giảng viên", S_SWIM, x=40, y=40, w=340, h=690),
    cell("l_sys", "Hệ thống", S_SWIM, x=380, y=40, w=430, h=690),
    cell("start", "", S_START, x=190, y=85, w=30, h=30),
    cell("a1", "Chọn chức năng QUẢN LÝ LỚP HỌC", S_ACTION, x=95, y=140, w=220, h=45),
    cell("a2", "Chọn thao tác (Tạo lớp / Sửa thông tin /\nThêm-xóa sinh viên / Xóa lớp)", S_ACTION, x=95, y=215, w=220, h=45),
    cell("a3", "Nhập Mã lớp, Tên lớp, danh sách MSSV\nhoặc chọn lớp cần xóa", S_ACTION, x=95, y=290, w=220, h=45),
    cell("a4", "Nhấn nút 'Lưu' hoặc xác nhận Xóa lớp", S_ACTION, x=95, y=365, w=220, h=45),
    cell("s1", "Kiểm tra tính duy nhất của Mã lớp\nvà tính hợp lệ của MSSV", S_ACTION, x=470, y=365, w=240, h=45),
    cell("s2", "Nếu xóa lớp: kiểm tra lớp\nđã có kết quả chấm thi chưa? (QĐ5)", S_ACTION, x=470, y=440, w=240, h=45),
    cell("d1", "Hợp lệ & Chưa có điểm?", S_DECISION, x=540, y=515, w=100, h=50),
    cell("s_err", "Báo lỗi vi phạm quy định QĐ5\n(Mã lớp trùng hoặc lớp đã có điểm thi)", S_ACTION, x=470, y=590, w=240, h=45),
    cell("s_ok", "Lưu lớp học / danh sách sinh viên\nhoặc xóa lớp khỏi cơ sở dữ liệu", S_ACTION, x=470, y=650, w=240, h=40),
    cell("a_ok", "Nhận thông báo cập nhật lớp thành công", S_ACTION, x=95, y=650, w=220, h=40),
    cell("end", "", S_END, x=45, y=655, w=30, h=30),
    cell("f0", "", S_FLOW, edge=1, source="start", target="a1"),
    cell("f1", "", S_FLOW, edge=1, source="a1", target="a2"),
    cell("f2", "", S_FLOW, edge=1, source="a2", target="a3"),
    cell("f3", "", S_FLOW, edge=1, source="a3", target="a4"),
    cell("f4", "", S_FLOW, edge=1, source="a4", target="s1"),
    cell("f5", "", S_FLOW, edge=1, source="s1", target="s2"),
    cell("f6", "", S_FLOW, edge=1, source="s2", target="d1"),
    cell("f_fail", "[Không]", S_FLOW, edge=1, source="d1", target="s_err"),
    cell("f_back", "", S_FLOW, edge=1, source="s_err", target="a3", points=[(730, 612), (730, 312)]),
    cell("f_pass", "[Hợp lệ]", S_FLOW, edge=1, source="d1", target="s_ok"),
    cell("f_notify", "", S_FLOW, edge=1, source="s_ok", target="a_ok"),
    cell("f_end", "", S_FLOW, edge=1, source="a_ok", target="end")
]
add_diag("Hình 2.16 Biểu đồ hoạt động UC07", c_act07)

# Helper for Sequence Diagrams
def make_seq(actor_name, msg_list, alt_cond, alt_success_msgs, alt_fail_msgs):
    cells = [
        cell("p0", actor_name, S_ACTOR, x=80, y=80, w=40, h=70),
        cell("p1", ":GiaoDien", S_LIFE, x=240, y=80, w=110, h=600),
        cell("p2", ":BoXuLy", S_LIFE, x=480, y=80, w=110, h=600),
        cell("p3", ":CoSoDuLieu", S_LIFE, x=720, y=80, w=110, h=600)
    ]
    cur_y = 170
    midx = 1
    for src, tgt, txt, is_ret in msg_list:
        st = S_RET if is_ret else S_SYNC
        cells.append(cell(f"m{midx}", f"{midx}. {txt}", st, edge=1, source=src, target=tgt, points=[(0, cur_y)]))
        midx += 1
        cur_y += 45
    
    # Alt frame
    alt_top = cur_y - 10
    cells.append(cell("alt", f"alt [{alt_cond}]", S_ALT, x=60, y=alt_top, w=790, h=240))
    cur_y += 20
    for src, tgt, txt, is_ret in alt_success_msgs:
        st = S_RET if is_ret else S_SYNC
        cells.append(cell(f"m{midx}", f"{midx}. {txt}", st, edge=1, source=src, target=tgt, points=[(0, cur_y)]))
        midx += 1
        cur_y += 40
        
    cur_y += 15
    cells.append(cell("alt_sep", "", "edgeStyle=none;strokeColor=#000000;dashed=1;endArrow=none;", edge=1, points=[(60, cur_y), (850, cur_y)]))
    cells.append(cell("else_lbl", "[Ngược lại / Vi phạm quy định]", "text;strokeColor=none;fillColor=none;fontSize=11;fontFamily=Times New Roman;", x=70, y=cur_y+5, w=200, h=20))
    cur_y += 35
    for src, tgt, txt, is_ret in alt_fail_msgs:
        st = S_RET if is_ret else S_SYNC
        cells.append(cell(f"m{midx}", f"{midx}. {txt}", st, edge=1, source=src, target=tgt, points=[(0, cur_y)]))
        midx += 1
        cur_y += 40
        
    return cells

# 17. TUẦN TỰ UC00 (Hình 2.17)
add_diag("Hình 2.17 Biểu đồ tuần tự UC00", make_seq(
    "Người dùng",
    [("p0", "p1", "Nhập tên đăng nhập & mật khẩu", False),
     ("p1", "p2", "xacThucTaiKhoan(username, password)", False),
     ("p2", "p3", "truyVanTaiKhoan(username)", False),
     ("p3", "p2", "thongTinTaiKhoan, matKhauHash", True)],
    "Thông tin khớp & Đang hoạt động",
    [("p2", "p1", "khoiTaoPhien(vaiTro, quyen)", True),
     ("p1", "p0", "Hiển thị menu chức năng theo vai trò", True)],
    [("p2", "p1", "thongBaoDangNhapThatBai()", True),
     ("p1", "p0", "Hiển thị lỗi đăng nhập", True)]
))

# 18. TUẦN TỰ UC01 (Hình 2.18)
add_diag("Hình 2.18 Biểu đồ tuần tự UC01", make_seq(
    "Giảng viên",
    [("p0", "p1", "Chọn Thêm / Sửa / Xóa câu hỏi", False),
     ("p0", "p1", "Nhập thông tin câu hỏi và đáp án", False),
     ("p1", "p2", "xuLyLuuCauHoi(duLieuCauHoi)", False),
     ("p2", "p3", "kiemTraCauHoiThuocDeThi(maCauHoi)", False),
     ("p3", "p2", "ketQuaSuDung", True)],
    "Hợp lệ & Chưa thuộc đề thi (QĐ1)",
    [("p2", "p3", "luuCauHoiVaoCSDL(cauHoi)", False),
     ("p3", "p2", "xacNhanLuuThanhCong", True),
     ("p2", "p1", "thongBaoThanhCong()", True),
     ("p1", "p0", "Hiển thị thông báo thành công", True)],
    [("p2", "p1", "thongBaoLoiViPhamQD1()", True),
     ("p1", "p0", "Báo lỗi: Câu hỏi đã có trong đề thi", True)]
))

# 19. TUẦN TỰ UC02 (Hình 2.19)
add_diag("Hình 2.19 Biểu đồ tuần tự UC02", make_seq(
    "Giảng viên",
    [("p0", "p1", "Nhập thông tin đề, chọn câu hỏi & gán điểm", False),
     ("p1", "p2", "kiemTraVaLuuDeThi(thongTinDe, dsCauHoi)", False),
     ("p2", "p3", "kiemTraDeThiDaCoDiemCham(maDe)", False),
     ("p3", "p2", "tinhTrangChamThi", True)],
    "Thời lượng 30-180p, 1-5 câu, Tổng=10 (QĐ2)",
    [("p2", "p3", "luuDeThiVaChiTiet(deThi, dsCauHoiDiem)", False),
     ("p3", "p2", "xacNhanGhiThanhCong", True),
     ("p2", "p1", "thongBaoLuuDeThanhCong()", True),
     ("p1", "p0", "Hiển thị đề thi đã lưu", True)],
    [("p2", "p1", "thongBaoLoiViPhamQD2()", True),
     ("p1", "p0", "Báo lỗi sai quy định đề thi", True)]
))

# 20. TUẦN TỰ UC03 (Hình 2.20)
add_diag("Hình 2.20 Biểu đồ tuần tự UC03", make_seq(
    "Giảng viên",
    [("p0", "p1", "Chọn đề thi, chọn lớp & nhập điểm số", False),
     ("p1", "p2", "ghiNhanKetQuaCham(maDe, maLop, dsDiem)", False),
     ("p2", "p2", "kiemTraThangDiemVaQuyDoi(dsDiem)", False)],
    "Điểm 0–10 & Bội số của 0.5 (QĐ3)",
    [("p2", "p3", "luuBangDiem(maDe, maLop, dsDiemChu)", False),
     ("p3", "p2", "xacNhanLuuBangDiem", True),
     ("p2", "p1", "thongBaoLuuKetQuaThanhCong()", True),
     ("p1", "p0", "Hiển thị bảng điểm và điểm chữ", True)],
    [("p2", "p1", "thongBaoLoiDiemSoKhongHopLe()", True),
     ("p1", "p0", "Báo lỗi vi phạm thang điểm QĐ3", True)]
))

# 21. TUẦN TỰ UC04 (Hình 2.21)
add_diag("Hình 2.21 Biểu đồ tuần tự UC04", make_seq(
    "Giảng viên",
    [("p0", "p1", "Nhập tiêu chí tra cứu đề thi", False),
     ("p1", "p2", "traCuuDeThi(tieuChi, taiKhoanId)", False),
     ("p2", "p3", "truyVanDeThi(tieuChi, taiKhoanId)", False),
     ("p3", "p2", "danhSachDeThiPhuHop", True)],
    "Tìm thấy kết quả",
    [("p2", "p1", "traVeDanhSachDe(danhSachDe)", True),
     ("p1", "p0", "Hiển thị danh sách đề thi (BM4)", True)],
    [("p2", "p1", "thongBaoKhongCoKetQua()", True),
     ("p1", "p0", "Hiển thị thông báo không tìm thấy", True)]
))

# 22. TUẦN TỰ UC05 (Hình 2.22)
add_diag("Hình 2.22 Biểu đồ tuần tự UC05", make_seq(
    "Giảng viên",
    [("p0", "p1", "Chọn năm học cần lập báo cáo", False),
     ("p1", "p2", "lapBaoCaoNam(namHoc, taiKhoanId)", False),
     ("p2", "p3", "layDuLieuDeVaBaiCham(namHoc, taiKhoanId)", False),
     ("p3", "p2", "duLieuTho", True),
     ("p2", "p2", "tinhTongVaTyLeTheoMon(CT1.1, CT1.2)", False)],
    "Năm học hợp lệ",
    [("p2", "p1", "traVeBaoCaoNam(soLieuBaoCao)", True),
     ("p1", "p0", "Hiển thị bảng báo cáo năm (BM5)", True)],
    [("p2", "p1", "thongBaoNamHocKhongHopLe()", True),
     ("p1", "p0", "Yêu cầu chọn lại năm học", True)]
))

# 23. TUẦN TỰ UC06 (Hình 2.23)
add_diag("Hình 2.23 Biểu đồ tuần tự UC06", make_seq(
    "Quản trị viên",
    [("p0", "p1", "Nhập thông tin tài khoản hoặc đổi trạng thái", False),
     ("p1", "p2", "xuLyTaiKhoan(duLieuTK, thaoTac)", False),
     ("p2", "p3", "kiemTraTenDangNhapVaDuLieuLienQuan(username)", False),
     ("p3", "p2", "tinhTrangTaiKhoan", True)],
    "Tên duy nhất & Không xóa cứng TK có dữ liệu (QĐ4)",
    [("p2", "p3", "ghiNhanTaiKhoan(duLieuTK)", False),
     ("p3", "p2", "xacNhanLuuThanhCong", True),
     ("p2", "p1", "thongBaoCapNhatTaiKhoanThanhCong()", True),
     ("p1", "p0", "Hiển thị danh sách tài khoản mới", True)],
    [("p2", "p1", "thongBaoLoiViPhamQD4()", True),
     ("p1", "p0", "Báo lỗi: Trùng tên đăng nhập", True)]
))

# 24. TUẦN TỰ UC07 (Hình 2.24)
add_diag("Hình 2.24 Biểu đồ tuần tự UC07", make_seq(
    "Giảng viên",
    [("p0", "p1", "Nhập thông tin lớp, DSSV hoặc chọn Xóa", False),
     ("p1", "p2", "xuLyLopHoc(thongTinLop, dsSinhVien, thaoTac)", False),
     ("p2", "p3", "kiemTraLopDaCoDiemCham(maLop)", False),
     ("p3", "p2", "tinhTrangDiemLop", True)],
    "Mã lớp duy nhất & Chưa có điểm chấm (QĐ5)",
    [("p2", "p3", "luuLopHocVaSinhVien(lop, dsSV)", False),
     ("p3", "p2", "xacNhanGhiThanhCong", True),
     ("p2", "p1", "thongBaoCapNhatLopThanhCong()", True),
     ("p1", "p0", "Hiển thị danh sách lớp và sinh viên", True)],
    [("p2", "p1", "thongBaoLoiViPhamQD5()", True),
     ("p1", "p0", "Báo lỗi: Lớp đã có dữ liệu chấm thi", True)]
))

# Helper for Analysis Class Diagrams (ECB)
def make_ecb(title, b_name, b_attrs, b_methods, c_name, c_attrs, c_methods, entities):
    # entities is a list of (name, attrs, methods)
    cells = []
    # Boundary box
    cells.append(cell("b_hdr", f"&laquo;boundary&raquo;<br><b>{b_name}</b>", S_CLASS, x=60, y=70, w=220, h=250))
    cells.append(cell("b_att", "<br>".join(b_attrs), S_SEC, parent="b_hdr", x=0, y=26, w=220, h=105))
    cells.append(cell("b_mth", "<br>".join(b_methods), S_SEC, parent="b_hdr", x=0, y=131, w=220, h=115))
    
    # Control box
    cells.append(cell("c_hdr", f"&laquo;control&raquo;<br><b>{c_name}</b>", S_CLASS, x=360, y=70, w=230, h=250))
    cells.append(cell("c_att", "<br>".join(c_attrs), S_SEC, parent="c_hdr", x=0, y=26, w=230, h=95))
    cells.append(cell("c_mth", "<br>".join(c_methods), S_SEC, parent="c_hdr", x=0, y=121, w=230, h=125))
    
    # Association B-C
    cells.append(cell("l_bc", "1", S_LINE, edge=1, source="b_hdr", target="c_hdr"))
    
    # Entity boxes
    ent_y = 70
    for idx, (e_name, e_attrs, e_mths) in enumerate(entities):
        eid = f"e{idx}_hdr"
        cells.append(cell(eid, f"&laquo;entity&raquo;<br><b>{e_name}</b>", S_CLASS, x=670, y=ent_y, w=230, h=210))
        cells.append(cell(f"e{idx}_att", "<br>".join(e_attrs), S_SEC, parent=eid, x=0, y=26, w=230, h=95))
        cells.append(cell(f"e{idx}_mth", "<br>".join(e_mths), S_SEC, parent=eid, x=0, y=121, w=230, h=85))
        cells.append(cell(f"l_ce_{idx}", "1..*", S_LINE, edge=1, source="c_hdr", target=eid))
        ent_y += 240
        
    return cells

# 25. LỚP PHÂN TÍCH UC00 (Hình 2.25)
add_diag("Hình 2.25 Biểu đồ lớp UC00", make_ecb(
    "UC00", "FormDangNhap",
    ["+ txtTenDangNhap: Textbox", "+ txtMatKhau: Textbox", "+ btnDangNhap: Button", "+ btnDangXuat: Button"],
    ["+ nhanThongTin()", "+ hienThiLoi()", "+ dieuHuongGiaoDien()"],
    "DangNhapController",
    ["- taiKhoanHienTai: TaiKhoan", "- phienLamViec: Session"],
    ["+ xacThuc(user, pass)", "+ kiemTraTrangThai()", "+ taoPhien()", "+ huyPhien()"],
    [("TaiKhoan",
      ["- id: UUID", "- tenDangNhap: String", "- matKhauHash: String", "- vaiTro: String", "- trangThai: Boolean"],
      ["+ kiemTraMatKhau()", "+ layThongTin()", "+ capNhatTrangThai()"])]
))

# 26. LỚP PHÂN TÍCH UC01 (Hình 2.26)
add_diag("Hình 2.26 Biểu đồ lớp UC01", make_ecb(
    "UC01", "FormQuanLyCauHoi",
    ["+ cbMonHoc: Combobox", "+ cbDoKho: Combobox", "+ txtNoiDung: Textbox", "+ txtDapAn: Textbox", "+ btnLuu: Button", "+ btnXoa: Button"],
    ["+ onLuuClick()", "+ onXoaClick()", "+ hienThiDanhSach()"],
    "CauHoiController",
    ["- dsCauHoi: List<CauHoi>", "- taiKhoanId: UUID"],
    ["+ kiemTraHopLe(cauHoi)", "+ kiemTraChuaThuocDe(id)", "+ luuCauHoi(cauHoi)", "+ xoaCauHoi(id)"],
    [("CauHoi",
      ["- maCauHoi: String", "- maMon: String", "- doKho: String", "- noiDung: Text", "- dapAn: Text", "- taiKhoanId: UUID"],
      ["+ them()", "+ capNhat()", "+ xoa()", "+ kiemTraSuDung()"]),
     ("MonHoc",
      ["- maMon: String", "- tenMon: String"],
      ["+ layDanhSachMon()"])]
))

# 27. LỚP PHÂN TÍCH UC02 (Hình 2.27)
add_diag("Hình 2.27 Biểu đồ lớp UC02", make_ecb(
    "UC02", "FormSoanDeThi",
    ["+ txtMaDe: Textbox", "+ cbMon: Combobox", "+ txtThoiLuong: Textbox", "+ tableCauHoi: TableView", "+ txtDiem: Textbox", "+ btnLuuDe: Button"],
    ["+ onChonCauHoi()", "+ onPhanBoDiem()", "+ onLuuDeClick()"],
    "DeThiController",
    ["- deThiHienTai: DeThi", "- dsChiTiet: List<DeThi_CauHoi>"],
    ["+ kiemTraThoiLuong(tl)", "+ kiemTraSoLuongCau(ds)", "+ kiemTraTongDiem(ds)", "+ kiemTraChuaCham(id)", "+ luuDeThi()"],
    [("DeThi",
      ["- maDe: String", "- maMon: String", "- hocKy: String", "- namHoc: String", "- thoiLuong: Int", "- tongDiem: Float"],
      ["+ them()", "+ capNhat()", "+ xoa()", "+ kiemTraCoDiem()"]),
     ("DeThi_CauHoi",
      ["- maDe: String", "- maCauHoi: String", "- diem: Float"],
      ["+ themChiTiet()", "+ xoaTheoDe()"])]
))

# 28. LỚP PHÂN TÍCH UC03 (Hình 2.28)
add_diag("Hình 2.28 Biểu đồ lớp UC03", make_ecb(
    "UC03", "FormGhiNhanChamThi",
    ["+ cbDeThi: Combobox", "+ cbLopHoc: Combobox", "+ tableBangDiem: TableView", "+ txtGhiChu: Textbox", "+ btnLuuBangDiem: Button"],
    ["+ onChonLop()", "+ onNhapDiem()", "+ onLuuClick()"],
    "ChamThiController",
    ["- maDe: String", "- maLop: String", "- dsKetQua: List<KetQuaThi>"],
    ["+ taiDanhSachSinhVien(lop)", "+ kiemTraThangDiem(diem)", "+ quyDoiDiemChu(diem)", "+ luuKetQuaCham()"],
    [("KetQuaThi",
      ["- id: UUID", "- maDe: String", "- mssv: String", "- diemSo: Float", "- diemChu: String", "- ghiChu: String"],
      ["+ luuKetQua()", "+ capNhatDiem()", "+ layBangDiemLop()"]),
     ("SinhVien",
      ["- mssv: String", "- hoTen: String", "- maLop: String"],
      ["+ layTheoLop()"])]
))

# 29. LỚP PHÂN TÍCH UC04 (Hình 2.29)
add_diag("Hình 2.29 Biểu đồ lớp UC04", make_ecb(
    "UC04", "FormTraCuuDeThi",
    ["+ txtTieuChi: Textbox", "+ cbMon: Combobox", "+ cbNamHoc: Combobox", "+ tableKetQua: TableView", "+ btnTraCuu: Button", "+ btnInDe: Button"],
    ["+ onTraCuuClick()", "+ onXemChiTiet()", "+ onInDeClick()"],
    "TraCuuController",
    ["- tieuChiTimKiem: Criteria", "- ketQuaDeThi: List<DeThi>"],
    ["+ traCuuTheoTieuChi(tc)", "+ locTheoTaiKhoan(tkId)", "+ xuatBieuMauIn(deId)"],
    [("DeThi",
      ["- maDe: String", "- maMon: String", "- hocKy: String", "- namHoc: String", "- thoiLuong: Int", "- ngayThi: Date"],
      ["+ timKiemTheoTieuChi()", "+ layChiTietDe()"])]
))

# 30. LỚP PHÂN TÍCH UC05 (Hình 2.30)
add_diag("Hình 2.30 Biểu đồ lớp UC05", make_ecb(
    "UC05", "FormBaoCaoNam",
    ["+ cbNamHoc: Combobox", "+ tableBaoCao: TableView", "+ txtTongDe: Label", "+ txtTongBaiCham: Label", "+ btnLapBaoCao: Button"],
    ["+ onChonNamHoc()", "+ onLapBaoCaoClick()", "+ onXuatBaoCao()"],
    "BaoCaoController",
    ["- namHoc: String", "- soLieuThongKe: List<BaoCaoMon>"],
    ["+ laySoLuongDe(nam, mon)", "+ laySoLuongBaiCham(nam, mon)", "+ tinhTyLeDe(CT1.1)", "+ tinhTyLeBaiCham(CT1.2)", "+ xuatBieuMauBM5()"],
    [("DeThi",
      ["- maDe: String", "- maMon: String", "- namHoc: String"],
      ["+ demSoDeTheoNam()"]),
     ("KetQuaThi",
      ["- id: UUID", "- maDe: String", "- diemSo: Float"],
      ["+ demSoBaiChamTheoNam()"])]
))

# 31. LỚP PHÂN TÍCH UC06 (Hình 2.31)
add_diag("Hình 2.31 Biểu đồ lớp UC06", make_ecb(
    "UC06", "FormQuanLyTaiKhoan",
    ["+ txtTenDangNhap: Textbox", "+ txtMatKhau: Textbox", "+ txtHoTen: Textbox", "+ cbTrangThai: Combobox", "+ btnLuu: Button", "+ btnKhoa: Button"],
    ["+ onThemTKClick()", "+ onCapNhatClick()", "+ onDoiTrangThaiClick()"],
    "TaiKhoanController",
    ["- dsTaiKhoan: List<TaiKhoan>", "- adminSession: Session"],
    ["+ kiemTraTenDuyNhat(username)", "+ kiemTraKhongXoaCung(id)", "+ taoTaiKhoan()", "+ doiTrangThai()", "+ datLaiMatKhau()"],
    [("TaiKhoan",
      ["- id: UUID", "- tenDangNhap: String", "- matKhauHash: String", "- hoTen: String", "- vaiTro: String", "- trangThai: Boolean"],
      ["+ them()", "+ capNhatThongTin()", "+ khoaTaiKhoan()", "+ datLaiMatKhau()"])]
))

# 32. LỚP PHÂN TÍCH UC07 (Hình 2.32 - QUẢN LÝ LỚP HỌC)
add_diag("Hình 2.32 Biểu đồ lớp UC07", make_ecb(
    "UC07", "FormQuanLyLopHoc",
    ["+ txtMaLop: Textbox", "+ txtTenLop: Textbox", "+ tableSinhVien: TableView", "+ btnThemLop: Button", "+ btnSuaLop: Button", "+ btnXoaLop: Button"],
    ["+ onThemLopClick()", "+ onCapNhatLopClick()", "+ onXoaLopClick()", "+ onImportDSSV()"],
    "LopHocController",
    ["- dsLop: List<Lop>", "- lopHienTai: Lop", "- taiKhoanId: UUID"],
    ["+ kiemTraMaLopDuyNhat(ma)", "+ kiemTraLopChuaCoDiem(ma)", "+ luuLopHoc(lop)", "+ xoaLopHoc(ma)", "+ capNhatDSSinhVien(ds)"],
    [("Lop",
      ["- maLop: String", "- tenLop: String", "- taiKhoanId: UUID"],
      ["+ them()", "+ capNhat()", "+ xoa()", "+ kiemTraCoDiem()"]),
     ("SinhVien",
      ["- mssv: String", "- maLop: String", "- hoTen: String"],
      ["+ them()", "+ xoaTheoLop()", "+ layDanhSachTheoLop()"])]
))

# ==========================================
# 33. BIỂU ĐỒ ERD TOÀN HỆ THỐNG (Hình 2.33)
# ==========================================
def make_erd():
    cells = []
    # Helper to add entity table
    def add_table(tid, name, fields, x, y, w=190, h=160):
        cells.append(cell(tid, f"<b>{name}</b>", S_ERD, x=x, y=y, w=w, h=h))
        cells.append(cell(f"{tid}_f", "<br>".join(fields), S_SEC, parent=tid, x=0, y=28, w=w, h=h-28))

    add_table("t_tk", "TaiKhoan",
              ["<b>PK</b> id: UUID", "tenDangNhap: String", "matKhauHash: String", "hoTen: String", "vaiTro: String", "trangThai: Boolean", "ngayTao: DateTime"],
              x=40, y=60, w=190, h=160)

    add_table("t_mon", "MonHoc",
              ["<b>PK</b> maMon: String", "tenMon: String"],
              x=310, y=60, w=170, h=90)

    add_table("t_cauhoi", "CauHoi",
              ["<b>PK</b> maCauHoi: String", "<b>FK</b> maMon: String", "doKho: String", "noiDung: Text", "dapAn: Text", "<b>FK</b> taiKhoanId: UUID"],
              x=310, y=210, w=180, h=150)

    add_table("t_dethi", "DeThi",
              ["<b>PK</b> maDe: String", "<b>FK</b> maMon: String", "hocKy: String", "namHoc: String", "ngayThi: Date", "thoiLuong: Int", "tongDiem: Float", "<b>FK</b> taiKhoanId: UUID"],
              x=560, y=60, w=190, h=180)

    add_table("t_dt_ch", "DeThi_CauHoi",
              ["<b>PK, FK</b> maDe: String", "<b>PK, FK</b> maCauHoi: String", "thuTu: Int", "diem: Float"],
              x=560, y=300, w=190, h=110)

    add_table("t_lop", "Lop",
              ["<b>PK</b> maLop: String", "tenLop: String", "<b>FK</b> taiKhoanId: UUID"],
              x=820, y=60, w=180, h=100)

    add_table("t_sv", "SinhVien",
              ["<b>PK</b> mssv: String", "<b>FK</b> maLop: String", "hoTen: String"],
              x=820, y=220, w=180, h=100)

    add_table("t_kq", "KetQuaThi",
              ["<b>PK</b> id: UUID", "<b>FK</b> maDe: String", "<b>FK</b> mssv: String", "diemSo: Float", "diemChu: String", "ghiChu: String", "ngayCham: DateTime"],
              x=820, y=380, w=190, h=160)

    # Relationships (Lines)
    # MonHoc 1 -> n CauHoi
    cells.append(cell("r1", "1           n", S_LINE, edge=1, source="t_mon", target="t_cauhoi"))
    # MonHoc 1 -> n DeThi
    cells.append(cell("r2", "1           n", S_LINE, edge=1, source="t_mon", target="t_dethi"))
    # DeThi 1 -> n DeThi_CauHoi
    cells.append(cell("r3", "1           n", S_LINE, edge=1, source="t_dethi", target="t_dt_ch"))
    # CauHoi 1 -> n DeThi_CauHoi
    cells.append(cell("r4", "1           n", S_LINE, edge=1, source="t_cauhoi", target="t_dt_ch"))
    # Lop 1 -> n SinhVien
    cells.append(cell("r5", "1           n", S_LINE, edge=1, source="t_lop", target="t_sv"))
    # DeThi 1 -> n KetQuaThi
    cells.append(cell("r6", "1           n", S_LINE, edge=1, source="t_dethi", target="t_kq", points=[(655, 460)]))
    # SinhVien 1 -> n KetQuaThi
    cells.append(cell("r7", "1           n", S_LINE, edge=1, source="t_sv", target="t_kq"))
    # TaiKhoan 1 -> n CauHoi, DeThi, Lop
    cells.append(cell("r8", "1           n", S_LINE, edge=1, source="t_tk", target="t_cauhoi"))
    cells.append(cell("r9", "1           n", S_LINE, edge=1, source="t_tk", target="t_dethi"))
    cells.append(cell("r10", "1          n", S_LINE, edge=1, source="t_tk", target="t_lop", points=[(135, 20), (910, 20)]))

    return cells

add_diag("Hình 2.33 Biểu đồ thực thể liên kết ERD", make_erd())

# ==========================================
# WRITE OUT ALL DRAWIO FILES & MASTER FILE
# ==========================================
file_map = {
    "Hình 2.1 Biểu đồ Use Case tổng quan": "usecase_overview.drawio",
    "Hình 2.2 Biểu đồ Use Case phân rã UC01": "usecase_uc01.drawio",
    "Hình 2.3 Biểu đồ Use Case phân rã UC02": "usecase_uc02.drawio",
    "Hình 2.4 Biểu đồ Use Case phân rã UC03": "usecase_uc03.drawio",
    "Hình 2.5 Biểu đồ Use Case phân rã UC04": "usecase_uc04.drawio",
    "Hình 2.6 Biểu đồ Use Case phân rã UC05": "usecase_uc05.drawio",
    "Hình 2.7 Biểu đồ Use Case phân rã UC06": "usecase_uc06.drawio",
    "Hình 2.8 Biểu đồ Use Case phân rã UC07": "usecase_uc07.drawio",
    "Hình 2.9 Biểu đồ hoạt động UC00": "activity_uc00.drawio",
    "Hình 2.10 Biểu đồ hoạt động UC01": "activity_uc01.drawio",
    "Hình 2.11 Biểu đồ hoạt động UC02": "activity_uc02.drawio",
    "Hình 2.12 Biểu đồ hoạt động UC03": "activity_uc03.drawio",
    "Hình 2.13 Biểu đồ hoạt động UC04": "activity_uc04.drawio",
    "Hình 2.14 Biểu đồ hoạt động UC05": "activity_uc05.drawio",
    "Hình 2.15 Biểu đồ hoạt động UC06": "activity_uc06.drawio",
    "Hình 2.16 Biểu đồ hoạt động UC07": "activity_uc07.drawio",
    "Hình 2.17 Biểu đồ tuần tự UC00": "sequence_uc00.drawio",
    "Hình 2.18 Biểu đồ tuần tự UC01": "sequence_uc01.drawio",
    "Hình 2.19 Biểu đồ tuần tự UC02": "sequence_uc02.drawio",
    "Hình 2.20 Biểu đồ tuần tự UC03": "sequence_uc03.drawio",
    "Hình 2.21 Biểu đồ tuần tự UC04": "sequence_uc04.drawio",
    "Hình 2.22 Biểu đồ tuần tự UC05": "sequence_uc05.drawio",
    "Hình 2.23 Biểu đồ tuần tự UC06": "sequence_uc06.drawio",
    "Hình 2.24 Biểu đồ tuần tự UC07": "sequence_uc07.drawio",
    "Hình 2.25 Biểu đồ lớp UC00": "class_uc00.drawio",
    "Hình 2.26 Biểu đồ lớp UC01": "class_uc01.drawio",
    "Hình 2.27 Biểu đồ lớp UC02": "class_uc02.drawio",
    "Hình 2.28 Biểu đồ lớp UC03": "class_uc03.drawio",
    "Hình 2.29 Biểu đồ lớp UC04": "class_uc04.drawio",
    "Hình 2.30 Biểu đồ lớp UC05": "class_uc05.drawio",
    "Hình 2.31 Biểu đồ lớp UC06": "class_uc06.drawio",
    "Hình 2.32 Biểu đồ lớp UC07": "class_uc07.drawio",
    "Hình 2.33 Biểu đồ thực thể liên kết ERD": "erd_system.drawio"
}

def build_xml(name, cells):
    root = ET.Element("mxfile", host="Electron", agent="Antigravity", version="21.0.0", type="device")
    clean_id = "".join(ch if ch.isalnum() else "_" for ch in name)
    diag = ET.SubElement(root, "diagram", id=clean_id, name=name)
    model = ET.SubElement(diag, "mxGraphModel", dx="1400", dy="900", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1400", pageHeight="1000", math="0", shadow="0")
    rc = ET.SubElement(model, "root")
    ET.SubElement(rc, "mxCell", id="0")
    ET.SubElement(rc, "mxCell", id="1", parent="0")
    for cell_el in cells:
        rc.append(cell_el)
    return ET.tostring(root, encoding="utf-8").decode("utf-8")

render_tasks = []
for name, filename in file_map.items():
    cells = all_diagrams[name]
    xml_str = build_xml(name, cells)
    filepath = os.path.join(DRAWIO_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(xml_str)
    
    img_name = filename.replace(".drawio", ".png")
    out_img = os.path.join("Đồ án/rendered_images", img_name)
    render_tasks.append({
        "name": name,
        "xml": xml_str,
        "outputPath": out_img,
        "filename": filename
    })

# Also write master multi-tab drawio file
root_master = ET.Element("mxfile", host="Electron", agent="Antigravity", version="21.0.0", type="device")
for name, cells in all_diagrams.items():
    clean_id = "".join(ch if ch.isalnum() else "_" for ch in name)
    diag = ET.SubElement(root_master, "diagram", id=clean_id, name=name)
    model = ET.SubElement(diag, "mxGraphModel", dx="1400", dy="900", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1400", pageHeight="1000", math="0", shadow="0")
    rc = ET.SubElement(model, "root")
    ET.SubElement(rc, "mxCell", id="0")
    ET.SubElement(rc, "mxCell", id="1", parent="0")
    for cell_el in cells:
        rc.append(cell_el)

master_path = os.path.join("Đồ án", "EduExam_Master_All_33_Diagrams.drawio")
with open(master_path, "w", encoding="utf-8") as f:
    f.write(ET.tostring(root_master, encoding="utf-8").decode("utf-8"))

print(f"Generated {len(file_map)} individual .drawio files in {DRAWIO_DIR}")
print(f"Generated master .drawio file: {master_path}")

# Write tasks JSON for Node.js batch renderer
import json
with open("/tmp/render_tasks.json", "w", encoding="utf-8") as f:
    json.dump(render_tasks, f)
print("Saved render tasks to /tmp/render_tasks.json")
