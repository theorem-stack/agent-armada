from .target import Target
from .obstacle import Obstacle
from .agent import Agent
import numpy as np

from .utils import get_height_at_position

# def create_height_map_surface():
#     """Create a surface representation of the height map."""
#     surface = pygame.Surface((WIDTH, HEIGHT))
    
#     # Normalize the height map for color mapping
#     max_height = HEIGHT_MAP.max()
#     min_height = HEIGHT_MAP.min()

#     for y in range(HEIGHT):
#         for x in range(WIDTH):
#             # Get the height at the current screen position
#             height = get_height_at_position(x, y)

#             # Normalize height value to a range of [0, 1]
#             normalized_height = (height - min_height) / (max_height - min_height)
            
#             # Map normalized height to a color (white for low, dark gray for high)
#             color_value = int(255 * (1 - normalized_height))  # Invert the color value
#             color = (color_value, color_value, color_value)  # Grayscale color
            
#             surface.set_at((x, y), color)
    
#     return surface

def create_targets_from_dict(target_dict):
    # Create a dict of Target objects by iterating over the dictionary
    return {
        target_id: Target(
            target_id,
            np.array(target_data["position"], dtype=float),  # Extract position and convert to NumPy array
            target_data["radius"]  # Extract radius
        )
        for target_id, target_data in target_dict.items()
    }

def create_obstacles_from_dict(obstacles_dict):
    # Create a dict of Target objects by iterating over the dictionary
    return [
        Obstacle(
            obstacle_id,
            np.array(obstacle_data["position"], dtype=float),
            obstacle_data["radius"]
        )
        for obstacle_id, obstacle_data in obstacles_dict.items()
    ]

def create_agents_from_dict(agents_dict):
    # Create a list of Agent objects by iterating over the dictionary
    return [
        Agent(
            agent_id,
            np.array(data["position"], dtype=float),  # Convert position to a NumPy array of floats
            data["target_id"]
        )
        for agent_id, data in agents_dict.items()
    ]