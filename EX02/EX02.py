"""EX02."""
import PiBot


class Robot:
    """Robot class."""

    def __init__(self):
        """Initialize the robot."""
        self.robot = PiBot.PiBot()
        self.shutdown = False

        self.front_middle_laser = 0.0

        self.state = "unknown"

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """
        Set the reference to PiBot object.

        Returns:
          None
        """
        self.robot = robot

    def get_state(self) -> str:
        """
        Return the current state.

        Returns:
          The current state as a string.
        """
        return self.state

    def sense(self):
        """Gather information using the sensors."""
        self.front_middle_laser = self.robot.get_front_middle_laser()

    def plan(self):
        """
        Perform the planning steps as required by the problem statement.

        Returns:
          None
        """
        if self.front_middle_laser >= 2.0:
            self.state = "very far"
        elif self.front_middle_laser > 1.5:
            self.state = "far"
        elif 0.5 < self.front_middle_laser and self.front_middle_laser <= 1.5:
            self.state = "ok"
        elif self.front_middle_laser <= 0.5 and self.front_middle_laser != 0.0:
            self.state = "close"
        else:
            self.state = "unknown"

    def spin(self):
        """Call sense and plan methods cyclically."""
        while not self.shutdown:
            print(f'The time is {self.robot.get_time()}!')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.sense()
                self.plan()
                self.shutdown = True


def main():
    """Create a Robot object and spin it."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
