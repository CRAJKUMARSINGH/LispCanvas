import streamlit as st
import os
import tempfile
import sys

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all page modules
try:
    from modules.sunshade import page_sunshade
    from modules.circular_column import page_circular_column
    from modules.rectangular_column import page_rectangular_column
    from modules.rect_column_footing import page_rect_column_footing
    from modules.circular_column_footing import page_circular_column_footing
    from modules.road_lsection import page_road_lsection
    from modules.road_plan import page_road_plan
    from modules.road_cross_section import page_road_cross_section
    from modules.pmgsy_road import page_pmgsy_road
    from modules.lintel import page_lintel
    from modules.t_beam import page_t_beam
    from modules.l_beam import page_l_beam
    from modules.staircase import page_staircase
    from modules.bridge import page_bridge
except ImportError as e:
    st.error(f"Error importing modules: {str(e)}")
    st.error("Please make sure all module files exist in the modules/ directory.")
    st.stop()

def main():
    st.set_page_config(
        page_title="Structural Design Suite",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar navigation
    st.sidebar.title("🏗️ Structural Design Suite")
    st.sidebar.markdown("---")
    
    # Group related modules
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Select Module",
        [
            "Home",
            "Circular Column",
            "Rectangular Column",
            "Rect Column with Footing",
            "Circular Column with Footing",
            "Road L-Section",
            "Road Plan",
            "Road Cross Section",
            "PMGSY Road",
            "Lintel",
            "Sunshade",
            "T-Beam",
            "L-Beam",
            "Staircase",
            "Bridge"
        ]
    )

    # Page routing
    if page == "Home":
        st.title("🏗️ Structural Design Suite")
        st.markdown("""
        Welcome to the Structural Design Suite! This application provides tools for various structural design calculations and drawings.
        
        ### Available Modules:
        - **Columns**
          - Circular Column
          - Rectangular Column
          - Rectangular Column with Footing
          - Circular Column with Footing
        - **Beams**
          - T-Beam
          - L-Beam
        - **Other Structures**
          - Lintel
          - Sunshade
          - Staircase
        - **Road Design**
          - Road L-Section
          - Road Plan
          - Road Cross Section
          - PMGSY Road
        - **Bridge**
          - Bridge Design (from TESTED_BRIDGE_GAD)
        
        Select a module from the sidebar to get started.
        """)
    elif page == "Sunshade":
        def page_sunshade():
            st.title("🌞 Sunshade Design")
            
            # Create a form for all inputs to prevent reruns on each change
            with st.form("sunshade_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.header("🔧 Beam Dimensions")
                    # Use number inputs with min/max values and step sizes
                    web_width = st.number_input("Web Width (mm)", 
                                              min_value=200, max_value=1000, 
                                              value=300, step=10,
                                              help="Width of the supporting beam")
                    
                    total_depth = st.number_input("Beam Depth (mm)", 
                                                min_value=200, max_value=1000, 
                                                value=450, step=10,
                                                help="Total depth of the supporting beam")
                    
                    st.header("📏 Sunshade Dimensions")
                    projection = st.number_input("Projection (mm)", 
                                               min_value=500, max_value=3000, 
                                               value=1000, step=50,
                                               help="Horizontal projection of the sunshade")
                    
                    support_thickness = st.number_input("Thickness at Support (mm)", 
                                                      min_value=100, max_value=300, 
                                                      value=150, step=10,
                                                      help="Thickness where sunshade meets the wall")
                    
                    edge_thickness = st.number_input("Thickness at Edge (mm)", 
                                                   min_value=50, max_value=200, 
                                                   value=100, step=5,
                                                   help="Thickness at the outer edge of sunshade")
                
                with col2:
                    st.header("🔩 Beam Reinforcement")
                    
                    bottom_bar_dia = st.selectbox("Bottom Bar Diameter (mm)", 
                                                [8, 10, 12, 16, 20, 25, 32], 
                                                index=3,
                                                help="Diameter of bottom reinforcement bars")
                    
                    num_bottom_bars = st.slider("Number of Bottom Bars", 
                                               min_value=2, max_value=10, 
                                               value=4, step=1,
                                               help="Number of bars at the bottom of the beam")
                    
                    top_bar_dia = st.selectbox("Top Bar Diameter (mm)", 
                                             [8, 10, 12, 16, 20, 25], 
                                             index=2,
                                             help="Diameter of top reinforcement bars")
                    
                    num_top_bars = st.slider("Number of Top Bars", 
                                           min_value=2, max_value=8, 
                                           value=2, step=1,
                                           help="Number of bars at the top of the beam")
                    
                    stirrup_dia = st.selectbox("Stirrup Diameter (mm)", 
                                             [6, 8, 10, 12], 
                                             index=1,
                                             help="Diameter of shear reinforcement stirrups")
                    
                    stirrup_spacing = st.slider("Stirrup Spacing (mm)", 
                                              min_value=50, max_value=300, 
                                              value=150, step=10,
                                              help="Spacing between stirrups")
                
                # Second row of inputs
                col3, col4 = st.columns(2)
                
                with col3:
                    st.header("🌞 Sunshade Reinforcement")
                    
                    main_bar_dia = st.selectbox("Main Bar Diameter (mm)", 
                                              [8, 10, 12, 16], 
                                              index=1,
                                              help="Diameter of main reinforcement bars in sunshade")
                    
                    dist_bar_dia = st.selectbox("Distribution Bar Diameter (mm)", 
                                              [6, 8, 10, 12], 
                                              index=1,
                                              help="Diameter of distribution bars in sunshade")
                    
                    dist_bar_spacing = st.slider("Distribution Bar Spacing (mm)", 
                                               min_value=100, max_value=300, 
                                               value=150, step=10,
                                               help="Spacing between distribution bars")
                
                with col4:
                    st.header("⚙️ Drawing Settings")
                    
                    scale = st.slider("Drawing Scale (1:?)", 
                                    min_value=10, max_value=100, 
                                    value=25, step=5,
                                    help="Scale factor for the drawing")
                    
                    sunshade_num = st.text_input("Sunshade Number", 
                                               value="01",
                                               help="Identifier for this sunshade design")
                    
                    # Add a reset button
                    if st.form_submit_button("🔄 Reset to Defaults"):
                        st.session_state.clear()
                        st.experimental_rerun()
                    
                    # Submit button for generating the drawing
                    submit_button = st.form_submit_button("🖨️ Generate Sunshade Drawing")
            
            # Generate and display the drawing when the form is submitted
            if submit_button:
                with st.spinner("🔄 Generating Sunshade Drawing..."):
                    try:
                        # Generate the drawing
                        doc = draw_sunshade(
                            web_width, total_depth, projection, support_thickness, edge_thickness,
                            bottom_bar_dia, num_bottom_bars, top_bar_dia, num_top_bars,
                            stirrup_dia, stirrup_spacing, main_bar_dia, dist_bar_dia,
                            dist_bar_spacing, scale, sunshade_num
                        )
                        
                        # Display success message
                        st.success("✅ Sunshade drawing generated successfully!")
                        
                        # Display a preview of the drawing
                        st.subheader("📐 Sunshade Design Preview")
                        col_preview, col_download = st.columns([2, 1])
                        
                        with col_preview:
                            # Placeholder for actual drawing preview
                            st.image("https://via.placeholder.com/800x500?text=Sunshade+Design+Preview\n(Actual+Drawing+Will+Be+In+DXF+File)", 
                                    use_column_width=True)
                        
                        with col_download:
                            st.subheader("📥 Download")
                            st.write("Download the DXF file to view in CAD software:")
                            
                            # Generate and download DXF
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as fp:
                                doc.saveas(fp.name)
                                st.download_button(
                                    label="⬇️ Download DXF",
                                    data=open(fp.name, "rb").read(),
                                    file_name=f"sunshade_ss_{sunshade_num}.dxf",
                                    mime="application/dxf",
                                    help="Download the DXF file for this design"
                                )
                        
                        # Show design summary
                        with st.expander("📋 Design Summary", expanded=True):
                            st.subheader("Design Parameters")
                            
                            col_sunshade, col_beam = st.columns(2)
                            
                            with col_sunshade:
                                st.write("**Sunshade Dimensions**")
                                st.write(f"- Projection: {projection} mm")
                                st.write(f"- Thickness at Support: {support_thickness} mm")
                                st.write(f"- Thickness at Edge: {edge_thickness} mm")
                                st.write("\n**Sunshade Reinforcement**")
                                st.write(f"- Main Bars: {main_bar_dia}mm")
                                st.write(f"- Distribution Bars: {dist_bar_dia}mm @ {dist_bar_spacing}mm c/c")
                            
                            with col_beam:
                                st.write("**Beam Dimensions**")
                                st.write(f"- Width: {web_width} mm")
                                st.write(f"- Depth: {total_depth} mm")
                                st.write("\n**Beam Reinforcement**")
                                st.write(f"- Bottom: {num_bottom_bars}⌀{bottom_bar_dia}mm")
                                st.write(f"- Top: {num_top_bars}⌀{top_bar_dia}mm")
                                st.write(f"- Stirrups: ⌀{stirrup_dia}mm @ {stirrup_spacing}mm c/c")
                    
                    except Exception as e:
                        st.error(f"❌ Error generating drawing: {str(e)}")
                        st.error("Please check your input values and try again.")
            else:
                # Show instructions when the page first loads
                st.info("ℹ️ Fill in the parameters on the left and click 'Generate Sunshade Drawing' to create your design.")
                
                # Add a visual guide
                with st.expander("📏 How to measure sunshade dimensions", expanded=False):
                    st.image("https://via.placeholder.com/600x300?text=Sunshade+Dimensioning+Guide\n(Visual+Guide+to+Measuring+Sunshade+Dimensions)", 
                           use_column_width=True)
                    st.write("""
                    1. **Web Width**: Width of the supporting beam
                    2. **Beam Depth**: Total depth of the supporting beam
                    3. **Projection**: Horizontal distance from the wall to the edge
                    4. **Thickness at Support**: Where the sunshade meets the wall
                    5. **Thickness at Edge**: At the outer edge of the sunshade
                    """)
        page_sunshade()
    elif page == "Circular Column":
        page_circular_column()
    elif page == "Rectangular Column":
        page_rectangular_column()
    elif page == "Rect Column with Footing":
        page_rect_column_footing()
    elif page == "Circular Column with Footing":
        page_circular_column_footing()
    elif page == "Road L-Section":
        page_road_lsection()
    elif page == "Road Plan":
        page_road_plan()
    elif page == "Road Cross Section":
        page_road_cross_section()
    elif page == "PMGSY Road":
        page_pmgsy_road()
    elif page == "Lintel":
        page_lintel()
    elif page == "T-Beam":
        page_t_beam()
    elif page == "L-Beam":
        page_l_beam()
    elif page == "Staircase":
        page_staircase()
    elif page == "Bridge":
        page_bridge()

if __name__ == "__main__":
    main()