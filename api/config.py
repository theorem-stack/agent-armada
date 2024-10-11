import numpy as np
from pathlib import Path

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent

# SIMULATION ENVIRONMENT PARAMETERS
ENV_WIDTH, ENV_HEIGHT = 800, 600
DETECT_FILTER_SIZE = 450

# Agent parameters
NUM_AGENTS = 20
MAX_SPEED = 2.5
MAX_FORCE = 0.1
RADIUS = 100  # Perception radius for alignment, cohesion, separation

# AGENT BEHAVIOR PARAMETERS
ALIGNMENT_WEIGHT = 0
COHESION_WEIGHT = 0
SEPARATION_WEIGHT = 0
TARGET_WEIGHT = 1.5
OBSTACLE_WEIGHT = 0
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
    [6, 0, 4, 4, 4]
])
MAP_WIDTH, MAP_HEIGHT = TERRAIN_HEIGHT_MAP.shape

# EVALUATION PARAMETERS
EVAL_TOLERANCE = 10
MAX_EVALS = 5 # Number of evals before the system skips step and progresses

# LLM PARAMETERS
LLM_PROMPT_SYSTEM_RESPONSE = "Hello World."
OPENAI_MODEL = "gpt-3.5-turbo-0125" # "o1-mini"
MAX_TOKENS = 1200
TEMPERATURE = 0.7