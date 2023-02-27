"""EX04 - Line tracking."""
import PiBot


class Robot:
    """The robot class."""

    def __init__(self):
        """Class initialization."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.leftmost_line_sensor = 0.0
        self.second_line_sensor_from_left = 0.0
        self.third_line_sensor_from_left = 0.0
        self.rightmost_line_sensor = 0.0
        self.second_line_sensor_from_right = 0.0
        self.third_line_sensor_from_right = 0.0
        self.current_direction_state = 0

        self.left_sensors = [0.0, 0.0]
        self.left_middle_sensors = [0.0, 0.0]
        self.middle_sensors = [0.0, 0.0]
        self.right_sensors = [0.0, 0.0]
        self.right_middle_sensors = [0.0, 0.0]

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set robot reference."""
        self.robot = robot

    def sense(self):
        """Sense method as per SPA architecture."""
        [self.leftmost_line_sensor, self.second_line_sensor_from_left,
            self.third_line_sensor_from_left] = [self.robot.get_leftmost_line_sensor(), self.robot.get_second_line_sensor_from_left(),
                                                 self.robot.get_third_line_sensor_from_left()]
        [self.rightmost_line_sensor, self.second_line_sensor_from_right,
         self.third_line_sensor_from_right] = [self.robot.get_rightmost_line_sensor(), self.robot.get_second_line_sensor_from_right(),
                                               self.robot.get_third_line_sensor_from_right()]

        self.left_sensors = [self.leftmost_line_sensor, self.second_line_sensor_from_left]
        self.left_middle_sensors = [self.second_line_sensor_from_left, self.third_line_sensor_from_left]
        self.middle_sensors = [self.third_line_sensor_from_left, self.third_line_sensor_from_right]
        self.right_middle_sensors = [self.second_line_sensor_from_right, self.third_line_sensor_from_right]
        self.right_sensors = [self.second_line_sensor_from_right, self.rightmost_line_sensor]

    def get_line_direction(self):
        """
        Return the direction of the line based on sensor readings.

        Returns:
          -1: Line is on the right (i.e., the robot should turn right to reach the line again)
           0: Robot is on the line (i.e., the robot should not turn to stay on the line) or no sensor info
           1: Line is on the left (i.e., the robot should turn left to reach the line again)
        """
        if all(i > 400 for i in self.left_sensors) and all(i > 400 for i in self.left_middle_sensors) and \
                all(i > 400 for i in self.middle_sensors) and all(i > 400 for i in self.right_middle_sensors) and \
                all(i > 400 for i in self.right_sensors):
            return self.current_direction_state
        elif all(i < 400 for i in self.left_middle_sensors) or all(i < 400 for i in self.middle_sensors) or \
                all(i < 400 for i in self.right_middle_sensors):
            self.current_direction_state = 0
        elif sum(self.left_sensors) > 1300 and sum(self.right_sensors) > 1300 and sum(self.middle_sensors) < 1300:
            self.current_direction_state = 0
        elif sum(self.middle_sensors) > 1300 and sum(self.right_sensors) > 1300 and sum(self.left_sensors) < 1300:
            self.current_direction_state = 1
        elif sum(self.middle_sensors) > 1300 and sum(self.left_sensors) > 1300 and sum(self.right_sensors) < 1300:
            self.current_direction_state = -1
        return self.current_direction_state

    def spin(self):
        """Call sense cyclically."""
        while not self.shutdown:
            timestamp = self.robot.get_time()
            print(f'timestamp is {timestamp}')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True


def main():
    """Create a Robot object and spin it."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
