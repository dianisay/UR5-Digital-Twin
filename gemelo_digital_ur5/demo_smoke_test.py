import math
from ur5_environment import UR5Environment
from kinematics_solver import KinematicsSolver

def generate_hexagon(center_x, center_y, z, radius):
    """Genera 7 puntos para formar un hexágono cerrado (guiño a Honeycomb)"""
    points = []
    for i in range(7): 
        angle = i * (math.pi / 3)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append([x, y, z])
    return points

def main():
    print("🤖 Iniciando Gemelo Digital - Smoke Test")
    
    # 1. Levantar el entorno virtual
    # Nota: Coloca tu archivo 'ur5.urdf' en este directorio.
    # Si no lo encuentra, PyBullet cargará un brazo temporal para no fallar el demo.
    env = UR5Environment(urdf_path="ur5.urdf", gui=True)
    
    # 2. Inicializar el motor matemático (Solver IK)
    solver = KinematicsSolver(env.robot_id, env.end_effector_index)
    
    # 3. Crear trayectoria de prueba (Hexágono a 20cm de altura, frente al robot)
    trayectoria = generate_hexagon(center_x=0.4, center_y=0.0, z=0.2, radius=0.1)
    
    print("⏳ Asentando simulación...")
    for _ in range(100):
        env.step()

    # 4. Ejecutar el movimiento
    print("🚀 Trazando trayectoria tipo Honeycomb...")
    prev_pos = env.get_end_effector_pos()
    
    for point in trayectoria:
        print(f"📍 Moviendo a: {point}")
        
        # A) Resolver matemáticas (Dónde deben estar los motores)
        target_angles = solver.calculate_ik(point)
        
        # B) Enviar señales a los motores virtuales
        env.set_joint_angles(target_angles)
        
        # C) Avanzar el tiempo y dibujar (240 steps = ~1 segundo en simulación)
        for _ in range(240):
            env.step()
            
            # Renderizar el filamento virtual
            current_pos = env.get_end_effector_pos()
            if prev_pos is not None:
                # Diferencia mínima para no dibujar puntos duplicados
                dist = math.dist(prev_pos, current_pos)
                if dist > 0.005: 
                    # Dibuja la línea color naranja
                    env.draw_line(prev_pos, current_pos, color=[1, 0.5, 0], width=3)
                    prev_pos = current_pos

    print("✅ Smoke test completado. Presiona Ctrl+C en la terminal para salir.")
    
    # Bucle infinito para mantener la ventana 3D abierta
    try:
        while True:
            env.step()
    except KeyboardInterrupt:
        print("Cerrando simulación...")

if __name__ == "__main__":
    main()
