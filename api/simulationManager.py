import asyncio
import random

from .simulation.environment import create_targets_from_dict, create_agents_from_dict, create_obstacles_from_dict
from .lib.dataProcessing import map_to_json, filter_objects_by_size
from .simulation.maps import hurricane_map
from .llm import LLM
from .translator import translate

from .config import ENV_WIDTH, ENV_HEIGHT, NUM_TARGETS, NUM_OBSTACLES, NUM_AGENTS, TARGET_RADIUS, OBSTACLE_RADIUS, ALIGNMENT_WEIGHT, COHESION_WEIGHT, SEPARATION_WEIGHT, TARGET_WEIGHT, OBSTACLE_WEIGHT, TERRAIN_WEIGHT

# Global variable to hold the state of the simulation
agents_data = {}
targets_data = {}
obstacles_data = {}
agent_detections_data = {}

async def run_simulation(user_mission_statement):

    # Initialize Environment
    global agents_data
    global targets_data
    global obstacles_data
    global agent_detections_data

    # # Detailed Exact Map (use for environment representation)
    # hurricane_map_representation = map_to_json(hurricane_map)

    # # Course Filtered Map (use as LLM input. Leaves out small objects to be found by agents)
    # satellite_hurricane_map_objects = filter_objects_by_size(hurricane_map, min_size=10)

    # # LLM Planning ---------------------
    # # LLM generates a plan based on the user input
    # # The plan is a sequence of actions that the agents will execute
    # # Each action is represented as a python function, which outputs numerical values for the agents to follow
    # actions = LLM(user_mission_statement, "user_input")

    # # Execute the LLM plan ---------------------
    # targets = []
    # for action in actions:
    #     translation = translate(action)
    #     targets.append(translation)

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

    # DEBUG: Temporarily assign random swarm ids to agents.
    # In practice, the LLM will assign the swarm ids.
    target_ids = list(targets_data.keys())
    agents_dict = { agent_id: {"target_id": random.choices(target_ids, k=1)[0], "position": [random.randint(0, ENV_WIDTH), random.randint(0, ENV_HEIGHT), 0]} for agent_id in range(NUM_AGENTS) }
        
    # ------------------------------------------------

    # Define targets
    targets = create_targets_from_dict(targets_data)

    # Define obstacles
    obstacles = create_obstacles_from_dict(obstacles_data)

    # Create agent flock and assign them to swarms
    agents = create_agents_from_dict(agents_dict)

    # Main simulation loop
    running = True

    while running:

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

            # Update agent detections
            # DEBUG: THIS IS A TEMPORARY IMPLEMENTATION should be map objects
            if agent.detect(targets[agent.target_id]):
                agent_detections_data[agent.target_id] = {
                    "position": targets[agent.target_id].position.copy().tolist(),
                }

        await asyncio.sleep(0.01)  # Control the update frequency