"use client";

// pages/index.js
import { useState } from 'react';
import ThreeScene from './components/ThreeScene';
import SimulationControl from './components/SimulationControl';
import MissionInput from './components/MissionInput';

export default function Home() {

  const [status, setStatus] = useState('Simulation not running');

  const handleMissionSubmit = (message: any) => {
    console.log("Mission Submitted:", message);
  };

  return (
    
    <div>
      <main>
        <h1>Multi-Agent Swarm Demo</h1>
        <ThreeScene />
        <SimulationControl status={status} setStatus={setStatus} />
        <MissionInput onMissionSubmit={handleMissionSubmit} />
      </main>
    </div>
  );
}
