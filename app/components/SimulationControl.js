export default function SimulationControl({ status, setStatus }) {

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
            <button onClick={stopSimulation}>Stop Simulation</button>
            <p>{status}</p> {/* This will show the current status */}
        </div>
    );
}
