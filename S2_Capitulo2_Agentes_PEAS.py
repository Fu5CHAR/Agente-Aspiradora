import matplotlib.pyplot as plt
import numpy as np
import random
import time

class VisualEnvironment2x2:
    def __init__(self):
        # Cuadrícula 2x2: 0 = Limpio, 1 = Sucio
        self.grid = np.random.choice([0, 1], size=(2, 2))
        # Posición inicial aleatoria (fila, columna)
        self.agent_pos = [random.randint(0, 1), random.randint(0, 1)]
        
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
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

    def render(self, step, action):
        self.ax.clear()
        self.ax.matshow(self.grid, cmap='Blues', vmin=0, vmax=1.5)
        self.ax.plot(self.agent_pos[1], self.agent_pos[0], 'ro', markersize=40)
        
        for i in range(2):
            for j in range(2):
                estado = "SUCIO" if self.grid[i, j] == 1 else "LIMPIO"
                self.ax.text(j, i, estado, ha='center', va='center', 
                             color='black', weight='bold', fontsize=12)

        self.ax.set_title(f"Paso: {step} | Acción: {action}", pad=20)
        self.ax.set_xticks([0, 1])
        self.ax.set_yticks([0, 1])
        self.ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
        
        plt.draw()
        plt.pause(1.5)

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

        elif action == 'Down' and self.agent_pos[0] < 1:
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

        elif action == 'Right' and self.agent_pos[1] < 1:
            target_row, target_col = self.agent_pos[0], self.agent_pos[1] + 1
            if self.grid[target_row, target_col] == 1:
                self.move_counts['Right_to_dirty'] += 1
            else:
                self.move_counts['Right_to_clean'] += 1
            self.agent_pos[1] = target_col

    def is_completely_clean(self):
        return np.sum(self.grid) == 0

    def print_movement_summary(self):
        print("\n--- Resumen Detallado de Acciones y Eficiencia ---")
        for move, count in self.move_counts.items():
            print(f"  {move}: {count}")
            
        # Cálculos de métricas
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
        if pos[0] < 1: movimientos_posibles.append('Down')
        if pos[1] > 0: movimientos_posibles.append('Left')
        if pos[1] < 1: movimientos_posibles.append('Right')
        
        return random.choice(movimientos_posibles)

if __name__ == "__main__":
    env = VisualEnvironment2x2()
    agent = RandomVacuumAgent()

    env.render(step=0, action="Inicio")

    for paso in range(1, 16):
        percept = env.get_percept()
        action = agent.act(percept)
        env.execute_action(action)
        env.render(step=paso, action=action)
        
        if env.is_completely_clean() and action != 'Suck':
            print("¡Entorno 2x2 completamente limpio!")
            break

    env.print_movement_summary()

    plt.ioff()
    plt.show()