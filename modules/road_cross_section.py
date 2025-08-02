import streamlit as st
import ezdxf
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def page_road_cross_section():
    st.title("Road Cross Section Designer")
    
    with st.sidebar:
        st.header("Vertical Alignment")
        
        # Basic Parameters
        st.subheader("Basic Parameters")
        chainage_start = st.number_input("Start Chainage (m)", min_value=0.0, value=0.0, step=10.0)
        chainage_end = st.number_input("End Chainage (m)", min_value=10.0, value=500.0, step=10.0)
        
        # Existing Ground Level
        st.subheader("Existing Ground Level")
        use_manual_egl = st.checkbox("Specify Manual Ground Levels")
        if use_manual_egl:
            egl_start = st.number_input("Start EGL (m)", value=100.0, step=0.1)
            egl_end = st.number_input("End EGL (m)", value=105.0, step=0.1)
        else:
            egl_slope = st.number_input("EGL Slope (%)", value=1.0, step=0.1) / 100.0
        
        # Formation Level
        st.subheader("Formation Level")
        formation_start = st.number_input("Start Formation Level (m)", value=100.5, step=0.1)
        formation_end = st.number_input("End Formation Level (m)", value=105.5, step=0.1)
        
        # Vertical Curves
        st.subheader("Vertical Curves")
        use_vertical_curve = st.checkbox("Include Vertical Curve")
        if use_vertical_curve:
            vc_chainage = st.number_input("Chainage at VPI (m)", 
                                        min_value=chainage_start, 
                                        max_value=chainage_end,
                                        value=(chainage_start + chainage_end)/2,
                                        step=10.0)
            vc_elevation = st.number_input("Elevation at VPI (m)", value=103.0, step=0.1)
            vc_length = st.number_input("Curve Length (m)", min_value=20.0, value=100.0, step=5.0)
            
            # Calculate gradients
            g1 = ((formation_end - formation_start) / (chainage_end - chainage_start)) * 100
            st.write(f"**Approx. Gradient:** {g1:.2f}%")
        
        # Cross Section Elements
        st.subheader("Cross Section")
        carriageway_width = st.number_input("Carriageway Width (m)", min_value=3.0, value=7.0, step=0.5)
        
        # Shoulders
        has_shoulders = st.checkbox("Include Shoulders")
        if has_shoulders:
            left_shoulder = st.number_input("Left Shoulder Width (m)", min_value=0.5, value=1.5, step=0.25)
            right_shoulder = st.number_input("Right Shoulder Width (m)", min_value=0.5, value=1.5, step=0.25)
        
        # Side Slopes
        st.subheader("Side Slopes")
        left_slope = st.number_input("Left Side Slope (H:V)", min_value=0.5, value=2.0, step=0.5)
        right_slope = st.number_input("Right Side Slope (H:V)", min_value=0.5, value=2.0, step=0.5)
        
        # Cut/Fill Options
        st.subheader("Cut/Fill Options")
        min_cover = st.number_input("Minimum Cover (m)", min_value=0.1, value=0.3, step=0.1)
        max_cut = st.number_input("Maximum Cut (m)", min_value=0.0, value=3.0, step=0.5)
    
    # Calculate chainages and levels
    chainages = np.linspace(chainage_start, chainage_end, 100)
    
    # Calculate formation level profile
    if use_vertical_curve and vc_chainage > chainage_start and vc_chainage < chainage_end:
        # Calculate gradients for vertical curve
        g1 = ((vc_elevation - formation_start) / (vc_chainage - chainage_start)) * 100
        g2 = ((formation_end - vc_elevation) / (chainage_end - vc_chainage)) * 100
        
        # Calculate vertical curve parameters
        l = vc_length
        a = g2 - g1
        
        # Calculate formation levels
        formation_levels = []
        for x in chainages:
            if x <= vc_chainage - l/2:
                # Before curve
                y = formation_start + (g1/100) * (x - chainage_start)
            elif x >= vc_chainage + l/2:
                # After curve
                y = vc_elevation + (g2/100) * (x - vc_chainage)
            else:
                # On curve (parabolic)
                x_vc = x - (vc_chainage - l/2)
                y = formation_start + (g1/100) * (x - chainage_start) + (a * x_vc**2) / (200 * l)
            formation_levels.append(y)
    else:
        # Simple linear profile
        formation_levels = np.linspace(formation_start, formation_end, len(chainages))
    
    # Calculate existing ground levels
    if use_manual_egl:
        egl_levels = np.linspace(egl_start, egl_end, len(chainages))
    else:
        egl_levels = formation_levels[0] - min_cover + egl_slope * (chainages - chainage_start)
    
    # Calculate cut/fill
    cut_fill = [f - e for f, e in zip(formation_levels, egl_levels)]
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [2, 1]})
    
    # Plot profiles
    ax1.plot(chainages, formation_levels, 'b-', label='Formation Level')
    ax1.plot(chainages, egl_levels, 'g-', label='Existing Ground Level')
    
    # Fill between cut and fill
    ax1.fill_between(chainages, formation_levels, egl_levels, 
                    where=np.array(formation_levels) > np.array(egl_levels),
                    color='lightblue', alpha=0.5, label='Fill')
    ax1.fill_between(chainages, formation_levels, egl_levels,
                    where=np.array(formation_levels) <= np.array(egl_levels),
                    color='lightcoral', alpha=0.5, label='Cut')
    
    # Plot vertical curve if applicable
    if use_vertical_curve and vc_chainage > chainage_start and vc_chainage < chainage_end:
        vc_x = [vc_chainage - vc_length/2, vc_chainage, vc_chainage + vc_length/2]
        vc_y = [formation_levels[0] + g1/100 * (vc_x[0] - chainage_start),
               vc_elevation,
               formation_levels[-1] - g2/100 * (chainage_end - vc_x[2])]
        ax1.plot(vc_x, vc_y, 'r--', label='Vertical Curve')
    
    ax1.set_xlabel('Chainage (m)')
    ax1.set_ylabel('Level (m)')
    ax1.set_title('Longitudinal Profile')
    ax1.grid(True)
    ax1.legend()
    
    # Plot cut/fill
    ax2.fill_between(chainages, 0, cut_fill, 
                    where=np.array(cut_fill) > 0,
                    color='lightblue', label='Fill')
    ax2.fill_between(chainages, 0, cut_fill,
                    where=np.array(cut_fill) <= 0,
                    color='lightcoral', label='Cut')
    ax2.axhline(0, color='black', linewidth=0.5)
    ax2.set_xlabel('Chainage (m)')
    ax2.set_ylabel('Cut/Fill (m)')
    ax2.set_title('Cut/Fill Profile')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    
    # Display the plot
    st.pyplot(fig)
    
    # DXF Generation
    if st.button("Generate DXF"):
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()
        
        # Add layers
        doc.layers.new(name='PROFILE', dxfattribs={'color': 1})
        doc.layers.new(name='EGL', dxfattribs={'color': 3})
        doc.layers.new(name='CUT_FILL', dxfattribs={'color': 4})
        
        # Draw formation level
        formation_points = list(zip(chainages, formation_levels))
        msp.add_lwpolyline(formation_points, dxfattribs={'layer': 'PROFILE'})
        
        # Draw EGL
        egl_points = list(zip(chainages, egl_levels))
        msp.add_lwpolyline(egl_points, dxfattribs={'layer': 'EGL'})
        
        # Draw cut/fill areas
        for i in range(len(chainages)-1):
            if cut_fill[i] > 0:  # Fill
                points = [
                    (chainages[i], formation_levels[i]),
                    (chainages[i+1], formation_levels[i+1]),
                    (chainages[i+1], egl_levels[i+1]),
                    (chainages[i], egl_levels[i]),
                    (chainages[i], formation_levels[i])
                ]
                msp.add_lwpolyline(points, dxfattribs={'layer': 'CUT_FILL'})
        
        # Add dimensions
        msp.add_aligned_dim(
            p1=(chainages[0], min(formation_levels) - 2),
            p2=(chainages[-1], min(formation_levels) - 2),
            distance=min(formation_levels) - 3,
            dimstyle='EZDXF',
            override={
                'dimtxsty': 'Standard',
                'dimtxt': 1.0,
                'dimgap': 0.5,
                'dimscale': 1.0
            }
        )
        
        # Save DXF to bytes
        dxf_bytes = BytesIO()
        doc.saveas(dxf_bytes)
        dxf_bytes.seek(0)
        
        # Download button
        st.download_button(
            label="Download Road Profile DXF",
            data=dxf_bytes,
            file_name="road_profile.dxf",
            mime="application/dxf"
        )
        
        st.success("Road Profile DXF generated successfully!")
    
    # Show design calculations
    with st.expander("Design Calculations", expanded=False):
        st.write("### Vertical Alignment Calculations")
        
        if use_vertical_curve and vc_chainage > chainage_start and vc_chainage < chainage_end:
            st.write(f"- Gradient In (G1): {g1:.2f}%")
            st.write(f"- Gradient Out (G2): {g2:.2f}%")
            st.write(f"- Algebraic Difference (A): {a:.2f}%")
            st.write(f"- Curve Length (L): {vc_length:.2f} m")
            
            # K-value (rate of vertical curvature)
            k = vc_length / abs(a) if a != 0 else 0
            st.write(f"- K-value (L/A): {k:.2f} m/%")
            
            # High/Low point calculations
            if a != 0:
                x = (-g1 * vc_length) / a
                if 0 <= x <= vc_length:
                    y = vc_elevation - (g1/100) * (vc_length/2) + (g1/100) * x - (a * x**2) / (200 * vc_length)
                    st.write(f"- High/Low Point at {x:.2f} m from PVC")
                    st.write(f"  - Elevation: {y:.3f} m")
            
            # Stopping sight distance check
            ssd = (design_speed/3.6) * 2.5 + (design_speed**2) / (254 * 0.35)  # Simple SSD formula
            if vc_length < ssd:
                st.warning(f"Warning: Curve length ({vc_length:.1f}m) is less than stopping sight distance ({ssd:.1f}m)")
            
            # Minimum curve length check
            min_l = 0.6 * design_speed  # Simplified minimum length
            if vc_length < min_l:
                st.warning(f"Warning: Curve length ({vc_length:.1f}m) is below recommended minimum ({min_l:.1f}m)")
        
        # Cut/Fill volumes
        total_length = chainage_end - chainage_start
        avg_cut_fill = np.mean(cut_fill)
        total_volume = avg_cut_fill * total_length * (carriageway_width + (left_shoulder if has_shoulders else 0) + (right_shoulder if has_shoulders else 0))
        
        st.write("### Earthwork Quantities")
        st.write(f"- Total Length: {total_length:.1f} m")
        st.write(f"- Average Cut/Fill: {avg_cut_fill:.3f} m")
        st.write(f"- Estimated Total Volume: {abs(total_volume):.1f} m³ ({'Cut' if total_volume < 0 else 'Fill'})")
        
        # Cross section area calculation
        typical_section_area = avg_cut_fill * (carriageway_width + (left_shoulder if has_shoulders else 0) + (right_shoulder if has_shoulders else 0))
        st.write(f"- Typical Cross-Section Area: {abs(typical_section_area):.2f} m²")
