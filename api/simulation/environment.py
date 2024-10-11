from .target import Target
from .obstacle import Obstacle
from .agent import Agent
import numpy as np

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