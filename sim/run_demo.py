import time
from pathlib import Path

import mujoco
import mujoco.viewer

# Load the scene from the same folder as this script
scene_path = Path(__file__).parent / "scene.xml"
model = mujoco.MjModel.from_xml_string(scene_path.read_text())
data = mujoco.MjData(model)

# Run for 10 seconds of simulated time
duration = 10.0

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running() and data.time < duration:
        step_start = time.time()

        # Robot 1 moves forward in x at 0.5 m/s, robot 2 stays still
        data.ctrl[0] = 0.5
        data.ctrl[1] = 0.0
        data.ctrl[2] = 0.0

        mujoco.mj_step(model, data)
        viewer.sync()

        # Wait so the simulation runs at real speed
        time_left = model.opt.timestep - (time.time() - step_start)
        if time_left > 0:
            time.sleep(time_left)

    # Print where robot 1 and the ball ended up
    print("robot 1:", data.body("robot1").xpos.round(2))
    print("ball:", data.body("ball").xpos.round(2))
