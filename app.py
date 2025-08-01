# RECTANGLE COLUMN WOTH FOOTING
# # app.py
import streamlit as st
import ezdxf
from math import ceil, sin, cos, radians
import tempfile, os, datetime, json

st.set_page_config(page_title="RC Column-Footing Detailer", layout="wide")

st.title("📐 RC Column-Footing Detailer (Desktop)")
st.caption("Port of the original AutoLISP `FOOTSQR` to Streamlit")

# ---------- Sidebar = design inputs ----------
with st.sidebar:
    st.header("Rectangular Column")
    b        = st.number_input("Column width B (mm)", 200, 800, 300)
    d        = st.number_input("Column depth D (mm)", 200, 800, 450)
    dia_long = st.number_input("Long. bar dia (mm)", 10, 40, 20)
    n_total  = st.number_input("Total #long bars", 4, 20, 8)
    n_flange = st.number_input("#bars per flange", 2, 10, 3)
    dia_tie  = st.number_input("Tie dia (mm)", 6, 16, 8)
    spacing  = st.number_input("Tie spacing (mm)", 50, 300, 150)
    col_num  = st.text_input("Column mark", "C-42")

    st.header("Footing")
    footing_side      = st.number_input("Footing side (mm)", 1000, 4000, 2100)
    depth_edge        = st.number_input("Depth at edge (mm)", 150, 600, 300)
    depth_centre      = st.number_input("Depth at centre (mm)", 200, 1000, 600)
    mesh_dia_x        = st.number_input("Mesh dia X (mm)", 8, 25, 16)
    mesh_spacing_x    = st.number_input("Mesh spacing X (mm)", 50, 300, 150)
    mesh_dia_y        = st.number_input("Mesh dia Y (mm)", 8, 25, 16)
    mesh_spacing_y    = st.number_input("Mesh spacing Y (mm)", 50, 300, 150)
    pcc_proj          = st.number_input("PCC projection (mm)", 0, 200, 75)
    pcc_thick         = st.number_input("PCC thickness (mm)", 50, 150, 100)
    pedestal_proj     = st.number_input("Pedestal projection (mm)", 0, 300, 150)
    scale             = st.number_input("Drawing scale", 1, 100, 25)
    
    # ---------- Circular column ----------
    st.header("Circular Column")
    d_circ = st.number_input("Diameter (mm)", 200, 800, 300, key="d_circ")
    dia_long_circ = st.number_input("Long. bar dia (mm)", 10, 40, 20, key="dialc")
    n_total_circ = st.number_input("Total #bars", 4, 20, 8, key="ntc")
    dia_tie_circ = st.number_input("Tie dia (mm)", 6, 16, 8, key="dtc")
    spacing_circ = st.number_input("Tie spacing (mm)", 50, 300, 150, key="spc")
    col_num_circ = st.text_input("Column mark", "C-43", key="cnc")

    # --------------------------------------------------
    #  NEW  –  STAIRCASE DETAILER
    # --------------------------------------------------
    st.sidebar.header("Staircase")
    if st.sidebar.checkbox("Add Staircase"):
        # ----------- Parameters (same names as LISP) ----------
        cl = st.number_input("Clear span (mm)", 2000, 6000, 3000, key="cl")
        wst = st.number_input("Stair width (mm)", 800, 2000, 1000, key="wst")
        thwall = st.number_input("Support wall width (mm)", 200, 400, 230, key="thwall")
        ll = st.number_input("Live load (kN/m²)", 2.0, 5.0, 3.0, key="ll")
        ff = st.number_input("Floor finish (kN/m²)", 0.5, 2.0, 1.0, key="ff")
        nrise = st.number_input("No. of risers", 8, 20, 12, key="nrise")
        rise = st.number_input("Riser (mm)", 140, 190, 150, key="rise")
        tread = st.number_input("Tread (mm)", 250, 320, 280, key="tread")
        fck = st.number_input("fck (N/mm²)", 15, 50, 25, key="fck")
        fy = st.number_input("fy (N/mm²)", 250, 500, 415, key="fy")

        # ----------- DESIGN CALCULATIONS (same as LISP) -------------
        import math
        ntread = nrise - 1
        wgoing = ntread * tread
        incl = math.sqrt(rise**2 + tread**2)
        thkwsb = max(20, round((cl / 20) / 10) * 10)           # waist slab (mm)
        cover = 20
        edepth = thkwsb - cover - 12/2                         # 12 mm main bar
        swstsb = 25 * thkwsb * incl / tread / 1000**2          # kN/m²
        swstps = 25 * rise/2 / 1000**2                         # kN/m²
        tloadg = swstsb + swstps + ll + ff
        ftloadg = tloadg * 1.5
        sfsb = 25 * thkwsb / 1000**2                           # landing
        tloadl = sfsb + ll + ff
        ftloadl = tloadl * 1.5
        golth = (wgoing + tread + thwall/2) / 1000
        lanth = (cl/1000 - golth)
        ra = ((ftloadg * golth * (golth/2 + lanth) + ftloadl * lanth**2/2) * 1000) / cl
        xmax = ra / ftloadg
        mmax = (ra * xmax - ftloadg * xmax**2 / 2) * 1e3       # kN-mm
        ast_req = (mmax * 1e3) / (0.87 * fy * 0.8 * edepth)    # mm²/m
        spacing12 = min(300, round(113 * 1000 / ast_req / 10) * 10)  # 12 mm bars
        ast_dist = 0.0012 * thkwsb * 1000                      # mm²/m
        spacing8 = min(300, round(50.3 * 1000 / ast_dist / 10) * 10) # 8 mm bars

        # ----------- 2-D DRAWING ----------
        doc_stair = ezdxf.new("R2010")
        msp = doc_stair.modelspace()
        
        # Plan
        plan_pts = [(0, 0), (wgoing + tread, 0), (wgoing + tread, wst), (0, wst)]
        msp.add_lwpolyline(plan_pts, close=True)
        
        # Elevation (positioned below plan)
        elev_y_offset = -wst - 500
        elev_pts = [
            (0, elev_y_offset),
            (wgoing, elev_y_offset),
            (wgoing, elev_y_offset + nrise*rise),
            (0, elev_y_offset + nrise*rise)
        ]
        msp.add_lwpolyline(elev_pts, close=True)
        
        # Add riser lines in elevation
        for i in range(1, nrise + 1):
            y = elev_y_offset + i * rise
            msp.add_line((0, y), (wgoing, y))
        
        # Add text labels
        msp.add_text(f"Staircase Design", dxfattribs={'height': 100}).set_pos((0, elev_y_offset - 200))
        msp.add_text(f"Plan View", dxfattribs={'height': 50}).set_pos((100, -100))
        msp.add_text(f"Elevation View", dxfattribs={'height': 50}).set_pos((100, elev_y_offset - 100))
        
        # ----------- RESULTS ----------
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write(f"Staircase Design Report\n")
            f.write("="*40 + "\n\n")
            f.write(f"Clear span (CL)    : {cl} mm\n")
            f.write(f"Stair width (WST) : {wst} mm\n")
            f.write(f"No. of risers     : {nrise}\n")
            f.write(f"Riser x Tread     : {rise} x {tread} mm\n")
            f.write(f"Waist slab thick. : {thkwsb} mm\n")
            f.write(f"Main bars (12 mm) : @ {spacing12} mm c/c\n")
            f.write(f"Dist. bars (8 mm) : @ {spacing8} mm c/c\n")
            f.write(f"Max BM            : {mmax/1e6:.2f} kN-m/m\n")
            f.write("\nDesign by RajStructure\n")
            f.flush()
            
            # Save DXF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as dxf_file:
                doc_stair.saveas(dxf_file.name)
                
                # Display download buttons in a column
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📄 Download Design Report",
                        data=open(f.name, "rb").read(),
                        file_name="staircase_design_report.txt",
                        mime="text/plain"
                    )
                with col2:
                    st.download_button(
                        "⬇️ Download Staircase DXF",
                        data=open(dxf_file.name, "rb").read(),
                        file_name="staircase_drawing.dxf",
                        mime="application/dxf"
                    )
        
        # Display preview
        st.image("https://via.placeholder.com/800x400?text=Staircase+Plan+%26+Elevation")

