from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, BackgroundTasks, WebSocketDisconnect
import asyncio
import random

from .environment import create_targets_from_dict, create_agents_from_dict, create_obstacles_from_dict
from .maps import hurricane_map, national_park_map, small_town_map
from .dataProcessing import map_to_json, filter_objects_by_size
from .config import ENV_WIDTH, ENV_HEIGHT, NUM_TARGETS, NUM_OBSTACLES, NUM_BOIDS, TARGET_RADIUS, OBSTACLE_RADIUS, ALIGNMENT_WEIGHT, COHESION_WEIGHT, SEPARATION_WEIGHT, TARGET_WEIGHT, OBSTACLE_WEIGHT, TERRAIN_WEIGHT

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

# CORS to allow frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to hold the state of the simulation
agents_data = {}
targets_data = {}
obstacles_data = {}
agent_detections_data = {}

# Control the simulation state
simulation_running = False
simulation_task = None  # To keep track of the running simulation task

class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_data(self, message, websocket: WebSocket):
        """Direct Message"""
        await websocket.send_json(message)
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)

manager = ConnectionManager()

async def run_simulation():

    # Initialize Environment
    global agents_data
    global targets_data
    global obstacles_data
    global agent_detections_data

    # Detailed Exact Map (use for environment representation)
    hurricane_map_representation = map_to_json(hurricane_map)

    # Course Filtered Map (use as LLM input)
    satellite_hurricane_map = filter_objects_by_size(hurricane_map, min_size=10)
    satellite_hurricane_map_representation = map_to_json(satellite_hurricane_map)

    # LLM Process the map data to create dictionaries ---------------------

    targets_data = {}
    for target_id in range(NUM_TARGETS):
        targets_data[target_id] = {
            "position": [random.randint(0, ENV_WIDTH), random.randint(0, ENV_HEIGHT)],
            "radius": TARGET_RADIUS
        }

    obstacles_data = {}
    for obstacle_id in range(NUM_OBSTACLES):
        obstacles_data[obstacle_id] = {
            "position": [random.randint(0, ENV_WIDTH), random.randint(0, ENV_HEIGHT)],
            "radius": OBSTACLE_RADIUS
        }

    # Ids from the target dictionary
    target_ids = list(targets_data.keys())

    # Temporarily assign random swarm ids to agents.
    # In practice, the LLM will assign the swarm ids.
    agents_dict = { agent_id: {"target_id": random.choices(target_ids, k=1)[0], "position": [random.randint(0, ENV_WIDTH), random.randint(0, ENV_HEIGHT), 0]} for agent_id in range(NUM_BOIDS) }
        
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

# Start the background task on application startup
@app.on_event("startup")
async def startup_event():
    print("FastAPI server has started. Waiting for simulation start.")

# WebSocket endpoint for real-time updates
@app.websocket("/ws/agents")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        print("Connection Established")
        while True:
            # Your logic to send data to the client
            data = {
                "targets": targets_data,
                "obstacles": obstacles_data,
                "agents": agents_data,
                "agent_detections": agent_detections_data
            }

            await manager.send_data(data, websocket)
            await asyncio.sleep(0.01)  # Control how often you send data
    except WebSocketDisconnect:
        print("Connection Closed")
        manager.disconnect(websocket)

# Start the simulation on a button click
@app.post("/api/start_simulation")
async def start_simulation():
    global simulation_running, simulation_task
    if not simulation_running:
        simulation_running = True
        simulation_task = asyncio.create_task(run_simulation())  # Run the simulation in the background
        return {"status": "Simulation started"}
    else:
        return {"status": "Simulation is already running"}

# Stop the simulation on a button click
@app.post("/api/stop_simulation")
async def stop_simulation():
    global simulation_running, simulation_task
    if simulation_running:
        simulation_running = False
        if simulation_task:
            simulation_task.cancel()  # Cancel the running task if needed

            # Clear Global Variables
            agents_data.clear()
            targets_data.clear()
            obstacles_data.clear()
            
        return {"status": "Simulation stopped"}
    else:
        return {"status": "Simulation is not running"}
    
# Optional: API endpoint to get the current state of the simulation
@app.get("/api/agents")
async def get_agents():
    return agents_data