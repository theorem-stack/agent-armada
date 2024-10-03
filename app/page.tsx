"use client";

// pages/index.js
import { useState } from 'react';
import ThreeScene from './components/ThreeScene';
import SimulationControl from './components/SimulationControl';

export default function Home() {

  const [status, setStatus] = useState('Simulation not running');

  return (
    
    <div>
      <main>
        <h1>Multi-Agent Swarm Demo</h1>
        <ThreeScene />
        <SimulationControl status={status} setStatus={setStatus} />
      </main>
    </div>
  );
}
