import numpy as np
import re

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

def parse_llm_response(llm_response: str) -> dict:
    # Step 1: Extract the step description using regex
    step_match = re.search(r'(Step \d+: .+)', llm_response)
    step = step_match.group(1) if step_match else "Step description not found"
    
    # Step 2: Extract the Python code block
    python_code_match = re.search(r'```python\n([\s\S]+?)```', llm_response)
    python_code = python_code_match.group(1) if python_code_match else "Python code not found"
    
    return {
        "step": step,
        "python_code": python_code
    }