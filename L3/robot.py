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

        self.front_left_distance_sensor = 0.0
        self.front_middle_distance_sensor = 0.0
        self.front_right_distance_sensor = 0.0

        self.current_direction_state = None
        self.right_wheel_speed = 0
        self.left_wheel_speed = 0
        self.threshold = 400

        self.obstacle_found = False
        self.off_the_line = False
        self.obstacle_avoid_step = 0
        self.timeout = 0

        self.left_buffer = []
        self.right_buffer = []

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
        [self.front_left_distance_sensor, self.front_middle_distance_sensor,
         self.front_right_distance_sensor] = [self.robot.get_front_left_laser(), self.robot.get_front_middle_laser(), self.robot.get_front_right_laser()]

    def get_line_direction(self):
        """
        Return the direction of the line based on sensor readings.

        Returns:
          -1: Line is on the right (i.e., the robot should turn right to reach the line again)
           0: Robot is on the line (i.e., the robot should not turn to stay on the line) or no sensor info
           1: Line is on the left (i.e., the robot should turn left to reach the line again)
        """
        if self.obstacle_avoid_step == 6:
            if not any(v < 400 for v in [self.third_line_sensor_from_left, self.third_line_sensor_from_right]):
                self.off_the_line = True

            if any(v < 400 for v in [self.third_line_sensor_from_left, self.third_line_sensor_from_right]):
                if self.off_the_line is False:
                    return

                self.obstacle_avoid_step = 0
                self.obstacle_found = False
                self.off_the_line = False
                print(f"\n\n\n\n OBSTACLE ENDED \n\n\n\n")
                return

            if self.timeout > self.robot.get_time():
                return

            if (min(self.left_buffer) > min(self.right_buffer)):
                if self.front_left_distance_sensor > 1:
                    self.current_direction_state = 1
                    return
        
                if self.front_left_distance_sensor < 0.25:
                    # self.timeout = self.robot.get_time() + (max(self.front_left_distance_sensor, 0.15) / 0.20)
                    self.current_direction_state = -1
                    return

                if self.front_right_distance_sensor < 0.25:
                    # self.timeout = self.robot.get_time() + (max(self.front_right_distance_sensor, 0.15) / 0.20)
                    self.current_direction_state = 1
                    return
                
                return
            else:
                if self.front_right_distance_sensor > 1:
                    self.current_direction_state = -1
                    return
        
                if self.front_right_distance_sensor < 0.25:
                    # self.timeout = self.robot.get_time() + (max(self.front_right_distance_sensor, 0.15) / 0.20)                    
                    self.current_direction_state = 1
                    return

                if self.front_left_distance_sensor < 0.25:
                    # self.timeout = self.robot.get_time() + (max(self.front_left_distance_sensor, 0.15) / 0.20)
                    self.current_direction_state = -1
                    return
                
                return

        if self.obstacle_found or self.front_middle_distance_sensor < 0.10:
            self.obstacle_found = True

            if self.front_middle_distance_sensor < 0.15:
                self.current_direction_state = 4
                return

            if self.obstacle_avoid_step == 0:
                self.current_direction_state = 3
                self.obstacle_avoid_step = 1
                self.timeout = self.robot.get_time() + 1
                return
            
            if self.obstacle_avoid_step == 1:
                self.left_buffer.append(self.front_right_distance_sensor)
                self.current_direction_state = 2
                if self.timeout < self.robot.get_time():
                    self.obstacle_avoid_step = 2
                    self.timeout = self.robot.get_time() + 1
                return
            
            if self.obstacle_avoid_step in [2, 3]:
                self.current_direction_state = -2
                if self.timeout < self.robot.get_time():
                    self.obstacle_avoid_step += 1
                    self.timeout = self.robot.get_time() + 1
                return
            
            if self.obstacle_avoid_step == 4:
                self.right_buffer.append(self.front_left_distance_sensor)
                self.current_direction_state = 2
                if self.timeout < self.robot.get_time():
                    self.obstacle_avoid_step = 5
                    self.timeout = self.robot.get_time() + 1
                    print(f"\n\n\n\nMIN TO LEFT: {min(self.left_buffer)} | MIN TO RIGHT: {min(self.right_buffer)}\n\n\n\n")
                return
            
            if self.obstacle_avoid_step == 5:
                if (min(self.left_buffer) > min(self.right_buffer)):
                    self.current_direction_state = -2
                else:
                    self.current_direction_state = 2

                if self.timeout < self.robot.get_time():
                    self.obstacle_avoid_step = 6
                return
            return

        if self.third_line_sensor_from_left <= self.threshold or self.third_line_sensor_from_right <= self.threshold:
            self.current_direction_state = 0
        elif self.leftmost_line_sensor <= self.threshold or self.second_line_sensor_from_left <= self.threshold:
            self.current_direction_state = 1
        elif self.rightmost_line_sensor <= self.threshold or self.second_line_sensor_from_right <= self.threshold:
            self.current_direction_state = -1

        if self.third_line_sensor_from_left > self.threshold and self.third_line_sensor_from_right > self.threshold and self.current_direction_state in [None, 0]:
            self.current_direction_state = 2

    def stop(self):
        """Stop robot."""
        self.right_wheel_speed = 0
        self.left_wheel_speed = 0

    def move_forward(self):
        """Make robot go forward."""
        self.right_wheel_speed = 10
        self.left_wheel_speed = 10

    def move_backward(self):
        """Make robot go backward."""
        self.right_wheel_speed = -10
        self.left_wheel_speed = -10        

    def make_spin_left(self):
        """Make robot spin."""
        self.right_wheel_speed = 10
        self.left_wheel_speed = -10

    def make_spin_right(self):
        """Make robot spin."""
        self.right_wheel_speed = -10
        self.left_wheel_speed = 10        

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
        self.get_line_direction()
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
            print("SPIN LEFT")
            self.make_spin_left()
        elif self.current_direction_state == -2:
            print("SPIN RIGHT")
            self.make_spin_right()
        elif self.current_direction_state == 3:
            print("STOP")
            self.stop()
        elif self.current_direction_state == 4:
            print("BACKWARD")
            self.move_backward()            

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
            print("\n", self.front_left_distance_sensor, self.front_middle_distance_sensor, self.front_right_distance_sensor, "\n")
            self.robot.sleep(0.05)


def main():
    """Create a Robot object and spin it."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
