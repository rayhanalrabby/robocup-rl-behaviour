import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np

# Load the scene from the same folder as this script
scene_path = Path(__file__).parent / "scene.xml"
model = mujoco.MjModel.from_xml_string(scene_path.read_text())
data = mujoco.MjData(model)
mujoco.mj_forward(model, data)  # work out positions before the first step

# Behaviour settings
max_speed = 0.8  # m/s
max_turn = 2.0  # rad/s
stop_distance = 0.35  # stop this far from the ball centre (m)
duration = 15.0  # seconds of simulated time


def get_pose(name):
    """Return the robot's x, y position and heading on the field."""
    body = data.body(name)
    x, y = body.xpos[0], body.xpos[1]
    heading = np.arctan2(body.xmat[3], body.xmat[0])
    return np.array([x, y]), heading


def wrap_angle(a):
    """Keep an angle between -pi and pi."""
    return (a + np.pi) % (2 * np.pi) - np.pi


def go_to_ball(robot_name):
    """Speed command that drives the robot to the ball and faces it."""
    robot_pos, heading = get_pose(robot_name)
    ball_pos = data.body("ball").xpos[:2]

    to_ball = ball_pos - robot_pos
    distance = np.linalg.norm(to_ball)

    # Turn to face the ball
    angle_to_ball = np.arctan2(to_ball[1], to_ball[0])
    turn = np.clip(3.0 * wrap_angle(angle_to_ball - heading), -max_turn, max_turn)

    # Drive towards the ball, slowing down as it gets close
    if distance > stop_distance:
        speed = min(max_speed, 1.5 * (distance - stop_distance))
        velocity = speed * to_ball / distance
    else:
        velocity = np.zeros(2)

    return velocity[0], velocity[1], turn, distance


with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running() and data.time < duration:
        step_start = time.time()

        # Robot 1 goes to the ball, robot 2 stays still
        vx, vy, turn, distance = go_to_ball("robot1")
        data.ctrl[0:3] = [vx, vy, turn]
        data.ctrl[3:6] = [0.0, 0.0, 0.0]

        mujoco.mj_step(model, data)
        viewer.sync()

        # Wait so the simulation runs at real speed
        time_left = model.opt.timestep - (time.time() - step_start)
        if time_left > 0:
            time.sleep(time_left)

    print("distance to ball:", round(distance, 2), "m")
