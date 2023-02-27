"""L1 - line follower."""
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
        self.third_line_sensor_from_right = 0.0
        self.second_line_sensor_from_right = 0.0
        self.rightmost_line_sensor = 0.0

        self.current_direction_state = None
        self.right_wheel_speed = 0
        self.left_wheel_speed = 0
        self.threshold = 400

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set robot reference."""
        self.robot = robot

    def sense(self):
        """Read the sensor values from the PiBot API."""
        [self.leftmost_line_sensor, self.second_line_sensor_from_left,
            self.third_line_sensor_from_left] = [self.robot.get_leftmost_line_sensor(), self.robot.get_second_line_sensor_from_left(),
                                                 self.robot.get_third_line_sensor_from_left()]
        [self.rightmost_line_sensor, self.second_line_sensor_from_right,
         self.third_line_sensor_from_right] = [self.robot.get_rightmost_line_sensor(), self.robot.get_second_line_sensor_from_right(),
                                               self.robot.get_third_line_sensor_from_right()]
        [self.front_left_distance_sensor, self.front_middle_distance_sensor,
         self.front_right_distance_sensor] = [self.robot.get_front_left_laser(), self.robot.get_front_middle_laser(), self.robot.get_front_right_laser()]        
        
        self.get_line_direction()

    def get_line_direction(self):
        """
        Return the direction of the line based on sensor readings.

        Returns:
          -1: Line is on the right (i.e., the robot should turn right to reach the line again)
           0: Robot is on the line (i.e., the robot should not turn to stay on the line) or no sensor info
           1: Line is on the left (i.e., the robot should turn left to reach the line again)
        """
        if self.third_line_sensor_from_left <= self.threshold or self.third_line_sensor_from_right <= self.threshold:
            self.current_direction_state = 0
        elif self.leftmost_line_sensor <= self.threshold or self.second_line_sensor_from_left <= self.threshold:
            self.current_direction_state = 1
        elif self.rightmost_line_sensor <= self.threshold or self.second_line_sensor_from_right <= self.threshold:
            self.current_direction_state = -1

        if self.third_line_sensor_from_left > self.threshold and self.third_line_sensor_from_right > self.threshold and self.current_direction_state in [None, 0]:
            self.current_direction_state = 2

    def move_forward(self):
        """Make robot go forward."""
        self.right_wheel_speed = 10
        self.left_wheel_speed = 10

    def make_spin(self):
        """Make robot spin."""
        self.right_wheel_speed = 10
        self.left_wheel_speed = -10

    def turn_left(self):
        """Make robot turn left."""
        self.right_wheel_speed = 11
        self.left_wheel_speed = 0

    def turn_right(self):
        """Make robot turn right."""
        self.right_wheel_speed = 0
        self.left_wheel_speed = 11

    def plan(self):
        """Plan the next move."""
        if self.current_direction_state == -1:
            print("RIGHT")
            self.turn_right()
        elif self.current_direction_state == 1:
            print("LEFT")
            self.turn_left()
        elif self.current_direction_state == 0:
            print("FORWARD")
            self.move_forward()
        elif self.current_direction_state == 2:
            print("SPIN")
            self.make_spin()

    def act(self):
        """Do the moves."""
        self.robot.set_right_wheel_speed(self.right_wheel_speed)
        self.robot.set_left_wheel_speed(self.left_wheel_speed)

    def spin(self):
        """Call sense cyclically."""
        while not self.shutdown:
            self.sense()
            self.plan()
            self.act()
            self.robot.sleep(0.05)


def main():
    """Create a Robot object and spin it."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
