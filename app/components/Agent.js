import * as THREE from 'three';

class Agent {
    constructor(id, target_id, position, z_position, velocity, acceleration, color) {
        this.id = id;
        this.target_id = target_id;
        this.position = new THREE.Vector3(position.x, position.y, z_position); // Include z_position
        this.velocity = new THREE.Vector3(velocity.x, velocity.y, 0);
        this.acceleration = new THREE.Vector3(acceleration.x, acceleration.y, 0);

        this.size = 0.4; // Default Agent size (used for bounding box, sphere size, etc.)
        this.detectionRadius = 0.2; // Detection radius used for indicators (can vary)
        this.batteryLife = 100; // Health value (can be updated dynamically)
        this.direction = new THREE.Vector3(1, 0, 0); // Initial direction, can be based on velocity

        this.mesh = this.createMesh(color);
        this.updateMeshPosition(); // Sync the initial position with the mesh

        this.indicators = [];
    }

    createMesh(color) {
        const geometry = new THREE.SphereGeometry(0.025); // Smaller geometry for better scaling
        const material = new THREE.MeshBasicMaterial({ color: color }); // Default color, can be changed based on target_id
        return new THREE.Mesh(geometry, material);
    }

    update() {
        // Update velocity by adding acceleration (3D)
        this.velocity.add(this.acceleration);

        // Update position by adding velocity (3D)
        this.position.add(this.velocity);

        // Reset acceleration after each frame
        this.acceleration.set(0, 0, 0);

        // Sync the mesh position with the updated position
        this.updateMeshPosition();

        // Update the direction based on the velocity
        this.direction = this.velocity.clone().normalize();
    }

    applyForce(force) {
        // Apply force to acceleration in 3D (assuming force is a THREE.Vector3)
        this.acceleration.add(force);
    }

    updateMeshPosition() {
        // Ensure the mesh's position matches the Agent's 3D position
        this.mesh.position.copy(this.position);
    }

    updateColor(color) {
        // Update the color of the Agent's mesh
        this.mesh.material.color.set(color);
    }
}

export default Agent;
