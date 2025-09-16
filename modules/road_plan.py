import streamlit as st
import ezdxf
import math
from io import BytesIO

def page_road_plan():
    st.title("Road Plan Designer")
    
    with st.sidebar:
        st.header("Road Alignment")
        
        # Basic Road Parameters
        st.subheader("Basic Parameters")
        road_length = st.number_input("Road Length (m)", min_value=10.0, value=500.0, step=10.0)
        road_width = st.number_input("Road Width (m)", min_value=3.0, value=7.0, step=0.5)
        design_speed = st.number_input("Design Speed (km/h)", min_value=20.0, value=60.0, step=5.0)
        
        # Horizontal Alignment
        st.subheader("Horizontal Alignment")
        alignment_type = st.selectbox("Alignment Type", ["Straight", "Curved", "Combined"])
        
        if alignment_type != "Straight":
            curve_radius = st.number_input("Curve Radius (m)", min_value=15.0, value=100.0, step=5.0)
            curve_angle = st.number_input("Deflection Angle (degrees)", min_value=1.0, value=45.0, step=1.0)
            
            # Calculate curve length
            if alignment_type == "Curved" and st.checkbox("Show Curve Calculations"):
                curve_length = (math.pi * curve_radius * curve_angle) / 180.0
                st.write(f"**Curve Length:** {curve_length:.2f} m")
                
                # Stopping Sight Distance (SSD)
                reaction_time = 2.5  # seconds
                friction_coeff = 0.35  # for wet pavement
                grade = 0.0  # level grade
                
                ssd = (design_speed/3.6) * reaction_time + \
                      (design_speed**2) / (254 * (friction_coeff + (grade/100)))
                st.write(f"**Stopping Sight Distance (SSD):** {ssd:.2f} m")
        
        # Superelevation
        st.subheader("Superelevation")
        superelevation = st.number_input("Superelevation (%)", min_value=0.0, value=5.0, step=0.5) / 100.0
        
        # Cross Section Elements
        st.subheader("Cross Section")
        has_shoulders = st.checkbox("Include Shoulders")
        if has_shoulders:
            shoulder_width = st.number_input("Shoulder Width (m)", min_value=0.5, value=1.5, step=0.25)
        
        # Design Standards
        st.subheader("Design Standards")
        design_standard = st.selectbox("Design Standard", ["IRC:73-1980", "AASHTO", "BS Standards"])
        
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Road Plan View")
        
        # Generate road plan button
        if st.button("Generate Road Plan"):
            # Create DXF for road plan
            doc = ezdxf.new('R2010', setup=True)
            msp = doc.modelspace()
            
            # Draw centerline
            if alignment_type == "Straight":
                start_point = (0, 0)
                end_point = (road_length, 0)
                msp.add_line(start_point, end_point, dxfattribs={'color': 1})
                
            elif alignment_type == "Curved":
                # Simple curved road approximation
                points = []
                num_segments = 20
                for i in range(num_segments + 1):
                    t = i / num_segments
                    if curve_angle <= 90:
                        x = curve_radius * math.sin(math.radians(curve_angle * t))
                        y = curve_radius * (1 - math.cos(math.radians(curve_angle * t)))
                    else:
                        x = t * road_length
                        y = 0
                    points.append((x, y))
                
                # Draw curve as polyline
                msp.add_lwpolyline(points)
            
            # Add road edges
            road_edge_offset = road_width / 2
            if has_shoulders:
                road_edge_offset += shoulder_width
            
            # Add dimensions and labels
            msp.add_text(f"Road Length: {road_length}m", dxfattribs={
                'height': 2.0,
                'insert': (road_length/2, -10)
            })
            
            # Convert to downloadable file
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as temp_file:
                doc.saveas(temp_file.name)
                with open(temp_file.name, 'rb') as f:
                    dxf_bytes = f.read()
            
            st.success("Road plan generated successfully!")
            st.download_button(
                label="Download DXF",
                data=dxf_bytes,
                file_name=f"road_plan_{int(road_length)}m.dxf",
                mime="application/dxf"
            )
    
    with col2:
        st.header("Road Specifications")
        
        # Display calculated parameters
        st.subheader("Calculated Parameters")
        st.write(f"**Road Length:** {road_length} m")
        st.write(f"**Road Width:** {road_width} m")
        st.write(f"**Design Speed:** {design_speed} km/h")
        
        if alignment_type != "Straight":
            st.write(f"**Curve Radius:** {curve_radius} m")
            st.write(f"**Deflection Angle:** {curve_angle}°")
            
        if has_shoulders:
            st.write(f"**Shoulder Width:** {shoulder_width} m")
            st.write(f"**Total Width:** {road_width + 2*shoulder_width} m")
        
        st.write(f"**Superelevation:** {superelevation*100:.1f}%")
        st.write(f"**Design Standard:** {design_standard}")
        
        # Show design checks
        st.subheader("Design Checks")
        
        if alignment_type != "Straight":
            # Minimum radius check
            min_radius = design_speed**2 / (127 * (0.15 + superelevation))  # IRC formula
            if curve_radius >= min_radius:
                st.success(f"✅ Radius OK (Min: {min_radius:.1f}m)")
            else:
                st.error(f"❌ Radius too small (Min: {min_radius:.1f}m)")
        
        # Speed consistency check
        if design_speed > 80:
            st.info("High-speed road - consider expressway standards")
        elif design_speed < 30:
            st.warning("Low-speed road - check urban design guidelines")
