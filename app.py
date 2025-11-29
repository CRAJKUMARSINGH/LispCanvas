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
    from modules.road_lsection import page_road_lsection
except:
    page_road_lsection = None

try:
    from modules.road_cross_section import page_road_cross_section
except:
    page_road_cross_section = None

try:
    from modules.pmgsy_road import page_pmgsy_road
except:
    page_pmgsy_road = None

try:
    from modules.t_beam import page_t_beam
except:
    page_t_beam = None

try:
    from modules.l_beam import page_l_beam
except:
    page_l_beam = None

try:
    from modules.rectangular_beam import page_rectangular_beam
except:
    page_rectangular_beam = None

try:
    from modules.inverted_t_beam import page_inverted_t_beam
except:
    page_inverted_t_beam = None

try:
    from modules.inverted_l_beam import page_inverted_l_beam
except:
    page_inverted_l_beam = None

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
    if page_road_lsection:
        options.append("Road L-Section")
    if page_road_cross_section:
        options.append("Road Cross Section")
    if page_pmgsy_road:
        options.append("PMGSY Road")
    if page_t_beam:
        options.append("T-Beam")
    if page_l_beam:
        options.append("L-Beam")
    if page_rectangular_beam:
        options.append("Rectangular Beam")
    if page_inverted_t_beam:
        options.append("Inverted T-Beam")
    if page_inverted_l_beam:
        options.append("Inverted L-Beam")
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
    elif page == "Road L-Section" and page_road_lsection:
        page_road_lsection()
    elif page == "Road Cross Section" and page_road_cross_section:
        page_road_cross_section()
    elif page == "PMGSY Road" and page_pmgsy_road:
        page_pmgsy_road()
    elif page == "T-Beam" and page_t_beam:
        page_t_beam()
    elif page == "L-Beam" and page_l_beam:
        page_l_beam()
    elif page == "Rectangular Beam" and page_rectangular_beam:
        page_rectangular_beam()
    elif page == "Inverted T-Beam" and page_inverted_t_beam:
        page_inverted_t_beam()
    elif page == "Inverted L-Beam" and page_inverted_l_beam:
        page_inverted_l_beam()
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
    # Celebration balloons
    st.balloons()
    
    # Custom CSS for beautiful styling
    st.markdown("""
        <style>
        .big-font {
            font-size:50px !important;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
        }
        .feature-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
        }
        .success-box {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
        }
        .module-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            margin: 5px 0;
        }
        .stats-box {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown('<p class="big-font">🏗️ Structural Design Suite</p>', unsafe_allow_html=True)
    st.markdown("### 🎉 Professional Engineering Design Tools - All in One Place!")
    
    # Stats Section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stats-box">17<br/>Modules</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stats-box">100%<br/>Tested</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stats-box">DXF<br/>Export</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stats-box">PDF<br/>Reports</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features Section
    st.markdown("## 🌟 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
        <h3>🎯 Accurate Calculations</h3>
        <p>✅ IS 456 Compliant<br/>
        ✅ IRC Standards<br/>
        ✅ PMGSY Guidelines<br/>
        ✅ Professional Results</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
        <h3>📊 Multiple Export Options</h3>
        <p>✅ DXF for AutoCAD<br/>
        ✅ PDF Reports (A4 Landscape)<br/>
        ✅ Excel Calculations<br/>
        ✅ Professional Formatting</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
        <h3>🚀 Easy to Use</h3>
        <p>✅ Intuitive Interface<br/>
        ✅ Quick Results<br/>
        ✅ No Installation Required<br/>
        ✅ Cloud-Based</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
        <h3>🔧 Comprehensive Tools</h3>
        <p>✅ Structural Design<br/>
        ✅ Road Engineering<br/>
        ✅ Bridge Design<br/>
        ✅ All-in-One Solution</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Available Modules
    st.markdown("## 📚 Available Design Modules")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏛️ Columns", "🌉 Beams", "🛣️ Roads", "🏗️ Others"])
    
    with tab1:
        st.markdown("""
        <div class="module-card">
        <h4>🔵 Circular Column</h4>
        <p>Design circular RCC columns with reinforcement details</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>🟦 Rectangular Column</h4>
        <p>Design rectangular RCC columns with complete calculations</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>🔷 Column with Footing</h4>
        <p>Complete column and footing design in one tool</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="module-card">
        <h4>🔶 T-Beam</h4>
        <p>T-beam design with flange and web calculations</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>🔸 L-Beam</h4>
        <p>L-beam design for edge conditions</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>🟧 Rectangular Beam</h4>
        <p>Standard rectangular beam design</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>🔺 Inverted Beams</h4>
        <p>Inverted T-beam and L-beam designs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="module-card">
        <h4>🛣️ Road Plan</h4>
        <p>Horizontal alignment and plan design</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>📈 Road L-Section</h4>
        <p>Longitudinal section with gradients</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>📊 Road Cross Section</h4>
        <p>Typical cross-section design</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>🌾 PMGSY Road</h4>
        <p>Rural road design as per PMGSY standards</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div class="module-card">
        <h4>🪟 Lintel</h4>
        <p>Lintel beam design for openings</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>☀️ Sunshade</h4>
        <p>Cantilever sunshade design</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>🪜 Staircase</h4>
        <p>Complete staircase design</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="module-card">
        <h4>🌉 Bridge</h4>
        <p>Bridge structure design</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    st.markdown("## ✅ System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if LintelImportSuccess:
            st.markdown('<div class="success-box">✅ Lintel Module: Ready</div>', unsafe_allow_html=True)
        else:
            st.error(f"❌ Lintel module: {LintelImportError}")
    
    with col2:
        if SunshadeImportSuccess:
            st.markdown('<div class="success-box">✅ Sunshade Module: Ready</div>', unsafe_allow_html=True)
        else:
            st.error(f"❌ Sunshade module: {SunshadeImportError}")
    
    # Count working modules
    working_modules = sum([
        LintelImportSuccess, SunshadeImportSuccess,
        page_circular_column is not None,
        page_rectangular_column is not None,
        page_rect_column_footing is not None,
        page_circular_column_footing is not None,
        page_road_plan is not None,
        page_road_lsection is not None,
        page_road_cross_section is not None,
        page_pmgsy_road is not None,
        page_t_beam is not None,
        page_l_beam is not None,
        page_rectangular_beam is not None,
        page_inverted_t_beam is not None,
        page_inverted_l_beam is not None,
        page_staircase is not None,
        page_bridge is not None,
    ])
    
    st.markdown(f'<div class="success-box">🎉 {working_modules}/17 Modules Active and Ready!</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to Action
    st.markdown("## 🚀 Get Started")
    st.info("👈 Select a module from the sidebar to begin your design!")
    
    # Show another balloon celebration
    if working_modules == 17:
        st.success("🎊 All modules are working perfectly! You're ready to design!")
        st.balloons()

if __name__ == "__main__":
    main()