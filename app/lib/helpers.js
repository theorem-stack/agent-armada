import * as THREE from 'three';
import { ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT } from '../data/globalVars';


// Utility function to generate colors based on swarm_id
function getColorBySwarmId(swarm_id) {
    const colors = {
        0: 0xff0000, // Red
        1: 0x00ff00, // Green
        2: 0x0000ff, // Blue
        3: 0xffff00, // Yellow
        4: 0xff00ff, // Magenta
        5: 0x00ffff, // Cyan
        // More colors can be added here...
    };
    // Default color if swarm_id is not found
    return colors[swarm_id] || 0xffffff; // Default to white
}

const createRefinedHeightMapTexture = (heightMap, scaleFactor) => {
    const originalWidth = heightMap[0].length;
    const originalHeight = heightMap.length;

    // Calculate new dimensions based on the scale factor
    const width = originalWidth * scaleFactor;
    const height = originalHeight * scaleFactor;

    // Initialize a new array for the refined height map
    const refinedHeightMap = new Array(height);
    for (let y = 0; y < height; y++) {
        refinedHeightMap[y] = new Array(width);
    }

    // Fill the refined height map with interpolated values
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            // Calculate the corresponding coordinates in the original height map
            const srcX = x / scaleFactor;
            const srcY = y / scaleFactor;

            const x0 = Math.floor(srcX);
            const x1 = Math.min(x0 + 1, originalWidth - 1);
            const y0 = Math.floor(srcY);
            const y1 = Math.min(y0 + 1, originalHeight - 1);

            // Get the heights at the corners
            const q11 = heightMap[y0][x0];
            const q12 = heightMap[y1][x0];
            const q21 = heightMap[y0][x1];
            const q22 = heightMap[y1][x1];

            // Bilinear interpolation
            const fX1 = q11 * (x1 - srcX) + q21 * (srcX - x0);
            const fX2 = q12 * (x1 - srcX) + q22 * (srcX - x0);
            refinedHeightMap[y][x] = fX1 * (y1 - srcY) + fX2 * (srcY - y0);
        }
    }

    // Now we will create the texture using the refined height map
    const data = new Uint8Array(width * height * 4); // RGBA format

    // Find min and max heights in the refined height map for normalization
    let max_height = -Infinity;
    let min_height = Infinity;

    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const value = refinedHeightMap[y][x];
            if (value > max_height) max_height = value;
            if (value < min_height) min_height = value;
        }
    }

    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const value = refinedHeightMap[y][x];

            // Normalize the height to a range of [0, 1]
            const normalizedHeight = (value - min_height) / (max_height - min_height);

            // Invert the normalized value to create a black-to-white gradient
            const colorValue = Math.round(255 * (1 - normalizedHeight)); // 255 is white, 0 is black

            const index = (x + y * width) * 4;
            data[index] = colorValue;       // R channel
            data[index + 1] = colorValue;   // G channel
            data[index + 2] = colorValue;   // B channel
            data[index + 3] = 255;          // Alpha channel (fully opaque)
        }
    }

    const texture = new THREE.DataTexture(data, width, height, THREE.RGBAFormat);
    texture.needsUpdate = true;
    return texture;
};

function convertEnvPositionToThree(position, envWidth, envHeight, threeWidth, threeHeight) {
    // Calculate aspect ratios for both Env (simulation) and Three.js environments
    const aspectRatioEnv = envWidth / envHeight;
    const aspectRatioThree = threeWidth / threeHeight;

    // Determine scale factors based on aspect ratios
    let scaleX, scaleY;
    
    if (aspectRatioEnv > aspectRatioThree) {
        // If simulation has a wider aspect ratio, scale based on width
        scaleX = threeWidth / envWidth;
        scaleY = scaleX; // Maintain uniform scaling
    } else {
        // If simulation has a taller aspect ratio, scale based on height
        scaleY = threeHeight / envHeight;
        scaleX = scaleY; // Maintain uniform scaling
    }

    // Convert the X and Y coordinates
    const x = (position[0] - envWidth / 2) * scaleX;
    const y = (position[1] - envHeight / 2) * scaleY;

    // Return as Three.js Vector3 (assuming Z = 0 for 2D)
    return new THREE.Vector3(x, y, 0);
}

