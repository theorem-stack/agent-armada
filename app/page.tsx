"use client";

import Image from 'next/image'; // Import Image from next/image for optimized loading
import ThreeScene from './components/ThreeScene';
import MissionInput from './components/MissionInput';
import { WebSocketProvider } from './components/WebSocketContext';
import { PlanOverview } from './components/PlanOverview';
import { LogTerminal } from './components/LogTerminal';

export default function Home() {

  const handleMissionSubmit = (message: any) => {
    console.log("Mission Submitted:", message);
  };

  return (
    <WebSocketProvider>
      <div className="flex h-screen">
        {/* Sidebar */}
        <div className="w-2/4 bg-gray-800 p-4 space-y-4 border-r border-gray-300 flex flex-col">
          {/* Header Section */}
          <div className="bg-gray-700 flex items-center p-2 rounded-md mb-2"> {/* Reduced margin bottom to mb-2 */}
            <Image 
              src="/images/logo.jpg" // Path to your image
              alt="Project Logo"
              width={50} // Set the width of the image
              height={50} // Set the height of the image
              style={{ borderRadius: '8px' }} // Add border radius to the image
              className="mr-4" // Add margin to the right of the image
            />
            <h1 className="text-3xl font-bold text-gray-300">Agent Armada</h1>
          </div>
          {/* Content Below Header */}
          <PlanOverview />
          <MissionInput onMissionSubmit={handleMissionSubmit} />
          <LogTerminal />
        </div>

        {/* Main Three.js Scene */}
        <div className="flex-grow bg-gray-200">
          <ThreeScene mapName="hurricane_map" />
        </div>
      </div>
    </WebSocketProvider>
  );
}
