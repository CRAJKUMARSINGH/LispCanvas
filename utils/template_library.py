"""
Built-in Template Library
Pre-made templates for common structural elements
"""

from utils.template_engine import Template, TemplateEngine
from typing import List

# Lintel Templates
LINTEL_TEMPLATES = [
    {
        'id': 'lintel_basic',
        'name': 'Basic Lintel',
        'element_type': 'lintel',
        'category': 'basic',
        'description': 'Simple rectangular lintel with reinforcement',
        'tags': ['basic', 'rectangular', 'simple'],
        'code': '''; Basic Lintel Design
(def span {{span}})
(def width {{width}})
(def depth {{depth}})

; Background
(background #f5f5f5)

; Main lintel
(fill #cccccc)
(rect 0 0 span depth)

; Reinforcement
(fill #ff6b6b)
(def bar-dia {{bar_dia}})
(def num-bars {{num_bars}})
(def spacing (/ span (+ num-bars 1)))

(repeat num-bars
  (circle (+ spacing (* spacing (index))) (- depth 50) bar-dia))

; Dimensions
(stroke #333)
(text (/ span 2) -20 (str "Span: " span "mm") 14)
(text -50 (/ depth 2) (str "Depth: " depth "mm") 14)
''',
        'variables': {
            'span': 1200,
            'width': 230,
            'depth': 250,
            'bar_dia': 12,
            'num_bars': 3
        }
    },
    {
        'id': 'lintel_tbeam',
        'name': 'T-Beam Lintel',
        'element_type': 'lintel',
        'category': 'advanced',
        'description': 'T-beam lintel with flange and web',
        'tags': ['t-beam', 'advanced', 'flange'],
        'code': '''; T-Beam Lintel Design
(def span {{span}})
(def flange-width {{flange_width}})
(def flange-depth {{flange_depth}})
(def web-width {{web_width}})
(def web-depth {{web_depth}})

; Background
(background #ffffff)

; Flange
(fill #d4d4d4)
(rect 0 0 span flange-depth)

; Web
(def web-offset (/ (- flange-width web-width) 2))
(rect web-offset flange-depth web-width web-depth)

; Reinforcement in flange
(fill #ff6b6b)
(def bar-dia {{bar_dia}})
(def num-bars-top {{num_bars_top}})
(def spacing-top (/ span (+ num-bars-top 1)))

(repeat num-bars-top
  (circle (+ spacing-top (* spacing-top (index))) 30 bar-dia))

; Reinforcement in web
(def num-bars-bottom {{num_bars_bottom}})
(def spacing-bottom (/ web-width (+ num-bars-bottom 1)))

(repeat num-bars-bottom
  (circle (+ web-offset spacing-bottom (* spacing-bottom (index))) 
          (+ flange-depth web-depth -30) bar-dia))

; Stirrups
(stroke #4a90e2)
(def stirrup-spacing {{stirrup_spacing}})
(def num-stirrups (/ span stirrup-spacing))

(repeat num-stirrups
  (line (* (index) stirrup-spacing) flange-depth
        (* (index) stirrup-spacing) (+ flange-depth web-depth)))

; Dimensions
(stroke #333)
(text (/ span 2) -30 (str "Span: " span "mm") 16)
(text -80 (/ (+ flange-depth web-depth) 2) 
      (str "Total Depth: " (+ flange-depth web-depth) "mm") 14)
''',
        'variables': {
            'span': 1500,
            'flange_width': 600,
            'flange_depth': 150,
            'web_width': 230,
            'web_depth': 300,
            'bar_dia': 16,
            'num_bars_top': 2,
            'num_bars_bottom': 4,
            'stirrup_spacing': 150
        }
    },
    {
        'id': 'lintel_precast',
        'name': 'Precast Lintel',
        'element_type': 'lintel',
        'category': 'precast',
        'description': 'Precast concrete lintel with lifting hooks',
        'tags': ['precast', 'industrial', 'lifting'],
        'code': '''; Precast Lintel Design
(def span {{span}})
(def width {{width}})
(def depth {{depth}})

; Background
(background #e8f4f8)

; Main lintel body
(fill #b8b8b8)
(rect 0 0 span depth)

; Chamfers at corners
(fill #a0a0a0)
(def chamfer {{chamfer}})
(polygon 0 0 chamfer 0 0 chamfer)
(polygon span 0 (- span chamfer) 0 span chamfer)

; Reinforcement
(fill #ff4757)
(def bar-dia {{bar_dia}})
(def cover {{cover}})

; Bottom bars
(def num-bottom {{num_bars_bottom}})
(def spacing-bottom (/ span (+ num-bottom 1)))
(repeat num-bottom
  (circle (+ spacing-bottom (* spacing-bottom (index))) 
          (- depth cover) bar-dia))

; Top bars
(def num-top {{num_bars_top}})
(def spacing-top (/ span (+ num-top 1)))
(repeat num-top
  (circle (+ spacing-top (* spacing-top (index))) cover bar-dia))

; Lifting hooks
(stroke #ffa502)
(def hook-offset {{hook_offset}})
(circle hook-offset 50 20)
(circle (- span hook-offset) 50 20)

; Identification mark
(fill #333)
(text (/ span 2) (/ depth 2) "PRECAST" 20)

; Dimensions
(stroke #2c3e50)
(text (/ span 2) -40 (str "L = " span "mm") 16)
(text -70 (/ depth 2) (str "D = " depth "mm") 14)
''',
        'variables': {
            'span': 1800,
            'width': 230,
            'depth': 300,
            'chamfer': 20,
            'bar_dia': 16,
            'cover': 40,
            'num_bars_bottom': 4,
            'num_bars_top': 2,
            'hook_offset': 300
        }
    }
]

