"""OT05 - Noise."""
import PiBot
import statistics


class Robot:
    """Robot class."""

    def __init__(self):
        """Initialize object."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.buffer = []

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set the PiBot reference."""
        self.robot = robot

    def sense(self):
        """Read the sensor values from the PiBot API."""
        self.buffer.append(self.robot.get_front_middle_laser())
        if len(self.buffer) > 5:
            self.buffer.pop(0)

    def get_front_middle_laser(self) -> float:
        """
        Return the filtered value.

        Returns:
          None if filter is empty, filtered value otherwise.
        """
        if not self.buffer:
            return None

        return statistics.median(sorted(self.buffer))

    def spin(self):
        """Call sense cyclically."""
        while not self.shutdown:
            print(f'Value is {self.get_front_middle_laser()}')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True


def main():
    """Create a Robot object and spin it."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
