# Vision-Based Gesture Teleoperation & Autonomous Navigation (Engineer's Day Demo)

Real-time hand-gesture teleoperation node and autonomous navigation system using OpenCV, MediaPipe Hands, and ROS 2 Humble to steer a robot via `/turtle1/cmd_vel`.

## Prerequisites

- Ubuntu 22.04 + ROS 2 Humble (`ros-humble-turtlesim`)
- Python 3.10+ with webcam access

## Setup

```bash
# Clone the repository
git clone https://github.com/orange-cat-apple/gesture_control_turtlesim
cd gesture_teleop

# Create and activate venv with access to system ROS 2 packages
python3 -m venv --system-site-packages venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Gesture Teleop Demo

**Terminal 1:**
```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2:**
```bash
source /opt/ros/humble/setup.bash
source venv/bin/activate
python3 gesture_teleop.py
```

### Controls

- **Open Palm**: Drive (Up/Down for throttle, Left/Right for steering)
- **Closed Fist**: Emergency stop (halts all velocity commands)
- **Q / Esc**: Exit

## Running the Autonomous Navigation Demo

**Terminal 1:**
```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 — draw the maze walls:**
```bash
source /opt/ros/humble/setup.bash
source venv/bin/activate
python3 draw_maze.py
```

**Terminal 3 — run the autonomous navigator:**
```bash
source /opt/ros/humble/setup.bash
source venv/bin/activate
python3 auto_nav.py
```

`auto_nav.py` drives the turtle through a predefined sequence of waypoints, using proportional control on heading and distance to `/turtle1/pose`. `draw_maze.py` spawns a temporary helper turtle to trace maze walls with the pen before resetting `turtle1` to its start position.

## Files

| File | Description |
|---|---|
| `gesture_teleop.py` | Hand-gesture teleoperation node |
| `auto_nav.py` | Waypoint-following autonomous navigation node |
| `draw_maze.py` | Maze wall generator using a helper turtle |
| `requirements.txt` | Python dependencies |
