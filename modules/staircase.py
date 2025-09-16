"""
Staircase Design Module
Based on staircase.LSP functionality for creating staircase structural drawings.
"""

import streamlit as st
import ezdxf
from io import BytesIO
import tempfile
import math

def generate_staircase_dxf(clear_length, width_stair, beam_width, live_load, finish_load, 
                          num_risers, riser_height, tread_width, concrete_grade, 
                          steel_grade, scale):
    """
    Generate DXF for staircase design with structural calculations.
    
    Args:
        clear_length: Clear length of staircase in mm
        width_stair: Width of staircase in mm
        beam_width: Width of supporting beam in mm
        live_load: Live load in kN/m²
        finish_load: Finishes load in kN/m²
        num_risers: Number of risers
        riser_height: Height of each riser in mm
        tread_width: Width of each tread in mm
        concrete_grade: Concrete grade (fck)
        steel_grade: Steel grade (fy)
        scale: Drawing scale factor
        
    Returns:
        bytes: DXF file content as bytes
    """
    # Create a new DXF document
    doc = ezdxf.new('R2010', setup=True)
    msp = doc.modelspace()
    
    # Convert inputs to consistent units
    lc = clear_length / 1000  # Convert to meters
    wstr = width_stair / 1000
    thwall = beam_width / 1000
    ll = live_load
    ff = finish_load
    nrise = num_risers
    rs = riser_height / 1000  # Convert to meters
    td = tread_width / 1000
    fck = concrete_grade
    fy = steel_grade
    
    # Calculate width of going
    ntread = nrise - 1
    wgoing = ntread * td
    
    # Calculate inclination
    incl = math.sqrt(rs**2 + td**2)
    
    # Assume waist slab thickness = L/20
    thkwsb1 = lc / 20
    thkwsb2 = int((thkwsb1 + 0.01) * 100) / 100  # Round up to nearest cm
    thkwsb = max(thkwsb2, 0.15)  # Minimum 150mm
    
    # Design parameters
    clcover = 20  # mm
    mbar = 12  # mm
    mbar1 = mbar / 2
    edepth = thkwsb * 1000 - clcover - mbar1  # Effective depth in mm
    
    # Load calculations
    # 1) Loads on going
    swstsb = 25 * thkwsb * (incl / td)  # Self weight of waist slab
    swstps = 25 * (rs / 2)  # Self weight of steps
    tloadg = swstsb + swstps + ll + ff
    ftloadg = tloadg * 1.5  # Factored load
    
    # 2) Loads on landing
    sfsb = 25 * thkwsb
    tloadl = sfsb + ll + ff
    ftloadl = tloadl * 1.5
    
    # Bending moment calculation
    golth = wgoing + td + (thwall / 2)
    lanth = lc - golth
    raa = ftloadg * golth * (golth / 2 + lanth)
    raaa = ftloadl * lanth * (lanth / 2)
    ra = (raa + raaa) / lc * 1000  # Reaction in N/m
    xmax = ra / ftloadg if ftloadg > 0 else 0
    mmax = ra * xmax - ftloadg * (xmax**2 / 2) if xmax > 0 else 0
    
    # Main reinforcement calculation
    breadth = 1000  # mm (per meter width)
    rrrr = mmax * 1e6
    rrr = rrrr / (breadth * edepth**2) if edepth > 0 else 0
    
    if rrr > 0:
        astm1 = math.sqrt(max(0, 1 - (4.6 * rrr / fck)))
        astm2 = 1 - astm1
        astm3 = edepth * 1000 * 0.5 * fck / fy
        attm = astm2 * astm3
    else:
        attm = 0
    
    # Minimum reinforcement
    attm = max(attm, 0.0012 * breadth * thkwsb * 1000)  # 0.12% minimum
    
    # Spacing of main bars
    bar_area = math.pi * (mbar/2)**2  # Area of one bar in mm²
    bspace = bar_area * 1000 / attm if attm > 0 else 200
    bspace = min(max(int(bspace/10)*10, 100), 300)  # Round and limit
    attmp = bar_area * 1000 / bspace  # Provided area
    
    # Distribution reinforcement
    astdreq = thkwsb * 0.0012 * 1000  # 0.12% of gross area
    dist_bar = 8  # mm
    dist_area = math.pi * (dist_bar/2)**2
    bspaced = dist_area * 1000 / astdreq if astdreq > 0 else 200
    bspaced = min(max(int(bspaced/10)*10, 150), 300)
    
    # Scale factor for drawing
    scale_factor = scale / 1000.0
    
    # Drawing parameters
    drawing_width = clear_length * scale_factor
    drawing_height = (num_risers * riser_height) * scale_factor
    
    # Draw staircase profile
    current_x = 0
    current_y = 0
    
    # Draw the flight profile
    flight_points = [(current_x, current_y)]
    
    # Going portion
    for i in range(ntread):
        current_x += tread_width * scale_factor
        flight_points.append((current_x, current_y))
        current_y += riser_height * scale_factor
        flight_points.append((current_x, current_y))
    
    # Landing portion
    landing_length = (clear_length - wgoing * 1000) * scale_factor
    current_x += landing_length
    flight_points.append((current_x, current_y))
    
    # Draw the flight line
    for i in range(len(flight_points) - 1):
        msp.add_line(flight_points[i], flight_points[i + 1])
    
    # Draw waist slab (underneath the steps)
    waist_points = [(0, -thkwsb * 1000 * scale_factor)]
    
    for i, (x, y) in enumerate(flight_points):
        if i == 0:
            continue
        # Project point down to waist slab
        waist_y = y - thkwsb * 1000 * scale_factor * math.cos(math.atan(rs/td))
        waist_points.append((x, waist_y))
    
    # Close the waist slab outline
    waist_points.append((flight_points[-1][0], flight_points[-1][1] - thkwsb * 1000 * scale_factor))
    waist_points.append((0, 0))
    
    # Draw waist slab as polyline
    msp.add_lwpolyline(waist_points, close=True)
    
    # Add reinforcement indication
    # Main bars (along the span)
    num_bars_shown = 5
    for i in range(num_bars_shown):
        y_pos = -thkwsb * 1000 * scale_factor / 2
        x_start = (clear_length * scale_factor / num_bars_shown) * i + clear_length * scale_factor / (2 * num_bars_shown)
        x_end = x_start
        y_end = y_pos + (num_risers * riser_height * scale_factor) / 2
        msp.add_line((x_start, y_pos), (x_end, y_end))
        
        # Add bar symbol
        msp.add_circle((x_start, y_pos), mbar * scale_factor / 2)
    
    # Add dimensions
    # Overall length
    msp.add_linear_dim(
        base=(clear_length * scale_factor / 2, -100 * scale_factor),
        p1=(0, 0),
        p2=(clear_length * scale_factor, 0),
        dimstyle='EZDXF'
    ).render()
    
    # Overall height
    msp.add_linear_dim(
        base=(-100 * scale_factor, (num_risers * riser_height * scale_factor) / 2),
        p1=(0, 0),
        p2=(0, num_risers * riser_height * scale_factor),
        angle=90,
        dimstyle='EZDXF'
    ).render()
    
    # Add text annotations
    text_height = max(50 * scale_factor, 2.0)
    
    # Title
    title_pos = (clear_length * scale_factor / 2, num_risers * riser_height * scale_factor + 100 * scale_factor)
    msp.add_text("STAIRCASE STRUCTURAL DETAILS", dxfattribs={
        'height': text_height * 1.5,
        'insert': title_pos,
        'rotation': 0,
        'halign': 1  # Center alignment
    })
    
    # Design data table
    table_x = clear_length * scale_factor + 200 * scale_factor
    table_y = num_risers * riser_height * scale_factor
    line_spacing = text_height * 1.2
    
    design_info = [
        f"DESIGN DATA:",
        f"Clear Length: {clear_length/1000:.2f} m",
        f"Width: {width_stair/1000:.2f} m", 
        f"No. of Risers: {num_risers}",
        f"Riser Height: {riser_height} mm",
        f"Tread Width: {tread_width} mm",
        f"Waist Slab: {thkwsb*1000:.0f} mm thick",
        f"Live Load: {live_load} kN/m²",
        f"fck: {concrete_grade} N/mm²",
        f"fy: {steel_grade} N/mm²",
        "",
        f"REINFORCEMENT:",
        f"Main Bars: {mbar}mm ⌀ @ {bspace}mm c/c",
        f"Distribution: {dist_bar}mm ⌀ @ {bspaced}mm c/c",
        f"Cover: {clcover}mm clear",
        "",
        f"Max. Moment: {mmax/1e6:.2f} kNm/m",
        f"Steel Required: {attm:.0f} mm²/m",
        f"Steel Provided: {attmp:.0f} mm²/m"
    ]
    
    for i, info in enumerate(design_info):
        pos = (table_x, table_y - i * line_spacing)
        msp.add_text(info, dxfattribs={
            'height': text_height * 0.8,
            'insert': pos,
            'rotation': 0
        })
    
    # Convert to bytes
    with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as temp_file:
        doc.saveas(temp_file.name)
        with open(temp_file.name, 'rb') as f:
            dxf_bytes = f.read()
    
    return dxf_bytes