# Sunshade Templates
SUNSHADE_TEMPLATES = [
    {
        'id': 'sunshade_basic',
        'name': 'Basic Sunshade',
        'element_type': 'sunshade',
        'category': 'basic',
        'description': 'Simple horizontal sunshade projection',
        'tags': ['basic', 'horizontal', 'simple'],
        'code': '''; Basic Sunshade Design
(def projection {{projection}})
(def width {{width}})
(def thickness {{thickness}})

; Background
(background #e3f2fd)

; Main sunshade slab
(fill #90caf9)
(rect 0 0 projection thickness)

; Support brackets
(fill #64b5f6)
(def bracket-width {{bracket_width}})
(def num-brackets {{num_brackets}})
(def bracket-spacing (/ projection num-brackets))

(repeat num-brackets
  (rect (* (index) bracket-spacing) thickness 
        bracket-width (- 0 bracket-width)))

; Reinforcement
(fill #e53935)
(def bar-dia {{bar_dia}})
(def bar-spacing {{bar_spacing}})
(def num-bars (/ projection bar-spacing))

(repeat num-bars
  (circle (* (index) bar-spacing) (/ thickness 2) bar-dia))

; Dimensions
(stroke #1565c0)
(text (/ projection 2) -30 (str "Projection: " projection "mm") 14)
(text -80 (/ thickness 2) (str "Thickness: " thickness "mm") 12)
''',
        'variables': {
            'projection': 800,
            'width': 1200,
            'thickness': 120,
            'bracket_width': 100,
            'num_brackets': 3,
            'bar_dia': 10,
            'bar_spacing': 150
        }
    },
    {
        'id': 'sunshade_louvered',
        'name': 'Louvered Sunshade',
        'element_type': 'sunshade',
        'category': 'advanced',
        'description': 'Sunshade with adjustable louvers',
        'tags': ['louvers', 'advanced', 'adjustable'],
        'code': '''; Louvered Sunshade Design
(def projection {{projection}})
(def height {{height}})
(def num-louvers {{num_louvers}})
(def louver-angle {{louver_angle}})

; Background
(background #fff3e0)

; Frame
(stroke #ff6f00)
(fill none)
(rect 0 0 projection height)

; Louvers
(fill #ffb74d)
(def louver-height (/ height (+ num-louvers 1)))
(def louver-depth {{louver_depth}})

(repeat num-louvers
  (let ((y (* (+ (index) 1) louver-height)))
    ; Louver blade
    (rect 0 y projection louver-depth)
    ; Shadow effect
    (fill #ff9800 0.3)
    (rect 0 (+ y louver-depth) projection 5)))

; Support posts
(fill #e65100)
(def post-width {{post_width}})
(rect 0 0 post-width height)
(rect (- projection post-width) 0 post-width height)

; Angle indicator
(stroke #d84315)
(text (/ projection 2) -40 
      (str "Louver Angle: " louver-angle "°") 14)

; Dimensions
(stroke #bf360c)
(text (/ projection 2) (+ height 30) 
      (str "Projection: " projection "mm") 14)
(text -80 (/ height 2) 
      (str "Height: " height "mm") 12)
''',
        'variables': {
            'projection': 1000,
            'height': 1500,
            'num_louvers': 8,
            'louver_angle': 45,
            'louver_depth': 80,
            'post_width': 100
        }
    }
]

