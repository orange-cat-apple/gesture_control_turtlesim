import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class AutoNav(Node):
    def __init__(self):
        super().__init__('auto_nav')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.pose = None
        self.waypoints = [
            (9.5, 1.5),
            (9.5, 5.25),
            (1.5, 5.25),
            (1.5, 9.0),
            (9.5, 9.0)
        ]
        self.current_idx = 0
        self.timer = self.create_timer(0.05, self.control_loop)

    def pose_callback(self, msg):
        self.pose = msg

    def control_loop(self):
        if self.pose is None or self.current_idx >= len(self.waypoints):
            return

        target_x, target_y = self.waypoints[self.current_idx]
        dx = target_x - self.pose.x
        dy = target_y - self.pose.y
        distance = math.hypot(dx, dy)
        target_theta = math.atan2(dy, dx)
        angle_err = target_theta - self.pose.theta

        while angle_err > math.pi:
            angle_err -= 2.0 * math.pi
        while angle_err < -math.pi:
            angle_err += 2.0 * math.pi

        twist = Twist()
        if distance < 0.2:
            self.current_idx += 1
            if self.current_idx >= len(self.waypoints):
                twist.linear.x = 0.0
                twist.angular.z = 0.0
                self.publisher_.publish(twist)
                return

        if abs(angle_err) > 0.1:
            twist.angular.z = 2.5 * angle_err
            twist.linear.x = 0.5 * max(0.0, math.cos(angle_err))
        else:
            twist.linear.x = 2.0 * min(distance, 1.0)
            twist.angular.z = 1.0 * angle_err

        self.publisher_.publish(twist)

def main():
    rclpy.init()
    node = AutoNav()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