def page_staircase():
    """Streamlit page for Staircase design."""
    st.title("🏢 Staircase Structural Design")
    st.markdown("Design reinforced concrete staircases with structural calculations and detailed drawings.")
    
    with st.form("staircase_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("📐 Staircase Geometry")
            clear_length = st.number_input("Clear Length (mm)", min_value=2000, max_value=8000, value=3600, step=100,
                                         help="Clear span length of the staircase")
            
            width_stair = st.number_input("Width of Stair (mm)", min_value=900, max_value=3000, value=1200, step=50,
                                        help="Width of the staircase")
            
            beam_width = st.number_input("Support Beam Width (mm)", min_value=200, max_value=500, value=300, step=25,
                                       help="Width of supporting beam")
            
            st.header("📏 Step Details")
            num_risers = st.slider("Number of Risers", min_value=10, max_value=25, value=18, step=1,
                                 help="Total number of risers in the flight")
            
            riser_height = st.number_input("Riser Height (mm)", min_value=150, max_value=200, value=175, step=5,
                                         help="Height of each riser (150-200mm typical)")
            
            tread_width = st.number_input("Tread Width (mm)", min_value=250, max_value=350, value=275, step=5,
                                       help="Width of each tread (250-350mm typical)")
        
        with col2:
            st.header("📊 Design Loads")
            live_load = st.number_input("Live Load (kN/m²)", min_value=2.0, max_value=10.0, value=4.0, step=0.5,
                                      help="Live load as per IS 875 (4.0 for residential)")
            
            finish_load = st.number_input("Finishes Load (kN/m²)", min_value=0.5, max_value=3.0, value=1.0, step=0.1,
                                        help="Load due to flooring and finishes")
            
            st.header("🔧 Material Properties")
            concrete_grade = st.selectbox("Concrete Grade (fck)", [20, 25, 30, 35, 40], index=1,
                                        help="Characteristic compressive strength of concrete")
            
            steel_grade = st.selectbox("Steel Grade (fy)", [415, 500, 550], index=0,
                                     help="Characteristic strength of reinforcing steel")
            
            st.header("⚙️ Drawing Settings")
            scale = st.slider("Drawing Scale (1:?)", min_value=20, max_value=100, value=50, step=10,
                            help="Scale factor for the drawing")
        
        # Validation and calculations preview
        st.header("📋 Design Summary")
        col3, col4 = st.columns(2)
        
        with col3:
            # Calculate basic parameters
            if num_risers > 0 and riser_height > 0 and tread_width > 0:
                total_rise = num_risers * riser_height
                total_going = (num_risers - 1) * tread_width
                slope_angle = math.degrees(math.atan(riser_height / tread_width))
                
                st.write(f"**Total Rise**: {total_rise}mm ({total_rise/1000:.2f}m)")
                st.write(f"**Total Going**: {total_going}mm ({total_going/1000:.2f}m)")
                st.write(f"**Slope Angle**: {slope_angle:.1f}°")
                
                # Check 2R + T rule
                two_r_plus_t = 2 * riser_height + tread_width
                st.write(f"**2R + T**: {two_r_plus_t}mm")
                if 550 <= two_r_plus_t <= 700:
                    st.success("✅ Comfortable proportions (550-700mm)")
                else:
                    st.warning("⚠️ Check step proportions")
        
        with col4:
            if clear_length > 0:
                # Estimate waist slab thickness
                est_thickness = max(clear_length / 20, 150)
                st.write(f"**Est. Waist Slab**: {est_thickness:.0f}mm")
                st.write(f"**Span/Depth Ratio**: {clear_length/est_thickness:.1f}")
                
                # Load estimate
                total_load = 25 * (est_thickness/1000) + live_load + finish_load  # Self weight + loads
                st.write(f"**Total Load**: {total_load:.1f} kN/m²")
                
                # Rough moment estimate
                moment_est = total_load * (clear_length/1000)**2 / 8
                st.write(f"**Est. Moment**: {moment_est:.1f} kNm/m")
        
        submitted = st.form_submit_button("🖨️ Generate Staircase Design")
    
    if submitted:
        # Validate inputs
        if num_risers <= 0 or riser_height <= 0 or tread_width <= 0:
            st.error("Please enter valid step dimensions.")
            return
        
        if clear_length <= 0 or width_stair <= 0:
            st.error("Please enter valid staircase dimensions.")
            return
        
        with st.spinner("🔄 Generating staircase design..."):
            try:
                # Generate the DXF
                dxf_bytes = generate_staircase_dxf(
                    clear_length, width_stair, beam_width, live_load, finish_load,
                    num_risers, riser_height, tread_width, concrete_grade, 
                    steel_grade, scale
                )
                
                st.success("✅ Staircase design generated successfully!")
                
                # Display preview and download
                col_preview, col_download = st.columns([2, 1])
                
                with col_preview:
                    st.subheader("🏗️ Design Summary")
                    
                    # Calculate key results
                    total_rise = num_risers * riser_height
                    total_going = (num_risers - 1) * tread_width
                    waist_thickness = max(clear_length / 20, 150)
                    
                    st.write(f"**Dimensions**: {clear_length/1000:.2f}m × {width_stair/1000:.2f}m")
                    st.write(f"**Steps**: {num_risers} risers of {riser_height}mm")
                    st.write(f"**Total Rise**: {total_rise/1000:.2f}m")
                    st.write(f"**Waist Slab**: {waist_thickness:.0f}mm thick")
                    st.write(f"**Materials**: M{concrete_grade} concrete, Fe{steel_grade} steel")
                
                with col_download:
                    st.subheader("📥 Download")
                    filename = f"staircase_{int(clear_length/1000)}m_{num_risers}R_1-{scale}.dxf"
                    st.download_button(
                        label="⬇️ Download DXF",
                        data=dxf_bytes,
                        file_name=filename,
                        mime="application/dxf",
                        help="Download the DXF file for this staircase design"
                    )
                
                # Show design checks
                with st.expander("🔍 Design Checks", expanded=False):
                    st.subheader("Code Compliance (IS 456:2000)")
                    
                    # Step proportion checks
                    two_r_plus_t = 2 * riser_height + tread_width
                    
                    checks = {
                        "Riser Height": {
                            "Value": f"{riser_height}mm",
                            "Limit": "150-190mm (residential)",
                            "Status": "✅ OK" if 150 <= riser_height <= 190 else "❌ Check"
                        },
                        "Tread Width": {
                            "Value": f"{tread_width}mm",
                            "Limit": "≥250mm",
                            "Status": "✅ OK" if tread_width >= 250 else "❌ Check"
                        },
                        "2R + T": {
                            "Value": f"{two_r_plus_t}mm",
                            "Limit": "550-700mm",
                            "Status": "✅ OK" if 550 <= two_r_plus_t <= 700 else "❌ Check"
                        },
                        "Waist Slab": {
                            "Value": f"{waist_thickness:.0f}mm",
                            "Limit": "≥L/20, min 150mm",
                            "Status": "✅ OK" if waist_thickness >= clear_length/20 and waist_thickness >= 150 else "❌ Check"
                        }
                    }
                    
                    import pandas as pd
                    df = pd.DataFrame.from_dict(checks, orient='index')
                    st.dataframe(df, use_container_width=True)
            
            except Exception as e:
                st.error(f"❌ Error generating design: {str(e)}")
                st.error("Please check your input values and try again.")
    
    else:
        # Show instructions
        st.info("ℹ️ Configure the staircase parameters and click 'Generate Staircase Design'.")
        
        with st.expander("📖 Staircase Design Guidelines", expanded=False):
            st.markdown("""
            ### IS 456:2000 Guidelines for Staircase Design
            
            #### Step Proportions:
            - **Riser Height**: 150-190mm (residential), 120-190mm (public)
            - **Tread Width**: Minimum 250mm, typically 275-300mm
            - **2R + T Rule**: Should be between 550-700mm for comfort
            - **R + T Rule**: Should be between 400-450mm
            
            #### Structural Design:
            - **Waist Slab Thickness**: Minimum L/20, not less than 150mm
            - **Reinforcement**: Minimum 0.12% of gross area
            - **Cover**: 20mm for interior, 25mm for exterior
            - **Main Steel**: Along the span direction
            - **Distribution Steel**: Perpendicular to main steel
            
            #### Loading:
            - **Live Load**: 3.0 kN/m² (residential), 4.0 kN/m² (office)
            - **Finishes**: 1.0-1.5 kN/m² typically
            - **Self Weight**: 25 kN/m³ for RCC
            
            **Example**: 3.6m span with 18 risers of 175mm and 275mm treads
            """)
