// components/PlanOverview.js
import React from 'react';
import { useWebSocketData } from './WebSocketContext';

export const PlanOverview = () => {
  const { plan_progress } = useWebSocketData();

  // Convert plan_progress (object) into an array to iterate over
  const planSteps = plan_progress ? Object.entries(plan_progress) : [];

  if (!planSteps.length) {
    return <p className="text-gray-500 text-center text-sm">Waiting for plan updates...</p>;
  }

  return (
    <div className="plan-overview w-full p-4 bg-gray-800 border border-gray-600 rounded-md h-64 overflow-y-auto">
      <label htmlFor="plan-overview" className="block text-sm font-medium mb-1 text-gray-300">
        System Plan Overview
      </label>
      <div className="space-y-2">
        {planSteps.map(([step, data], index) => (
          <div
            key={index}
            className="flex justify-between items-center p-2 border-b border-gray-700 last:border-b-0"
          >
            <div className="flex-grow">
              <h4 className="text-sm font-semibold text-gray-200">Step {index + 1}</h4>
              <p className="text-gray-400 text-xs"><strong>Objective:</strong> {data.objective}</p>
            </div>
            <span
              className={`px-2 py-1 rounded-full font-semibold text-xs 
                ${data.completed ? 'bg-green-600 text-white' : 'bg-blue-600 text-white'}`}
            >
              {data.completed ? 'Completed' : 'Pending'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
