import sys
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill, SetPen, TeleportAbsolute

class MazeDrawer(Node):
    def __init__(self):
        super().__init__('maze_drawer')
        self.spawn_cli = self.create_client(Spawn, '/spawn')
        self.kill_cli = self.create_client(Kill, '/kill')
        self.reset_cli = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen_cli_turtle1 = self.create_client(SetPen, '/turtle1/set_pen')

    def run(self):
        self.spawn_cli.wait_for_service()
        self.kill_cli.wait_for_service()
        self.reset_cli.wait_for_service()
        self.pen_cli_turtle1.wait_for_service()

        spawn_req = Spawn.Request()
        spawn_req.x = 0.0
        spawn_req.y = 0.0
        spawn_req.theta = 0.0
        spawn_req.name = 'builder'
        future = self.spawn_cli.call_async(spawn_req)
        rclpy.spin_until_future_complete(self, future)

        set_pen = self.create_client(SetPen, '/builder/set_pen')
        teleport = self.create_client(TeleportAbsolute, '/builder/teleport_absolute')
        set_pen.wait_for_service()
        teleport.wait_for_service()

        walls = [
            ((0.0, 3.5), (8.5, 3.5)),
            ((2.5, 7.0), (11.0, 7.0))
        ]

        for (x1, y1), (x2, y2) in walls:
            pen_off = SetPen.Request()
            pen_off.off = 1
            f = set_pen.call_async(pen_off)
            rclpy.spin_until_future_complete(self, f)

            tp = TeleportAbsolute.Request()
            tp.x = float(x1)
            tp.y = float(y1)
            tp.theta = 0.0
            f = teleport.call_async(tp)
            rclpy.spin_until_future_complete(self, f)

            pen_on = SetPen.Request()
            pen_on.r = 255
            pen_on.g = 255
            pen_on.b = 255
            pen_on.width = 6
            pen_on.off = 0
            f = set_pen.call_async(pen_on)
            rclpy.spin_until_future_complete(self, f)

            tp.x = float(x2)
            tp.y = float(y2)
            f = teleport.call_async(tp)
            rclpy.spin_until_future_complete(self, f)

        kill_req = Kill.Request()
        kill_req.name = 'builder'
        f = self.kill_cli.call_async(kill_req)
        rclpy.spin_until_future_complete(self, f)

        pen1_off = SetPen.Request()
        pen1_off.off = 1
        f = self.pen_cli_turtle1.call_async(pen1_off)
        rclpy.spin_until_future_complete(self, f)

        reset_t1 = TeleportAbsolute.Request()
        reset_t1.x = 1.5
        reset_t1.y = 1.5
        reset_t1.theta = 0.0
        f = self.reset_cli.call_async(reset_t1)
        rclpy.spin_until_future_complete(self, f)

        pen1_on = SetPen.Request()
        pen1_on.r = 0
        pen1_on.g = 255
        pen1_on.b = 100
        pen1_on.width = 3
        pen1_on.off = 0
        f = self.pen_cli_turtle1.call_async(pen1_on)
        rclpy.spin_until_future_complete(self, f)

def main():
    rclpy.init()
    drawer = MazeDrawer()
    drawer.run()
    drawer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

