from PiBot import PiBot

# Create a robot instance
robot = PiBot()

# Get distance from object using the front middle IR sensor
distance_from_object = robot.get_front_middle_laser()

# Drive towards object
robot.set_wheels_speed(30)
while distance_from_object > 0.2:
    distance_from_object = robot.get_front_middle_laser()
    robot.sleep(0.05)
    
# Stop the robot when done
robot.set_wheels_speed(0)