# ---------- Geometry helpers ----------
cover = 40
def bar_xy(n, spacing, cover):
    return [cover + i*spacing for i in range(n)]

# ---------- DXF generation ----------
@st.cache_data
def make_dxf():
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    # footing plan rectangle
    half = footing_side/2
    msp.add_lwpolyline([(-half, -half), (half, -half), (half, half), (-half, half)], close=True)
    # column rectangle
    msp.add_lwpolyline([(-b/2, -d/2), (b/2, -d/2), (b/2, d/2), (-b/2, d/2)], close=True)
    # footing mesh X
    y = bar_xy(ceil((footing_side-2*cover)/mesh_spacing_x)+1, mesh_spacing_x, -half+cover)
    for yc in y:
        msp.add_line((-half, yc), (half, yc))
    # footing mesh Y
    x = bar_xy(ceil((footing_side-2*cover)/mesh_spacing_y)+1, mesh_spacing_y, -half+cover)
    for xc in x:
        msp.add_line((xc, -half), (xc, half))
    # column bars (simplified)
    dy = bar_xy(n_flange, (d-2*cover)/(n_flange-1), -d/2+cover)
    for yc in dy:
        msp.add_line((0, yc), (0, yc+depth_centre))
    # text
    msp.add_text(f"Column {col_num}", dxfattribs={'height': 50, 'layer': "TEXT"}).set_pos((-half-200, -half-200))
    return doc

