import React from 'react';

const PlanStep = ({ step }) => {
  return (
    <div className="plan-step">
      <h4>Objective: {step.objective}</h4>
      <p>Status: {step.completed ? 'Completed' : 'Pending'}</p>
      <style jsx>{`
        .plan-step {
          border: 1px solid #ccc;
          padding: 10px;
          margin: 5px 0;
          border-radius: 5px;
          background-color: #f9f9f9;
        }
      `}</style>
    </div>
  );
};

export default PlanStep;
