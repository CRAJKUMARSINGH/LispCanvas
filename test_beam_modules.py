import os
import sys
import streamlit as st
from io import BytesIO

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the modules to test
from modules.inverted_t_beam import generate_inverted_t_beam_dxf
from modules.inverted_l_beam import generate_inverted_l_beam_dxf

def test_inverted_t_beam():
    """Test the Inverted T-Beam module with sample parameters."""
    st.header("🔧 Inverted T-Beam Test")
    
    # Test parameters
    params = {
        'bf': 1500,      # Flange width (mm)
        'tf': 150,       # Flange thickness (mm)
        'bw': 300,       # Web width (mm)
        'D': 600,        # Overall depth (mm)
        'd': 550,        # Effective depth (mm)
        'main_bars_dia': 20,    # Main bars diameter (mm)
        'num_bars': 5,          # Number of tension bars
        'stirrup_dia': 10,      # Stirrup diameter (mm)
        'stirrup_spacing': 150  # Stirrup spacing (mm)
    }
    
    # Generate DXF
    try:
        dxf_bytes = generate_inverted_t_beam_dxf(**params)
        
        # Display success message
        st.success("✅ Inverted T-Beam DXF generated successfully!")
        
        # Create download button
        st.download_button(
            label="⬇️ Download Inverted T-Beam DXF",
            data=dxf_bytes,
            file_name=f"test_inverted_t_beam_{params['bf']}x{params['D']}.dxf",
            mime="application/dxf"
        )
        
        # Display parameters
        st.subheader("Test Parameters")
        st.json(params)
        
    except Exception as e:
        st.error(f"❌ Error generating Inverted T-Beam DXF: {str(e)}")

def test_inverted_l_beam():
    """Test the Inverted L-Beam module with sample parameters."""
    st.header("🔧 Inverted L-Beam Test")
    
    # Test parameters
    params = {
        'bf': 900,       # Flange width (mm)
        'tf': 150,       # Flange thickness (mm)
        'bw': 250,       # Web width (mm)
        'D': 550,        # Overall depth (mm)
        'd': 500,        # Effective depth (mm)
        'main_bars_dia': 16,    # Main bars diameter (mm)
        'num_bars': 4,          # Number of tension bars
        'stirrup_dia': 8,       # Stirrup diameter (mm)
        'stirrup_spacing': 150, # Stirrup spacing (mm)
        'flange_position': "Bottom Left"  # Flange position
    }
    
    # Generate DXF
    try:
        dxf_bytes = generate_inverted_l_beam_dxf(**params)
        
        # Display success message
        st.success("✅ Inverted L-Beam DXF generated successfully!")
        
        # Create download button
        st.download_button(
            label="⬇️ Download Inverted L-Beam DXF",
            data=dxf_bytes,
            file_name=f"test_inverted_l_beam_{params['bf']}x{params['D']}_{params['flange_position'].replace(' ', '_').lower()}.dxf",
            mime="application/dxf"
        )
        
        # Display parameters
        st.subheader("Test Parameters")
        st.json(params)
        
    except Exception as e:
        st.error(f"❌ Error generating Inverted L-Beam DXF: {str(e)}")

def main():
    """Main function to run the test script."""
    st.set_page_config(
        page_title="Beam Modules Test",
        page_icon="🧪",
        layout="wide"
    )
    
    st.title("🧪 Beam Modules Test")
    st.markdown("""
    This script tests the functionality of the Inverted T-Beam and Inverted L-Beam modules.
    It generates sample DXF files that you can download and inspect.
    """)
    
    # Create tabs for each test
    tab1, tab2 = st.tabs(["Inverted T-Beam", "Inverted L-Beam"])
    
    with tab1:
        test_inverted_t_beam()
    
    with tab2:
        test_inverted_l_beam()

if __name__ == "__main__":
    main()