doc = make_dxf()

# ---------- Circular-column DXF generator ----------
@st.cache_data
def make_dxf_circ():
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    # outer circle
    msp.add_circle((0, 0), d_circ/2)
    # rebar circle
    radius_bars = d_circ/2 - cover - dia_long_circ/2
    angle_step = 360 / n_total_circ
    for i in range(n_total_circ):
        a = radians(i * angle_step)
        x = radius_bars * cos(a)
        y = radius_bars * sin(a)
        msp.add_circle((x, y), dia_long_circ/2)
    # text
    msp.add_text(f"Column {col_num_circ}", dxfattribs={'height': 50}).set_pos((0, -d_circ/2 - 100))
    return doc

doc_circ = make_dxf_circ()

# ---------- Material take-off (circular) ----------
steel_circ = n_total_circ * 3.1416*(dia_long_circ/2)**2 * 3 * 7850 * 1e-6  # kg (3 m stub)

# --------------------------------------------------
#  PMGSY / RURAL ROADS  (Part-C)
# --------------------------------------------------
with st.sidebar:
    if st.checkbox("Enable PMGSY Roads"):
        st.subheader("PMGSY Roads")
        detailer = st.selectbox("Choose PMGSY detailer",
                               ["Road Plan", "Road L-Section", "Cross-Section"])

        # --- parameters common to all three ---
        road_mark = st.text_input("Road mark", "PMGSY-01")
        fw = st.number_input("Formation width (m)", 4.0, 10.0, 7.5)
        cw = st.number_input("Carriageway width (m)", 3.0, 7.5, 3.75)
        max_level = st.number_input("Max level (m)", 90.0, 150.0, 100.0)
        min_level = st.number_input("Min level (m)", 85.0, 95.0, 88.0)
        datum = int(min_level / 5) * 5   # auto-datum like LISP
        camber_c = st.number_input("Camber carriageway (%)", 1.0, 5.0, 3.0)
        camber_s = st.number_input("Camber shoulder (%)", 2.0, 6.0, 4.0)
        side_slope = st.number_input("Side slope (n:1)", 1.0, 5.0, 1.5)

        # --- detailer-specific ---
        if detailer == "Road Plan":
            n_lines = st.number_input("No. of plan lines", 1, 20, 5)
            lengths = [st.number_input(f"Length {i+1} (m)", 10.0, 500.0, 50.0, key=f"len{i}")
                      for i in range(n_lines)]
            angles = [st.number_input(f"Angle {i+1} (deg)", -180, 180, 0, key=f"ang{i}")
                     for i in range(n_lines)]

        elif detailer == "Road L-Section":
            length = st.number_input("Road length (m)", 50.0, 1000.0, 500.0)
            interval = st.number_input("Survey interval (m)", 5.0, 50.0, 20.0)
            nsl_first = st.number_input("NSL first point (m)", 85.0, 95.0, 89.0)
            # allow user to enter NSL for every station
            nof = int(length / interval)
            ns_list = [st.number_input(f"NSL @ {i*interval} m",
                                     min_level-2, max_level+2,
                                     nsl_first - i*0.5, key=f"nsl{i}")
                      for i in range(nof+1)]

        elif detailer == "Cross-Section":
            # pre-filled 3-pt example, user can override
            pts_l = [(st.number_input(f"Left pt {i+1} offset (m)", -fw-5, 0.0, -i-1.0, key=f"lo{i}"),
                      st.number_input(f"Left pt {i+1} NSL (m)", min_level-2, max_level+2,
                                    88.0-i*0.5, key=f"ln{i}"))
                    for i in range(3)]
            pts_r = [(st.number_input(f"Right pt {i+1} offset (m)", 0.0, fw+5, i+1.0, key=f"ro{i}"),
                      st.number_input(f"Right pt {i+1} NSL (m)", min_level-2, max_level+2,
                                    88.0-i*0.5, key=f"rn{i}"))
                    for i in range(3)]

        fl_point = st.number_input("Formation level (m)", 85.0, 95.0, 90.0)

        @st.cache_data
        def make_pmgsy_dxf(detailer, **kw):
            doc = ezdxf.new("R2010")
            msp = doc.modelspace()
            if detailer == "Road Plan":
                pt = (0, 0)
                for L, A in zip(kw["lengths"], kw["angles"]):
                    rad = math.radians(A)
                    next_pt = (pt[0] + L * math.cos(rad),
                              pt[1] + L * math.sin(rad))
                    msp.add_line(pt, next_pt)
                    pt = next_pt
                # Add chainage markers
                for i, (L, A) in enumerate(zip(kw["lengths"], kw["angles"])):
                    msp.add_text(f"{L:.1f}m", dxfattribs={'height': 5}) \
                       .set_pos((pt[0]/2, pt[1]/2 - 5))

            elif detailer == "Road L-Section":
                length, interval, ns_list = kw["length"], kw["interval"], kw["ns_list"]
                # vertical datum line
                msp.add_line((0, -10), (0, kw["max_level"] - kw["datum"]))
                # datum text
                msp.add_text(f"Datum {kw['datum']} m", dxfattribs={'height': 1}) \
                   .set_pos((-15, 0))
                # NSL polyline
                pts = [(i * interval, ns - kw["datum"])
                      for i, ns in enumerate(ns_list)]
                msp.add_lwpolyline(pts)
                # formation line
                yf = kw["fl"] - kw["datum"]
                msp.add_line((0, yf), (length, yf))
                # Add chainage markers
                for i in range(0, int(length) + 1, 50):
                    if i <= length:
                        msp.add_line((i, -1), (i, -3))
                        msp.add_text(f"{i}", dxfattribs={'height': 2}) \
                           .set_pos((i, -5))

            elif detailer == "Cross-Section":
                fw, cw, fl, datum = kw["fw"], kw["cw"], kw["fl"], kw["datum"]
                camber_c, camber_s, side_slope = kw["camber_c"], kw["camber_s"], kw["side_slope"]
                sw = (fw - cw) / 2
                yf = fl - datum
                # centre
                ptfc = (0, yf)
                ptfl1 = (-cw/2, yf - (camber_c * cw / 100))
                ptfl2 = (-fw/2, ptfl1[1] - (camber_s * sw / 100))
                r = side_slope * (ptfl2[1] - 0)
                ptfl3 = (ptfl2[0] - r, 0)
                ptfr1 = (cw/2, ptfl1[1])
                ptfr2 = (fw/2, ptfl2[1])
                ptfr3 = (ptfr2[0] + r, 0)
                msp.add_lwpolyline([ptfl3, ptfl2, ptfl1, ptfc, ptfr1, ptfr2, ptfr3])
                # survey points
                for x, y in kw["pts_l"] + kw["pts_r"][::-1]:  # Reverse right points for correct order
                    msp.add_line((x, y - datum), (x, y - datum + 2))
                    msp.add_text(f"{y:.2f}", dxfattribs={'height': 0.5}) \
                       .set_pos((x, y - datum + 2.5))
                # Add labels
                msp.add_text("C/L", dxfattribs={'height': 1}).set_pos((0, yf + 1))
                msp.add_text(f"FW={fw}m", dxfattribs={'height': 1}).set_pos((0, yf + 2))
                msp.add_text(f"CW={cw}m", dxfattribs={'height': 1}).set_pos((0, yf + 3))
            
            # Add title block
            msp.add_text(f"PMGSY Road - {detailer}", dxfattribs={'height': 3}) \
               .set_pos((0, -10))
            msp.add_text(f"Mark: {kw.get('road_mark', '')}", dxfattribs={'height': 2}) \
               .set_pos((0, -15))
            msp.add_text(f"Scale: 1:100 | Date: {datetime.date.today()}", 
                        dxfattribs={'height': 1.5}) \
               .set_pos((0, -18))
            
            return doc

        # ---------- Generate and download DXF ----------
        kw = {
            "detailer": detailer,
            "fw": fw, "cw": cw, "max_level": max_level, "min_level": min_level,
            "datum": datum, "camber_c": camber_c, "camber_s": camber_s,
            "side_slope": side_slope, "fl": fl_point, "road_mark": road_mark
        }

        if detailer == "Road Plan":
            kw.update(lengths=lengths, angles=angles)
        elif detailer == "Road L-Section":
            kw.update(length=length, interval=interval, ns_list=ns_list)
        elif detailer == "Cross-Section":
            kw.update(pts_l=pts_l, pts_r=pts_r)

        if st.button("Generate Drawing"):
            doc = make_pmgsy_dxf(**kw)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as fp:
                doc.saveas(fp.name)
                st.download_button(
                    "⬇️ Download PMGSY DXF", 
                    data=open(fp.name, "rb").read(),
                    file_name=f"{road_mark}_{detailer.replace(' ', '_')}.dxf",
                    mime="application/dxf"
                )

        # Display preview
        st.image(f"https://via.placeholder.com/800x400?text=PMGSY+{detailer.replace(' ', '+')}")

