import numpy as np

# Screen settings
ENV_WIDTH, ENV_HEIGHT = 800, 600

# Agent parameters
NUM_BOIDS = 20
MAX_SPEED = 3
MAX_FORCE = 0.1
RADIUS = 100  # Perception radius for alignment, cohesion, separation
NUM_TARGETS = 4  # Number of targets
TARGET_RADIUS = 10  # Radius for the target area
NUM_OBSTACLES = 3  # Number of obstacles
OBSTACLE_RADIUS = 30  # Radius for the obstacles

# SYSTEM BEHAVIOR PARAMETERS
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 1.2
SEPARATION_WEIGHT = 1.2
TARGET_WEIGHT = 1.3
OBSTACLE_WEIGHT = 1.7
TERRAIN_WEIGHT = 0.13

# Example height map (can be loaded from an external source)
TERRAIN_HEIGHT_MAP = np.array([
    [0, 0, 0, 0, 6],
    [2, 4, 0, 0, 0],
    [2, 0, 8, 0, 0],
    [0, 0, 0, 2, 0],
    [6, 0, 0, 0, 0]
])
MAP_WIDTH, MAP_HEIGHT = TERRAIN_HEIGHT_MAP.shape

LLM_PROMPT_USER_INPUT = "What are the benefits of exercise?"

LLM_PROMPT_SYSTEM_RESPONSE = "The benefits of exercise include improved cardiovascular health, increased muscle strength and endurance, better flexibility and balance, and enhanced mood and mental well-being. Regular exercise can also help with weight management, reduce the risk of chronic diseases, and improve overall quality of life."