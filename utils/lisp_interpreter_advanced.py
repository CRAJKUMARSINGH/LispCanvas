"""
Advanced Lisp Interpreter with Loops, Functions, and More Commands
Week 1 - Days 4-5 Implementation
"""

import re
import math
from typing import List, Dict, Any, Union, Callable


class AdvancedLispInterpreter:
    """
    Advanced Lisp interpreter with:
    - User-defined functions
    - Loops (repeat, for)
    - Advanced math (sin, cos, sqrt, etc.)
    - More drawing commands
    """
    
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.current_color = '#ffffff'
        self.current_fill = True
        self.current_stroke_width = 2
        
    def tokenize(self, code: str) -> List[str]:
        """Convert Lisp code to tokens"""
        lines = code.split('\n')
        code_without_comments = '\n'.join(
            line.split(';')[0] if ';' in line else line 
            for line in lines
        )
        
        tokens = []
        current = ''
        in_string = False
        
        for char in code_without_comments:
            if in_string:
                if char == '"':
                    in_string = False
                    tokens.append(f'"{current}"')
                    current = ''
                else:
                    current += char
            elif char == '"':
                if current.strip():
                    tokens.append(current.strip())
                current = ''
                in_string = True
            elif char in '()':
                if current.strip():
                    tokens.append(current.strip())
                current = ''
                tokens.append(char)
            elif char.isspace():
                if current.strip():
                    tokens.append(current.strip())
                current = ''
            else:
                current += char
        
        if current.strip():
            tokens.append(current.strip())
        
        return tokens
    
    def parse(self, tokens: List[str]) -> Any:
        """Parse tokens into AST"""
        if not tokens:
            return None
        
        token = tokens.pop(0)
        
        if token == '(':
            ast = []
            while tokens and tokens[0] != ')':
                ast.append(self.parse(tokens))
            if tokens:
                tokens.pop(0)
            return ast
        elif token == ')':
            raise SyntaxError("Unexpected )")
        else:
            if token.startswith('"') and token.endswith('"'):
                return token[1:-1]
            try:
                if '.' in token:
                    return float(token)
                return int(token)
            except ValueError:
                return token
    
    def evaluate(self, expr: Any, local_scope: Dict = None) -> Any:
        """Evaluate expression with optional local scope"""
        scope = {**self.variables, **(local_scope or {})}
        
        # Atomic values
        if isinstance(expr, (int, float)):
            return expr
        
        if isinstance(expr, str):
            if expr in scope:
                return scope[expr]
            return expr
        
        if not isinstance(expr, list) or len(expr) == 0:
            return None
        
        cmd = expr[0]
        
        # Special forms
        if cmd == 'def':
            var_name = expr[1]
            value = self.evaluate(expr[2], local_scope)
            if local_scope is not None:
                local_scope[var_name] = value
            else:
                self.variables[var_name] = value
            return value
        
        if cmd == 'defn':
            # (defn name (args) body)
            func_name = expr[1]
            args = expr[2] if isinstance(expr[2], list) else []
            body = expr[3]
            self.functions[func_name] = {'args': args, 'body': body}
            return None
        
        if cmd == 'if':
            condition = self.evaluate(expr[1], local_scope)
            if condition:
                return self.evaluate(expr[2], local_scope)
            elif len(expr) > 3:
                return self.evaluate(expr[3], local_scope)
            return None
        
        if cmd == 'do':
            # Execute multiple expressions
            result = None
            for e in expr[1:]:
                result = self.evaluate(e, local_scope)
            return result
        
        if cmd == 'repeat':
            # (repeat n body)
            count = self.evaluate(expr[1], local_scope)
            body = expr[2]
            results = []
            for i in range(int(count)):
                # Add loop variable 'i'
                loop_scope = {**(local_scope or {}), 'i': i}
                result = self.evaluate(body, loop_scope)
                if isinstance(result, dict) and 'type' in result:
                    results.append(result)
            return results if results else None
        
        if cmd == 'for':
            # (for var start end body)
            var_name = expr[1]
            start = self.evaluate(expr[2], local_scope)
            end = self.evaluate(expr[3], local_scope)
            body = expr[4]
            results = []
            for i in range(int(start), int(end)):
                loop_scope = {**(local_scope or {}), var_name: i}
                result = self.evaluate(body, loop_scope)
                if isinstance(result, dict) and 'type' in result:
                    results.append(result)
            return results if results else None
        
        # Check for user-defined functions
        if cmd in self.functions:
            func = self.functions[cmd]
            args = [self.evaluate(arg, local_scope) for arg in expr[1:]]
            func_scope = dict(zip(func['args'], args))
            return self.evaluate(func['body'], func_scope)
        
        # Evaluate arguments for built-in functions
        args = [self.evaluate(arg, local_scope) for arg in expr[1:]]
        
        # Math operations
        if cmd == '+':
            return sum(args)
        elif cmd == '-':
            return -args[0] if len(args) == 1 else args[0] - sum(args[1:])
        elif cmd == '*':
            result = 1
            for arg in args:
                result *= arg
            return result
        elif cmd == '/':
            return args[0] / args[1] if len(args) == 2 and args[1] != 0 else 0
        elif cmd == '%':
            return args[0] % args[1] if len(args) == 2 else 0
        
        # Advanced math
        elif cmd == 'sin':
            return math.sin(args[0]) if args else 0
        elif cmd == 'cos':
            return math.cos(args[0]) if args else 0
        elif cmd == 'tan':
            return math.tan(args[0]) if args else 0
        elif cmd == 'sqrt':
            return math.sqrt(args[0]) if args and args[0] >= 0 else 0
        elif cmd == 'pow':
            return math.pow(args[0], args[1]) if len(args) == 2 else 0
        elif cmd == 'abs':
            return abs(args[0]) if args else 0
        elif cmd == 'min':
            return min(args) if args else 0
        elif cmd == 'max':
            return max(args) if args else 0
        elif cmd == 'floor':
            return math.floor(args[0]) if args else 0
        elif cmd == 'ceil':
            return math.ceil(args[0]) if args else 0
        elif cmd == 'round':
            return round(args[0]) if args else 0
        
        # Comparison
        elif cmd == '>':
            return args[0] > args[1] if len(args) == 2 else False
        elif cmd == '<':
            return args[0] < args[1] if len(args) == 2 else False
        elif cmd == '>=':
            return args[0] >= args[1] if len(args) == 2 else False
        elif cmd == '<=':
            return args[0] <= args[1] if len(args) == 2 else False
        elif cmd == '=':
            return args[0] == args[1] if len(args) == 2 else False
        
        # Logic
        elif cmd == 'and':
            return all(args)
        elif cmd == 'or':
            return any(args)
        elif cmd == 'not':
            return not args[0] if args else True
        
        # Drawing state
        elif cmd == 'fill':
            self.current_color = args[0] if args else '#ffffff'
            self.current_fill = True
            return None
        
        elif cmd == 'stroke':
            self.current_color = args[0] if args else '#ffffff'
            self.current_fill = False
            return None
        
        elif cmd == 'stroke-width':
            self.current_stroke_width = args[0] if args else 2
            return None
        
        # Drawing commands
        elif cmd == 'rect':
            if len(args) >= 4:
                return {
                    'type': 'rect',
                    'x': args[0],
                    'y': args[1],
                    'width': args[2],
                    'height': args[3],
                    'color': self.current_color,
                    'fill': self.current_fill,
                    'stroke_width': self.current_stroke_width
                }
        
        elif cmd == 'circle':
            if len(args) >= 3:
                return {
                    'type': 'circle',
                    'x': args[0],
                    'y': args[1],
                    'radius': args[2],
                    'color': self.current_color,
                    'fill': self.current_fill,
                    'stroke_width': self.current_stroke_width
                }
        
        elif cmd == 'line':
            if len(args) >= 4:
                return {
                    'type': 'line',
                    'x1': args[0],
                    'y1': args[1],
                    'x2': args[2],
                    'y2': args[3],
                    'color': self.current_color,
                    'stroke_width': self.current_stroke_width
                }
        
        elif cmd == 'text':
            if len(args) >= 3:
                return {
                    'type': 'text',
                    'x': args[0],
                    'y': args[1],
                    'text': str(args[2]),
                    'size': args[3] if len(args) > 3 else 12,
                    'color': self.current_color
                }
        
        elif cmd == 'polygon':
            # (polygon ((x1 y1) (x2 y2) (x3 y3) ...))
            if args and isinstance(args[0], list):
                points = []
                for point in args[0]:
                    if isinstance(point, list) and len(point) >= 2:
                        points.append({'x': point[0], 'y': point[1]})
                return {
                    'type': 'polygon',
                    'points': points,
                    'color': self.current_color,
                    'fill': self.current_fill,
                    'stroke_width': self.current_stroke_width
                }
        
        elif cmd == 'arc':
            # (arc x y radius start-angle end-angle)
            if len(args) >= 5:
                return {
                    'type': 'arc',
                    'x': args[0],
                    'y': args[1],
                    'radius': args[2],
                    'start': args[3],
                    'end': args[4],
                    'color': self.current_color,
                    'fill': self.current_fill,
                    'stroke_width': self.current_stroke_width
                }
        
        return None
    
    def execute(self, code: str) -> List[Dict]:
        """Execute Lisp code and return drawing commands"""
        try:
            tokens = self.tokenize(code)
            commands = []
            
            while tokens:
                expr = self.parse(tokens)
                if expr is not None:
                    result = self.evaluate(expr)
                    
                    # Handle single command
                    if isinstance(result, dict) and 'type' in result:
                        commands.append(result)
                    
                    # Handle list of commands (from loops)
                    elif isinstance(result, list):
                        for item in result:
                            if isinstance(item, dict) and 'type' in item:
                                commands.append(item)
            
            return commands
        
        except Exception as e:
            return [{
                'type': 'error',
                'message': str(e)
            }]
    
    def get_variables(self) -> Dict[str, Any]:
        """Get all defined variables"""
        return self.variables.copy()
    
    def get_functions(self) -> Dict[str, Any]:
        """Get all defined functions"""
        return self.functions.copy()


# Example usage
if __name__ == "__main__":
    # Test advanced features
    test_code = """
    ; Test loops and functions
    (def size 50)
    (def spacing 60)
    
    ; Draw a row of circles using repeat
    (fill #ff0000)
    (repeat 5 (do
        (circle (+ 50 (* i spacing)) 100 (/ size 2))
    ))
    
    ; Define a function
    (defn draw-square (x y s)
        (rect x y s s))
    
    ; Use the function
    (fill #00ff00)
    (draw-square 50 200 size)
    (draw-square 150 200 size)
    
    ; Advanced math
    (def angle 0.5)
    (def x (+ 300 (* 100 (cos angle))))
    (def y (+ 300 (* 100 (sin angle))))
    (fill #0000ff)
    (circle x y 20)
    """
    
    interpreter = AdvancedLispInterpreter()
    commands = interpreter.execute(test_code)
    
    print("Drawing Commands:")
    for i, cmd in enumerate(commands):
        print(f"  {i+1}. {cmd.get('type')}: {cmd}")
    
    print("\nVariables:")
    for var, value in interpreter.get_variables().items():
        print(f"  {var} = {value}")
    
    print("\nFunctions:")
    for func_name in interpreter.get_functions().keys():
        print(f"  {func_name}")
