import numpy as np

# SIMULATION ENVIRONMENT PARAMETERS
ENV_WIDTH, ENV_HEIGHT = 800, 600

# Agent parameters
NUM_AGENTS = 20
MAX_SPEED = 3
MAX_FORCE = 0.1
RADIUS = 100  # Perception radius for alignment, cohesion, separation

# AGENT BEHAVIOR PARAMETERS
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 1.2
SEPARATION_WEIGHT = 1.2
TARGET_WEIGHT = 1.3
OBSTACLE_WEIGHT = 1.7
TERRAIN_WEIGHT = 0.13

# DEBUG: Temporary, will be replaced by the LLM identified target and obstacle positions
NUM_TARGETS = 4
TARGET_RADIUS = 10
NUM_OBSTACLES = 3
OBSTACLE_RADIUS = 30

# DEBUG: Example height map (can be loaded from an external source)
TERRAIN_HEIGHT_MAP = np.array([
    [0, 0, 0, 0, 6],
    [2, 4, 0, 0, 0],
    [2, 0, 8, 0, 0],
    [0, 0, 0, 2, 0],
    [6, 0, 0, 0, 0]
])
MAP_WIDTH, MAP_HEIGHT = TERRAIN_HEIGHT_MAP.shape

# LLM PARAMETERS
LLM_MISSION_STATEMENT_PROMPT = "You are a helpful AI mission controller. Your job is to provide detailed, multi-step plans to help users achieve their goals. Each step in your plan must include an accurate and concise python function."
LLM_PROMPT_SYSTEM_RESPONSE = "The benefits of exercise include improved cardiovascular health, increased muscle strength and endurance, better flexibility and balance, and enhanced mood and mental well-being. Regular exercise can also help with weight management, reduce the risk of chronic diseases, and improve overall quality of life."
OPENAI_MODEL = "gpt-3.5-turbo-0125"
MAX_TOKENS = 150
TEMPERATURE = 0.7