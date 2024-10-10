from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from pydantic import BaseModel
from typing import List

from .connectionManager import ConnectionManager
from .simulationManager import run_simulation, agents_data, targets_data, obstacles_data, agent_detections_data, plan_progress, new_detections
from .lib.dataProcessing import detected_objects_filter, update_map_detections
from .simulation.maps import maps
from .llm.llm import LLM_Planning
from .config import ENV_WIDTH, ENV_HEIGHT, NUM_AGENTS, DETECT_FILTER_SIZE

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

class MissionInput(BaseModel):
    user_mission_statement: str

class MapResponse(BaseModel):
    name: str
    position: List[float]
    boundingBox: tuple
    object_type: str
    condition: str = None
    properties: dict = None
    detected: bool = False

# Global variables
simulation_running = False
simulation_task = None
map = None
existing_agent_data = None

manager = ConnectionManager()

@app.on_event("startup")
async def initialize_global_vars():
    global simulation_running, simulation_task, map, existing_agent_data
    # You can initialize or reset any global variables here, if needed.
    simulation_running = False
    simulation_task = None
    map = None
    existing_agent_data = None

@app.get("/api/py/maps/{map_name}", response_model=List[MapResponse])
async def get_map(map_name: str):
    """Get the map data by name."""
    global map
    if map_name in maps:
        detailed_map = maps[map_name]  # Detailed Exact Map
        map = detected_objects_filter(detailed_map, min_size=DETECT_FILTER_SIZE)  # Detect large objects with satellite
        
        return map
    else:
        return {"status": "Failed to get map data", "error": "Map not found"}

@app.post("/api/py/mission-input")
async def receive_mission_input(mission_input: MissionInput):
    global simulation_running, simulation_task, map, existing_agent_data
    # Stop and reset the simulation if it's already running
    if simulation_running:
        await stop_simulation()  # Ensure the current simulation is stopped before proceeding

    # Call the LLM Planning function
    mission_statement = mission_input.user_mission_statement
    N = NUM_AGENTS
    BBox = [0, 0, ENV_WIDTH, ENV_HEIGHT]

    try:
        # Create context based on detected objects
        llm_map_context = [map_obj for map_obj in map if map_obj.detected == True]

        # Get the LLM plan asynchronously
        llm_plan = await LLM_Planning(mission_statement, N, llm_map_context, BBox)
    except Exception as e:
        print(f"Error generating LLM plan: {e}")
        return {"status": "Error generating mission plan", "error": str(e)}

    if llm_plan:
        simulation_running = True
        # Pass the LLM plan to run_simulation and start the simulation asynchronously
        simulation_task = asyncio.create_task(run_simulation(llm_plan, map, existing_agent_data)) 
        return {"status": "Simulation started", "mission": mission_input.user_mission_statement}
    else:
        # Return an error if the LLM plan could not be generated
        return {"status": "Failed to generate mission plan"}

# Start the background task on application startup
@app.on_event("startup")
async def startup_event():
    print("FastAPI server has started. Waiting for simulation start.")

# WebSocket endpoint for real-time updates
@app.websocket("/ws/agents")
async def websocket_endpoint(websocket: WebSocket):
    global map, existing_agent_data
    await manager.connect(websocket)
    try:
        print("Connection Established")
        while True:

            # Logic to send data to the client
            data = {
                "targets": targets_data,
                "obstacles": obstacles_data,
                "agents": agents_data,
                "agent_detections": agent_detections_data,
                "plan_progress": plan_progress,
                "new_detections": new_detections
            }

            # Update map for LLM recursive context and sequential user mission statements
            if new_detections and map:
                map = update_map_detections(map, new_detections)

            # Save agent data for sequential user mission statements
            if agents_data:
                existing_agent_data = agents_data.copy()

            await manager.send_data(data, websocket)
            await asyncio.sleep(0.01)  # Control how often you send data
    except WebSocketDisconnect:
        print("Connection Closed")
        manager.disconnect(websocket)

# Stop the simulation on a button click
@app.post("/api/py/stop_simulation")
async def stop_simulation():
    global simulation_running, simulation_task
    if simulation_running:
        simulation_running = False
        if simulation_task:
            simulation_task.cancel()  # Cancel the running task if it's active

        # Clear Global Variables to reset the environment
        agents_data.clear()
        targets_data.clear()
        obstacles_data.clear()
        agent_detections_data.clear()
        plan_progress.clear()

        return {"status": "Simulation stopped and reset"}
    else:
        return {"status": "Simulation is not running"}
