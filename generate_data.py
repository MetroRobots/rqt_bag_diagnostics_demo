from diagnostic_msgs.msg import DiagnosticStatus
import random
import rclpy
from rclpy.node import Node

MODES = ['OK', 'WARN', 'ERROR']


class DiagnosticPub(Node):
    def __init__(self):
        super().__init__('diagnostic_pub')
        self.last_status = None
        self.publisher = self.create_publisher(DiagnosticStatus, '/single_diagnostic', 10)
        self.timer = self.create_timer(1, self.callback)

    def callback(self):
        if self.last_status is None:
            # Random initial status
            status = random.randint(0, len(MODES) - 1)
        elif random.randint(0, 5) != 0:
            # Do not publish a msg every cycle
            return
        else:
            # Random new (different) status
            delta = random.randint(1, 2)
            status = (self.last_status + delta) % len(MODES)

        self.get_logger().info(f'Publishing {MODES[status]} status')
        self.publisher.publish(DiagnosticStatus(name='Demo', level=bytes(status)))
        self.last_status = status


def main(args=None):
    rclpy.init(args=args)
    node = DiagnosticPub()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
