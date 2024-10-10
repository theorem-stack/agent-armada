// context/WebSocketContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const WebSocketContext = createContext();

export const WebSocketProvider = ({ children }) => {
    const [data, setData] = useState({ agents: {}, targets: {}, obstacles: {} });

    // Create the WebSocket connection and manage incoming messages
    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws/agents');

        socket.onmessage = (event) => {
            const messageData = JSON.parse(event.data);
            setData(messageData);
        };

        return () => {
            socket.close();
        };
    }, []);

    return (
        <WebSocketContext.Provider value={data}>
            {children}
        </WebSocketContext.Provider>
    );
};

export const useWebSocketData = () => useContext(WebSocketContext);
