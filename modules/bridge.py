"""
Bridge General Arrangement Drawing (GAD) Module
Smart integration with existing Tested_Bridge_GAD functionality and PNG reference images.
"""

import streamlit as st
import pandas as pd
import ezdxf
from io import BytesIO
import tempfile
import os
import sys
import base64
from pathlib import Path

# Add the Tested_Bridge_GAD directory to Python path to import existing functionality
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Tested_Bridge_GAD'))

def create_bridge_reference_images():
    """Create PNG reference images for bridge components using matplotlib."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import numpy as np
        
        # Bridge Elevation Reference Image
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 30)
        
        # Draw bridge elevation schematic
        # Abutments
        rect1 = patches.Rectangle((5, 5), 8, 15, linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.7)
        rect2 = patches.Rectangle((87, 5), 8, 15, linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.7)
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        
        # Piers
        for i, x in enumerate([25, 45, 65]):
            pier = patches.Rectangle((x-1, 5), 2, 12, linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.7)
            ax.add_patch(pier)
            
        # Deck slab
        deck = patches.Rectangle((5, 17), 90, 3, linewidth=2, edgecolor='red', facecolor='lightcoral', alpha=0.7)
        ax.add_patch(deck)
        
        # Labels
        ax.text(9, 25, 'Abutment', ha='center', fontsize=10, weight='bold')
        ax.text(26, 25, 'Pier', ha='center', fontsize=10, weight='bold')
        ax.text(50, 25, 'Deck Slab', ha='center', fontsize=10, weight='bold')
        ax.text(91, 25, 'Abutment', ha='center', fontsize=10, weight='bold')
        
        # Dimensions
        ax.annotate('', xy=(5, 2), xytext=(95, 2), arrowprops=dict(arrowstyle='<->', color='black'))
        ax.text(50, 0.5, 'Bridge Length', ha='center', fontsize=12, weight='bold')
        
        ax.set_title('Bridge General Arrangement - Elevation View', fontsize=14, weight='bold')
        ax.set_xlabel('Chainage (m)')
        ax.set_ylabel('Elevation (m)')
        ax.grid(True, alpha=0.3)
        
        # Save as bytes for embedding
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        elevation_img = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        # Bridge Plan Reference Image
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 20)
        
        # Draw bridge plan schematic
        # Deck outline
        deck_plan = patches.Rectangle((5, 8), 90, 4, linewidth=3, edgecolor='red', facecolor='lightcoral', alpha=0.5)
        ax.add_patch(deck_plan)
        
        # Pier footings in plan
        for i, x in enumerate([25, 45, 65]):
            footing = patches.Rectangle((x-3, 6), 6, 8, linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.7)
            ax.add_patch(footing)
            
        # Abutment footings
        abt1 = patches.Rectangle((2, 6), 10, 8, linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.7)
        abt2 = patches.Rectangle((88, 6), 10, 8, linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.7)
        ax.add_patch(abt1)
        ax.add_patch(abt2)
        
        # Center line
        ax.plot([0, 100], [10, 10], 'k--', linewidth=2, alpha=0.7, label='Center Line')
        
        ax.set_title('Bridge General Arrangement - Plan View', fontsize=14, weight='bold')
        ax.set_xlabel('Chainage (m)')
        ax.set_ylabel('Offset (m)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Save as bytes
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plan_img = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        return elevation_img, plan_img
        
    except ImportError:
        # If matplotlib is not available, return None
        return None, None

def get_default_bridge_variables():
    """Get default bridge variables from the existing HTML editor."""
    return {
        'SCALE1': 186,
        'SCALE2': 100,
        'SKEW': 0.0,
        'DATUM': 100.0,
        'TOPRL': 110.98,
        'LEFT': 0.0,
        'RIGHT': 43.2,
        'XINCR': 10.0,
        'YINCR': 1.0,
        'NOCH': 21,
        'NSPAN': 4,
        'LBRIDGE': 43.2,
        'ABTL': 0.0,
        'RTL': 110.98,
        'SOFL': 110.0,
        'KERBW': 0.23,
        'KERBD': 0.23,
        'CCBR': 11.1,
        'SLBTHC': 0.9,
        'SLBTHE': 0.75,
        'SLBTHT': 0.75,
        'CAPT': 110.0,
        'CAPB': 109.4,
        'CAPW': 1.2,
        'PIERTW': 1.2,
        'BATTR': 10.0,
        'PIERST': 12.0,
        'PIERN': 1.0,
        'SPAN1': 10.8,
        'FUTRL': 100.0,
        'FUTD': 1.0,
        'FUTW': 4.5,
        'FUTL': 12.0,
        'ABTLEN': 12.0,
        'LASLAB': 3.5,
        'APWTH': 12.0,
        'APTHK': 0.38,
        'WCTH': 0.08,
        # Abutment parameters
        'DWTH': 0.3,
        'ALCW': 0.75,
        'ALFL': 100.0,
        'ARFL': 100.75,
        'ALCD': 1.2,
        'ALFB': 10.0,
        'ALFBL': 101.0,
        'ALFBR': 100.75,
        'ALTB': 10.0,
        'ALTBL': 101.0,
        'ALTBR': 100.75,
        'ALFO': 1.5,
        'ALFD': 1.0,
        'ALBB': 3.0,
        'ALBBL': 101.0,
        'ALBBR': 100.75
    }

def generate_bridge_dxf_smart(variables):
    """
    Generate bridge DXF using the existing bridge_gad_app.py functionality.
    This smartly reuses the existing comprehensive bridge drawing code.
    """
    try:
        # Import the existing bridge GAD functionality
        from bridge_gad_app import generate_bridge_design
        
        # Create a DataFrame in the expected format
        data = []
        for var, value in variables.items():
            description = get_variable_description(var)
            data.append([value, var, description])
        
        df = pd.DataFrame(data, columns=['Value', 'Variable', 'Description'])
        
        # Generate the bridge design using existing functionality
        doc = generate_bridge_design(df)
        
        # Convert to bytes
        with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as temp_file:
            doc.saveas(temp_file.name)
            with open(temp_file.name, 'rb') as f:
                dxf_bytes = f.read()
        
        return dxf_bytes
        
    except ImportError:
        # Fallback: create a simple bridge DXF if the existing functionality isn't available
        return generate_simple_bridge_dxf(variables)

def generate_simple_bridge_dxf(variables):
    """Generate a simplified bridge DXF as fallback."""
    doc = ezdxf.new('R2010', setup=True)
    msp = doc.modelspace()
    
    # Extract key variables
    bridge_length = variables.get('LBRIDGE', 43.2)
    num_spans = int(variables.get('NSPAN', 4))
    span_length = variables.get('SPAN1', 10.8)
    deck_level = variables.get('RTL', 110.98)
    soffit_level = variables.get('SOFL', 110.0)
    datum = variables.get('DATUM', 100.0)
    
    # Simple bridge elevation drawing
    scale = 1000  # 1:1000 scale
    
    # Draw deck slab
    deck_start = (0, (deck_level - datum) * scale)
    deck_end = (bridge_length * scale, (deck_level - datum) * scale)
    msp.add_line(deck_start, deck_end, dxfattribs={'color': 1})
    
    # Draw soffit line
    soffit_start = (0, (soffit_level - datum) * scale)
    soffit_end = (bridge_length * scale, (soffit_level - datum) * scale)
    msp.add_line(soffit_start, soffit_end, dxfattribs={'color': 2})
    
    # Draw piers
    for i in range(1, num_spans):
        pier_x = i * span_length * scale
        pier_top = (pier_x, (soffit_level - datum) * scale)
        pier_bottom = (pier_x, 0)
        msp.add_line(pier_top, pier_bottom, dxfattribs={'color': 3})
    
    # Add title
    title_pos = (bridge_length * scale / 2, (deck_level - datum + 5) * scale)
    msp.add_text("BRIDGE GENERAL ARRANGEMENT DRAWING", dxfattribs={
        'height': 2 * scale,
        'insert': title_pos,
        'halign': 1
    })
    
    # Convert to bytes
    with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as temp_file:
        doc.saveas(temp_file.name)
        with open(temp_file.name, 'rb') as f:
            dxf_bytes = f.read()
    
    return dxf_bytes

def get_variable_description(var):
    """Get description for bridge variables."""
    descriptions = {
        'SCALE1': 'Scale1',
        'SCALE2': 'Scale2',
        'SKEW': 'Degree Of Skew In Plan Of The Bridge',
        'DATUM': 'Datum',
        'TOPRL': 'Top RL Of The Bridge',
        'LEFT': 'Left Most Chainage Of The Bridge',
        'RIGHT': 'Right Most Chainage Of The Bridge',
        'XINCR': 'Chainage Increment In X Direction',
        'YINCR': 'Elevation Increment In Y Direction',
        'NOCH': 'Total No. Of Chainages On C/S',
        'NSPAN': 'Number of Spans',
        'LBRIDGE': 'Length Of Bridge',
        'ABTL': 'Chainage Of Left Abutment',
        'RTL': 'Road Top Level',
        'SOFL': 'Soffit Level',
        'KERBW': 'Width Of Kerb At Deck Top',
        'KERBD': 'Depth Of Kerb Above Deck Top',
        'CCBR': 'Clear Carriageway Width Of Bridge',
        'SLBTHC': 'Thickness Of Slab At Centre',
        'SLBTHE': 'Thickness Of Slab At Edge',
        'SLBTHT': 'Thickness Of Slab At Tip',
        'CAPT': 'Pier Cap Top RL',
        'CAPB': 'Pier Cap Bottom RL',
        'CAPW': 'Cap Width',
        'PIERTW': 'Pier Top Width',
        'BATTR': 'Pier Batter',
        'PIERST': 'Straight Length Of Pier',
        'PIERN': 'Sr No Of Pier',
        'SPAN1': 'Span Individual Length',
        'FUTRL': 'Founding RL Of Pier Found',
        'FUTD': 'Depth Of Footing',
        'FUTW': 'Width Of Rect Footing',
        'FUTL': 'Length Of Footing Along Current Direction',
        'ABTLEN': 'Length Of Abutment Along Current Direction',
        'LASLAB': 'Length of approach slab',
        'APWTH': 'Width of approach slab',
        'APTHK': 'Thickness of approach slab',
        'WCTH': 'Thickness of wearing course'
    }
    return descriptions.get(var, f"Parameter {var}")

def page_bridge():
    """Streamlit page for Bridge GAD design."""
    st.title("🌉 Bridge General Arrangement Drawing")
    st.markdown("Create comprehensive bridge GAD drawings using the proven bridge design system.")
    
    # Create reference images
    elevation_img, plan_img = create_bridge_reference_images()
    
    # Show reference images if available
    if elevation_img and plan_img:
        st.header("📊 Bridge Reference Images")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Elevation View")
            st.markdown(f'<img src="data:image/png;base64,{elevation_img}" style="width:100%">', unsafe_allow_html=True)
        
        with col2:
            st.subheader("Plan View")  
            st.markdown(f'<img src="data:image/png;base64,{plan_img}" style="width:100%">', unsafe_allow_html=True)
    
    # Load existing bridge editor HTML for reference
    html_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Tested_Bridge_GAD', 'bridge_editor.html')
    if os.path.exists(html_file_path):
        st.info("💡 **Tip**: Use the existing Bridge Editor HTML file for comprehensive parameter editing.")
        with st.expander("🔧 Open Bridge Parameter Editor", expanded=False):
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=600, scrolling=True)
    
    # Bridge parameter input form
    with st.form("bridge_form"):
        st.header("🏗️ Bridge Parameters")
        
        # Get default variables
        default_vars = get_default_bridge_variables()
        variables = {}
        
        # Organize parameters into tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📐 General", "🏗️ Structure", "🌁 Spans & Piers", "🛣️ Details"])
        
        with tab1:
            st.subheader("General Parameters")
            col1, col2 = st.columns(2)
            
            with col1:
                variables['LBRIDGE'] = st.number_input("Bridge Length (m)", value=default_vars['LBRIDGE'], min_value=10.0, max_value=1000.0, step=0.1)
                variables['NSPAN'] = st.number_input("Number of Spans", value=int(default_vars['NSPAN']), min_value=1, max_value=20, step=1)
                variables['SPAN1'] = st.number_input("Span Length (m)", value=default_vars['SPAN1'], min_value=5.0, max_value=50.0, step=0.1)
                variables['SKEW'] = st.number_input("Skew Angle (degrees)", value=default_vars['SKEW'], min_value=0.0, max_value=45.0, step=1.0)
            
            with col2:
                variables['DATUM'] = st.number_input("Datum Level (m)", value=default_vars['DATUM'], min_value=0.0, max_value=200.0, step=0.1)
                variables['RTL'] = st.number_input("Road Top Level (m)", value=default_vars['RTL'], min_value=100.0, max_value=200.0, step=0.01)
                variables['SOFL'] = st.number_input("Soffit Level (m)", value=default_vars['SOFL'], min_value=100.0, max_value=200.0, step=0.01)
                variables['CCBR'] = st.number_input("Carriageway Width (m)", value=default_vars['CCBR'], min_value=3.0, max_value=20.0, step=0.1)
        
        with tab2:
            st.subheader("Structural Elements")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Deck Slab**")
                variables['SLBTHC'] = st.number_input("Slab Thickness - Centre (m)", value=default_vars['SLBTHC'], min_value=0.2, max_value=2.0, step=0.05)
                variables['SLBTHE'] = st.number_input("Slab Thickness - Edge (m)", value=default_vars['SLBTHE'], min_value=0.2, max_value=2.0, step=0.05)
                variables['SLBTHT'] = st.number_input("Slab Thickness - Tip (m)", value=default_vars['SLBTHT'], min_value=0.2, max_value=2.0, step=0.05)
                variables['WCTH'] = st.number_input("Wearing Course (m)", value=default_vars['WCTH'], min_value=0.05, max_value=0.2, step=0.01)
            
            with col2:
                st.write("**Kerb & Details**")
                variables['KERBW'] = st.number_input("Kerb Width (m)", value=default_vars['KERBW'], min_value=0.15, max_value=0.5, step=0.01)
                variables['KERBD'] = st.number_input("Kerb Depth (m)", value=default_vars['KERBD'], min_value=0.15, max_value=0.5, step=0.01)
                variables['LASLAB'] = st.number_input("Approach Slab Length (m)", value=default_vars['LASLAB'], min_value=2.0, max_value=10.0, step=0.1)
                variables['APTHK'] = st.number_input("Approach Slab Thickness (m)", value=default_vars['APTHK'], min_value=0.2, max_value=0.6, step=0.01)
        
        with tab3:
            st.subheader("Piers and Caps")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Pier Dimensions**")
                variables['PIERTW'] = st.number_input("Pier Top Width (m)", value=default_vars['PIERTW'], min_value=0.5, max_value=3.0, step=0.1)
                variables['PIERST'] = st.number_input("Pier Straight Length (m)", value=default_vars['PIERST'], min_value=8.0, max_value=20.0, step=0.5)
                variables['BATTR'] = st.number_input("Pier Batter Ratio", value=default_vars['BATTR'], min_value=5.0, max_value=20.0, step=0.5)
            
            with col2:
                st.write("**Pier Caps**")
                variables['CAPT'] = st.number_input("Cap Top Level (m)", value=default_vars['CAPT'], min_value=100.0, max_value=200.0, step=0.01)
                variables['CAPB'] = st.number_input("Cap Bottom Level (m)", value=default_vars['CAPB'], min_value=100.0, max_value=200.0, step=0.01)
                variables['CAPW'] = st.number_input("Cap Width (m)", value=default_vars['CAPW'], min_value=0.8, max_value=2.5, step=0.1)
        
        with tab4:
            st.subheader("Foundation Details")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Footings**")
                variables['FUTRL'] = st.number_input("Founding Level (m)", value=default_vars['FUTRL'], min_value=80.0, max_value=150.0, step=0.1)
                variables['FUTD'] = st.number_input("Footing Depth (m)", value=default_vars['FUTD'], min_value=0.5, max_value=3.0, step=0.1)
                variables['FUTW'] = st.number_input("Footing Width (m)", value=default_vars['FUTW'], min_value=2.0, max_value=8.0, step=0.1)
                variables['FUTL'] = st.number_input("Footing Length (m)", value=default_vars['FUTL'], min_value=8.0, max_value=20.0, step=0.1)
            
            with col2:
                st.write("**Drawing Scales**")
                variables['SCALE1'] = st.number_input("Scale 1", value=default_vars['SCALE1'], min_value=50, max_value=500, step=10)
                variables['SCALE2'] = st.number_input("Scale 2", value=default_vars['SCALE2'], min_value=50, max_value=500, step=10)
                variables['XINCR'] = st.number_input("X Increment (m)", value=default_vars['XINCR'], min_value=1.0, max_value=20.0, step=1.0)
                variables['YINCR'] = st.number_input("Y Increment (m)", value=default_vars['YINCR'], min_value=0.5, max_value=5.0, step=0.5)
        
        # Add remaining calculated parameters
        variables['LEFT'] = 0.0
        variables['RIGHT'] = variables['LBRIDGE']
        variables['ABTL'] = 0.0
        variables['NOCH'] = int((variables['RIGHT'] - variables['LEFT']) / variables['XINCR']) + 1
        variables['TOPRL'] = variables['RTL']
        variables['APWTH'] = variables['CCBR'] + 2 * variables['KERBW']
        variables['ABTLEN'] = variables['APWTH']
        
        # Add default abutment parameters (simplified)
        abutment_defaults = {
            'DWTH': 0.3, 'ALCW': 0.75, 'ALFL': variables['FUTRL'], 'ARFL': variables['FUTRL'],
            'ALCD': 1.2, 'ALFB': 10.0, 'ALFBL': variables['FUTRL'] + 1.0, 'ALFBR': variables['FUTRL'] + 1.0,
            'ALTB': 10.0, 'ALTBL': variables['FUTRL'] + 1.0, 'ALTBR': variables['FUTRL'] + 1.0,
            'ALFO': 1.5, 'ALFD': 1.0, 'ALBB': 3.0, 'ALBBL': variables['FUTRL'] + 1.0, 'ALBBR': variables['FUTRL'] + 1.0,
            'PIERN': 1.0
        }
        variables.update(abutment_defaults)
        
        submitted = st.form_submit_button("🖨️ Generate Bridge GAD Drawing")
    
    if submitted:
        # Validate key parameters
        if variables['NSPAN'] <= 0 or variables['SPAN1'] <= 0:
            st.error("Please enter valid span parameters.")
            return
        
        if variables['RTL'] <= variables['SOFL']:
            st.error("Road top level must be higher than soffit level.")
            return
        
        with st.spinner("🔄 Generating comprehensive bridge GAD drawing..."):
            try:
                # Generate the DXF
                dxf_bytes = generate_bridge_dxf_smart(variables)
                
                st.success("✅ Bridge GAD drawing generated successfully!")
                
                # Display preview and download
                col_preview, col_download = st.columns([2, 1])
                
                with col_preview:
                    st.subheader("🏗️ Bridge Summary")
                    
                    total_length = variables['LBRIDGE']
                    num_spans = int(variables['NSPAN'])
                    pier_count = num_spans - 1
                    
                    st.write(f"**Total Length**: {total_length:.1f}m")
                    st.write(f"**Number of Spans**: {num_spans}")
                    st.write(f"**Span Length**: {variables['SPAN1']:.1f}m")
                    st.write(f"**Number of Piers**: {pier_count}")
                    st.write(f"**Carriageway Width**: {variables['CCBR']:.1f}m")
                    st.write(f"**Deck Level**: {variables['RTL']:.2f}m")
                    st.write(f"**Skew Angle**: {variables['SKEW']:.0f}°")
                    
                    if variables['SKEW'] > 0:
                        st.info(f"🔄 Bridge has {variables['SKEW']:.0f}° skew angle")
                
                with col_download:
                    st.subheader("📥 Download")
                    filename = f"bridge_GAD_{int(total_length)}m_{num_spans}span.dxf"
                    st.download_button(
                        label="⬇️ Download Bridge DXF",
                        data=dxf_bytes,
                        file_name=filename,
                        mime="application/dxf",
                        help="Download the comprehensive bridge GAD DXF file"
                    )
                
                # Show detailed parameters
                with st.expander("📋 Complete Parameter List", expanded=False):
                    st.subheader("Bridge Design Variables")
                    
                    # Create a DataFrame for better display
                    param_data = []
                    for var, value in variables.items():
                        if isinstance(value, (int, float)):
                            param_data.append({
                                'Variable': var,
                                'Value': f"{value:.3f}" if isinstance(value, float) else str(value),
                                'Description': get_variable_description(var)
                            })
                    
                    df_params = pd.DataFrame(param_data)
                    st.dataframe(df_params, use_container_width=True)
                
                # Reference to existing tools
                st.info("""
                **💡 Advanced Features Available:**
                - Use `bridge_gad_app.py` directly for complete functionality
                - Edit `input.xlsx` for detailed parameter control  
                - Use `bridge_editor.html` for interactive parameter editing
                - Generate tender reports with the full GAD system
                """)
            
            except Exception as e:
                st.error(f"❌ Error generating bridge drawing: {str(e)}")
                st.error("Falling back to simplified bridge drawing.")
                
                # Try simplified version
                try:
                    dxf_bytes = generate_simple_bridge_dxf(variables)
                    filename = f"bridge_simple_{int(variables['LBRIDGE'])}m.dxf"
                    st.download_button(
                        label="⬇️ Download Simplified Bridge DXF",
                        data=dxf_bytes,
                        file_name=filename,
                        mime="application/dxf"
                    )
                except Exception as e2:
                    st.error(f"❌ Error with simplified drawing: {str(e2)}")
    
    else:
        st.info("ℹ️ Configure bridge parameters and click 'Generate Bridge GAD Drawing'.")
        
        # Show existing tools
        st.markdown("---")
        st.subheader("🔧 Existing Bridge Tools")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🖥️ Direct Tools:**")
            st.code("python ./Tested_Bridge_GAD/bridge_gad_app.py", language="bash")
            st.markdown("*Run the full bridge GAD generator*")
        
        with col2:
            st.markdown("**📝 Parameter Files:**")
            st.markdown("- `input.xlsx` - Main parameter file")
            st.markdown("- `bridge_editor.html` - Interactive editor")
            st.markdown("- `test_input.xlsx` - Test parameters")
