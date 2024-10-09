import asyncio
import random
import json
from pathlib import Path

from .simulation.environment import create_targets_from_dict, create_agents_from_dict, create_obstacles_from_dict
from .config import ENV_WIDTH, ENV_HEIGHT, NUM_TARGETS, NUM_OBSTACLES, NUM_AGENTS, TARGET_RADIUS, OBSTACLE_RADIUS, ALIGNMENT_WEIGHT, COHESION_WEIGHT, SEPARATION_WEIGHT, TARGET_WEIGHT, OBSTACLE_WEIGHT, TERRAIN_WEIGHT, EVAL_TOLERANCE
from .lib.utils import evaluate_coordinates

from .config import BASE_DIR

# Global variable to hold the state of the simulation
agents_data = {}
targets_data = {}
obstacles_data = {}
agent_detections_data = {}

async def run_simulation():

    # Initialize Environment
    global agents_data
    global targets_data
    global obstacles_data
    global agent_detections_data

    # Define the path to the folder where JSON files are stored
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "simulation"

    # ------------------------------------------------
    # THIS SECTION IS TEMPORARY AND WILL BE REMOVED

    # DEBUG: Randomly assign target and obstacle positions
    for target_id in range(NUM_TARGETS):
        targets_data[target_id] = {
            "position": [random.randint(0, ENV_WIDTH), random.randint(0, ENV_HEIGHT)],
            "radius": TARGET_RADIUS
        }

    for obstacle_id in range(NUM_OBSTACLES):
        obstacles_data[obstacle_id] = {
            "position": [random.randint(0, ENV_WIDTH), random.randint(0, ENV_HEIGHT)],
            "radius": OBSTACLE_RADIUS
        }

    # DEBUG: Randomly assign agent initial positions and targets
    target_ids = list(range(NUM_TARGETS))
    agents_dict = { agent_id: {"target_id": random.choices(target_ids, k=1)[0], "position": [random.randint(0, ENV_WIDTH), random.randint(0, ENV_HEIGHT), 0]} for agent_id in range(NUM_AGENTS) }
        
    # ------------------------------------------------

    # Define objects
    targets = create_targets_from_dict(targets_data)
    obstacles = create_obstacles_from_dict(obstacles_data)
    agents = create_agents_from_dict(agents_dict)

    # Read the LLM plan from json file
    file_path = BASE_DIR / "simulation/llm_plan.json"
    with open(file_path, 'r') as f:
        llm_plan = json.load(f)

    # Main simulation loop
    running = True

    # Variables to track the current step
    current_step = 1
    step_completed = True

    update_frequency = 100
    update_counter = 0

    while running:

        # # Step through the LLM plan
        # if step_completed:
        #     step_data = llm_plan[str(current_step)]

        #     # Update the targets
        #     targets_data.clear()
        #     coords = step_data["coordinates"]
        #     for i in range(len(coords)):
        #         targets_data[i] = {
        #             "position": coords[i],
        #             "radius": TARGET_RADIUS
        #         }

        #     # Define target objects
        #     targets = create_targets_from_dict(targets_data)

        #     # Update Agents with new targets
        #     coords = step_data["coordinates"]
        #     for i in range(len(coords)):
        #         agents[i].target_id = i

        #     current_step += 1
        #     step_completed = False

        # Clear previous agents data
        agents_data.clear()

        for agent in agents:
            agent.edges()  # Handle screen wrapping
            agent.flock(agents, targets[agent.target_id], obstacles, 
                    ALIGNMENT_WEIGHT,
                    COHESION_WEIGHT,
                    SEPARATION_WEIGHT,
                    TARGET_WEIGHT,
                    OBSTACLE_WEIGHT,
                    TERRAIN_WEIGHT,
                )
            
            # Update agent position based on velocity
            agent.update()

            # Append the agent's ID and position to the agents_data
            agents_data[agent.id] = {
                "target_id": agent.target_id, # Swarm identifier
                "position": agent.position.copy().tolist(),  # Convert numpy array to list
                "z_positon": agent.z_position,  # For 3D simulations
                "velocity": agent.velocity.tolist(),  # 2D vector for velocity
                "acceleration": agent.acceleration.tolist(),  # Initialize acceleration to zero
            }

            # DEBUG: THIS IS A TEMPORARY IMPLEMENTATION should be map objects
            if agent.detect(targets[agent.target_id]):
                agent_detections_data[agent.target_id] = {
                    "position": targets[agent.target_id].position.copy().tolist(),
                }

        # Evaluate agent positions
        # if update_frequency % update_counter == 0:
        #     agent_positions = [agent.position for agent in agents]
        #     step_completed = evaluate_coordinates(step_data["coordinates"], agent_positions, EVAL_TOLERANCE)

        # update_counter += 1

        await asyncio.sleep(0.01)  # Control the update frequency