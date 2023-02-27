"""EX03 - Instantaneous velocity."""
import PiBot
import math


class Robot:
    """The robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.current_time = 0
        self.left_wheel_velocity = 0
        self.right_wheel_velocity = 0
        self.timestamps = [0, 0, 0, 0, 0]
        self.left_wheel_encoders = [0, 0, 0, 0, 0]
        self.right_wheel_encoders = [0, 0, 0, 0, 0]

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set robot reference."""
        self.robot = robot

    def get_left_velocity(self) -> float:
        """
        Return the current left wheel velocity.

        Returns:
          The current wheel translational velocity in meters per second.
        """
        self.timestamps.pop(0)
        self.timestamps.append(self.current_time)

        delta_time = self.current_time - self.timestamps[0]
        delta_vel = (self.left_wheel_velocity - self.left_wheel_encoders[0]) * (math.pi / 360)
        if delta_time == 0:
            return 0

        return (delta_vel / delta_time) * (self.robot.WHEEL_DIAMETER / 2)

    def get_right_velocity(self) -> float:
        """
        Return the current right wheel velocity.

        Returns:
          The current wheel translational velocity in meters per second.
        """
        self.timestamps.pop(0)
        self.timestamps.append(self.current_time)

        delta_time = self.current_time - self.timestamps[0]
        delta_vel = (self.right_wheel_velocity - self.right_wheel_encoders[0]) * (math.pi / 360)
        if delta_time == 0:
            return 0

        return (delta_vel / delta_time) * (self.robot.WHEEL_DIAMETER / 2)

    def sense(self):
        """Read the sensor values from the PiBot API."""
        self.left_wheel_velocity = self.robot.get_left_wheel_encoder()
        self.left_wheel_encoders.pop(0)
        self.left_wheel_encoders.append(self.left_wheel_velocity)
        self.right_wheel_velocity = self.robot.get_right_wheel_encoder()
        self.right_wheel_encoders.pop(0)
        self.right_wheel_encoders.append(self.right_wheel_velocity)
        self.current_time = self.robot.get_time()

    def spin(self):
        """Call sense cyclically."""
        while not self.shutdown:
            self.sense()
            timestamp = self.robot.get_time()
            left_velocity = self.get_left_velocity()
            right_velocity = self.get_right_velocity()
            print(f'{timestamp}: {left_velocity} {right_velocity}')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True


def main():
    """Create a Robot object and spin it."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
