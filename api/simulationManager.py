import asyncio
import random
import json

from .simulation.environment import create_targets_from_dict, create_agents_from_dict, create_obstacles_from_dict
from .config import ENV_WIDTH, ENV_HEIGHT, NUM_TARGETS, NUM_OBSTACLES, NUM_AGENTS, TARGET_RADIUS, OBSTACLE_RADIUS, ALIGNMENT_WEIGHT, COHESION_WEIGHT, SEPARATION_WEIGHT, TARGET_WEIGHT, OBSTACLE_WEIGHT, TERRAIN_WEIGHT

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
                "z_position": agent.z_position,  # For 3D simulations
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