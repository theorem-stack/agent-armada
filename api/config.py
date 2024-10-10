import numpy as np
from pathlib import Path

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent

# SIMULATION ENVIRONMENT PARAMETERS
ENV_WIDTH, ENV_HEIGHT = 800, 600

# Agent parameters
NUM_AGENTS = 20
MAX_SPEED = 1
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
    [6, 0, 0, 0, 0]
])
MAP_WIDTH, MAP_HEIGHT = TERRAIN_HEIGHT_MAP.shape

# EVALUATION PARAMETERS
EVAL_TOLERANCE = 10

# LLM PARAMETERS
LLM_PROMPT_SYSTEM_RESPONSE = "Hello World."
OPENAI_MODEL = "gpt-3.5-turbo-0125"
MAX_TOKENS = 600
TEMPERATURE = 0.7

LLM_MISSION_STATEMENT_PROMPT = """
You are a mission planner for a swarm of autonomous agents. Your job is to interpret the user's mission statement into a multi-step plan for the agents to follow.
Each step should include the following:
    1. Objective: The goal of the step
    2. Action Function: The Python code to execute the step

The input to the action function should be as follows:
N = Number of agents
Objects = List of Object
bbox = [x1, y1, x2, y2] # Bounding box for the map

The output of the action function should be a list of (x, y) coordinates for the agents to move to.

Below is an example Object:
Object = {
    "type": "", # Barn, Building, Car, Tree, etc.
    "position": [x, y],
    "radius": r
}

Below is the Action Function Template:
def mission_action(N:int, Objects:List[Object], BBox:List[int]) -> List[Tuple[int, int]]:
    # Your action code here
    # Return a list of (x, y) coordinates, of length N, for the agents to move to

Make sure each step is a well defined python function with the above specified inputs and outputs. Each Python function should be a self-contained step that the agents can execute.
Python functions should not should not call other functions or rely on external state. Each function should be able to run independently.

"""

LLM_PLAN_REVIEWER_PROMPT = """
You are a mission plan reviewer for a swarm of autonomous agents. Your job is to interpret review the user's mission plan so that it meets the following criteria:
    1. Each step must include the following:
        - Objective: The goal of the step
        - Action Function: The Python code to execute the step
    2. The input to the action function must be as follows:
        - N = Number of agents
        - Objects = List of Object
        - bbox = [x1, y1, x2, y2] # Bounding box for the map
    3. The output of the action function must be a list of (x, y) coordinates for the agents to move to.
    4. Each step must be a well defined python function with the above specified inputs and outputs. 
    5. Each Python function must be a self-contained step that the agents can execute without external dependencies.

Correct the mission plan so that it meets the above criteria.
"""

# DEBUG: Example LLM reponse
# LLM Prompt: "Find and surround the barn."

# LLM Response: Step 1: Move towards the barn
# Objective: Move the agents towards the barn
# Action Function: 
# ```python
# def move_towards_barn(N:int, Objects:List[Object], BBox:List[int]) -> List[Tuple[int, int]]:
#     barn = [obj for obj in Objects if obj["type"]=="Barn"][0]
#     center_x = (BBox[0] + BBox[2]) / 2
#     center_y = (BBox[1] + BBox[3]) / 2
#     return [(barn["position"][0] + center_x) / 2, (barn["position"][1] + center_y) / 2] * N
# ```

# Step 2: Surround the barn
# Objective: Surround the barn by moving around it
# Action Function: 
# ```python
# def surround_barn(N:int, Objects:List[Object], BBox:List[int]) -> List[Tuple[int, int]]:
#     barn = [obj for obj in Objects if obj["type"]=="Barn"][0]
#     radius = barn["radius"] + 10  # Add a buffer distance to the barn radius
#     angle = 0
#     coordinates = []
#     for i in range(N):
#         x = barn["position"][0] + radius * math.cos(angle)
#         y = barn["position"][1] + radius * math.sin(angle)
#         coordinates.append((x, y))
#         angle += 2 * math.pi / N
#     return coordinates
# ```