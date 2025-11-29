"""
AI Code Generator for Structural Design
Converts natural language descriptions to Lisp code
"""

import os
from typing import List, Dict, Optional
import json

class AICodeGenerator:
    """AI-powered Lisp code generator for structural designs"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI generator
        
        Args:
            api_key: OpenAI API key (optional, will check env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.has_api_key = bool(self.api_key)
        
        # Template-based fallback for when API is not available
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load design templates for fallback generation"""
        return {
            'lintel': '''
; Lintel Design - {span}mm span
(def span {span})
(def width {width})
(def depth {depth})
(def num-bars {num_bars})
(def bearing 150)

; Draw lintel elevation
(background #fff)
(fill #ccc)
(rect 0 0 (+ span (* 2 bearing)) depth)

; Reinforcement
(def bar-spacing (/ span (- num-bars 1)))
(def y-pos (- depth 40))

; Draw main bars
(fill #000)
{bars_code}

; Dimensions
(text (/ span 2) -20 (+ "SPAN = " span "mm") 12)
(text (/ span 2) -40 (+ num-bars " - ø{bar_dia}mm BARS") 10)
''',
            'sunshade': '''
; Sunshade Design - {projection}mm projection
(def projection {projection})
(def thickness {thickness})
(def beam-depth {beam_depth})
(def beam-width 300)

; Background
(background #fff)

; Supporting beam
(fill #ddd)
(rect 0 0 beam-width beam-depth)

; Sunshade slab
(fill #eee)
(rect 0 beam-depth projection thickness)

; Reinforcement indication
(stroke #888)
(line 20 (+ beam-depth 20) (- projection 20) (+ beam-depth 20))

; Labels
(fill #000)
(text (/ projection 2) (+ beam-depth thickness 30) "SUNSHADE" 14)
(text (/ projection 2) (+ beam-depth thickness 50) (+ "PROJECTION: " projection "mm") 10)
''',
            'column': '''
; Column Design - {height}mm height
(def col-width {width})
(def col-height {height})
(def bar-dia {bar_dia})
(def num-bars {num_bars})

; Background
(background #fff)

; Column outline
(fill #ddd)
(rect 100 100 col-width col-height)

; Reinforcement
(def cover 40)
(def bar-spacing (/ (- col-width (* 2 cover)) (- num-bars 1)))

; Draw bars
(fill #000)
{bars_code}

; Stirrups indication
(stroke #888)
(rect (+ 100 cover) (+ 100 cover) (- col-width (* 2 cover)) (- col-height (* 2 cover)))

; Labels
(fill #000)
(text (+ 100 (/ col-width 2)) 80 "COLUMN" 14)
(text (+ 100 (/ col-width 2)) (+ 100 col-height 30) (+ col-width "x" col-height "mm") 10)
''',
            'beam': '''
; Beam Design - {length}mm length
(def beam-length {length})
(def beam-width {width})
(def beam-depth {depth})

; Background
(background #fff)

; Beam elevation
(fill #ccc)
(rect 0 200 beam-length beam-depth)

; Stirrups indication
(stroke #888)
(def stirrup-spacing 150)
(def num-stirrups (/ beam-length stirrup-spacing))
(repeat num-stirrups
  (do
    (def x-pos (* t stirrup-spacing))
    (line x-pos 200 x-pos (+ 200 beam-depth))
  ))

; Labels
(fill #000)
(text (/ beam-length 2) 180 "BEAM ELEVATION" 14)
(text (/ beam-length 2) (+ 200 beam-depth 30) (+ beam-width "x" beam-depth "mm") 10)
''',
            'footing': '''
; Footing Design - {width}mm x {length}mm
(def footing-width {width})
(def footing-length {length})
(def footing-depth {depth})
(def column-width {column_width})

; Background
(background #fff)

; Footing base
(fill #bbb)
(rect 100 300 footing-width footing-depth)

; Pedestal
(fill #999)
(rect (+ 100 (/ (- footing-width column-width) 2)) 280 column-width 20)

; Column stub
(fill #ddd)
(rect (+ 100 (/ (- footing-width column-width) 2)) 200 column-width 80)

; Labels
(fill #000)
(text (+ 100 (/ footing-width 2)) 180 "ISOLATED FOOTING" 14)
(text (+ 100 (/ footing-width 2)) (+ 300 footing-depth 30) (+ footing-width "x" footing-length "mm") 10)
'''
        }
    
    def generate_code(self, description: str, element_type: str, 
                     parameters: Optional[Dict] = None) -> str:
        """
        Generate Lisp code from natural language description
        
        Args:
            description: Natural language description of the design
            element_type: Type of element (lintel, sunshade, column, etc.)
            parameters: Optional parameters extracted from description
            
        Returns:
            Generated Lisp code
        """
        if self.has_api_key:
            return self._generate_with_ai(description, element_type, parameters)
        else:
            return self._generate_with_template(description, element_type, parameters)
    
    def _generate_with_ai(self, description: str, element_type: str,
                         parameters: Optional[Dict] = None) -> str:
        """Generate code using OpenAI API"""
        try:
            import openai
            openai.api_key = self.api_key
            
            # Build prompt
            prompt = self._build_prompt(description, element_type, parameters)
            
            # Call OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a civil engineering CAD expert who generates Lisp code for structural designs."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            code = response.choices[0].message.content
            
            # Extract code block if wrapped
            if "```" in code:
                code = code.split("```")[1]
                if code.startswith("lisp") or code.startswith("scheme"):
                    code = "\n".join(code.split("\n")[1:])
            
            return code.strip()
            
        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_with_template(description, element_type, parameters)
    
    def _generate_with_template(self, description: str, element_type: str,
                                parameters: Optional[Dict] = None) -> str:
        """Generate code using templates (fallback)"""
        # Extract parameters from description if not provided
        if parameters is None:
            parameters = self._extract_parameters(description, element_type)
        
        # Get template
        template = self.templates.get(element_type, self.templates['lintel'])
        
        # Generate bars code if needed
        if 'num_bars' in parameters:
            bars_code = self._generate_bars_code(parameters)
            parameters['bars_code'] = bars_code
        
        # Fill template
        try:
            code = template.format(**parameters)
            return code
        except KeyError as e:
            # Missing parameter, use defaults
            defaults = self._get_default_parameters(element_type)
            defaults.update(parameters)
            if 'num_bars' in defaults and 'bars_code' not in defaults:
                defaults['bars_code'] = self._generate_bars_code(defaults)
            code = template.format(**defaults)
            return code
    
    def _extract_parameters(self, description: str, element_type: str) -> Dict:
        """Extract parameters from natural language description"""
        import re
        
        params = {}
        
        # Common patterns
        patterns = {
            'span': r'(\d+\.?\d*)\s*(?:mm|m)?\s*(?:span|long|length)',
            'width': r'(\d+\.?\d*)\s*(?:mm|m)?\s*(?:wide|width)',
            'depth': r'(\d+\.?\d*)\s*(?:mm|m)?\s*(?:deep|depth|high|height)',
            'height': r'(\d+\.?\d*)\s*(?:mm|m)?\s*(?:tall|height|high)',
            'thickness': r'(\d+\.?\d*)\s*(?:mm|m)?\s*(?:thick|thickness)',
            'projection': r'(\d+\.?\d*)\s*(?:mm|m)?\s*(?:projection|projecting|cantilever)',
            'num_bars': r'(\d+)\s*(?:bars?|reinforcement)',
            'bar_dia': r'(?:ø|diameter|dia\.?)\s*(\d+)',
            'length': r'(\d+\.?\d*)\s*(?:mm|m)?\s*(?:long|length)',
        }
        
        for param, pattern in patterns.items():
            match = re.search(pattern, description.lower())
            if match:
                value = float(match.group(1))
                # Convert to mm if in meters
                if 'm' in match.group(0) and 'mm' not in match.group(0):
                    value *= 1000
                params[param] = int(value) if param in ['num_bars', 'bar_dia'] else value
        
        return params
    
    def _get_default_parameters(self, element_type: str) -> Dict:
        """Get default parameters for element type"""
        defaults = {
            'lintel': {
                'span': 1200,
                'width': 200,
                'depth': 250,
                'num_bars': 3,
                'bar_dia': 12,
                'bearing': 150
            },
            'sunshade': {
                'projection': 1000,
                'thickness': 150,
                'beam_depth': 450,
                'beam_width': 300
            },
            'column': {
                'width': 300,
                'height': 3000,
                'num_bars': 4,
                'bar_dia': 16
            },
            'beam': {
                'length': 5000,
                'width': 230,
                'depth': 450
            },
            'footing': {
                'width': 1500,
                'length': 1500,
                'depth': 400,
                'column_width': 300
            }
        }
        return defaults.get(element_type, defaults['lintel'])
    
    def _generate_bars_code(self, parameters: Dict) -> str:
        """Generate code for reinforcement bars"""
        num_bars = parameters.get('num_bars', 3)
        bar_dia = parameters.get('bar_dia', 12)
        
        bars_code = []
        for i in range(num_bars):
            bars_code.append(f"(circle (+ cover (* {i} bar-spacing)) y-pos (/ {bar_dia} 2))")
        
        return "\n".join(bars_code)
    
    def _build_prompt(self, description: str, element_type: str,
                     parameters: Optional[Dict] = None) -> str:
        """Build prompt for AI generation"""
        prompt = f"""
Generate Lisp code for a {element_type} design based on this description:

"{description}"

Available Lisp commands:
- (def variable value) - Define variable
- (rect x y width height) - Draw rectangle
- (circle x y radius) - Draw circle
- (line x1 y1 x2 y2) - Draw line
- (text x y "string" size) - Draw text
- (fill color) - Set fill color
- (stroke color) - Set stroke color
- (background color) - Set background
- Math: +, -, *, /, sin, cos
- (repeat n body) - Repeat n times

Requirements:
1. Use (background #fff) for white background
2. Define key dimensions as variables with (def)
3. Use appropriate colors (#ccc for concrete, #888 for steel, etc.)
4. Add labels with (text) for dimensions
5. Include reinforcement representation
6. Keep code clean and well-commented

Generate clean, well-commented Lisp code:
"""
        
        if parameters:
            prompt += f"\n\nExtracted parameters: {json.dumps(parameters, indent=2)}"
        
        return prompt
    
    def generate_variations(self, base_code: str, num_variations: int = 3) -> List[str]:
        """
        Generate design variations from base code
        
        Args:
            base_code: Base Lisp code to vary
            num_variations: Number of variations to generate
            
        Returns:
            List of code variations
        """
        if self.has_api_key:
            return self._generate_variations_with_ai(base_code, num_variations)
        else:
            return self._generate_variations_with_rules(base_code, num_variations)
    
    def _generate_variations_with_ai(self, base_code: str, num_variations: int) -> List[str]:
        """Generate variations using AI"""
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""
Given this Lisp design code:

