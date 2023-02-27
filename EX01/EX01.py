"""EX01."""
import PiBot


class Robot:
    """Robot class."""

    def __init__(self):
        """Initialize class."""
        self.robot = PiBot.PiBot()
        self.shutdown = False

        self.front_left_laser = 0.0
        self.front_middle_laser = 0.0
        self.front_right_laser = 0.0

        self.rear_left_straight_ir = 0.0
        self.rear_left_diagonal_ir = 0.0
        self.rear_left_side_ir = 0.0

        self.rear_right_straight_ir = 0.0
        self.rear_right_diagonal_ir = 0.0
        self.rear_right_side_ir = 0.0

        self.leftmost_line_sensor = 0.0
        self.second_line_sensor_from_left = 0.0
        self.third_line_sensor_from_left = 0.0

        self.rightmost_line_sensor = 0.0
        self.second_line_sensor_from_right = 0.0
        self.third_line_sensor_from_right = 0.0

        self.rotation = 0.0

        self.right_wheel_speed = 0
        self.left_wheel_speed = 0
        self.grabber_height = 0

    def sense(self):
        """Gather information using the sensors."""
        [self.front_left_laser, self.front_middle_laser,
            self.front_right_laser] = self.robot.get_front_lasers()
        [self.rear_left_side_ir, self.rear_left_diagonal_ir, self.rear_left_straight_ir, self.rear_right_straight_ir,
            self.rear_right_diagonal_ir, self.rear_right_side_ir] = self.robot.get_rear_irs()
        [self.leftmost_line_sensor, self.second_line_sensor_from_left,
            self.third_line_sensor_from_left] = self.robot.get_left_line_sensors()
        [self.rightmost_line_sensor, self.second_line_sensor_from_right,
         self.third_line_sensor_from_right] = self.robot.get_right_line_sensors()
        self.rotation = self.robot.get_rotation()

    def plan(self):
        """Plan the next move."""
        self.right_wheel_speed = 20
        self.left_wheel_speed = -20

        if self.rotation > 360:
            self.right_wheel_speed = 0
            self.left_wheel_speed = 0

    def act(self):
        """Do the moves."""
        self.robot.set_right_wheel_speed(self.right_wheel_speed)
        self.robot.set_left_wheel_speed(self.left_wheel_speed)
        self.robot.set_grabber_height(self.grabber_height)

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """
        Set the reference to the robot instance.

        NB! This is required for automatic testing.
        You are not expected to call this method in your code.

        Arguments:
          robot -- the reference to the robot instance.
        """
        self.robot = robot

    def spin(self):
        """
        Call sense, plan, act methods cyclically.

        This is the main loop of the robot and is expected to call sense, plan, act methods cyclically.
        """
        robot = Robot()
        while not self.shutdown:
            print(f'The time is {self.robot.get_time()}!')
            robot.sense()
            robot.plan()
            robot.act()
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True


def main():
    """Create a Robot class object and run it."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
