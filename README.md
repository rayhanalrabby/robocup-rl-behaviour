# robocup-rl-behaviour

Reinforcement learning for behaviour-level decision making in RoboCup humanoid
robot soccer.

EE496 Final Year Project, BSc Robotics and Intelligent Devices, Maynooth
University, 2026/27.

- **Student:** Md Rayhan Mia (23740371)
- **Supervisor:** Dr. Rudi Villing
- **Group:** RoboEireann, Maynooth University RoboCup team
- **Platform:** Booster K1 humanoid
- **Simulator:** MuJoCo

## What this is

A robot soccer system is built in layers. Perception interprets the camera
image, modelling estimates where the robot and the ball are, the behaviour
layer decides what the robot should do, and the motion layer works out the
joint commands that carry that decision out.

The motion layer on the Booster K1 is already reinforcement-learned. This
project applies reinforcement learning to the behaviour layer and measures it
against the existing hand-coded behaviour.

Two policies are in scope:

1. Attacking agents passing the ball or running with it in midfield play.
2. A goalkeeper and an assisting defender, two agents, defending against
   multiple attackers.

Multi agent behaviour is the priority. The motion layer, perception,
localisation and kick accuracy are out of scope.

## Simulation approach

The simulation is kept simple so it runs fast. Each robot is modelled as a
capsule that can move in x, y and turn about its vertical axis, driven by
velocity commands. The ball is a sphere with rolling friction. This matches
the interface between the behaviour layer and the motion layer: the behaviour
layer decides where to go and when to kick, and the motion layer is not
simulated.

## Layout

```
sim/          simple MuJoCo scene and scripted behaviour demos
```

Planned as the project grows:

```
envs/         Gymnasium environment wrapping the simulation
train/        training scripts
results/      training output, not tracked
```

## Setup (Windows, Anaconda)

```
conda create -n ee496 python=3.11 -y
conda activate ee496
pip install mujoco numpy
```

Check the install:

```
python -m mujoco.viewer
```

## Status

| Milestone | Target | Status |
|---|---|---|
| Simulator running | Nov 2026 | Done |
| Simple scene: field, ball, two robots | Nov 2026 | In progress |
| Simple behaviours: go to ball, pass | Nov 2026 | Not started |
| Interim report | 18 Dec 2026 | In progress |
| Evaluation harness and baseline | Feb 2027 | Not started |
| Single agent policy | Mar 2027 | Not started |
| Multi agent policy | Apr 2027 | Not started |
| Final report | 7 May 2027 | Not started |
