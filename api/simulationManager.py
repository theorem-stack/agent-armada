import asyncio
import random

from .simulation.environment import create_targets_from_dict, create_agents_from_dict, create_obstacles_from_dict
from .config import ENV_WIDTH, ENV_HEIGHT, NUM_AGENTS, TARGET_RADIUS, ALIGNMENT_WEIGHT, COHESION_WEIGHT, SEPARATION_WEIGHT, TARGET_WEIGHT, OBSTACLE_WEIGHT, TERRAIN_WEIGHT, EVAL_TOLERANCE
from .lib.utils import evaluate_coordinates
from .simulation.mapObject import mapObject

# Global variable to hold the state of the simulation
agents_data = {}
targets_data = {}
obstacles_data = {}
agent_detections_data = {}
plan_progress = {}
new_detections = []

async def run_simulation(llm_plan: dict, map: list[mapObject], existing_agent_data: dict):

    # Initialize Environment
    global agents_data, targets_data, obstacles_data, agent_detections_data, targets, agents, new_detections

    # Initialize the agents at random positions
    if existing_agent_data:
        agents_dict = existing_agent_data.copy()
    else:
        agents_dict = { agent_id: {"target_id": agent_id, "position": [random.randint(0, ENV_WIDTH), random.randint(0, ENV_HEIGHT)]} for agent_id in range(NUM_AGENTS) }
    
    agents = create_agents_from_dict(agents_dict)

    targets = []
    obstacles = []
    target_positions = []

    running = True
    step_completed = True
    current_step = 1

    loop_counter = 0
    eval_interval = 50  # Number of steps before evaluating the agent positions
    agent_detection_eval_interval = 10  # Number of steps before evaluating agent detections

    # Get each step and the objective from the LLM plan
    for step in llm_plan:
        plan_progress[step] = {
            "objective": llm_plan[step]["objective"],
            "completed": False
        }

    # Main simulation loop
    while running:

        # Increment the loop counter
        loop_counter += 1

        # Check if we should move to the next step
        if step_completed and llm_plan:
            step_data = llm_plan.get(current_step)

            if step_data:
                # Update the targets and agents
                targets_data, targets = update_targets_from_llm(step_data)
                target_positions = [target.position for target in targets.values()]

                # future feature: high level obstacles to be set by LLM

                agents = update_agents_from_llm(step_data, agents)

                current_step += 1
                step_completed = False

        # Clear agent status data and new detections
        agents_data.clear()
        new_detections.clear()

        if agents:
            for agent in agents:
                agent.edges()
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

                # Agent status data
                agents_data[agent.id] = {
                    "target_id": agent.target_id,                # Swarm identifier
                    "position": agent.position.copy().tolist(),  # Convert numpy array to list
                    "z_positon": agent.z_position,               # For 3D simulations
                    "velocity": agent.velocity.tolist(),         # 2D vector for velocity
                    "acceleration": agent.acceleration.tolist(), # Initialize acceleration to zero
                }

                # Agent detections
                if loop_counter % agent_detection_eval_interval == 0:
                    for object in map:
                        if agent.detect(object):
                            agent_detections_data[agent.id] = object.name

                            if not object.detected:
                                object.detected = True  # Set detection flag

                                # Add to newly detected
                                obj_dict = object.convert_to_dict()
                                new_detections.append(obj_dict)

            # Check if all agents have reached their targets
            if loop_counter % eval_interval == 0 and step in llm_plan:
                agent_positions = [agent.position for agent in agents]
                step_completed = evaluate_coordinates(agent_positions, target_positions, EVAL_TOLERANCE)
                plan_progress[current_step - 1]["completed"] = step_completed

                # print(f"Step {current_step - 1} completed: {step_completed}")

            await asyncio.sleep(0.01)  # Control the update frequency

def update_targets_from_llm(step_data):
    """Update targets based on the current step of the LLM plan."""
    coords = step_data["coordinates"]

    targets_data = {}
    for i, coord in enumerate(coords):
        targets_data[i] = {
            "position": coord,
            "radius": TARGET_RADIUS
        }
    
    # Recreate the target objects with new data
    targets = create_targets_from_dict(targets_data)

    return targets_data, targets

def update_agents_from_llm(step_data, agents):
    """Update agents with new target assignments from the LLM plan."""
    coords = step_data["coordinates"]
    
    for i, coord in enumerate(coords):
        agents[i].target_id = i

    return agents
