import pybullet as p

class KinematicsSolver:
    def __init__(self, robot_id, end_effector_index):
        self.robot_id = robot_id
        self.ee_idx = end_effector_index
        
    def calculate_ik(self, target_pos, target_orn=None):
        """
        Calcula la Cinemática Inversa (IK).
        target_pos: [x, y, z] en metros
        target_orn: [rx, ry, rz] en ángulos de Euler (opcional)
        """
        if target_orn is None:
            # Orientación estándar para extrusor (apuntando hacia abajo hacia la cama de impresión)
            target_orn = p.getQuaternionFromEuler([0, 3.14159, 0])
        elif len(target_orn) == 3:
            target_orn = p.getQuaternionFromEuler(target_orn)
            
        # PyBullet IK solver nativo
        joint_poses = p.calculateInverseKinematics(
            self.robot_id, 
            self.ee_idx, 
            target_pos, 
            target_orn,
            maxNumIterations=100,
            residualThreshold=1e-5
        )
        
        return joint_poses
