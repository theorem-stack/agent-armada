import * as THREE from 'three';

class Obstacle {
    constructor(id, position, radius, color) {
        this.id = id;
        this.position = new THREE.Vector3(position.x, position.y, position.z || 0); // 3D position with default Z=0
        this.radius = radius;  // Define radius for the target

        // Create the mesh for the target
        this.mesh = this.createMesh(color);
        this.updateMeshPosition();  // Sync initial position with the mesh
    }

    createMesh(color) {
        const geometry = new THREE.SphereGeometry(this.radius); // Smaller geometry for better scaling
        const material = new THREE.MeshBasicMaterial({ color: color }); // Default color, can be changed based on target_id
        return new THREE.Mesh(geometry, material);
    }

    updateMeshPosition() {
        // Ensure the mesh's position matches the Agent's 3D position
        this.mesh.position.copy(this.position);
    }

    updateColor(color) {
        // Update the mesh color
        this.mesh.material.color.set(color);
    }
}

export default Obstacle;