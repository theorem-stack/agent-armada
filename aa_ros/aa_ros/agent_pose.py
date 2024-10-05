import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests
import json

# example data from the FastAPI endpoint
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

PORT = 3000 # This is the port our FastAPI app uses

class AgentPoseNode(Node):
    def __init__(self):
        super().__init__('agent_positions', namespace='aa')

        self.publisher_ = self.create_publisher(String, 'agents_data', 10)

        self.url = f"http://host.docker.internal:{PORT}/api/py/agents" 

        self.timer = self.create_timer(0.1, self.fetch_and_publish)

    def fetch_and_publish(self):
        try:
            response = requests.get(self.url)

            if response.status_code == 200:
                agents_data = json.dumps(response.json())
                self.get_logger().info(str(type(agents_data)))

                # for agent_data in agents_data.values():
                #     x = agents_data['position'][0]
                #     y = agents_data['position'][1]
                #     z = agents_data['z_position']
                #     self.get_logger().info(f"Fetched Agents Data: {x}, {y}, {z}")

                msg = String()
                msg.data = agents_data
                self.publisher_.publish(msg)
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
