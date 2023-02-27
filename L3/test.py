import math
import robot

# Set up the robot
r = robot.Robot()

# Define the potential field parameters
k_att = 0.5 # attractive force constant
k_rep = 1.0 # repulsive force constant
d_min = 0.3 # minimum distance to obstacles

# Define the attractive force function
def attractive_force(x, y, x_goal, y_goal):
    dx = x_goal - x
    dy = y_goal - y
    d = math.sqrt(dx**2 + dy**2)
    fx = k_att * dx / d
    fy = k_att * dy / d
    return fx, fy

# Define the repulsive force function
def repulsive_force(x, y, x_obs, y_obs):
    dx = x_obs - x
    dy = y_obs - y
    d = math.sqrt(dx**2 + dy**2)
    if d > d_min:
        return 0, 0
    else:
        fx = -k_rep * (1/d - 1/d_min) * dx / d**3
        fy = -k_rep * (1/d - 1/d_min) * dy / d**3
        return fx, fy

# Define the potential field function
def potential_field(x, y, obstacles):
    fx_rep = 0
    fy_rep = 0
    for obs in obstacles:
        fx, fy = repulsive_force(x, y, obs[0], obs[1])
        fx_rep += fx
        fy_rep += fy
    fx = fx_rep
    fy = fy_rep
    return fx, fy

# Define the line following function
def follow_line():
    line_pos = r.get_sensor_data()[1]
    error = 0.5 - line_pos
    k_p = 0.5
    speed = 0.3
    turn = k_p * error
    return speed - turn, speed + turn

# Define the obstacle detection function
def detect_obstacle():
    distance = r.get_sensor_data()[0]
    if distance < d_min:
        return True
    else:
        return False

# Main loop
while True:
    # Get the robot's position
    x, y = r.get_position()

    # Check for obstacles and follow the line
    if detect_obstacle():
        # Avoid the obstacle using the potential field method
        obstacles = [(x + d_min, y)]
        fx, fy = potential_field(x, y, obstacles)
        r.move(fx, fy)
    else:
        # Follow the line
        fx, fy = follow_line()
        r.move(fx, fy)