# --------------------------------------------------
#  ROAD CROSS-SECTION DETAILER (Part-B)
# --------------------------------------------------
with st.sidebar:
    if st.checkbox("Enable Road Segment"):
        st.subheader("Road Cross-Section")
        fw = st.number_input("Formation width (m)", 5.0, 20.0, 10.0)
        cw = st.number_input("Carriageway width (m)", 3.0, 15.0, 7.0)
        max_level = st.number_input("Max level (m)", 90.0, 150.0, 100.0)
        min_level = st.number_input("Min level (m)", 85.0, 95.0, 88.0)
        nsl = st.number_input("Centre NSL (m)", 85.0, 95.0, 89.0)
        fl = st.number_input("Formation level (m)", 85.0, 95.0, 90.0)
        camber_c = st.number_input("Carriageway camber (%)", 1.0, 5.0, 2.0)
        camber_s = st.number_input("Shoulder camber (%)", 2.0, 6.0, 3.0)
        side_slope = st.number_input("Side slope (n : 1) – n", 1.0, 5.0, 2.0)
        points_l = st.number_input("Survey points left", 1, 10, 3)
        points_r = st.number_input("Survey points right", 1, 10, 3)

        # quick survey points array
        left_pts = []
        for i in range(int(points_l)):
            dl = st.number_input(f"Left pt {i+1} offset (m)", -fw, 0.0, -i-1.0, key=f"dl{i}")
            nsl_l = st.number_input(f"Left pt {i+1} NSL (m)", min_level, max_level, 88.0-i*0.5, key=f"nsl_l{i}")
            left_pts.append((dl, nsl_l))
        right_pts = []
        for i in range(int(points_r)):
            dr = st.number_input(f"Right pt {i+1} offset (m)", 0.0, fw, i+1.0, key=f"dr{i}")
            nsl_r = st.number_input(f"Right pt {i+1} NSL (m)", min_level, max_level, 88.0-i*0.5, key=f"nsl_r{i}")
            right_pts.append((dr, nsl_r))

        road_mark = st.text_input("Road mark", "RD-101")

