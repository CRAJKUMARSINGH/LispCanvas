"""
Lisp Code Templates for All Modules
Week 1 - Day 6 Implementation
"""

TEMPLATES = {
    "lintel": {
        "name": "Lintel Beam",
        "description": "Standard lintel beam with reinforcement",
        "code": """
; Lintel Beam Design
(def span 1200)
(def width 200)
(def depth 250)
(def bearing 150)
(def num-bars 3)
(def bar-dia 12)

; Calculations
(def total-length (+ span (* 2 bearing)))
(def cover 40)
(def bar-spacing (/ (- span (* 2 cover)) (- num-bars 1)))

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
(repeat num-bars (do
    (circle (+ bearing cover (* i bar-spacing)) bar-y (/ bar-dia 2))
))

; Annotations
(fill #ffffff)
(text (/ total-length 2) 80 "LINTEL BEAM" 14)
(text (/ total-length 2) 370 (+ "SPAN = " span "mm") 12)
"""
    },
    
    "sunshade": {
        "name": "Sunshade (Chajja)",
        "description": "Cantilever sunshade with supporting beam",
        "code": """
; Sunshade Design
(def projection 1000)
(def thickness-support 150)
(def thickness-edge 100)
(def beam-width 300)
(def beam-depth 450)

; Supporting beam
(fill #cccccc)
(rect 0 0 beam-width beam-depth)

; Sunshade slab (tapered)
(fill #dddddd)
(rect 0 beam-depth projection thickness-support)

; Taper line
(stroke #999999)
(line projection (+ beam-depth thickness-support) 
      projection (+ beam-depth thickness-edge))

; Reinforcement in beam
(fill #ff6600)
(def cover 40)
(circle (+ cover 20) (- beam-depth cover) 8)
(circle (+ cover 80) (- beam-depth cover) 8)
(circle (+ cover 140) (- beam-depth cover) 8)

; Annotations
(fill #ffffff)
(text (/ projection 2) (- beam-depth 20) "SUNSHADE" 14)
(text (/ projection 2) (+ beam-depth thickness-support 30) 
      (+ "PROJECTION = " projection "mm") 12)
"""
    },
    
    "bridge": {
        "name": "Bridge Elevation",
        "description": "Simple bridge elevation with piers and deck",
        "code": """
; Bridge Elevation
(def span 10000)
(def num-piers 3)
(def pier-height 8000)
(def pier-width 1200)
(def deck-depth 900)

; Ground level
(stroke #8b4513)
(line 0 (+ pier-height deck-depth) 
      (+ span (* num-piers pier-width)) 
      (+ pier-height deck-depth))

; Draw piers
(fill #999999)
(def pier-spacing (/ span (+ num-piers 1)))
(repeat num-piers (do
    (def pier-x (+ (* (+ i 1) pier-spacing) (* i pier-width)))
    (rect pier-x deck-depth pier-width pier-height)
))

; Draw deck
(fill #666666)
(rect 0 0 (+ span (* num-piers pier-width)) deck-depth)

; Annotations
(fill #ffffff)
(text (/ span 2) (- 0 50) "BRIDGE ELEVATION" 16)
(text (/ span 2) (+ pier-height deck-depth 100) 
      (+ "SPAN = " span "mm") 12)
"""
    },
    
    "column": {
        "name": "Rectangular Column",
        "description": "Column with reinforcement details",
        "code": """
; Rectangular Column
(def width 300)
(def depth 400)
(def height 3000)
(def num-bars-width 3)
(def num-bars-depth 4)
(def bar-dia 16)

; Draw column (elevation)
(fill #dddddd)
(rect 100 100 width height)

; Draw reinforcement
(fill #ff6600)
(def cover 40)
(def spacing-w (/ (- width (* 2 cover)) (- num-bars-width 1)))
(def spacing-d (/ (- depth (* 2 cover)) (- num-bars-depth 1)))

; Bars along width
(repeat num-bars-width (do
    (circle (+ 100 cover (* i spacing-w)) (+ 100 cover) (/ bar-dia 2))
    (circle (+ 100 cover (* i spacing-w)) (+ 100 height (- cover)) (/ bar-dia 2))
))

; Stirrups
(stroke #ff6600)
(def stirrup-spacing 150)
(repeat (/ height stirrup-spacing) (do
    (rect (+ 100 cover) (+ 100 (* i stirrup-spacing)) 
          (- width (* 2 cover)) (- depth (* 2 cover)))
))

; Annotations
(fill #ffffff)
(text (+ 100 (/ width 2)) 80 "COLUMN" 14)
(text (+ 100 (/ width 2)) (+ 100 height 30) 
      (+ width "x" depth "mm") 12)
"""
    },
    
    "staircase": {
        "name": "Staircase",
        "description": "Staircase with steps",
        "code": """
; Staircase Design
(def num-steps 10)
(def tread 250)
(def riser 150)
(def width 1200)

; Draw steps
(fill #cccccc)
(repeat num-steps (do
    (def step-x (* i tread))
    (def step-y (* i riser))
    (rect step-x (- 500 step-y) tread riser)
))

; Draw stringer
(stroke #666666)
(line 0 500 (* num-steps tread) (- 500 (* num-steps riser)))

; Annotations
(fill #ffffff)
(text (/ (* num-steps tread) 2) 550 "STAIRCASE" 14)
(text (/ (* num-steps tread) 2) 570 
      (+ num-steps " STEPS | TREAD=" tread " | RISER=" riser) 10)
"""
    },
    
    "footing": {
        "name": "Isolated Footing",
        "description": "Column footing with pedestal",
        "code": """
; Isolated Footing
(def footing-width 2000)
(def footing-depth 2000)
(def footing-height 400)
(def pedestal-width 600)
(def pedestal-height 300)
(def column-width 300)
(def column-height 500)

; Draw footing
(fill #bbb)
(rect 100 400 footing-width footing-height)

; Draw pedestal
(fill #999)
(rect (+ 100 (/ (- footing-width pedestal-width) 2)) 
      (- 400 pedestal-height) 
      pedestal-width pedestal-height)

; Draw column
(fill #ddd)
(rect (+ 100 (/ (- footing-width column-width) 2)) 
      (- 400 pedestal-height column-height) 
      column-width column-height)

; Reinforcement
(fill #ff6600)
(def bar-spacing 200)
(repeat (/ footing-width bar-spacing) (do
    (circle (+ 100 (* i bar-spacing)) 600 6)
))

; Annotations
(fill #ffffff)
(text (+ 100 (/ footing-width 2)) 850 "ISOLATED FOOTING" 14)
(text (+ 100 (/ footing-width 2)) 870 
      (+ footing-width "x" footing-depth "x" footing-height "mm") 10)
"""
    },
    
    "beam": {
        "name": "T-Beam",
        "description": "T-beam with reinforcement",
        "code": """
; T-Beam Design
(def flange-width 1200)
(def flange-depth 150)
(def web-width 300)
(def web-depth 450)
(def length 5000)

; Draw T-beam (cross-section)
; Flange
(fill #cccccc)
(rect 100 100 flange-width flange-depth)

; Web
(rect (+ 100 (/ (- flange-width web-width) 2)) 
      (+ 100 flange-depth) 
      web-width web-depth)

; Reinforcement
(fill #ff6600)
(def cover 40)

; Bottom bars
(circle (+ 100 (/ flange-width 2) -60) 
        (+ 100 flange-depth web-depth (- cover)) 10)
(circle (+ 100 (/ flange-width 2)) 
        (+ 100 flange-depth web-depth (- cover)) 10)
(circle (+ 100 (/ flange-width 2) 60) 
        (+ 100 flange-depth web-depth (- cover)) 10)

; Top bars
(circle (+ 100 (/ flange-width 2) -40) (+ 100 cover) 8)
(circle (+ 100 (/ flange-width 2) 40) (+ 100 cover) 8)

; Stirrups
(stroke #ff6600)
(rect (+ 100 (/ (- flange-width web-width) 2) cover) 
      (+ 100 flange-depth cover)
      (- web-width (* 2 cover)) 
      (- web-depth (* 2 cover)))

; Annotations
(fill #ffffff)
(text (+ 100 (/ flange-width 2)) 80 "T-BEAM SECTION" 14)
"""
    },
    
    "road": {
        "name": "Road Cross-Section",
        "description": "Road layers and camber",
        "code": """
; Road Cross-Section
(def road-width 7000)
(def subgrade-h 400)
(def subbase-h 300)
(def base-h 200)
(def surface-h 100)
(def camber 2.5)

; Calculate camber height
(def camber-h (* road-width (/ camber 100)))

; Subgrade
(fill #dcb)
(rect 100 500 road-width subgrade-h)

; Sub-base
(fill #bbb)
(rect 100 (- 500 subbase-h) road-width subbase-h)

; Base course
(fill #999)
(rect 100 (- 500 subbase-h base-h) road-width base-h)

; Surface course with camber
(fill #333)
(def surface-y (- 500 subbase-h base-h surface-h))
(rect 100 surface-y road-width surface-h)

; Camber line
(stroke #ffff00)
(line 100 surface-y 
      (+ 100 (/ road-width 2)) (- surface-y camber-h))
(line (+ 100 (/ road-width 2)) (- surface-y camber-h)
      (+ 100 road-width) surface-y)

; Annotations
(fill #ffffff)
(text (+ 100 (/ road-width 2)) (- surface-y 50) "ROAD SECTION" 14)
(text (+ 100 (/ road-width 2)) (+ 500 subgrade-h 30) 
      (+ "WIDTH = " road-width "mm | CAMBER = " camber "%") 10)
"""
    }
}


def get_template(module_name: str) -> dict:
    """Get template for a module"""
    return TEMPLATES.get(module_name.lower(), TEMPLATES["lintel"])


def get_all_templates() -> dict:
    """Get all available templates"""
    return TEMPLATES


def list_templates() -> list:
    """Get list of template names"""
    return list(TEMPLATES.keys())
