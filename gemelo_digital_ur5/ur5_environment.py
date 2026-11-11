import pybullet as p
import pybullet_data
import time
import os

class UR5Environment:
    def __init__(self, urdf_path="ur5.urdf", gui=True):
        self.gui = gui
        self.client = p.connect(p.GUI if gui else p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        
        # Cargar el suelo (cama de impresión)
        self.plane_id = p.loadURDF("plane.urdf")
        
        # Intentar cargar el UR5, si no existe usar un robot provisorio para que el demo no falle
        if os.path.exists(urdf_path):
            print(f"Cargando URDF personalizado: {urdf_path}")
            self.robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)
        else:
            print(f"⚠️ No se encontró '{urdf_path}'.")
            print("Cargando brazo Kuka provisorio de pybullet_data para el Smoke Test...")
            self.robot_id = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=True)
        
        # Configurar cámara para ver la "cama de impresión"
        p.resetDebugVisualizerCamera(cameraDistance=1.2, cameraYaw=45, cameraPitch=-30, cameraTargetPosition=[0.4, 0, 0.2])
        
        # Mapear articulaciones móviles (excluir fixed joints)
        self.num_joints = p.getNumJoints(self.robot_id)
        self.revolute_joints = []
        for i in range(self.num_joints):
            info = p.getJointInfo(self.robot_id, i)
            if info[2] != p.JOINT_FIXED:
                self.revolute_joints.append(i)
        
        # Asumir que el efector final es el último eslabón móvil
        self.end_effector_index = self.revolute_joints[-1] if self.revolute_joints else -1

    def step(self):
        p.stepSimulation()
        if self.gui:
            time.sleep(1./240.)
        
    def set_joint_angles(self, angles):
        if not self.robot_id: return
        
        # A veces el solver IK devuelve más ángulos si el robot tiene más DOF.
        # Solo aplicamos los correspondientes a las articulaciones móviles.
        for i, joint_idx in enumerate(self.revolute_joints):
            if i < len(angles):
                p.setJointMotorControl2(
                    bodyIndex=self.robot_id,
                    jointIndex=joint_idx,
                    controlMode=p.POSITION_CONTROL,
                    targetPosition=angles[i],
                    force=200,     # Fuerza simulada de los servos
                    maxVelocity=1.0 # Velocidad máxima para suavizar el demo
                )
    
    def get_end_effector_pos(self):
        if not self.robot_id: return None
        state = p.getLinkState(self.robot_id, self.end_effector_index)
        return state[0] # Retorna (x, y, z)
        
    def draw_line(self, start, end, color=[1, 0, 0], width=3):
        p.addUserDebugLine(start, end, color, width, lifeTime=0)
