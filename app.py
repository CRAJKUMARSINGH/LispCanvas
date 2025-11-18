import streamlit as st
import os
import tempfile
import sys

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the lintel and sunshade modules specifically (these are the ones the user wants)
try:
    from modules.lintel import page_lintel
    LintelModule = page_lintel
    LintelImportSuccess = True
except Exception as e:
    LintelImportSuccess = False
    LintelImportError = str(e)

try:
    from modules.sunshade import page_sunshade
    SunshadeModule = page_sunshade
    SunshadeImportSuccess = True
except Exception as e:
    SunshadeImportSuccess = False
    SunshadeImportError = str(e)

# Import other modules that don't have dependency issues
try:
    from modules.circular_column import page_circular_column
except:
    page_circular_column = None

try:
    from modules.rectangular_column import page_rectangular_column
except:
    page_rectangular_column = None

try:
    from modules.rect_column_footing import page_rect_column_footing
except:
    page_rect_column_footing = None

try:
    from modules.circular_column_footing import page_circular_column_footing
except:
    page_circular_column_footing = None

try:
    from modules.road_plan import page_road_plan
except:
    page_road_plan = None

try:
    from modules.t_beam import page_t_beam
except:
    page_t_beam = None

try:
    from modules.l_beam import page_l_beam
except:
    page_l_beam = None

try:
    from modules.staircase import page_staircase
except:
    page_staircase = None

try:
    from modules.bridge import page_bridge
except:
    page_bridge = None

def main():
    # Set up the page
    if hasattr(st, 'set_page_config'):
        getattr(st, 'set_page_config')(
            page_title="Structural Design Suite",
            page_icon="🏗️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    else:
        # Fallback for older Streamlit versions
        pass

    # Sidebar navigation
    getattr(getattr(st, 'sidebar'), 'title')("🏗️ Structural Design Suite")
    getattr(getattr(st, 'sidebar'), 'markdown')("---")
    
    # Group related modules
    getattr(getattr(st, 'sidebar'), 'header')("Navigation")
    
    # Build the navigation options
    options = ["Home"]
    if LintelImportSuccess:
        options.append("Lintel")
    if SunshadeImportSuccess:
        options.append("Sunshade")
    
    # Add other modules that imported successfully
    if page_circular_column:
        options.append("Circular Column")
    if page_rectangular_column:
        options.append("Rectangular Column")
    if page_rect_column_footing:
        options.append("Rect Column with Footing")
    if page_circular_column_footing:
        options.append("Circular Column with Footing")
    if page_road_plan:
        options.append("Road Plan")
    if page_t_beam:
        options.append("T-Beam")
    if page_l_beam:
        options.append("L-Beam")
    if page_staircase:
        options.append("Staircase")
    if page_bridge:
        options.append("Bridge")
    
    page = getattr(getattr(st, 'sidebar'), 'radio')("Select Module", options)

    # Handle page routing
    if page == "Home":
        show_home_page()
    elif page == "Lintel" and LintelImportSuccess:
        LintelModule()
    elif page == "Sunshade" and SunshadeImportSuccess:
        SunshadeModule()
    elif page == "Circular Column" and page_circular_column:
        page_circular_column()
    elif page == "Rectangular Column" and page_rectangular_column:
        page_rectangular_column()
    elif page == "Rect Column with Footing" and page_rect_column_footing:
        page_rect_column_footing()
    elif page == "Circular Column with Footing" and page_circular_column_footing:
        page_circular_column_footing()
    elif page == "Road Plan" and page_road_plan:
        page_road_plan()
    elif page == "T-Beam" and page_t_beam:
        page_t_beam()
    elif page == "L-Beam" and page_l_beam:
        page_l_beam()
    elif page == "Staircase" and page_staircase:
        page_staircase()
    elif page == "Bridge" and page_bridge:
        page_bridge()
    else:
        getattr(st, 'error')(f"Module '{page}' is not available.")
        if page == "Lintel" and not LintelImportSuccess:
            getattr(st, 'error')(f"Lintel module import error: {LintelImportError}")
        if page == "Sunshade" and not SunshadeImportSuccess:
            getattr(st, 'error')(f"Sunshade module import error: {SunshadeImportError}")

def show_home_page():
    getattr(st, 'title')("🏗️ Structural Design Suite")
    getattr(st, 'markdown')("""
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
      - Road Plan
    - **Bridge**
      - Bridge Design (from TESTED_BRIDGE_GAD)
    
    Select a module from the sidebar to get started.
    """)
    
    # Show status of the specific modules the user is interested in
    getattr(st, 'subheader')("Target Module Status")
    if LintelImportSuccess:
        getattr(st, 'success')("✅ Lintel module is ready for use")
    else:
        getattr(st, 'error')(f"❌ Lintel module import failed: {LintelImportError}")
        
    if SunshadeImportSuccess:
        getattr(st, 'success')("✅ Sunshade module is ready for use")
    else:
        getattr(st, 'error')(f"❌ Sunshade module import failed: {SunshadeImportError}")

if __name__ == "__main__":
    main()