# Generate Road DXF if enabled
if st.sidebar.checkbox("Enable Road Segment", key="road_toggle"):
    # ---------- DESIGN ----------
    datum = int(min_level / 5) * 5
    sw = (fw - cw) / 2
    
    # 2-D cross-section
    doc_road = ezdxf.new("R2010")
    msp = doc_road.modelspace()
    
    # centre line
    msp.add_line((0, 0), (0, 5))
    
    # formation polygon
    yf = fl - datum
    ptfc = (0, yf)
    ptfl1 = (-cw/2, yf - (camber_c * cw / 200))
    ptfl2 = (-fw/2, ptfl1[1] - (camber_s * sw / 200))
    r = side_slope * (ptfl2[1] - 0)
    ptfl3 = (ptfl2[0] - r, 0)
    ptfr1 = (cw/2, ptfl1[1])
    ptfr2 = (fw/2, ptfl2[1])
    ptfr3 = (ptfr2[0] + r, 0)
    pts = [ptfl3, ptfl2, ptfl1, ptfc, ptfr1, ptfr2, ptfr3]
    msp.add_lwpolyline(pts, close=False)

    # survey lines
    for x, y in left_pts:
        msp.add_line((x, y - datum), (x, y - datum + 1))
    for x, y in right_pts:
        msp.add_line((x, y - datum), (x, y - datum + 1))

    # text labels
    texts = [
        (ptfl3[0] - 2, 0, f"Datum {datum} m"),
        (ptfl3[0] - 2, nsl - datum, f"NSL {nsl} m"),
        (ptfl3[0] - 2, fl - datum, f"FL {fl} m")
    ]
    for x, y, txt in texts:
        msp.add_text(txt, dxfattribs={'height': 0.5}).set_pos((x, y))

    # Add title and scale
    msp.add_text(f"Road Cross-Section: {road_mark}", 
                dxfattribs={'height': 1.0}).set_pos((0, yf + 2))
    msp.add_text(f"Scale: 1:100 | Date: {datetime.date.today()}",
                dxfattribs={'height': 0.5}).set_pos((0, yf + 1))

    # ---------- DOWNLOAD ----------
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as fp:
        doc_road.saveas(fp.name)
        st.download_button(
            "⬇️ Download Road DXF", 
            data=open(fp.name, "rb").read(),
            file_name=f"{road_mark}.dxf",
            mime="application/dxf"
        )

    # ---------- LIVE PREVIEW ----------
    st.subheader(f"Road Cross-Section: {road_mark}")
    st.image("https://via.placeholder.com/800x400?text=Road+Cross-Section")

