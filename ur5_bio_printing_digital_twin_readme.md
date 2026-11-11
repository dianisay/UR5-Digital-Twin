# 🤖 UR5 Digital Twin for Bio-Printing

Welcome to the UR5 Digital Twin project! 

This repository contains a **Digital Twin** (a virtual, simulated version) of a Universal Robots UR5 arm. We use this to test and visualize 3D bio-printing trajectories—specifically from our [Honeycomb Pipeline](https://github.com/dianisay/bioprinting-pipeline-honeycomb)—before sending them to the real, physical robot. 

Testing in a simulation means we can make mistakes, learn, and perfect our printing paths without breaking expensive hardware or wasting real bio-ink! 🧪

---

## 🚀 Getting Started

You don't need a supercomputer or a heavy robotics operating system (like ROS) to run this. We built it in pure Python using a lightweight physics engine called **PyBullet**.

### 1. Prerequisites
Make sure you have Python installed on your computer (Python 3.7 or newer is great). 

### 2. Installation
Open your terminal (or command prompt) and install the two libraries we need to run the physics and do the math:

```bash
pip install pybullet numpy
```

*(Note: If you have a `ur5.urdf` 3D model file, place it in this folder. If you don't have one yet, don't worry! The code is smart enough to load a temporary backup robot so you can still run the tests.)*

---

## 🎮 How to Run the Project

We have two main ways to test the robot. 

### Test 1: The "Smoke Test" (Quick Check)
Want to just make sure everything is working? Run the smoke test. This will open a 3D window and make the robot draw a simple hexagon in mid-air using an orange line. 

```bash
python demo_smoke_test.py
```
* **What you should see:** A 3D simulation pops up, the robot moves to the center, and it traces a hexagon shape. 

### Test 2: The Full Bio-Printing Pipeline
Once you know the simulation works, you can run the full pipeline. This script reads a list of coordinates (like a 3D connect-the-dots), mathematically smooths out the path so the robot doesn't jerk around, and draws it in cyan.

```bash
python main_twin.py
```
* **What you should see:** The robot smoothly traces a continuous honeycomb pattern, simulating how it would extrude bio-ink.

---

## 📂 What does each file do?

Here is a simple map of how the code is organized:

* 🌍 **`ur5_environment.py`**: The "Virtual World". This creates gravity, the floor (print bed), loads the robot model, and acts as the physics engine.
* 🧠 **`kinematics_solver.py`**: The "Math Brain". If we tell the robot "go to coordinate X, Y, Z", this script calculates exactly how much to bend each of the robot's 6 joints to reach that spot (this is called Inverse Kinematics).
* 📝 **`honeycomb_parser.py`**: The "Translator". It reads `.csv` files full of coordinates from your Honeycomb pipeline and scales them down to meters so the simulation understands them.
* 🎢 **`trajectory_planner.py`**: The "Smoother". If we just give the robot points, it moves in jerky straight lines. This script creates dozens of tiny micro-steps between points so the printing motion is perfectly smooth.
* 🎯 **`demo_smoke_test.py`**: A simple, standalone script to quickly test if the robot can move.
* 🎬 **`main_twin.py`**: The "Boss". This script puts everything together. It loads the world, reads the coordinates, smooths them out, and makes the robot move.

---

## 🛠️ Next Steps: Using Your Own Data

Right now, `main_twin.py` uses a built-in dummy data generator so you can test it immediately. 

When you are ready to connect it to your real GitHub pipeline:
1. Open `main_twin.py`.
2. Look for `parser.generate_dummy_data()`.
3. Change it to point directly to your real `.csv` file (e.g., `filepath = "my_real_honeycomb_path.csv"`).

Happy simulating! 🎉