"""
Enhanced Lintel Module with Live Code Editor
Week 1 Implementation
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.monaco_editor import monaco_editor, code_editor_simple
from components.canvas_preview import canvas_preview, canvas_preview_simple
from utils.lisp_interpreter import LispInterpreter


def page_lintel_enhanced():
    """Enhanced Lintel Designer with Code Mode"""
    
    st.title("🏗️ Lintel Beam Designer - Enhanced")
    st.markdown("Design lintel beams using forms or code")
    
    # Mode selection
    mode = st.radio(
        "Design Mode",
        ["📝 Form Mode (Traditional)", "💻 Code Mode (New!)"],
        horizontal=True,
        help="Choose between form-based design or code-based parametric design"
    )
    
    if mode == "📝 Form Mode (Traditional)":
        show_form_mode()
    else:
        show_code_mode()


def show_form_mode():
    """Traditional form-based design"""
    st.info("👉 Use the form below for guided lintel design")
    
    with st.sidebar:
        st.header("Lintel Parameters")
        
        # Basic Dimensions
        st.subheader("Dimensions")
        span = st.number_input("Clear Span (mm)", min_value=500.0, value=1200.0, step=50.0)
        width = st.number_input("Width (mm)", min_value=100.0, value=200.0, step=10.0)
        depth = st.number_input("Depth (mm)", min_value=150.0, value=250.0, step=10.0)
        bearing = st.number_input("Bearing Length (mm)", min_value=100.0, value=150.0, step=10.0)
        
        # Reinforcement
        st.subheader("Reinforcement")
        num_bars = st.number_input("Number of Main Bars", min_value=2, value=3, step=1)
        bar_dia = st.number_input("Bar Diameter (mm)", min_value=8.0, value=12.0, step=2.0)
    
    # Display design
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Design Summary")
        st.write(f"**Span:** {span} mm")
        st.write(f"**Size:** {width} x {depth} mm")
        st.write(f"**Total Length:** {span + 2*bearing} mm")
        st.write(f"**Reinforcement:** {num_bars}-ø{bar_dia}mm")
    
    with col2:
        st.subheader("Preview")
        # Generate Lisp code from form values
        code = generate_lintel_code(span, width, depth, bearing, num_bars, bar_dia)
        
        # Execute and preview
        interpreter = LispInterpreter()
        commands = interpreter.execute(code)
        canvas_preview(commands, width=400, height=300)
    
    # Show generated code
    with st.expander("📄 View Generated Code"):
        st.code(code, language="scheme")
        if st.button("Switch to Code Mode to Edit"):
            st.session_state.lintel_code = code
            st.rerun()


def show_code_mode():
    """Code-based parametric design"""
    st.info("💡 Write Lisp code for parametric design. Changes update in real-time!")
    
    # Default template
    default_code = """
; Lintel Beam Design
; All dimensions in mm

; === PARAMETERS ===
(def span 1200)
(def width 200)
(def depth 250)
(def bearing 150)
(def num-bars 3)
(def bar-dia 12)

; === CALCULATIONS ===
(def total-length (+ span (* 2 bearing)))
(def cover 40)
(def bar-spacing (/ (- span (* 2 cover)) (- num-bars 1)))

; === DRAWING ===

