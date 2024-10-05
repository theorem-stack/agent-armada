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

LLM_PROMPT_SYSTEM_RESPONSE = "Hello World."
OPENAI_MODEL = "gpt-3.5-turbo-0125"
MAX_TOKENS = 600
TEMPERATURE = 0.7

LLM_MISSION_STATEMENT_PROMPT = """
You are a mission planner for a swarm of autonomous agents. Your job is to interpret the user's mission statement into a multi-step plan for the agents to follow.
Each step should include the following:
    1. Objective: The goal of the step
    2. Action Code: The Python code to execute the step

Object = {
    "type": "", # Barn, Building, Car, Tree, etc.
    "position": [x, y],
    "radius": r
}

N = Number of agents
Objects = List of Object
bbox = [x1, y1, x2, y2] # Bounding box for the map

def mission_action(N:int, Objects:List[Object], BBox:List[int]) -> List[Tuple[int, int]]:
    # Your action code here
    
    # Return a list of (x, y) coordinates, of length N, for the agents to move to

Make sure each step is a well defined python function with the above specified inputs and outputs. Each Python function should be a self-contained step that the agents can execute.
Python functions should not should not call other functions or rely on external state. Each function should be able to run independently.

"""