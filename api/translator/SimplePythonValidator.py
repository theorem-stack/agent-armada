import ast
import re

class SimplePythonValidator:
    def __init__(self):
        # Define a whitelist of allowed operations
        self.whitelisted_functions = {
            'range',        # Allow range function
            'append',       # Allow list append method
            'len',          # Allow len function
            'sum',          # Allow sum function
            'min',          # Allow min function
            'max',          # Allow max function
            'abs',          # Allow abs function
            'math',         # Allow math module
            'cos',          # Allow cos function
            'sin',          # Allow sin function
            'sqrt',         # Allow sqrt function
            'random',       # Allow random module
            'uniform',      # Allow random.uniform function
            'choice',       # Allow random.choice function
        }
        
    def validate(self, code):
        try:
            # Parse the code into an AST
            tree = ast.parse(code)
            # Validate the AST for functions, loops, if statements, and disallowed operations
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    print(f"Validating function: {node.name}")
                elif isinstance(node, (ast.For, ast.While)):
                    print(f"Found loop: {'For loop' if isinstance(node, ast.For) else 'While loop'}")
                elif isinstance(node, ast.If):
                    print("Found if statement")
                elif isinstance(node, ast.Call):
                    # Check if the called function is whitelisted
                    if isinstance(node.func, ast.Name):
                        if node.func.id not in self.whitelisted_functions:
                            raise ValueError(f"Function '{node.func.id}' is not allowed.")
                    elif isinstance(node.func, ast.Attribute):
                        # Check for method calls on lists
                        if node.func.attr not in self.whitelisted_functions:
                            raise ValueError(f"Method '{node.func.attr}' is not allowed.")
            return True
        except (SyntaxError, ValueError) as e:
            print(f"Validation Error: {e}")
            return False