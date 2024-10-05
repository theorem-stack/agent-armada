# Agent Armada on ROS (Robot Operating System)

This module provides a translation layer between FastAPI and ROS so that we can view the simulation with popular robotics tools such as RViz and Foxglove.

ROS runs best on Linux, so a Docker file is provided here so that we can run it on Mac and Windows.

## Usage
1. Build the Docker container: docker compose build
1. Start the Docker container: docker compose up -d
1. Enter the Docker container: docker exec -it aa_ros_container /bin/bash



