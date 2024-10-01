export default function SimulationControl({ status, setStatus }) {
    // Function to start the simulation
    const startSimulation = async () => {
        try {
            const response = await fetch('/api/py/start_simulation', {
                method: 'POST',
            });
            const data = await response.json();
            setStatus(data.status);  // Update the parent status
        } catch (error) {
            console.error("Error starting simulation:", error);
        }
    };

    // Function to stop the simulation
    const stopSimulation = async () => {
        try {
            const response = await fetch('/api/py/stop_simulation', {
                method: 'POST',
            });
            const data = await response.json();
            setStatus(data.status);  // Update the parent status
        } catch (error) {
            console.error("Error stopping simulation:", error);
        }
    };

    return (
        <div>
            <h2>Simulation Control</h2>
            <button onClick={startSimulation}>Start Simulation</button>
            <button onClick={stopSimulation}>Stop Simulation</button>
            <p>{status}</p> {/* This will show the current status */}
        </div>
    );
}
