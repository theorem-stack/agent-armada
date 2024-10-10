// components/LogTerminal.js
import React, { useState, useEffect } from 'react';
import { useWebSocketData } from './WebSocketContext';

export const LogTerminal = () => {
  const [logs, setLogs] = useState(new Map()); // Initialize logs as a Map
  const { agent_detections } = useWebSocketData();

  useEffect(() => {
    // Check if agent_detections is defined and is an object
    if (agent_detections && typeof agent_detections === 'object') {
      Object.entries(agent_detections).forEach(([agentId, objectName]) => {
        // Check if the log already contains this agentId
        if (!logs.has(agentId)) {
          // If not, add the new entry to the logs
          setLogs(prevLogs => new Map(prevLogs).set(agentId, objectName));
        }
      });
    }
  }, [agent_detections, logs]);

  return (
    <div className="log-terminal bg-gray-900 text-white h-48 overflow-y-auto p-0 border-t border-gray-700">
      <h3 className="font-bold text-yellow-400 text-sm mb-0 bg-gray-900 p-2 sticky top-0 z-10">
        System Log
      </h3>
      <ul className="space-y-1 text-xs p-2">
        {[...logs.entries()].map(([agentId, objectName], index) => (
          <li key={index}>{`Agent ID: ${agentId} detected the object: ${objectName}`}</li>
        ))}
      </ul>
      <style jsx>{`
        .log-terminal {
          font-family: 'Courier New', Courier, monospace;
        }
      `}</style>
    </div>
  );
};
