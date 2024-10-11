import numpy as np

from ..lib.utils import get_gradient_at_position
from ..config import ENV_WIDTH, ENV_HEIGHT, MAX_SPEED, MAX_FORCE, RADIUS

class Agent:
    def __init__(self, agent_id, position, target_id, z_position=0):
        x, y = position[0], position[1]
        self.id = agent_id  # Unique identifier for the agent
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.random.uniform(-2, 2, 2)  # 2D vector for velocity
        self.acceleration = np.zeros(2, dtype=float)  # Initialize acceleration to zero
        self.target_id = target_id  # Swarm identifier
        self.z_position = z_position  # Separated for greater LLM control (similar to air traffic control altitude)
        self.role = None  # Role assigned to the agent

    def edges(self):
        """Keep the agents inside the environment boundaries."""
        if self.position[0] > ENV_WIDTH:
            self.position[0] = ENV_WIDTH
            self.velocity[0] = 0  # Stop horizontal movement
        elif self.position[0] < 0:
            self.position[0] = 0
            self.velocity[0] = 0
        
        if self.position[1] > ENV_HEIGHT:
            self.position[1] = ENV_HEIGHT
            self.velocity[1] = 0  # Stop vertical movement
        elif self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] = 0

    def apply_force(self, force):
        """Apply force (acceleration) to the agent."""
        self.acceleration += force

    def update(self):
        """Update agent position based on velocity and acceleration."""
        self.velocity += self.acceleration
        speed = np.linalg.norm(self.velocity)
        if speed > MAX_SPEED:
            self.velocity = (self.velocity / speed) * MAX_SPEED
        
        self.position += self.velocity
        self.acceleration *= 0  # Reset acceleration after each update

    def align(self, agents):
        """Calculate the alignment force."""
        steering = np.zeros(2, dtype=float)
        total = 0
        for agent in agents:
            if agent.target_id == self.target_id and np.linalg.norm(self.position - agent.position) < RADIUS:
                steering += agent.velocity
                total += 1
        if total > 0:
            steering /= total
            if np.linalg.norm(steering) > 0:  # Check if the vector is non-zero
                steering = (steering / np.linalg.norm(steering)) * MAX_SPEED
                steering -= self.velocity
                if np.linalg.norm(steering) > 0:
                    steering = (steering / np.linalg.norm(steering)) * min(np.linalg.norm(steering), MAX_FORCE)
        return steering

    def cohesion(self, agents):
        """Calculate the cohesion force."""
        steering = np.zeros(2, dtype=float)
        total = 0
        for agent in agents:
            if agent.target_id == self.target_id and np.linalg.norm(self.position - agent.position) < RADIUS:
                steering += agent.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            if np.linalg.norm(steering) > 0:  # Check if the vector is non-zero
                steering = (steering / np.linalg.norm(steering)) * MAX_SPEED
                steering -= self.velocity
                if np.linalg.norm(steering) > 0:
                    steering = (steering / np.linalg.norm(steering)) * min(np.linalg.norm(steering), MAX_FORCE)
        return steering

    def separation(self, agents):
        """Calculate the separation force."""
        steering = np.zeros(2, dtype=float)
        total = 0
        for agent in agents:
            distance = np.linalg.norm(self.position - agent.position)
            if agent.target_id == self.target_id and distance < RADIUS and distance > 0:
                diff = self.position - agent.position
                diff /= distance  # Weight by distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if np.linalg.norm(steering) > 0:  # Check if the vector is non-zero
                steering = (steering / np.linalg.norm(steering)) * MAX_SPEED
                steering -= self.velocity
                if np.linalg.norm(steering) > 0:
                    steering = (steering / np.linalg.norm(steering)) * min(np.linalg.norm(steering), MAX_FORCE)
        return steering

    def steer_towards_target(self, target):
        """Calculate the steering force towards a target with slowing down near the target."""
        desired = target.position - self.position
        distance = np.linalg.norm(desired)
        
        # If we're close enough to the target, slow down proportionally
        if distance < RADIUS:
            desired = (desired / distance) * (MAX_SPEED * (distance / RADIUS))  # Slow down as we approach the target
        else:
            desired = (desired / np.linalg.norm(desired)) * MAX_SPEED  # Move at full speed if far away

        steering = desired - self.velocity

        # Check if the steering vector is non-zero before normalizing
        if np.linalg.norm(steering) > 0:
            steering = (steering / np.linalg.norm(steering)) * min(np.linalg.norm(steering), MAX_FORCE)
        
        return steering
    
    def steer_away_from_obstacles(self, obstacles):
        """Calculate the steering force to avoid obstacles."""
        steering = np.zeros(2, dtype=float)
        total = 0
        for obstacle in obstacles:
            distance = np.linalg.norm(self.position - obstacle.position)
            if distance < RADIUS:
                diff = self.position - obstacle.position
                diff /= distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * MAX_SPEED
                steering -= self.velocity
                if np.linalg.norm(steering) > 0:
                    steering = (steering / np.linalg.norm(steering)) * min(np.linalg.norm(steering), MAX_FORCE)
        return steering
    
    def detect(self, object):
        """Check if the agent detected an object (e.g., target)."""
        distance = np.linalg.norm(self.position - object.position)
        return distance < RADIUS

    def flock(self, agents, target, obstacles, alignment_weight=1.0, cohesion_weight=1.0, separation_weight=1.25, target_weight=1.25, obstacle_weight=1.25, terrain_weight=0.1):
        """Calculate all forces (alignment, cohesion, separation) and apply them."""
        alignment = self.align(agents)
        cohesion = self.cohesion(agents)
        separation = self.separation(agents)

        # Steer towards the assigned target (based on the swarm)
        target_steering = self.steer_towards_target(target)

        # Avoid obstacles
        obstacle_steering = self.steer_away_from_obstacles(obstacles)

        # Calculate the terrain gradient and influence movement
        gradient = get_gradient_at_position(self.position[0], self.position[1])
        
        # Adjust velocity or position based on the slope of the terrain
        slope_factor = -0.1  # Negative slope for uphill movement
        terrain_steering = gradient * slope_factor

        # Weigh these forces to balance the behavior
        self.apply_force(alignment * alignment_weight)
        self.apply_force(cohesion * cohesion_weight)
        self.apply_force(separation * separation_weight)
        self.apply_force(target_steering * target_weight)
        self.apply_force(obstacle_steering * obstacle_weight)
        self.apply_force(terrain_steering * terrain_weight)
