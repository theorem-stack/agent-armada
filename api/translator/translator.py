from .SimplePythonInterpreter import SimplePythonInterpreter
from .SimplePythonValidator import SimplePythonValidator

def translate(code):
    """
    Translates the given code to another language.
    """
    
    # Validate the code
    validator = SimplePythonValidator()
    if validator.validate(code):
        print("Code is valid. Executing...")
        interpreter = SimplePythonInterpreter()
        local_scope = interpreter.execute(code)

        # Call the functions if they're defined
        if 'check_even_or_odd' in local_scope:
            test_num = 7
            result = local_scope['check_even_or_odd'](test_num)
            print(f"Result of check_even_or_odd({test_num}): {result}")

        if 'filter_even_numbers' in local_scope:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8]
            even_numbers = local_scope['filter_even_numbers'](numbers)
            print(f"Even numbers from {numbers}: {even_numbers}")

        if 'object_test' in local_scope:
            objects = [
                {'type': 'cube', 'volume': 0},
                {'type': 'sphere', 'volume': 0}
            ]
            N = 5
            updated_objects = local_scope['object_test'](objects, N)
            print(f"Updated objects: {updated_objects}")
        else:
            print("Function 'filter_even_numbers' not found in local scope.")
    else:
        print("Code validation failed.")

def main():
    # Sample input: a simple function with if statements and logical operators
    code = """
    def check_even_or_odd(n):
        if n % 2 == 0:
            return "Even"
        else:
            return "Odd"

    def filter_even_numbers(numbers):
        even_numbers = []
        for num in numbers:
            if num % 2 == 0:
                even_numbers.append(num)
        return even_numbers

    def object_test(objects, N):
        for obj in objects:
            if obj['type'] == 'cube':
                obj['volume'] = N ** 3
            elif obj['type'] == 'sphere':
                obj['volume'] = (4 / 3) * 3.14 * (N ** 3)
        return objects
    """

    translate(code)

if __name__ == "__main__":
    main()
