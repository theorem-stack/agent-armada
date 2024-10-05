"use client";

// components/ThreeScene.js
import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import Agent from './Agent';
import Target from './Target';
import Obstacle from './Obstacle';
import { getColorBySwarmId, createRefinedHeightMapTexture, convertEnvPositionToThree, convertEnvRadiusToThree } from '../lib/helpers';
import { TERRAIN_HEIGHT_MAP, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT } from '../data/globalVars';
import { attachIndicatorsToAgent, updateAgentIndicators } from './visuals/indicators';

const ThreeScene = () => {
    const agentsRef = useRef([]);
    const targetsRef = useRef([]);
    const obstaclesRef = useRef([]);
    const heightMapTexture = createRefinedHeightMapTexture(TERRAIN_HEIGHT_MAP, 8);

    useEffect(() => {
        // Create a basic Three.js scene
        const scene = new THREE.Scene();

        // Set up an Orthographic camera
        const aspect = window.innerWidth / window.innerHeight;
        const cameraSize = 4;  // Adjust this value to control the zoom level
        const camera = new THREE.OrthographicCamera(
            -cameraSize * aspect,   // left
            cameraSize * aspect,    // right
            cameraSize,             // top
            -cameraSize,            // bottom
            0.1,                    // near
            1000                    // far
        );

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Position the camera
        camera.position.set(0, 0, 5); // Camera is positioned at z=5
        camera.lookAt(0, 0, 0);       // Looking at the origin (center)

        // Create a background plane with the height map texture
        const geometry = new THREE.PlaneGeometry(THREE_WIDTH, THREE_HEIGHT, 32, 32);
        const material = new THREE.MeshStandardMaterial({
            map: heightMapTexture, // Use the height map as a texture
            transparent: true,
        });

        const backgroundPlane = new THREE.Mesh(geometry, material);
        backgroundPlane.rotation.x = -Math.PI * 2; // Rotate plane to lie flat
        backgroundPlane.position.y = 0; // Position it lower in the scene
        backgroundPlane.position.z = -1; // Push it back in the scene
        scene.add(backgroundPlane);

        // Lighting
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(0, 5, 5).normalize();
        scene.add(light);

        // Create border geometry
        const borderGeometry = new THREE.LineSegments(
            new THREE.EdgesGeometry(new THREE.BoxGeometry(THREE_WIDTH, THREE_HEIGHT, 0)),
            new THREE.LineBasicMaterial({ color: 0xff0000 }) // Red border color
        );
        scene.add(borderGeometry); // Add the border to the scene

        // --------------------------------------------------------------

        // WebSocket connection
        const socket = new WebSocket('ws://localhost:8000/ws/agents');

        socket.onopen = () => {
            console.log('WebSocket connection established');
            // Send a test message (optional)
            socket.send('Hello from the client!');
        };

        socket.onmessage = (event) => {

            const data = JSON.parse(event.data);

            const targetsData = data.targets;
            const obstaclesData = data.obstacles;
            const agentsData = data.agents;
            // const detectionData = data.agent_detections;

            // console.log('Received agents data:', agentsData);
            // console.log('Received targets data:', targetsData);
            // console.log('Received obstacles data:', obstaclesData);

            // Create or update targets
            Object.entries(targetsData).forEach(([id, targetData]) => {
                const {
                    position,
                    radius
                } = targetData;

                const pos = convertEnvPositionToThree(position, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT);

                // Find existing Agent by id
                let target = targetsRef.current.find(t => t.id === id);

                if (!target) {
                    // Create a new Agent if it doesn't exist
                    target = new Target(
                        id,
                        pos,
                        convertEnvRadiusToThree(radius, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT),
                        getColorBySwarmId(id)
                    );
                    scene.add(target.mesh);
                    targetsRef.current.push(target);
                } else {
                    // Update the existing Agent's position
                    target.position.copy(pos);
                    target.updateMeshPosition();
                    target.updateColor(getColorBySwarmId(id));
                }
            });

            // Create or update obstacles
            Object.entries(obstaclesData).forEach(([id, obstacleData]) => {
                const {
                    position,
                    radius
                } = obstacleData;

                const pos = convertEnvPositionToThree(position, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT);

                // Find existing Agent by id
                let obstacle = obstaclesRef.current.find(o => o.id === id);

                if (!obstacle) {
                    // Create a new Agent if it doesn't exist
                    obstacle = new Obstacle(
                        id,
                        pos,
                        convertEnvRadiusToThree(radius, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT),
                        getColorBySwarmId(getColorBySwarmId(id))
                    );
                    scene.add(obstacle.mesh);
                    obstaclesRef.current.push(obstacle);
                } else {
                    // Update the existing Agent's position
                    obstacle.position.copy(pos);
                    obstacle.updateMeshPosition();
                    obstacle.updateColor(getColorBySwarmId(id));
                }
            });

            // Create or update agents
            Object.entries(agentsData).forEach(([id, agentData]) => {
                const {
                    target_id,
                    position,
                    z_positon,
                    velocity,
                    acceleration
                } = agentData;

                const pos = convertEnvPositionToThree(position, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT);

                // Find existing Agent by id
                let agent = agentsRef.current.find(b => b.id === id);

                if (!agent) {
                    // Create a new Agent if it doesn't exist
                    agent = new Agent(
                        id,
                        target_id,
                        pos,
                        z_positon,
                        velocity,
                        acceleration,
                        getColorBySwarmId(target_id)
                    );

                    // Attach indicators to the new Agent
                    const indicators = attachIndicatorsToAgent(agent, {
                        boundingBox: true,
                        crosshair: false,
                        detectionRadius: false,
                    });
                    agent.indicators = indicators; // Attach indicators to the Agent object

                    scene.add(agent.mesh); // Add the new Agent mesh to the scene
                    scene.add(indicators); // Add the indicator group to the scene
                    agentsRef.current.push(agent); // Add the new Agent to the ref
                } else {
                    // Update the existing Agent's position
                    agent.position.copy(pos);
                    agent.updateMeshPosition();
                    agent.updateColor(getColorBySwarmId(target_id));

                    // Update indicators
                    updateAgentIndicators(agent);
                }
            });
        };

        socket.onclose = (event) => {
        console.log('WebSocket connection closed:', event);
        };

        socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        };

        // Simple animation loop (just to keep the scene active)
        const animate = () => {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        };
        
        animate();

        return () => {
            // Cleanup
            socket.close(); // Close WebSocket connection
            renderer.dispose();
            document.body.removeChild(renderer.domElement);
        };

    }, []); // Ensure this is an empty dependency array

    return null; // No JSX to render
};

export default ThreeScene;