{base_code}

Generate {num_variations} interesting variations by:
1. Changing dimensions (±20%)
2. Adding details (more reinforcement, annotations)
3. Modifying proportions
4. Adjusting colors/styling

Return each variation as a separate code block.
Keep the same overall structure but make meaningful changes.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a creative structural design assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            
            # Parse variations
            variations = []
            for block in content.split("```"):
                if "def" in block or "rect" in block:
                    clean_block = block.strip()
                    if clean_block.startswith("lisp") or clean_block.startswith("scheme"):
                        clean_block = "\n".join(clean_block.split("\n")[1:])
                    variations.append(clean_block.strip())
            
            return variations[:num_variations]
            
        except Exception as e:
            print(f"AI variation generation failed: {e}")
            return self._generate_variations_with_rules(base_code, num_variations)
    
    def _generate_variations_with_rules(self, base_code: str, num_variations: int) -> List[str]:
        """Generate variations using rule-based approach"""
        import re
        
        variations = []
        
        # Extract numeric values
        def_pattern = r'\(def\s+(\w+)\s+(\d+\.?\d*)\)'
        defs = re.findall(def_pattern, base_code)
        
        for i in range(num_variations):
            varied_code = base_code
            
            # Vary each dimension
            for var_name, value in defs:
                original_value = float(value)
                # Vary by ±10% to ±30%
                factor = 1.0 + ((i + 1) * 0.1) * (1 if i % 2 == 0 else -1)
                new_value = int(original_value * factor)
                
                # Replace in code
                varied_code = re.sub(
                    f'\\(def\\s+{var_name}\\s+{value}\\)',
                    f'(def {var_name} {new_value})',
                    varied_code
                )
            
            # Add variation comment
            varied_code = f"; Variation {i+1}\n" + varied_code
            variations.append(varied_code)
        
        return variations
    
    def suggest_improvements(self, code: str) -> List[str]:
        """Suggest improvements for existing code"""
        suggestions = []
        
        # Check for common improvements
        if '(def ' not in code or code.count('(def ') < 3:
            suggestions.append("💡 Add more variables for parametric design flexibility")
        
        if '(repeat' not in code:
            suggestions.append("💡 Use (repeat) for creating patterns and arrays")
        
        if '(text' not in code or code.count('(text') < 2:
            suggestions.append("💡 Add more labels and dimensions for clarity")
        
        if '(fill' not in code or code.count('(fill') < 2:
            suggestions.append("💡 Use different colors to distinguish elements")
        
        if '(background' not in code:
            suggestions.append("💡 Add (background #fff) for better visualization")
        
        # Check for reinforcement
        if 'circle' not in code and 'column' in code.lower():
            suggestions.append("💡 Add reinforcement bars with (circle) commands")
        
        return suggestions


# Convenience function
def generate_design_code(description: str, element_type: str = "lintel") -> str:
    """
    Quick function to generate design code
    
    Args:
        description: Natural language description
        element_type: Type of structural element
        
    Returns:
        Generated Lisp code
    """
    generator = AICodeGenerator()
    return generator.generate_code(description, element_type)
