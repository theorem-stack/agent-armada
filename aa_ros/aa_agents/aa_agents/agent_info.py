import rclpy
from rclpy.node import Node
import requests
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from rclpy.duration import Duration

from aa_interfaces.msg import AgentInfo

PORT = 8000 # This is the port our FastAPI app uses

class AgentPoseNode(Node):
  '''
  Get agent data from FaspAPI and publish it as ROS2 messages
  
  Example data from the FastAPI endpoint
  {
    "0": {
      "target_id": 2,
      "position": [272.16033808726246, 554.7173984415554],
      "z_position": 0.0,
      "velocity": [0.29415376421927936, 0.5747030135236273],
      "acceleration": [0.0, -0.0]
    },
    "1": {
      "target_id": 2,
      "position": [279.36066072461466, 571.6279438587526],
      "z_position": 0.0,
      "velocity": [0.0184946953537566, 0.02191040466728643],
      "acceleration": [0.0, -0.0]
    },
  }
  '''
  def __init__(self):
      super().__init__('agent_positions', namespace='aa')

      qos_profile = QoSProfile(depth=10000)
      qos_profile.reliability = QoSReliabilityPolicy.RELIABLE
      self.publisher_ = self.create_publisher(AgentInfo, 'agent_info', qos_profile)

      self.url = f"http://host.docker.internal:{PORT}/api/py/agents" 

      self.timer = self.create_timer(1/30, self.fetch_and_publish)

      self.has_started = False

  def fetch_and_publish(self):
      try:
          response = requests.get(self.url, timeout=1)
          response.raise_for_status()  # Raise an exception for 4xx/5xx errors

          if response.status_code == 200:
              if not self.has_started:
                  self.has_started = True
                  self.get_logger().info(f"Got first response from FastAPI")
              
              agents_data = response.json()
              for agent_id, agent_data in agents_data.items():
                  agent_id = int(agent_id)
                  # if agent_id == 1:
                  #     break
                  # TODO position data is in 'pixels'. How do we convert this to meters?
                  x = agent_data['position'][0]
                  y = agent_data['position'][1]
                  z = agent_data['z_position']
                  target_id = agent_data['target_id']

                  msg = AgentInfo()
                  msg.agent_id = agent_id
                  msg.target_id = target_id
                  msg.pose.position.x = x
                  msg.pose.position.y = y
                  msg.pose.position.z = z
                  
                  self.publisher_.publish(msg)
                  # self.get_clock().sleep_for(Duration(seconds=1/30/30))

          else:
              self.get_logger().error(f"Failed to fetch data. Status code: {response.status_code}")
      except requests.exceptions.RequestException as e:
          self.get_logger().error(f"Request failed: {e}")

def main(args=None):
    rclpy.init(args=args)

    node = AgentPoseNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