function convertEnvRadiusToThree(envRadius, envWidth, envHeight, threeWidth, threeHeight) {
    // Calculate aspect ratios for both Env (simulation) and Three.js environments
    const aspectRatioEnv = envWidth / envHeight;
    const aspectRatioThree = threeWidth / threeHeight;

    // Determine scale factors based on aspect ratios
    let scale;
    
    if (aspectRatioEnv > aspectRatioThree) {
        // If the simulation has a wider aspect ratio, scale based on width
        scale = threeWidth / envWidth;
    } else {
        // If the simulation has a taller aspect ratio, scale based on height
        scale = threeHeight / envHeight;
    }

    // Convert the radius using the same scale factor
    const adjustedRadius = envRadius * scale;

    return adjustedRadius;
}

function createMapObjects(mapObjects, scene) {
    mapObjects.forEach((mapObject) => {
        const { name, position, boundingBox, object_type, condition, properties } = mapObject;

        // Convert position to Three.js coordinates
        const threePosition = convertEnvPositionToThree(position, ENV_WIDTH, ENV_HEIGHT, THREE_WIDTH, THREE_HEIGHT);

        // Bounding box dimensions
        const [[BL_x, BL_y], [TR_x, TR_y]] = boundingBox;
        const width = TR_x - BL_x;
        const height = TR_y - BL_y;

        // Scale the bounding box to Three.js coordinates
        const scaledWidth = (width * THREE_WIDTH) / ENV_WIDTH;
        const scaledHeight = (height * THREE_HEIGHT) / ENV_HEIGHT;

        let geometry, material, mesh;

        // Define geometry and material based on object type
        switch (object_type) {
            case "building":
                geometry = new THREE.BoxGeometry(scaledWidth, scaledHeight, 1); // Height can be adjusted as needed
                material = new THREE.MeshStandardMaterial({
                    color: condition === 'damaged' ? 0xff0000 : 0x00ff00 // Red for damaged, green for intact
                });
                break;

            case "flood":
                geometry = new THREE.PlaneGeometry(scaledWidth, scaledHeight);
                material = new THREE.MeshStandardMaterial({
                    color: 0x0000ff,
                    transparent: true,
                    opacity: 0.5 // Blue for water
                });
                mesh = new THREE.Mesh(geometry, material);
                mesh.position.set(0, 0, -1); // Slightly below the origin
                break;

            case "tree":
                geometry = new THREE.CylinderGeometry(scaledWidth / 2, scaledWidth / 2, scaledHeight); // Use scaledWidth for trunk diameter
                material = new THREE.MeshStandardMaterial({ color: 0x8B4513 }); // Brown
                break;

            case "vehicle":
                geometry = new THREE.BoxGeometry(scaledWidth, scaledHeight, 0.5); // Vehicle shape
                material = new THREE.MeshStandardMaterial({ color: 0x687487 }); // Grayish blue
                break;

            case "person":
                geometry = new THREE.SphereGeometry(scaledWidth / 2, 32, 32); // Sphere for person
                material = new THREE.MeshStandardMaterial({ color: 0xffd700 }); // Gold
                break;

            default:
                console.warn(`Unknown object type: ${object_type}`);
                return; // Skip unknown object types
        }

        // Create the mesh and apply material
        if (geometry) {
            mesh = new THREE.Mesh(geometry, material);
        }

        // Rotate the mesh if necessary
        if (object_type === "tree" || object_type === "vehicle" || object_type === "person") {
            mesh.rotation.x = -Math.PI / 2; // Rotate to lie flat on the x-y plane
        }

        // Set the object's position in the scene
        if (mesh) {
            mesh.position.copy(threePosition);
            mesh.userData = { name, boundingBox, condition, properties }; // Store additional properties
            scene.add(mesh); // Add the mesh to the scene
        }
    });
}

export { createRefinedHeightMapTexture, convertEnvPositionToThree, getColorBySwarmId, convertEnvRadiusToThree, createMapObjects };