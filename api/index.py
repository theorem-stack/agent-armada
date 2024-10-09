from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from pydantic import BaseModel

from .connectionManager import ConnectionManager
from .simulationManager import run_simulation, agents_data, targets_data, obstacles_data, agent_detections_data, plan_progress
from .lib.dataProcessing import filter_objects_by_size
from .simulation.maps import hurricane_map
from .llm.llm import LLM_Planning
from .config import ENV_WIDTH, ENV_HEIGHT, NUM_AGENTS

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

# Control the simulation state
simulation_running = False
simulation_task = None  # To keep track of the running simulation task

manager = ConnectionManager()

class MissionInput(BaseModel):
    user_mission_statement: str

@app.post("/api/py/mission-input")
async def receive_mission_input(mission_input: MissionInput):
    print(f"Received mission: {mission_input.user_mission_statement}")

    # Process Satellite Map
    detailed_map = hurricane_map  # Detailed Exact Map (for environment representation)
    satellite_map_objects = filter_objects_by_size(hurricane_map, min_size=10)  # Filter for larger objects

    # Call the LLM Planning function
    mission_statement = mission_input.user_mission_statement
    N = NUM_AGENTS
    BBox = [0, 0, ENV_WIDTH, ENV_HEIGHT]
    
    try:
        # Get the LLM plan asynchronously
        llm_plan = await LLM_Planning(mission_statement, N, satellite_map_objects, BBox)
    except Exception as e:
        print(f"Error generating LLM plan: {e}")
        return {"status": "Error generating mission plan", "error": str(e)}

    if llm_plan:
        global simulation_running, simulation_task

        if not simulation_running:
            simulation_running = True
            # Pass the LLM plan to run_simulation and start the simulation asynchronously
            simulation_task = asyncio.create_task(run_simulation(llm_plan)) 
            return {"status": "Simulation started", "mission": mission_input.user_mission_statement}
        else:
            return {"status": "Simulation is already running", "mission": mission_input.user_mission_statement}
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
                "plan_progress": plan_progress
            }

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
            simulation_task.cancel()  # Cancel the running task if needed

            # Clear Global Variables
            agents_data.clear()
            targets_data.clear()
            obstacles_data.clear()
            
        return {"status": "Simulation stopped"}
    else:
        return {"status": "Simulation is not running"}
    
@app.get("/api/py/agents")
async def get_agents():
    return agents_data
