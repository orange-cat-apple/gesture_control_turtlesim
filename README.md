# Vision-Based Gesture Teleoperation (Engineer's Day Demo)

Real-time hand-gesture teleoperation node using OpenCV, MediaPipe Hands, and ROS 2 Humble to steer a robot via `/turtle1/cmd_vel`.

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

## Running the Demo

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

## Controls

- **Open Palm**: Drive (Up/Down for throttle, Left/Right for steering)
- **Closed Fist**: Emergency stop (halts all velocity commands)
- **Q / Esc**: Exit
