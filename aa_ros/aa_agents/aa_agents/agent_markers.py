import rclpy
from rclpy.node import Node
from aa_interfaces.msg import AgentInfo
from visualization_msgs.msg import Marker

class AgentMarkerNode(Node):
    def __init__(self):
        super().__init__('agent_marker_publisher', namespace='aa')

        self.subscription = self.create_subscription(
            AgentInfo,
            '/aa/agent_info',
            self.agent_info_callback,
            10000  # QoS profile depth
        )

        self.marker_publisher = self.create_publisher(Marker, '/agent_markers', 10000)

        self.marker = Marker()
        self.marker.header.frame_id = "map"
        self.marker.header.stamp = self.get_clock().now().to_msg()
        self.marker.ns = "agents"
        self.marker.type = Marker.SPHERE
        self.marker.action = Marker.ADD

        # Set the scale of the marker (sphere size)
        self.marker.scale.x = 10.0  # Diameter in meters
        self.marker.scale.y = 10.0
        self.marker.scale.z = 10.0

        # Set the color (RGBA)
        self.marker.color.r = 1.0
        self.marker.color.g = 0.0
        self.marker.color.b = 0.0
        self.marker.color.a = 1.0  # Fully opaque

        # Lifetime of the marker, 0 means the marker stays forever
        self.marker.lifetime = rclpy.duration.Duration(seconds=1.0).to_msg()

    def agent_info_callback(self, msg: AgentInfo) -> None:
        self.publish_marker(msg)

    def publish_marker(self, msg: AgentInfo) -> None:
        self.marker.header.stamp = self.get_clock().now().to_msg()
        self.marker.id = msg.agent_id  # Unique ID for each agent

        # Set the pose based on the received AgentInfo message
        self.marker.pose.position.x = msg.pose.position.x
        self.marker.pose.position.y = msg.pose.position.y
        self.marker.pose.position.z = msg.pose.position.z

        # We aren't getting orientation right now
        # # Set orientation (as received from the message)
        # self.marker.pose.orientation.x = msg.pose.orientation.x
        # self.marker.pose.orientation.y = msg.pose.orientation.y
        # self.marker.pose.orientation.z = msg.pose.orientation.z
        # self.marker.pose.orientation.w = msg.pose.orientation.w

        # Publish the marker
        self.marker_publisher.publish(self.marker)

def main(args=None):
    rclpy.init(args=args)
    node = AgentMarkerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()