# Column Templates
COLUMN_TEMPLATES = [
    {
        'id': 'column_rectangular',
        'name': 'Rectangular Column',
        'element_type': 'column',
        'category': 'basic',
        'description': 'Standard rectangular column with ties',
        'tags': ['basic', 'rectangular', 'tied'],
        'code': '''; Rectangular Column Design
(def width {{width}})
(def depth {{depth}})
(def height {{height}})

; Background
(background #fafafa)

; Column body
(fill #bdbdbd)
(rect 0 0 width depth)

; Corner reinforcement
(fill #d32f2f)
(def bar-dia {{bar_dia}})
(def cover {{cover}})

; 4 corner bars
(circle cover cover bar-dia)
(circle (- width cover) cover bar-dia)
(circle cover (- depth cover) bar-dia)
(circle (- width cover) (- depth cover) bar-dia)

; Intermediate bars
(def num-bars-side {{num_bars_side}})
(if (> num-bars-side 0)
  (let ((spacing (/ (- width (* 2 cover)) (+ num-bars-side 1))))
    (repeat num-bars-side
      (circle (+ cover (* (+ (index) 1) spacing)) cover bar-dia)
      (circle (+ cover (* (+ (index) 1) spacing)) (- depth cover) bar-dia))))

; Ties
(stroke #1976d2)
(def tie-spacing {{tie_spacing}})
(rect cover cover (- width (* 2 cover)) (- depth (* 2 cover)))

; Dimensions
(stroke #212121)
(text (/ width 2) -30 (str "Width: " width "mm") 14)
(text -70 (/ depth 2) (str "Depth: " depth "mm") 14)
(text (/ width 2) (+ depth 40) 
      (str "Main Bars: " (+ 4 (* 2 num-bars-side)) "Φ" bar-dia) 12)
''',
        'variables': {
            'width': 300,
            'depth': 400,
            'height': 3000,
            'bar_dia': 20,
            'cover': 40,
            'num_bars_side': 2,
            'tie_spacing': 200
        }
    },
    {
        'id': 'column_circular',
        'name': 'Circular Column',
        'element_type': 'column',
        'category': 'basic',
        'description': 'Circular column with spiral reinforcement',
        'tags': ['basic', 'circular', 'spiral'],
        'code': '''; Circular Column Design
(def diameter {{diameter}})
(def height {{height}})

; Background
(background #f5f5f5)

; Column body
(fill #9e9e9e)
(circle (/ diameter 2) (/ diameter 2) (/ diameter 2))

; Reinforcement bars
(fill #c62828)
(def bar-dia {{bar_dia}})
(def num-bars {{num_bars}})
(def cover {{cover}})
(def bar-circle-radius (- (/ diameter 2) cover))

(repeat num-bars
  (let ((angle (* (/ 360 num-bars) (index))))
    (let ((x (+ (/ diameter 2) (* bar-circle-radius (cos angle))))
          (y (+ (/ diameter 2) (* bar-circle-radius (sin angle)))))
      (circle x y bar-dia))))

; Spiral indicator
(stroke #1565c0)
(def spiral-pitch {{spiral_pitch}})
(circle (/ diameter 2) (/ diameter 2) bar-circle-radius)

; Center mark
(fill #424242)
(circle (/ diameter 2) (/ diameter 2) 5)

; Dimensions
(stroke #212121)
(text (/ diameter 2) -40 (str "Diameter: " diameter "mm") 16)
(text (/ diameter 2) (+ diameter 40) 
      (str num-bars "Φ" bar-dia " bars") 14)
(text (/ diameter 2) (+ diameter 65) 
      (str "Spiral: Φ8 @ " spiral-pitch "mm") 12)
''',
        'variables': {
            'diameter': 400,
            'height': 3000,
            'bar_dia': 20,
            'num_bars': 8,
            'cover': 40,
            'spiral_pitch': 100
        }
    }
]

