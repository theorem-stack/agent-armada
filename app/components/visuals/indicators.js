import * as THREE from 'three';

function attachIndicatorsToAgent(agent, config) {
    const indicators = new THREE.Group(); // Group to hold all indicators
    const { boundingBox, crosshair, detectionRadius } = config;

    // Position of the Agent (set once for all indicators)
    const position = agent.position.clone();

    // Bounding Box
    if (boundingBox) {
        const boxGeometry = new THREE.BoxGeometry(agent.size, agent.size, agent.size);
        const edges = new THREE.EdgesGeometry(boxGeometry);
        const boundingBoxHelper = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x00ff00 }));
        indicators.add(boundingBoxHelper);
    }

    // Crosshair
    if (crosshair) {
        const crosshairLength = 0.1;
        const crosshairMaterial = new THREE.LineBasicMaterial({ color: 0xff0000, depthWrite: false }); // Disable depth write

        // X-axis crosshair
        const crosshairX = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(-crosshairLength, 0, 0),
            new THREE.Vector3(crosshairLength, 0, 0)
        ]);
        const crosshairXLine = new THREE.Line(crosshairX, crosshairMaterial);

        // Y-axis crosshair
        const crosshairY = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(0, -crosshairLength, 0),
            new THREE.Vector3(0, crosshairLength, 0)
        ]);
        const crosshairYLine = new THREE.Line(crosshairY, crosshairMaterial);

        const crosshairGroup = new THREE.Group();
        crosshairGroup.add(crosshairXLine, crosshairYLine);
        crosshairGroup.position.set(0, 0, 1); // Move the crosshair group slightly forward
        indicators.add(crosshairGroup);
    }

    // Detection Radius// Detection Radius
    if (detectionRadius) {
        const detectionRadiusValue = agent.detectionRadius || 1.0; // Get the radius value

        // Create a group to hold the circle outline
        const detectionCircleGroup = new THREE.Group();

        // Create circle geometry points for the outline
        const circlePoints = [];
        const numSegments = 32; // Number of segments for the circle outline
        for (let i = 0; i <= numSegments; i++) {
            const angle = (i / numSegments) * Math.PI * 2; // Calculate angle
            const x = Math.cos(angle) * detectionRadiusValue; // X coordinate
            const y = Math.sin(angle) * detectionRadiusValue; // Y coordinate
            circlePoints.push(new THREE.Vector3(x, y, 0)); // Push to points array
        }

        // Create a geometry from the points
        const circleGeometry = new THREE.BufferGeometry().setFromPoints(circlePoints);
        
        // Create a LineBasicMaterial for the circle outline
        const circleMaterial = new THREE.LineBasicMaterial({ color: 0xffff00 }); // Solid color for the outline

        // Create the line (outline) from geometry and material
        const detectionCircleOutline = new THREE.Line(circleGeometry, circleMaterial);

        // Add the outline to the detection circle group
        detectionCircleGroup.add(detectionCircleOutline);

        // Add the detection circle group to indicators
        indicators.add(detectionCircleGroup); // Add group to the indicators
    }

    // Set the overall position of indicators group
    indicators.position.copy(position);
    
    // Return indicators group for attachment to the agent
    return indicators;
}

function updateAgentIndicators(agent) {
    const indicators = agent.indicators;

    // Update indicator group's position to match the agent's position
    indicators.position.copy(agent.position);

    // Update specific indicators like direction arrows and health bars
    indicators.children.forEach(indicator => {
        // Update direction arrow
        if (indicator instanceof THREE.ArrowHelper) {
            const directionVector = new THREE.Vector3(agent.velocity.x, agent.velocity.y, 0).normalize();
            indicator.setDirection(directionVector);  // Update direction
        }

        // Update health bar
        if (indicator.geometry instanceof THREE.PlaneGeometry && indicator.material.color.equals(new THREE.Color(0x00ff00))) {
            const healthPercent = agent.health / 100;
            indicator.scale.set(healthPercent, 1, 1);  // Update health bar width
            indicator.position.set(agent.position.x, agent.position.y + 1.2, 0); // Keep above the agent
            
            // Update health color based on percentage
            const barColor = new THREE.Color(0x00ff00).lerp(new THREE.Color(0xff0000), 1 - healthPercent); // Gradient
            indicator.material.color.set(barColor);
        }
    });
}

export { attachIndicatorsToAgent, updateAgentIndicators };
