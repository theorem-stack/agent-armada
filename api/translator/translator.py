import re
from .SimplePythonInterpreter import SimplePythonInterpreter
from .SimplePythonValidator import SimplePythonValidator

def extract_function_names(code: str) -> list:
    """
    Extracts function names from the given code string.
    
    Parameters:
    - code: A string containing Python code.
    
    Returns:
    - A list of function names found in the code.
    """
    pattern = r"def (\w+)\s*\("
    return re.findall(pattern, code)

def execute_function(function_name: str, local_scope: dict, N: int, Objects: list, BBox: list[int]):
    """
    Executes the specified function with the provided parameters.
    
    Parameters:
    - function_name: The name of the function to execute.
    - local_scope: A dictionary containing the function definitions.
    - N: The number of agents or objects.
    - Objects: The list of objects to be passed to the function.
    - BBox: The bounding box to be passed to the function.
    
    Returns:
    - The result of the function execution, or None if the function does not exist.
    """
    if function_name in local_scope:
        return local_scope[function_name](N, Objects, BBox)
    else:
        print(f"Function '{function_name}' not found in local scope.")
        return None

def translate(code: str, N: int, Objects: list, BBox: list[int]):
    """
    Translates the given code to another language and executes defined functions.
    
    Parameters:
    - code: A string containing Python code.
    - N: Number of agents or objects.
    - Objects: List of objects.
    - BBox: Bounding box as a list of integers.
    
    Returns:
    - The result of the executed function, or None if validation fails or no function is defined.
    """
    validator = SimplePythonValidator()
    
    if not validator.validate(code):
        print("Code validation failed.")
        return None

    print("Code is valid. Executing...")
    interpreter = SimplePythonInterpreter()
    local_scope = interpreter.execute(code)

    function_names = extract_function_names(code)

    if not function_names:
        print("No functions found in the provided code.")
        return None

    if len(function_names) > 1:
        print(f"Warning: Multiple functions found. Executing the first one: {function_names[0]}")

    return execute_function(function_names[0], local_scope, N, Objects, BBox)

def main():
    # Sample input: a simple function with if statements and logical operators
    code = """
    def move_to_center(N, Objects, BBox):
        center_x = (BBox[0] + BBox[2]) / 2
        center_y = (BBox[1] + BBox[3]) / 2
        return [(center_x, center_y) for _ in range(N)]

    def form_circle(N, Objects, BBox):
        import math
        center_x = (BBox[0] + BBox[2]) / 2
        center_y = (BBox[1] + BBox[3]) / 2
        radius = min((BBox[2] - BBox[0]), (BBox[3] - BBox[1])) / 4
        coordinates = []
        for i in range(N):
            angle = 2 * math.pi * i / N
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            coordinates.append((x, y))
        return coordinates
    """

    # Define inputs
    N = 5  # Number of agents or objects
    Objects = [{'type': 'cube', 'volume': 0}, {'type': 'sphere', 'volume': 0}]  # Example object list
    BBox = [0, 0, 10, 10]  # Example bounding box

    result = translate(code, N, Objects, BBox)
    if result is not None:
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
