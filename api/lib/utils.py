import numpy as np
import re
import math
import yaml
from typing import Dict, Any

from ..config import TERRAIN_HEIGHT_MAP, ENV_WIDTH, ENV_HEIGHT, MAP_WIDTH, MAP_HEIGHT

def get_height_at_position(x, y):
    """Fetch the height using bilinear interpolation at the given screen position (x, y)."""
    # Normalize to the height map grid
    # Scale X, Y to the height map size
    map_x = (x / ENV_WIDTH) * (MAP_WIDTH - 1)
    map_y = (y / ENV_HEIGHT) * (MAP_HEIGHT - 1)
    
    # Get the floor and ceil indices
    x0 = int(np.floor(map_x))
    x1 = min(x0 + 1, MAP_WIDTH - 1)
    y0 = int(np.floor(map_y))
    y1 = min(y0 + 1, MAP_HEIGHT - 1)

    # Get the heights at the corners of the square
    h00 = TERRAIN_HEIGHT_MAP[y0, x0]  # Bottom left
    h01 = TERRAIN_HEIGHT_MAP[y0, x1]  # Bottom right
    h10 = TERRAIN_HEIGHT_MAP[y1, x0]  # Top left
    h11 = TERRAIN_HEIGHT_MAP[y1, x1]  # Top right

    # Calculate the weights for interpolation
    tx = map_x - x0  # Weight in x-direction
    ty = map_y - y0  # Weight in y-direction

    # Perform bilinear interpolation
    height = (h00 * (1 - tx) * (1 - ty) +
              h01 * tx * (1 - ty) +
              h10 * (1 - tx) * ty +
              h11 * tx * ty)

    return height

def get_gradient_at_position(x, y):
        """Calculate the gradient (slope) at the given position from the height map."""
        grid_x = int(min(max(x / ENV_WIDTH * MAP_WIDTH, 1), MAP_WIDTH - 2))
        grid_y = int(min(max(y / ENV_HEIGHT * MAP_HEIGHT, 1), MAP_HEIGHT - 2))
        
        # Compute finite differences for gradient
        dx = TERRAIN_HEIGHT_MAP[grid_y, grid_x + 1] - TERRAIN_HEIGHT_MAP[grid_y, grid_x - 1]
        dy = TERRAIN_HEIGHT_MAP[grid_y + 1, grid_x] - TERRAIN_HEIGHT_MAP[grid_y - 1, grid_x]
    
        # Return gradient vector (influence on X and Y)
        return np.array([dx, dy], dtype=float)

def read_yaml_to_string(file_path: str) -> str:
    """
    Reads a YAML file and returns its content as a string.

    Parameters:
    - file_path: Path to the YAML file.

    Returns:
    - A string representation of the YAML content.
    """
    try:
        with open(file_path, 'r') as file:
            # Load the YAML content
            yaml_content = yaml.safe_load(file)
            # Convert the YAML content to a string
            yaml_string = yaml.dump(yaml_content, default_flow_style=False)
            return yaml_string
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except yaml.YAMLError as e:
        return f"Error parsing YAML: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def parse_yaml_steps(yaml_string: str) -> Dict[str, Any]:
    """
    Parses a YAML string containing steps and returns a list of steps with objectives and action functions.
    This version can handle extraneous text before or after the YAML content.

    Parameters:
    - yaml_string: A string that may contain additional text before or after the YAML format.

    Returns:
    - A list of dictionaries containing each step's details or an empty list if parsing fails.
    """
    try:
        # Use regex to find the YAML part in the string
        match = re.search(r'(?s)steps:\s*(.*?)(?=\Z|\n\S)', yaml_string)
        if not match:
            print("Error: No valid YAML steps found.")
            return []
        
        yaml_content = match.group(0)  # Get the matched YAML content

        # Load the YAML content
        data = yaml.safe_load(yaml_content)
        
        # Extract steps
        steps = data.get("steps", [])
        
        # Prepare the result list
        parsed_steps = {}
        
        for step in steps:
            # Extract step number, objective, and action function
            step_number = step.get("step")
            function_type = step.get("function_type")
            objective = step.get("objective")
            action_function = step.get("python_function").strip()  # Remove extra spaces
            
            # Store the parsed step details
            parsed_steps[step_number] = {
                "step": step_number,
                "function_type": function_type,
                "objective": objective,
                "python_function": action_function
            }
        
        return parsed_steps
    
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def evaluate_coordinates(target_coordinates: list[tuple[int, int]], 
                         current_coordinates: list[tuple[int, int]], 
                         tolerance: float) -> bool:
    """
    Compares a set of target coordinates to the current coordinates with a given tolerance.
    
    Args:
        target_coordinates (list[Tuple[int, int]]): list of target (x, y) coordinates.
        current_coordinates (list[Tuple[int, int]]): list of current (x, y) coordinates to compare.
        tolerance (float): Allowed maximum distance between target and current points.
        
    Returns:
        bool: True if all corresponding coordinates are within the tolerance, False otherwise.
    """
    if len(target_coordinates) != len(current_coordinates):
        raise ValueError("The number of target and current coordinates must match.")

    for i in range(len(target_coordinates)):
        target_x, target_y = target_coordinates[i]
        current_x, current_y = current_coordinates[i]

        # Calculate the Euclidean distance between the target and current coordinates
        distance = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
        
        # Check if the distance is within the allowed tolerance
        if distance > tolerance:
            return False

    return True
