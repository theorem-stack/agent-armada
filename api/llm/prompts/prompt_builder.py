# Develop a "Framework" for building prompts similar to React's JSX
# The goal is to dynamically build prompts based on context, and user statement
# The framework should outline the structure of the prompt, and provide a way to fill in the blanks
# The framework should include a ranking / similarity function to determine which "chunks" or "functions" to include in the prompt from a database of possible chunks

import yaml

# Load Python functions from a YAML file
def load_functions_from_yaml(file_path):
    with open(file_path, 'r') as f:
        functions = yaml.safe_load(f)
    return functions

# Example usage
functions = load_functions_from_yaml('functions.yaml')
for function in functions:
    print(f"ID: {function['id']}")
    print(f"Task Type: {function['task_type']}")
    print(f"Description: {function['description']}")
    print(f"Function:\n{function['python_function']}")