; Draw lintel beam (elevation)
(fill #cccccc)
(rect 0 100 total-length depth)

; Draw bearing areas
(fill #999999)
(rect 0 100 bearing depth)
(rect (- total-length bearing) 100 bearing depth)

; Draw reinforcement bars
(fill #ff6600)
(def bar-y (+ 100 (- depth cover)))
(def i 0)
(def draw-bar (+ cover (* i bar-spacing)))

; Bar 1
(circle (+ bearing cover) bar-y (/ bar-dia 2))
; Bar 2
(circle (+ bearing cover bar-spacing) bar-y (/ bar-dia 2))
; Bar 3
(circle (+ bearing cover (* 2 bar-spacing)) bar-y (/ bar-dia 2))

; === ANNOTATIONS ===
(fill #ffffff)
(text (/ total-length 2) 80 "LINTEL BEAM" 14)
(text (/ total-length 2) 370 (+ "SPAN = " span "mm") 12)
(text (/ total-length 2) 390 (+ num-bars "-ø" bar-dia "mm BARS") 12)

; Dimension lines
(stroke #ffff00)
(line bearing 90 (+ bearing span) 90)
(text (+ bearing (/ span 2)) 75 (+ span "mm") 10)
"""
    
    # Initialize session state
    if 'lintel_code' not in st.session_state:
        st.session_state.lintel_code = default_code
    
    # Layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💻 Code Editor")
        
        # Try Monaco Editor, fallback to simple editor
        try:
            code = monaco_editor(
                st.session_state.lintel_code,
                language="scheme",
                height=500,
                key="lintel_monaco"
            )
            
            if code and code != st.session_state.lintel_code:
                st.session_state.lintel_code = code
        
        except Exception as e:
            st.warning("Using simple editor (Monaco not available)")
            code = code_editor_simple(
                st.session_state.lintel_code,
                language="scheme",
                height=500,
                key="lintel_simple"
            )
            st.session_state.lintel_code = code
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("🔄 Reset to Template"):
                st.session_state.lintel_code = default_code
                st.rerun()
        with col_btn2:
            if st.button("📋 Copy Code"):
                st.code(st.session_state.lintel_code, language="scheme")
        with col_btn3:
            if st.button("💾 Save"):
                st.success("Code saved to session!")
    
    with col2:
        st.subheader("🎨 Live Preview")
        
        try:
            # Execute code
            interpreter = LispInterpreter()
            commands = interpreter.execute(st.session_state.lintel_code)
            
            # Show preview
            canvas_preview(commands, width=600, height=400, key="lintel_canvas")
            
            # Show variables
            with st.expander("📊 Variables"):
                variables = interpreter.get_variables()
                if variables:
                    for var, value in variables.items():
                        st.write(f"**{var}** = {value}")
                else:
                    st.info("No variables defined yet")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Check your code syntax")
    
    # Help section
    with st.expander("📚 Lisp Commands Reference"):
        st.markdown("""
        ### Variables
        ```lisp
        (def variable-name value)
        ```
        
        ### Math Operations
        ```lisp
        (+ a b c)      ; Addition
        (- a b)        ; Subtraction
        (* a b c)      ; Multiplication
        (/ a b)        ; Division
        ```
        
        ### Drawing Commands
        ```lisp
        (fill "#color")              ; Set fill color
        (stroke "#color")            ; Set stroke color
        (rect x y width height)      ; Draw rectangle
        (circle x y radius)          ; Draw circle
        (line x1 y1 x2 y2)          ; Draw line
        (text x y "string" size)     ; Draw text
        ```
        
        ### Colors
        - Use hex colors: `#ff0000` (red), `#00ff00` (green), `#0000ff` (blue)
        - Or named colors: `#fff` (white), `#000` (black)
        
        ### Tips
        - Use `;` for comments
        - All dimensions in mm
        - Coordinate system: (0,0) is top-left
        """)
    
    # Generate DXF button
    st.markdown("---")
    if st.button("📐 Generate DXF Drawing", type="primary"):
        st.info("DXF generation will be implemented in Week 2!")
        st.code("Coming soon: Convert your Lisp design to production DXF", language="text")


def generate_lintel_code(span, width, depth, bearing, num_bars, bar_dia):
    """Generate Lisp code from form parameters"""
    return f"""
; Lintel Beam Design (Generated from Form)
(def span {span})
(def width {width})
(def depth {depth})
(def bearing {bearing})
(def num-bars {num_bars})
(def bar-dia {bar_dia})

; Calculations
(def total-length (+ span (* 2 bearing)))
(def cover 40)

; Draw lintel
(fill #cccccc)
(rect 0 100 total-length depth)

; Draw bearing areas
(fill #999999)
(rect 0 100 bearing depth)
(rect (- total-length bearing) 100 bearing depth)

; Draw reinforcement
(fill #ff6600)
(def bar-y (+ 100 (- depth cover)))
(def bar-spacing (/ (- span (* 2 cover)) (- num-bars 1)))

; Draw bars
(circle (+ bearing cover) bar-y (/ bar-dia 2))
(circle (+ bearing cover bar-spacing) bar-y (/ bar-dia 2))
(circle (+ bearing cover (* 2 bar-spacing)) bar-y (/ bar-dia 2))

; Annotations
(fill #ffffff)
(text (/ total-length 2) 80 "LINTEL BEAM" 14)
(text (/ total-length 2) 370 (+ "SPAN = " span "mm") 12)
"""


# For testing
if __name__ == "__main__":
    page_lintel_enhanced()