# Beam Templates
BEAM_TEMPLATES = [
    {
        'id': 'beam_simply_supported',
        'name': 'Simply Supported Beam',
        'element_type': 'beam',
        'category': 'basic',
        'description': 'Simple beam with uniform reinforcement',
        'tags': ['basic', 'simply-supported', 'uniform'],
        'code': '''; Simply Supported Beam Design
(def span {{span}})
(def width {{width}})
(def depth {{depth}})

; Background
(background #fafafa)

; Beam body
(fill #9e9e9e)
(rect 0 0 span depth)

; Bottom reinforcement (tension)
(fill #e53935)
(def bar-dia-bottom {{bar_dia_bottom}})
(def num-bars-bottom {{num_bars_bottom}})
(def cover {{cover}})
(def spacing-bottom (/ width (+ num-bars-bottom 1)))

(repeat num-bars-bottom
  (circle (+ spacing-bottom (* spacing-bottom (index))) 
          (- depth cover) bar-dia-bottom))

; Top reinforcement (compression)
(fill #1e88e5)
(def bar-dia-top {{bar_dia_top}})
(def num-bars-top {{num_bars_top}})
(def spacing-top (/ width (+ num-bars-top 1)))

(repeat num-bars-top
  (circle (+ spacing-top (* spacing-top (index))) cover bar-dia-top))

; Stirrups
(stroke #43a047)
(def stirrup-spacing {{stirrup_spacing}})
(def num-stirrups (/ span stirrup-spacing))

(repeat num-stirrups
  (line (* (index) stirrup-spacing) 0
        (* (index) stirrup-spacing) depth))

; Support symbols
(fill #ff6f00)
(polygon 0 depth -30 (+ depth 30) 30 (+ depth 30))
(polygon span depth (- span 30) (+ depth 30) (+ span 30) (+ depth 30))

; Dimensions
(stroke #212121)
(text (/ span 2) -40 (str "Span: " span "mm") 16)
(text -80 (/ depth 2) (str "Depth: " depth "mm") 14)
(text (/ span 2) (+ depth 70) 
      (str "Bottom: " num-bars-bottom "Φ" bar-dia-bottom 
           " | Top: " num-bars-top "Φ" bar-dia-top) 12)
''',
        'variables': {
            'span': 4000,
            'width': 300,
            'depth': 500,
            'bar_dia_bottom': 20,
            'num_bars_bottom': 4,
            'bar_dia_top': 16,
            'num_bars_top': 2,
            'cover': 40,
            'stirrup_spacing': 150
        }
    }
]


def load_builtin_templates(engine: TemplateEngine):
    """
    Load all built-in templates into the template engine
    
    Args:
        engine: Template engine instance
    """
    all_templates = (
        LINTEL_TEMPLATES +
        SUNSHADE_TEMPLATES +
        COLUMN_TEMPLATES +
        BEAM_TEMPLATES
    )
    
    for template_data in all_templates:
        template = Template(
            template_id=template_data['id'],
            name=template_data['name'],
            code=template_data['code'],
            element_type=template_data['element_type'],
            category=template_data['category'],
            description=template_data['description'],
            tags=template_data['tags'],
            variables=template_data['variables'],
            author='system',
            is_public=True,
            rating=5.0
        )
        
        engine.save_template(template)


def get_template_count_by_type() -> dict:
    """Get count of templates by element type"""
    return {
        'lintel': len(LINTEL_TEMPLATES),
        'sunshade': len(SUNSHADE_TEMPLATES),
        'column': len(COLUMN_TEMPLATES),
        'beam': len(BEAM_TEMPLATES),
        'total': (len(LINTEL_TEMPLATES) + len(SUNSHADE_TEMPLATES) + 
                 len(COLUMN_TEMPLATES) + len(BEAM_TEMPLATES))
    }
