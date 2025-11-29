import streamlit as st
import ezdxf
import math
from io import BytesIO
import numpy as np
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except:
    HAS_MATPLOTLIB = False

def page_pmgsy_road():
    st.title("PMGSY Road Design")
    
    with st.sidebar:
        st.header("PMGSY Road Parameters")
        
        # Basic Parameters
        st.subheader("Basic Parameters")
        road_length = st.number_input("Road Length (km)", min_value=0.1, value=5.0, step=0.1)
        design_speed = st.selectbox("Design Speed (km/h)", [30, 40, 50, 65], index=1)
        
        # Carriageway
        st.subheader("Carriageway")
        carriageway_type = st.selectbox(
            "Carriageway Type",
            ["Single Lane", "Intermediate Lane", "Double Lane"]
        )
        
        # Shoulders
        st.subheader("Shoulders")
        has_shoulders = st.checkbox("Include Shoulders", value=True)
        if has_shoulders:
            shoulder_width = st.number_input("Shoulder Width (m)", min_value=0.5, value=1.0, step=0.1)
            shoulder_type = st.selectbox(
                "Shoulder Type",
                ["Earthen", "Granular", "Semi-rigid", "Rigid"]
            )
        
        # Cross Slope
        st.subheader("Cross Slope")
        cross_slope = st.number_input("Cross Slope (%)", min_value=2.0, value=2.5, step=0.1) / 100
        
        # Side Drains
        st.subheader("Side Drains")
        has_drains = st.checkbox("Include Side Drains", value=True)
        if has_drains:
            drain_width = st.number_input("Drain Width (m)", min_value=0.3, value=0.45, step=0.05)
            drain_depth = st.number_input("Drain Depth (m)", min_value=0.3, value=0.45, step=0.05)
        
        # Pavement Layers
        st.subheader("Pavement Layers")
        st.write("**Subgrade**")
        cbr_value = st.number_input("CBR Value (%)", min_value=2, value=5, step=1)
        
        st.write("**Base Course**")
        base_thickness = st.number_input("Base Thickness (mm)", min_value=100, value=225, step=25)
        base_material = st.selectbox(
            "Base Material",
            ["WBM", "WMM", "Graded Stone", "Cement Treated"]
        )
        
        st.write("**Surface Course**")
        surface_type = st.selectbox(
            "Surface Type",
            ["BT", "BM", "Semi-Dense Bituminous Concrete", "Dense Bituminous Macadam"]
        )
        surface_thickness = st.number_input("Surface Thickness (mm)", min_value=25, value=50, step=5)
        
        # Design Standards
        st.subheader("Design Standards")
        design_standard = st.selectbox(
            "Design Standard",
            ["PMGSY-III (Latest)", "PMGSY-II", "PMGSY-I"]
        )
    
    # Main content
    st.header("Design Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Geometric Design")
        st.write(f"- **Road Length:** {road_length} km")
        st.write(f"- **Design Speed:** {design_speed} km/h")
        st.write(f"- **Carriageway Type:** {carriageway_type}")
        if has_shoulders:
            st.write(f"- **Shoulder Width:** {shoulder_width} m")
            st.write(f"- **Shoulder Type:** {shoulder_type}")
        st.write(f"- **Cross Slope:** {cross_slope*100}%")
        
    with col2:
        st.subheader("Pavement Design")
        st.write(f"- **Subgrade CBR:** {cbr_value}%")
        st.write(f"- **Base Course:** {base_material} ({base_thickness}mm)")
        st.write(f"- **Surface Course:** {surface_type} ({surface_thickness}mm)")
        if has_drains:
            st.write(f"- **Side Drains:** {drain_width}m x {drain_depth}m")
    
    # DXF Generation
    if st.button("Generate DXF Drawing"):
        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()
        
        # Add layers
        doc.layers.new(name='ROAD', dxfattribs={'color': 1})
        doc.layers.new(name='DIM', dxfattribs={'color': 4})
        
        # Draw road cross-section
        y = 0
        x = 0
        
        # Draw carriageway
        if carriageway_type == "Single Lane":
            width = 3.75
        elif carriageway_type == "Intermediate Lane":
            width = 5.5
        else:  # Double Lane
            width = 7.0
            
        # Draw road surface
        points = [
            (x, y),
            (x + width, y),
            (x + width, y + 0.1),  # Surface thickness
            (x, y + 0.1)
        ]
        msp.add_lwpolyline(points, dxfattribs={'layer': 'ROAD'})
        
        # Draw base layer
        base_points = [
            (x - 0.1, y - (base_thickness/1000)),
            (x + width + 0.1, y - (base_thickness/1000)),
            (x + width + 0.1, y),
            (x - 0.1, y)
        ]
        msp.add_lwpolyline(base_points, dxfattribs={'layer': 'ROAD'})
        
        # Add dimensions
        msp.add_aligned_dim(
            p1=(x, y + 0.2),
            p2=(x + width, y + 0.2),
            distance=0.3,
            dimstyle='EZDXF'
        )
        
        # Save DXF to bytes
        dxf_bytes = BytesIO()
        doc.saveas(dxf_bytes)
        dxf_bytes.seek(0)
        
        # Download button
        st.download_button(
            label="Download PMGSY Road DXF",
            data=dxf_bytes,
            file_name="pmgsy_road.dxf",
            mime="application/dxf"
        )
        
        st.success("PMGSY Road DXF generated successfully!")
    
    # Show design calculations
    with st.expander("Design Calculations", expanded=False):
        st.write("### Pavement Design as per IRC:37")
        
        # Traffic calculation (simplified)
        st.write("#### Traffic Analysis")
        st.write(f"- Design Traffic (msa): {calculate_traffic(design_speed, road_length)}")
        
        # Pavement thickness calculation
        st.write("#### Pavement Thickness Design")
        st.write("- Minimum recommended thicknesses based on CBR and traffic")
        
        # Drainage requirements
        if has_drains:
            st.write("#### Drainage Design")
            st.write("- Side drains designed for 1 in 2 year storm event")
    
    # Show PMGSY standards
    with st.expander("PMGSY Standards", expanded=False):
        st.write("### PMGSY Design Standards")
        st.write("- Minimum carriageway width: 3.75m (Single Lane)")
        st.write("- Minimum shoulder width: 1.0m")
        st.write("- Maximum gradient: 1 in 15 (6.67%)")
        st.write("- Minimum curve radius: 50m")
        st.write("- Minimum CBR: 5% for subgrade")
        st.write("- Minimum pavement thickness: 530mm (including sub-base)")

def calculate_traffic(design_speed, road_length):
    # Simplified traffic calculation
    if design_speed <= 30:
        return round(1 * road_length, 2)
    elif design_speed <= 40:
        return round(2 * road_length, 2)
    elif design_speed <= 50:
        return round(3 * road_length, 2)
    else:
        return round(5 * road_length, 2)
