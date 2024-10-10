// components/MissionInput.js
import { useState } from "react";

const MissionInput = ({ onMissionSubmit }) => {
  const [missionStatement, setMissionStatement] = useState("");
  const [responseMessage, setResponseMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!missionStatement.trim()) {
      setResponseMessage("Mission statement cannot be empty.");
      return;
    }

    setIsLoading(true);
    setResponseMessage(null); // Clear previous response message

    try {
      // Send the mission statement to the backend
      const response = await fetch("/api/py/mission-input", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_mission_statement: missionStatement }),
      });

      if (response.ok) {
        const result = await response.json();
        setResponseMessage(result.message); // Set the response message from the backend
        onMissionSubmit && onMissionSubmit(result.message); // Optional callback
      } else {
        setResponseMessage("Failed to send mission input.");
      }
    } catch (error) {
      console.error("Error:", error);
      setResponseMessage("An error occurred while submitting.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full p-4 bg-gray-800"> {/* Set to the same color as LogTerminal */}
      <label htmlFor="mission" className="block text-sm font-medium mb-1 text-gray-300"> {/* Lightened text for contrast */}
        Your Mission Statement:
      </label>
      <textarea
        id="mission"
        value={missionStatement}
        onChange={(e) => setMissionStatement(e.target.value)}
        placeholder="Enter your mission statement..."
        rows="4"
        className="w-full p-2 text-sm border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-gray-200" // Darker textarea for better contrast
      />
      <div className="mt-2">
        <button
          onClick={handleSubmit}
          disabled={isLoading}
          className={`w-full py-2 text-sm text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-all duration-200 ${
            isLoading ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          {isLoading ? "Submitting..." : "Send Mission Statement"}
        </button>
      </div>
      {responseMessage && (
        <p className="mt-2 text-center text-xs text-red-500">{responseMessage}</p>
      )}
    </div>
  );
};

export default MissionInput;
