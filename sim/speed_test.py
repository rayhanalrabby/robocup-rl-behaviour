import time
from pathlib import Path

import mujoco

# Load the scene from the same folder as this script
scene_path = Path(__file__).parent / "scene.xml"
model = mujoco.MjModel.from_xml_string(scene_path.read_text())
data = mujoco.MjData(model)

# Run without the viewer and time it
steps = 100_000
start = time.perf_counter()
for _ in range(steps):
    mujoco.mj_step(model, data)
elapsed = time.perf_counter() - start

sim_seconds = steps * model.opt.timestep
print(f"{steps} steps in {elapsed:.2f} s")
print(f"{steps / elapsed:,.0f} steps per second")
print(f"{sim_seconds / elapsed:,.0f}x faster than real time")
