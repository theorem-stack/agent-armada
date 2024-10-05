FROM osrf/ros:humble-desktop

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y \
    ros-humble-rviz2 \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "cd /root/ros2_ws/src/aa_ros" >> ~/.bashrc

SHELL ["/bin/bash", "-c"]
CMD ["bash"]