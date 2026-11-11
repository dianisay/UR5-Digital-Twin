import numpy as np

class TrajectoryPlanner:
    def __init__(self, steps_per_segment=30):
        # Number of interpolation steps between two coordinate points
        self.steps = steps_per_segment
        
    def plan_cartesian_path(self, waypoints):
        """
        Performs linear interpolation between waypoints to ensure 
        the UR5 moves smoothly instead of jumping from point to point.
        """
        if not waypoints or len(waypoints) < 2:
            return waypoints
            
        smooth_path = []
        for i in range(len(waypoints) - 1):
            start = np.array(waypoints[i])
            end = np.array(waypoints[i+1])
            
            # Generate intermediate points
            for t in np.linspace(0, 1, self.steps):
                point = start + t * (end - start)
                smooth_path.append(point.tolist())
                
        return smooth_path
