"""
Simple Lisp Interpreter for Design Code
Week 1 Implementation - Basic Drawing Commands
"""

import re
from typing import List, Dict, Any, Union


class LispInterpreter:
    """
    Simple Lisp interpreter for parametric design
    Supports basic drawing commands and variables
    """
    
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.current_color = '#ffffff'
        self.current_fill = True
        
    def tokenize(self, code: str) -> List[str]:
        """Convert Lisp code to tokens"""
        # Remove comments (lines starting with ;)
        lines = code.split('\n')
        code_without_comments = '\n'.join(
            line.split(';')[0] if ';' in line else line 
            for line in lines
        )
        
        # Tokenize
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
                tokens.pop(0)  # Remove ')'
            return ast
        elif token == ')':
            raise SyntaxError("Unexpected )")
        else:
            # String literal
            if token.startswith('"') and token.endswith('"'):
                return token[1:-1]
            # Number
            try:
                if '.' in token:
                    return float(token)
                return int(token)
            except ValueError:
                return token
    
    def evaluate(self, expr: Any) -> Any:
        """Evaluate expression"""
        # Atomic values
        if isinstance(expr, (int, float)):
            return expr
        
        if isinstance(expr, str):
            # Variable lookup
            if expr in self.variables:
                return self.variables[expr]
            return expr
        
        if not isinstance(expr, list) or len(expr) == 0:
            return None
        
        cmd = expr[0]
        
        # Special forms (don't evaluate arguments immediately)
        if cmd == 'def':
            var_name = expr[1]
            value = self.evaluate(expr[2])
            self.variables[var_name] = value
            return value
        
        if cmd == 'if':
            condition = self.evaluate(expr[1])
            if condition:
                return self.evaluate(expr[2])
            elif len(expr) > 3:
                return self.evaluate(expr[3])
            return None
        
        # Evaluate arguments for other commands
        args = [self.evaluate(arg) for arg in expr[1:]]
        
        # Math operations
        if cmd == '+':
            return sum(args)
        elif cmd == '-':
            if len(args) == 1:
                return -args[0]
            return args[0] - sum(args[1:])
        elif cmd == '*':
            result = 1
            for arg in args:
                result *= arg
            return result
        elif cmd == '/':
            if len(args) == 2:
                return args[0] / args[1] if args[1] != 0 else 0
            return 0
        elif cmd == '%':
            return args[0] % args[1] if len(args) == 2 else 0
        
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
        
        # Drawing state
        elif cmd == 'fill':
            self.current_color = args[0] if args else '#ffffff'
            self.current_fill = True
            return None
        
        elif cmd == 'stroke':
            self.current_color = args[0] if args else '#ffffff'
            self.current_fill = False
            return None
        
        # Drawing commands - return as dict for canvas
        elif cmd == 'rect':
            if len(args) >= 4:
                return {
                    'type': 'rect',
                    'x': args[0],
                    'y': args[1],
                    'width': args[2],
                    'height': args[3],
                    'color': self.current_color,
                    'fill': self.current_fill
                }
        
        elif cmd == 'circle':
            if len(args) >= 3:
                return {
                    'type': 'circle',
                    'x': args[0],
                    'y': args[1],
                    'radius': args[2],
                    'color': self.current_color,
                    'fill': self.current_fill
                }
        
        elif cmd == 'line':
            if len(args) >= 4:
                return {
                    'type': 'line',
                    'x1': args[0],
                    'y1': args[1],
                    'x2': args[2],
                    'y2': args[3],
                    'color': self.current_color
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
        
        return None
    
    def execute(self, code: str) -> List[Dict]:
        """
        Execute Lisp code and return drawing commands
        
        Returns:
            List of drawing command dictionaries
        """
        try:
            tokens = self.tokenize(code)
            commands = []
            
            while tokens:
                expr = self.parse(tokens)
                if expr is not None:
                    result = self.evaluate(expr)
                    if isinstance(result, dict) and 'type' in result:
                        commands.append(result)
            
            return commands
        
        except Exception as e:
            # Return error as a text command
            return [{
                'type': 'error',
                'message': str(e)
            }]
    
    def get_variables(self) -> Dict[str, Any]:
        """Get all defined variables"""
        return self.variables.copy()


# Example usage and testing
if __name__ == "__main__":
    # Test the interpreter
    test_code = """
    ; Define variables
    (def width 200)
    (def height 300)
    
    ; Draw rectangle
    (fill #ff0000)
    (rect 10 10 width height)
    
    ; Draw circle
    (fill #00ff00)
    (circle 100 100 50)
    
    ; Draw line
    (stroke #0000ff)
    (line 0 0 200 200)
    
    ; Draw text
    (text 50 50 "Hello Lisp" 16)
    """
    
    interpreter = LispInterpreter()
    commands = interpreter.execute(test_code)
    
    print("Drawing Commands:")
    for cmd in commands:
        print(f"  {cmd}")
    
    print("\nVariables:")
    for var, value in interpreter.get_variables().items():
        print(f"  {var} = {value}")
