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
behind_distance = 0.35  # how far behind the ball the passer lines up (m)
kick_speed = 2.0  # ball speed after a kick (m/s)
duration = 20.0  # seconds of simulated time


def get_pose(name):
    """Return the robot's x, y position and heading on the field."""
    body = data.body(name)
    heading = np.arctan2(body.xmat[3], body.xmat[0])
    return body.xpos[:2].copy(), heading


def wrap_angle(a):
    """Keep an angle between -pi and pi."""
    return (a + np.pi) % (2 * np.pi) - np.pi


def drive_to(robot_name, target, face):
    """Speed command that drives the robot to a point while facing another point."""
    robot_pos, heading = get_pose(robot_name)

    to_target = target - robot_pos
    distance = np.linalg.norm(to_target)

    # Turn to face the given point
    to_face = face - robot_pos
    angle_error = wrap_angle(np.arctan2(to_face[1], to_face[0]) - heading)
    turn = np.clip(3.0 * angle_error, -max_turn, max_turn)

    # Drive towards the target, slowing down as it gets close
    if distance > 0.01:
        speed = min(max_speed, 1.5 * distance)
        velocity = speed * to_target / distance
    else:
        velocity = np.zeros(2)

    return velocity[0], velocity[1], turn, distance, angle_error


state = "GO_BEHIND_BALL"
print("state:", state)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running() and data.time < duration:
        step_start = time.time()

        ball_pos = data.body("ball").xpos[:2].copy()
        mate_pos, _ = get_pose("robot2")

        # Point behind the ball, on the line from the teammate through the ball
        to_mate = (mate_pos - ball_pos) / np.linalg.norm(mate_pos - ball_pos)
        behind_ball = ball_pos - behind_distance * to_mate

        if state == "GO_BEHIND_BALL":
            vx, vy, turn, distance, angle_error = drive_to(
                "robot1", behind_ball, mate_pos
            )
            # Close enough and facing the teammate: kick
            if distance < 0.05 and abs(angle_error) < 0.1:
                state = "KICK"
                print("state:", state, "at", round(data.time, 2), "s")

        if state == "KICK":
            # Give the ball a speed towards the teammate
            data.joint("ball_joint").qvel[0:2] = kick_speed * to_mate
            vx, vy, turn = 0.0, 0.0, 0.0
            state = "DONE"
            print("state:", state)

        if state == "DONE":
            vx, vy, turn = 0.0, 0.0, 0.0

        # Robot 2 stays in place and turns to watch the ball
        _, _, mate_turn, _, _ = drive_to("robot2", mate_pos, ball_pos)

        data.ctrl[0:3] = [vx, vy, turn]
        data.ctrl[3:6] = [0.0, 0.0, mate_turn]

        mujoco.mj_step(model, data)
        viewer.sync()

        # Wait so the simulation runs at real speed
        time_left = model.opt.timestep - (time.time() - step_start)
        if time_left > 0:
            time.sleep(time_left)

    ball_to_mate = np.linalg.norm(data.body("ball").xpos[:2] - get_pose("robot2")[0])
    print("ball distance from robot 2:", round(ball_to_mate, 2), "m")
