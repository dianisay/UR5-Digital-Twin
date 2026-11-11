import time
import math
from ur5_environment import UR5Environment
from kinematics_solver import KinematicsSolver
from honeycomb_parser import HoneycombParser
from trajectory_planner import TrajectoryPlanner

def main():
    print("🤖 Starting UR5 Digital Twin - Full Pipeline")
    
    # 1. Initialize environment and kinematics
    env = UR5Environment(urdf_path="ur5.urdf", gui=True)
    solver = KinematicsSolver(env.robot_id, env.end_effector_index)
    
    # 2. Initialize parser and planner
    parser = HoneycombParser(scale_factor=0.001) # Converts mm to meters
    planner = TrajectoryPlanner(steps_per_segment=40)
    
    # 3. Ingest Data (using dummy data generator for now)
    csv_path = parser.generate_dummy_data()
    raw_waypoints = parser.parse_csv(csv_path)
    
    # Apply an offset to place the print at a visible height/distance for testing
    offset_waypoints = []
    for wp in raw_waypoints:
        offset_waypoints.append([wp[0] + 0.2, wp[1], wp[2] + 0.2])
        
    # 4. Plan the continuous trajectory
    print(f"📐 Interpolating {len(raw_waypoints)} waypoints...")
    smooth_trajectory = planner.plan_cartesian_path(offset_waypoints)
    
    print("⏳ Settling simulation...")
    for _ in range(100):
        env.step()

    # 5. Execute the continuous path
    print(f"🚀 Executing {len(smooth_trajectory)} micro-steps for smooth bio-printing...")
    prev_pos = env.get_end_effector_pos()
    
    for point in smooth_trajectory:
        target_angles = solver.calculate_ik(point)
        env.set_joint_angles(target_angles)
        
        # Advance simulation in smaller chunks per micro-step
        for _ in range(15): 
            env.step()
            
            current_pos = env.get_end_effector_pos()
            if prev_pos is not None:
                dist = math.dist(prev_pos, current_pos)
                if dist > 0.001:
                    # Draw a cyan line for the full pipeline trajectory
                    env.draw_line(prev_pos, current_pos, color=[0, 0.8, 1], width=4)
                    prev_pos = current_pos

    print("✅ Trajectory complete. Press Ctrl+C to exit.")
    
    try:
        while True:
            env.step()
    except KeyboardInterrupt:
        print("Closing simulation...")

if __name__ == "__main__":
    main()
