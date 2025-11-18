import streamlit as st
import os
import sys

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import only the lintel and sunshade modules (these are the ones the user wants)
try:
    from modules.lintel import page_lintel
    LintelImportSuccess = True
    page_lintel_func = page_lintel
except Exception as e:
    LintelImportSuccess = False
    LintelImportError = str(e)
    page_lintel_func = None

try:
    from modules.sunshade import page_sunshade
    SunshadeImportSuccess = True
    page_sunshade_func = page_sunshade
except Exception as e:
    SunshadeImportSuccess = False
    SunshadeImportError = str(e)
    page_sunshade_func = None

def main():
    # Set up the page
    st.set_page_config(
        page_title="Lintel & Sunshade Designer",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar navigation
    st.sidebar.title("🏗️ Lintel & Sunshade Designer")
    st.sidebar.markdown("---")
    
    # Group related modules
    st.sidebar.header("Navigation")
    
    # Build the navigation options
    options = ["Home"]
    if LintelImportSuccess:
        options.append("Lintel")
    if SunshadeImportSuccess:
        options.append("Sunshade")
    
    page = st.sidebar.radio("Select Module", options)

    # Handle page routing
    if page == "Home":
        show_home_page()
    elif page == "Lintel" and LintelImportSuccess and page_lintel_func:
        page_lintel_func()
    elif page == "Sunshade" and SunshadeImportSuccess and page_sunshade_func:
        page_sunshade_func()
    else:
        st.error(f"Module '{page}' is not available.")
        if page == "Lintel" and not LintelImportSuccess:
            st.error(f"Lintel module import error: {LintelImportError}")
        if page == "Sunshade" and not SunshadeImportSuccess:
            st.error(f"Sunshade module import error: {SunshadeImportError}")

def show_home_page():
    st.title("🏗️ Lintel & Sunshade Designer")
    st.markdown("""
    Welcome to the Lintel & Sunshade Designer! This application provides tools for designing lintel beams and sunshades.
    
    ### Available Modules:
    - **Lintel**: Design lintel beams for door and window openings
    - **Sunshade**: Design cantilever sunshades with supporting beams
    
    Select a module from the sidebar to get started.
    """)
    
    # Show status of the specific modules the user is interested in
    st.subheader("Module Status")
    if LintelImportSuccess:
        st.success("✅ Lintel module is ready for use")
    else:
        st.error(f"❌ Lintel module import failed: {LintelImportError}")
        
    if SunshadeImportSuccess:
        st.success("✅ Sunshade module is ready for use")
    else:
        st.error(f"❌ Sunshade module import failed: {SunshadeImportError}")

if __name__ == "__main__":
    main()