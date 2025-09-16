import streamlit as st
import numpy as np
import ezdxf
from io import BytesIO
import matplotlib.pyplot as plt

def page_road_lsection():
    st.title("Road Longitudinal Section Designer")
    
    with st.sidebar:
        st.header("Road L-Section Parameters")
        
        # Basic Parameters
        st.subheader("Survey Data")
        road_length = st.number_input("Road Length (m)", min_value=100.0, value=1000.0, step=50.0)
        interval = st.number_input("Survey Interval (m)", min_value=10.0, value=20.0, step=5.0)
        
        st.subheader("Level Data")
        max_level = st.number_input("Maximum Level (m)", min_value=50.0, value=100.0, step=1.0)
        min_level = st.number_input("Minimum Level (m)", min_value=0.0, value=85.0, step=1.0)
        nsl_first = st.number_input("NSL of First Point (m)", min_value=0.0, value=88.0, step=0.1)
        
        st.subheader("Road Design Parameters")
        design_speed = st.selectbox("Design Speed (km/h)", [30, 40, 50, 65, 80])
        road_type = st.selectbox("Road Type", ["Village Road", "ODR", "Through Route"])
        gradient_max = st.number_input("Maximum Gradient (%)", min_value=1.0, value=6.0, step=0.5)
        
        # Generate sample data or allow manual input
        st.subheader("Generate Sample Data")
        if st.button("Generate Sample Levels"):
            st.session_state.generate_levels = True
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Longitudinal Section Profile")
        
        # Generate or use sample data
        num_points = int(road_length / interval) + 1
        stations = np.linspace(0, road_length, num_points)
        
        if 'generate_levels' in st.session_state:
            # Generate realistic ground levels with some variation
            base_level = nsl_first
            ground_levels = []
            for i, station in enumerate(stations):
                # Add some realistic variation
                variation = np.sin(station / 100) * 2 + np.random.normal(0, 0.5)
                level = base_level + variation + (station / road_length) * 2  # Slight overall gradient
                ground_levels.append(level)
        else:
            # Default linear interpolation
            ground_levels = np.linspace(nsl_first, nsl_first + 2, num_points)
        
        # Calculate design levels (simplified)
        design_levels = []
        for i, gl in enumerate(ground_levels):
            if i == 0:
                design_levels.append(gl)
            else:
                # Maintain maximum gradient
                max_rise = stations[i] * (gradient_max / 100)
                design_level = min(gl + 0.5, design_levels[0] + max_rise)
                design_levels.append(design_level)
        
        # Create matplotlib plot
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(stations, ground_levels, 'brown', linewidth=2, label='Ground Level')
        ax.plot(stations, design_levels, 'blue', linewidth=2, label='Design Level')
        ax.fill_between(stations, ground_levels, design_levels, alpha=0.3, color='yellow')
        
        ax.set_xlabel('Distance (m)')
        ax.set_ylabel('Level (m)')
        ax.set_title('Road Longitudinal Section')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
    
    with col2:
        st.subheader("Design Summary")
        st.write(f"**Road Length:** {road_length} m")
        st.write(f"**Survey Points:** {num_points}")
        st.write(f"**Design Speed:** {design_speed} km/h")
        st.write(f"**Max Gradient:** {gradient_max}%")
        
        if 'ground_levels' in locals():
            cut_fill_volumes = []
            for gl, dl in zip(ground_levels, design_levels):
                diff = dl - gl
                cut_fill_volumes.append(diff)
            
            total_cut = sum([abs(x) for x in cut_fill_volumes if x < 0]) * interval
            total_fill = sum([x for x in cut_fill_volumes if x > 0]) * interval
            
            st.write(f"**Total Cut:** {total_cut:.1f} m³")
            st.write(f"**Total Fill:** {total_fill:.1f} m³")
            
        st.subheader("Earthwork Analysis")
        if st.button("Calculate Detailed Earthwork"):
            st.write("Detailed earthwork calculation would include:")
            st.write("- Cross-sectional areas")
            st.write("- Prismoidal volumes")
            st.write("- Cut/fill balance")
            st.write("- Haul distances")
    
    # Data input section
    st.subheader("Manual Level Data Input")
    
    # Create a simple data editor for levels
    if st.checkbox("Enable Manual Data Entry"):
        level_data = []
        for i in range(min(10, num_points)):  # Show first 10 points for manual entry
            station = stations[i]
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"Station {station:.0f}m")
            with col_b:
                level = st.number_input(f"Level", value=nsl_first, key=f"level_{i}", step=0.1)
                level_data.append(level)
    
    # Generate DXF
    if st.button("Generate DXF Drawing"):
        dxf_content = generate_road_lsection_dxf(
            stations, ground_levels if 'ground_levels' in locals() else np.linspace(nsl_first, nsl_first + 2, num_points),
            design_levels if 'design_levels' in locals() else np.linspace(nsl_first, nsl_first + 2, num_points),
            road_length, interval, min_level
        )
        
        st.download_button(
            label="Download DXF File",
            data=dxf_content,
            file_name="road_longitudinal_section.dxf",
            mime="application/dxf"
        )
        st.success("DXF file generated successfully!")

def generate_road_lsection_dxf(stations, ground_levels, design_levels, road_length, interval, min_level):
    """Generate DXF for road longitudinal section"""
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Scale factors
    h_scale = 1.0  # Horizontal scale
    v_scale = 10.0  # Vertical scale (exaggerated)
    datum = min_level - 5
    
    # Draw grid
    for i, station in enumerate(stations):
        x = station * h_scale
        # Vertical grid lines
        msp.add_line((x, 0), (x, (max(ground_levels) - datum) * v_scale))
        
        # Station labels
        if i % 5 == 0:  # Every 5th station
            msp.add_text(f"{station:.0f}", 
                        dxfattribs={'height': 20, 'insert': (x, -50)})
    
    # Horizontal grid lines
    for level in range(int(min_level), int(max(ground_levels)) + 2):
        y = (level - datum) * v_scale
        msp.add_line((0, y), (road_length * h_scale, y))
        msp.add_text(f"{level}", 
                    dxfattribs={'height': 15, 'insert': (-100, y)})
    
    # Draw ground profile
    ground_points = [(station * h_scale, (level - datum) * v_scale) 
                    for station, level in zip(stations, ground_levels)]
    msp.add_lwpolyline(ground_points)
    
    # Draw design profile
    design_points = [(station * h_scale, (level - datum) * v_scale) 
                    for station, level in zip(stations, design_levels)]
    msp.add_lwpolyline(design_points)
    
    # Add title and labels
    msp.add_text("ROAD LONGITUDINAL SECTION", 
                dxfattribs={'height': 100, 'insert': (road_length * h_scale / 2, (max(ground_levels) - datum + 2) * v_scale)})
    
    msp.add_text("GROUND LEVEL", 
                dxfattribs={'height': 50, 'insert': (50, (max(ground_levels) - datum + 1) * v_scale)})
    msp.add_text("DESIGN LEVEL", 
                dxfattribs={'height': 50, 'insert': (50, (max(ground_levels) - datum + 0.5) * v_scale)})
    
    # Save to bytes
    buffer = BytesIO()
    doc.write(buffer)
    return buffer.getvalue()
