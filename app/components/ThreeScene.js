"use client";

// components/ThreeScene.js
import { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import Agent from './Agent';
import Target from './Target';
import Obstacle from './Obstacle';
import { getColorBySwarmId, createRefinedHeightMapTexture, convertEnvPositionToThree, convertEnvRadiusToThree, createMapObjects, updateDetections } from '../lib/helpers';
import { TERRAIN_HEIGHT_MAP, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT, TERRAIN_MAP_SCALE } from '../data/globalVars';
import { attachIndicatorsToAgent, updateAgentIndicators } from './visuals/indicators';
import { useWebSocketData } from './WebSocketContext';

const ThreeScene = ({ mapName }) => {
    const rendererRef = useRef(null);
    const sceneRef = useRef(null);
    const cameraRef = useRef(null);
    const containerRef = useRef(null); // Ref for the container

    const agentsRef = useRef([]);
    const targetsRef = useRef([]);
    const obstaclesRef = useRef([]);

    const [mapData, setMap] = useState([]);
    const { agents, targets, obstacles, new_detections } = useWebSocketData();

    // Load the map data
    useEffect(() => {
        const fetchMapData = async () => {
            try {
                const response = await fetch(`/api/py/maps/${mapName}`);

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(`Error fetching map data: ${errorData.detail || response.statusText}`);
                }

                const data = await response.json();
                setMap(data);
            } catch (error) {
                console.error("Error fetching map data:", error);
            }
        };

        fetchMapData();
    }, [mapName]);

    // Initialize the WebGL renderer and scene
    useEffect(() => {
        const scene = new THREE.Scene();
        sceneRef.current = scene;

        // Set up an Orthographic camera
        const aspect = THREE_WIDTH / THREE_HEIGHT; // Use the THREE_WIDTH and THREE_HEIGHT
        const cameraSize = 4; // Adjust this value to control the zoom level
        const camera = new THREE.OrthographicCamera(
            -cameraSize * aspect,   // left
            cameraSize * aspect,    // right
            cameraSize,             // top
            -cameraSize,            // bottom
            0.1,                    // near
            1000                    // far
        );
        cameraRef.current = camera;

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        document.body.appendChild(renderer.domElement);
        rendererRef.current = renderer;

        const width = Math.ceil(window.innerWidth / THREE_WIDTH);
        const height = Math.ceil(window.innerHeight / THREE_HEIGHT);

        // Function to set the size of the renderer and camera
        const setSize = () => {
            const scalingFactor = Math.min(width, height);
            renderer.setSize(THREE_WIDTH * scalingFactor, THREE_HEIGHT * scalingFactor);
            camera.updateProjectionMatrix();
        };

        // Set the initial size
        setSize();

        // Handle window resize
        window.addEventListener('resize', setSize);

        // Append renderer to the container
        if (containerRef.current) {
            containerRef.current.appendChild(renderer.domElement);
        }

        // Position the camera
        camera.position.set(0, 0, 5); // Move the camera back
        camera.lookAt(0, 0, 0); // Look at the origin

        // Create a background plane with the height map texture
        const geometry = new THREE.PlaneGeometry(THREE_WIDTH, THREE_HEIGHT, 32, 32);

        const heightMapTexture = createRefinedHeightMapTexture(TERRAIN_HEIGHT_MAP, TERRAIN_MAP_SCALE, width, height);

        const material = new THREE.MeshStandardMaterial({
            map: heightMapTexture,
            transparent: true,
        });

        const backgroundPlane = new THREE.Mesh(geometry, material);
        backgroundPlane.rotation.x = -Math.PI * 2; // Rotate plane to lie flat on the x-y plane
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
        scene.add(borderGeometry);

        // Create high-level map objects from satellite data
        createMapObjects(mapData, scene);

        // Simple animation loop
        const animate = () => {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        };
        
        animate();

        // Cleanup function
        return () => {
            renderer.dispose(); // Dispose the renderer
            if (containerRef.current) {
                containerRef.current.removeChild(renderer.domElement); // Remove the renderer from the container
            }
        };

    }, [mapData]);

    // Update the scene with new WebSocket data
    useEffect(() => {
        if (sceneRef.current) {
            const scene = sceneRef.current;

            // Update or create targets based on WebSocket data
            Object.entries(targets).forEach(([id, targetData]) => {
                const { position, radius } = targetData;
                const pos = convertEnvPositionToThree(position, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT);
                let target = targetsRef.current.find(t => t.id === id);

                if (!target) {
                    target = new Target(
                        id,
                        pos,
                        convertEnvRadiusToThree(radius, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT),
                        getColorBySwarmId(id)
                    );
                    scene.add(target.mesh);
                    targetsRef.current.push(target);
                } else {
                    target.position.copy(pos);
                    target.updateMeshPosition();
                    target.updateColor(getColorBySwarmId(id));
                }
            });

            // Update or create obstacles based on WebSocket data
            Object.entries(obstacles).forEach(([id, obstacleData]) => {
                const { position, radius } = obstacleData;
                const pos = convertEnvPositionToThree(position, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT);
                let obstacle = obstaclesRef.current.find(o => o.id === id);

                if (!obstacle) {
                    obstacle = new Obstacle(
                        id,
                        pos,
                        convertEnvRadiusToThree(radius, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT),
                        getColorBySwarmId(id)
                    );
                    scene.add(obstacle.mesh);
                    obstaclesRef.current.push(obstacle);
                } else {
                    obstacle.position.copy(pos);
                    obstacle.updateMeshPosition();
                    obstacle.updateColor(getColorBySwarmId(id));
                }
            });

            // Update or create agents based on WebSocket data
            Object.entries(agents).forEach(([id, agentData]) => {
                const { target_id, position, z_position, velocity, acceleration } = agentData;
                const pos = convertEnvPositionToThree(position, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT);
                let agent = agentsRef.current.find(b => b.id === id);

                if (!agent) {
                    agent = new Agent(
                        id,
                        target_id,
                        pos,
                        z_position,
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
                    agent.indicators = indicators;

                    scene.add(agent.mesh); // Add the new Agent mesh to the scene
                    scene.add(indicators); // Add the indicator group to the scene
                    agentsRef.current.push(agent);
                } else {
                    agent.position.copy(pos);
                    agent.updateMeshPosition();
                    agent.updateColor(getColorBySwarmId(target_id));

                    // Update indicators
                    updateAgentIndicators(agent);
                }
            });

            // Handle new detections from WebSocket data
            if (new_detections && new_detections.length > 0) {
                updateDetections(scene, new_detections);
            }
        }
    }, [agents, targets, obstacles, new_detections]);

    return <div ref={containerRef} className="flex-grow"></div>; // Return a div to contain the renderer
};

export default ThreeScene;
