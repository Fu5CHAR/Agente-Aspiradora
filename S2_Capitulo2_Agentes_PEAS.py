import matplotlib.pyplot as plt
import numpy as np
import random
import time

class VisualEnvironment3x3:
    def __init__(self):
        # Cuadrícula 3x3: 0 = Limpio, 1 = Sucio
        self.grid = np.random.choice([0, 1], size=(3, 3))
        # Posición inicial aleatoria (fila, columna) entre 0 y 2
        self.agent_pos = [random.randint(0, 2), random.randint(0, 2)]
        
        # Contadores diferenciados y de limpieza
        self.move_counts = {
            'Up_to_clean': 0, 'Up_to_dirty': 0,
            'Down_to_clean': 0, 'Down_to_dirty': 0,
            'Left_to_clean': 0, 'Left_to_dirty': 0,
            'Right_to_clean': 0, 'Right_to_dirty': 0,
            'Suck': 0
        }
        
        # Configuración del gráfico interactivo
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

    def render(self, step, action):
        self.ax.clear()
        self.ax.matshow(self.grid, cmap='Blues', vmin=0, vmax=1.5)
        self.ax.plot(self.agent_pos[1], self.agent_pos[0], 'ro', markersize=30)
        
        for i in range(3):
            for j in range(3):
                estado = "SUCIO" if self.grid[i, j] == 1 else "LIMPIO"
                self.ax.text(j, i, estado, ha='center', va='center', 
                             color='black', weight='bold', fontsize=10)

        self.ax.set_title(f"Paso: {step} | Acción: {action}", pad=20)
        self.ax.set_xticks([0, 1, 2])
        self.ax.set_yticks([0, 1, 2])
        self.ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
        
        plt.draw()
        plt.pause(1.0)

    def get_percept(self):
        return self.agent_pos.copy(), self.grid[self.agent_pos[0], self.agent_pos[1]]

    def execute_action(self, action):
        if action == 'Suck':
            self.grid[self.agent_pos[0], self.agent_pos[1]] = 0
            self.move_counts['Suck'] += 1

        elif action == 'Up' and self.agent_pos[0] > 0:
            target_row, target_col = self.agent_pos[0] - 1, self.agent_pos[1]
            if self.grid[target_row, target_col] == 1:
                self.move_counts['Up_to_dirty'] += 1
            else:
                self.move_counts['Up_to_clean'] += 1
            self.agent_pos[0] = target_row

        elif action == 'Down' and self.agent_pos[0] < 2:
            target_row, target_col = self.agent_pos[0] + 1, self.agent_pos[1]
            if self.grid[target_row, target_col] == 1:
                self.move_counts['Down_to_dirty'] += 1
            else:
                self.move_counts['Down_to_clean'] += 1
            self.agent_pos[0] = target_row

        elif action == 'Left' and self.agent_pos[1] > 0:
            target_row, target_col = self.agent_pos[0], self.agent_pos[1] - 1
            if self.grid[target_row, target_col] == 1:
                self.move_counts['Left_to_dirty'] += 1
            else:
                self.move_counts['Left_to_clean'] += 1
            self.agent_pos[1] = target_col

        elif action == 'Right' and self.agent_pos[1] < 2:
            target_row, target_col = self.agent_pos[0], self.agent_pos[1] + 1
            if self.grid[target_row, target_col] == 1:
                self.move_counts['Right_to_dirty'] += 1
            else:
                self.move_counts['Right_to_clean'] += 1
            self.agent_pos[1] = target_col

    def is_completely_clean(self):
        return np.sum(self.grid) == 0

    def print_movement_summary(self):
        print("\n--- Resumen Detallado de Acciones y Eficiencia (3x3) ---")
        for move, count in self.move_counts.items():
            print(f"  {move}: {count}")
            
        total_dirty = (self.move_counts['Up_to_dirty'] + self.move_counts['Down_to_dirty'] + 
                       self.move_counts['Left_to_dirty'] + self.move_counts['Right_to_dirty'])
        total_clean = (self.move_counts['Up_to_clean'] + self.move_counts['Down_to_clean'] + 
                       self.move_counts['Left_to_clean'] + self.move_counts['Right_to_clean'])
        suck_count = self.move_counts['Suck']
        
        total_actions = sum(self.move_counts.values())
        useful_actions = total_dirty + suck_count
        useless_actions = total_clean
        
        if total_actions > 0:
            useful_ratio = useful_actions / total_actions
            useless_ratio = useless_actions / total_actions
        else:
            useful_ratio = 0.0
            useless_ratio = 0.0
            
        print("\n  --- Métricas de Rendimiento ---")
        print(f"  Movimientos útiles (Dirty + Suck): {useful_actions}")
        print(f"  Movimientos no útiles (Clean): {useless_actions}")
        print(f"  Total de acciones totales: {total_actions}")
        print(f"  Ratio útiles / totales: {useful_ratio:.2f} ({useful_ratio * 100:.1f}%)")
        print(f"  Ratio no útiles / totales: {useless_ratio:.2f} ({useless_ratio * 100:.1f}%)")
    
class RandomVacuumAgent:
    def act(self, percept):
        pos, status = percept
        
        if status == 1:
            return 'Suck'
        
        movimientos_posibles = []
        if pos[0] > 0: movimientos_posibles.append('Up')
        if pos[0] < 2: movimientos_posibles.append('Down')
        if pos[1] > 0: movimientos_posibles.append('Left')
        if pos[1] < 2: movimientos_posibles.append('Right')
        
        return random.choice(movimientos_posibles)

if __name__ == "__main__":
    env = VisualEnvironment3x3()
    agent = RandomVacuumAgent()

    env.render(step=0, action="Inicio")

    # Configuración de tiempo y control de estado
    start_time = time.time()
    max_time_seconds = 20.0  # Límite de tiempo máximo en segundos
    completed_successfully = False

    for paso in range(1, 31):
        # Verificar si se excedió el tiempo límite antes de ejecutar el paso
        elapsed_time = time.time() - start_time
        if elapsed_time > max_time_seconds:
            print(f"\n[!] Tiempo límite excedido ({max_time_seconds} segundos).")
            break

        percept = env.get_percept()
        action = agent.act(percept)
        env.execute_action(action)
        env.render(step=paso, action=action)
        
        if env.is_completely_clean():
            print("¡Entorno 3x3 completamente limpio!")
            completed_successfully = True
            break

    # Calcular tiempo total transcurrido
    total_time = time.time() - start_time

    # Mostrar resumen de movimientos y métricas
    env.print_movement_summary()
    print(f"\n  Tiempo total de ejecución: {total_time:.2f} segundos")

    # Comprobación final de éxito o fracaso
    if not completed_successfully:
        print("\n  [ESTADO] Tarea no completada")

    plt.ioff()
    plt.show()