# ---------- Viewer ----------
col1, col2 = st.columns(2)
with col1:
    st.subheader("Rectangular Column Plan")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as fp:
        doc.saveas(fp.name)
        st.download_button("⬇️ Download Rectangular DXF", data=open(fp.name,'rb').read(), file_name=f"{col_num}.dxf")
    st.image("https://via.placeholder.com/400x400?text=Rectangular+Plan", use_column_width=True)

with col2:
    st.subheader("Circular Column Plan")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as fp:
        doc_circ.saveas(fp.name)
        st.download_button("⬇️ Download Circular DXF", data=open(fp.name,'rb').read(),
                         file_name=f"{col_num_circ}.dxf")
    st.image("https://via.placeholder.com/400x400?text=Circular+Plan", use_column_width=True)

# ---------- Material take-off ----------
st.header("Material Take-off")
st.subheader("Rectangular Column")
concrete = footing_side**2 * depth_centre * 1e-9    # m³
steel_long = n_total * 3.1416*(dia_long/2)**2 * (depth_centre/1000) * 7850 * 1e-6  # kg
st.metric("Concrete", f"{concrete:.2f} m³")
st.metric("Long. steel", f"{steel_long:.1f} kg")

st.subheader("Circular Column")
st.metric("Steel (3m stub)", f"{steel_circ:.1f} kg")