"""
Lintel Designer with AI Integration (Week 2)
Combines Week 1 features with AI code generation
"""

import streamlit as st
from components.monaco_editor import monaco_editor
from components.canvas_preview import canvas_preview
from components.ai_panel import ai_generator_panel, show_ai_examples
from utils.lisp_interpreter import LispInterpreter
from utils.lisp_templates import get_template, list_templates
from modules.lintel import page_lintel as original_lintel, generate_lintel_dxf
import numpy as np

def page_lintel_ai_enhanced():
    """Enhanced lintel designer with AI features"""
    
    st.set_page_config(
        page_title="Lintel Designer - AI Enhanced",
        page_icon="🏗️",
        layout="wide"
    )
    
    st.title("🏗️ Lintel Beam Designer - AI Enhanced")
    st.markdown("**Week 2**: Now with AI code generation! 🤖")
    
    # Tabs for different modes
    tab1, tab2, tab3 = st.tabs([
        "📝 Form Mode (Original)", 
        "💻 Code Mode (Week 1)", 
        "🤖 AI Mode (Week 2)"
    ])
    
    with tab1:
        st.info("📝 **Classic Mode**: Use the form below for guided design")
        original_lintel()
    
    with tab2:
        st.info("💻 **Code Mode**: Write Lisp code for parametric design")
        code_mode_interface()
    
    with tab3:
        st.info("🤖 **AI Mode**: Describe your design in plain English!")
        ai_mode_interface()


def code_mode_interface():
    """Code mode interface from Week 1"""
    
    # Get available templates
    templates = list_templates()
    
    col_sidebar, col_main = st.columns([1, 3])
    
    with col_sidebar:
        st.subheader("📐 Templates")
        
        selected_template = st.selectbox(
            "Choose Template",
            ["Custom"] + templates,
            help="Start with a template or write from scratch"
        )
        
        if selected_template != "Custom":
            if st.button("📋 Load Template"):
                template_code = get_template(selected_template)
                st.session_state['lintel_code'] = template_code
                st.success(f"✅ Loaded {selected_template} template")
        
        st.markdown("---")
        st.subheader("📚 Quick Reference")
        st.code("""
; Variables
(def name value)

; Drawing
(rect x y w h)
(circle x y r)
(line x1 y1 x2 y2)
(text x y "str" size)

; Colors
(fill #color)
(stroke #color)
(background #color)

; Math
(+ - * / sin cos)
        """, language="scheme")
    
    with col_main:
        # Default code
        if 'lintel_code' not in st.session_state:
            st.session_state['lintel_code'] = get_template("lintel_basic")
        
        col_editor, col_preview = st.columns([1, 1])
        
        with col_editor:
            st.subheader("📝 Code Editor")
            
            code = st.text_area(
                "Lisp Code",
                value=st.session_state.get('lintel_code', ''),
                height=500,
                key="code_editor",
                help="Write Lisp code here. Use Ctrl+Enter to run."
            )
            
            if code != st.session_state.get('lintel_code'):
                st.session_state['lintel_code'] = code
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("▶️ Run Code", use_container_width=True):
                    st.session_state['run_trigger'] = True
            with col2:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state['lintel_code'] = get_template("lintel_basic")
                    st.rerun()
            with col3:
                if st.button("💾 Save", use_container_width=True):
                    st.success("Code saved!")
        
        with col_preview:
            st.subheader("👁️ Live Preview")
            
            try:
                interpreter = LispInterpreter()
                commands = interpreter.execute(st.session_state.get('lintel_code', ''))
                
                # Display canvas
                canvas_preview(commands, width=600, height=400, key="lintel_canvas")
                
                # Show variables
                with st.expander("🔍 Variables", expanded=False):
                    if interpreter.variables:
                        for var, value in interpreter.variables.items():
                            st.text(f"{var} = {value}")
                    else:
                        st.text("No variables defined")
                
                # Show stats
                st.caption(f"📊 {len(commands)} drawing commands | {len(interpreter.variables)} variables")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.code(st.session_state.get('lintel_code', ''), language="scheme")


def ai_mode_interface():
    """AI-powered design interface (Week 2)"""
    
    col_left, col_right = st.columns([2, 3])
    
    with col_left:
        st.subheader("🤖 AI Design Assistant")
        
        # Show examples
        show_ai_examples('lintel')
        
        st.markdown("---")
        
        # AI Generator Panel
        current_code = st.session_state.get('ai_generated_code', None)
        generated_code = ai_generator_panel('lintel', current_code)
        
        if generated_code:
            st.session_state['ai_generated_code'] = generated_code
            st.success("✅ Code updated! Check the preview →")
            st.rerun()
    
    with col_right:
        st.subheader("👁️ Design Preview")
        
        if 'ai_generated_code' in st.session_state:
            code = st.session_state['ai_generated_code']
            
            # Show code
            with st.expander("📝 Generated Code", expanded=False):
                st.code(code, language="scheme")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Edit Code"):
                        st.session_state['lintel_code'] = code
                        st.info("💡 Switch to Code Mode tab to edit")
                with col2:
                    if st.button("📥 Generate DXF"):
                        st.info("💡 Extract parameters and generate DXF")
            
            # Render preview
            try:
                interpreter = LispInterpreter()
                commands = interpreter.execute(code)
                
                canvas_preview(commands, width=700, height=500, key="ai_canvas")
                
                # Show design info
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Drawing Commands", len(commands))
                with col2:
                    st.metric("Variables", len(interpreter.variables))
                with col3:
                    st.metric("Code Lines", len(code.split('\n')))
                
                # Show extracted parameters
                if interpreter.variables:
                    with st.expander("📊 Design Parameters", expanded=True):
                        for var, value in interpreter.variables.items():
                            if isinstance(value, (int, float)):
                                st.text(f"• {var}: {value}")
                
            except Exception as e:
                st.error(f"❌ Error rendering design: {str(e)}")
                st.code(code, language="scheme")
        
        else:
            st.info("👈 Use the AI generator to create your design!")
            
            # Show placeholder
            st.image("https://via.placeholder.com/700x500/f0f0f0/666666?text=Your+Design+Will+Appear+Here", 
                    use_column_width=True)


# Run the app
if __name__ == "__main__":
    page_lintel_ai_enhanced()
