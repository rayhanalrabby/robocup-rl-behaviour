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
velocity commands. A kick sets the ball's velocity directly. The ball is a
sphere with rolling friction. This matches the interface between the
behaviour layer and the motion layer: the behaviour layer decides where to go
and when to kick, and the motion layer is not simulated.

## Field

The field follows the RoboCup Humanoid Soccer League rules
([HSL-Rules](https://github.com/RoboCup-HumanoidSoccerLeague/HSL-Rules),
commit `fc2a449`, November 2026). The Booster K1 plays in the Middle division,
and this project uses the M-Field.

| Item | Value |
|---|---|
| Field | 14 x 9 m, plus 1 m border strip |
| Goal | 2.5 m wide, 1.7 m high, 1.0 m deep |
| Goal area | 1.0 x 4.0 m |
| Penalty area | 3.0 x 6.0 m |
| Penalty mark | 2.0 m from the goal line |
| Centre circle | 3.0 m diameter |
| Corner arcs | 0.5 m radius |
| Line width | 0.05 m |
| Ball | FIFA size 3, modelled as 0.095 m radius, 0.31 kg |

The rules give ranges for the goal size. The values above are taken from the
middle of each range. The ball values are approximate and still need to be
checked against the ball the team uses.

Field lines are visual only. Goal posts, crossbar and nets collide with the
ball and robots.

## Layout

```
sim/
  scene.xml       M-Field, goals, ball and two simple robots
  run_demo.py     scripted pass: robot 1 lines up behind the ball and passes to robot 2
  speed_test.py   measures simulation speed without the viewer
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

## Running

```
conda activate ee496
python sim\run_demo.py
python sim\speed_test.py
```

Set `show_panels` in `run_demo.py` to show or hide the viewer panels. In the
viewer, **Align** returns to the default view of the field.

## Status

| Milestone | Target | Status |
|---|---|---|
| Simulator running | Nov 2026 | Done |
| Simple scene: field, ball, two robots | Nov 2026 | Done |
| Scripted behaviours: go to ball, pass | Nov 2026 | Done |
| Interim report | 18 Dec 2026 | In progress |
| Evaluation harness and baseline | Feb 2027 | Not started |
| Single agent policy | Mar 2027 | Not started |
| Multi agent policy | Apr 2027 | Not started |
| Final report | 7 May 2027 | Not started |

Simulation speed: about 164,000 steps per second (820x real time) on the
development laptop without the viewer, measured before the field markings
were added. Run `sim\speed_test.py` for the current figure.
