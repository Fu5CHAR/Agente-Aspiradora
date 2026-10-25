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
        print("\n--- Resumen Detallado de Acciones y Eficiencia (3x3 - Serpiente con Memoria) ---")
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

class SmartSnakeAgent:
    """Agente con memoria que traduce una ruta de coordenadas en acciones (Up, Down, Left, Right, Suck)."""
    def decide_actions(self, current_pos, target_pos, status):
        actions_to_perform = []
        
        # 1. Movimiento vertical si es necesario
        curr_r, curr_c = current_pos
        target_r, target_c = target_pos
        
        if curr_r < target_r:
            actions_to_perform.append('Down')
            curr_r += 1
        elif curr_r > target_r:
            actions_to_perform.append('Up')
            curr_r -= 1
            
        # 2. Movimiento horizontal si es necesario
        if curr_c < target_c:
            actions_to_perform.append('Right')
        elif curr_c > target_c:
            actions_to_perform.append('Left')
            
        # 3. Si al llegar está sucio, agregar 'Suck'
        if status == 1:
            actions_to_perform.append('Suck')
            
        return actions_to_perform

if __name__ == "__main__":
    env = VisualEnvironment3x3()
    agent = SmartSnakeAgent()

    # Render inicial
    env.render(step=0, action="Inicio")

    # 1. Generar recorrido en serpiente basado en la posición inicial
    casillas = [(i, j) for i in range(3) for j in range(3)]
    inicio = tuple(env.agent_pos)

    recorrido = []
    for i in range(3):
        fila = (inicio[0] + i) % 3
        columnas = list(range(3))

        if i % 2 == 1:
            columnas.reverse()

        for j in columnas:
            recorrido.append((fila, j))

    # Reordenar para que la primera casilla sea la posición inicial
    indice = recorrido.index(inicio)
    recorrido = recorrido[indice:] + recorrido[:indice]

    # Evitar repetir casillas en la ruta planificada (memoria del recorrido)
    ruta_planificada = [inicio]
    visitadas = {inicio}

    while len(ruta_planificada) < 9:
        fila, columna = ruta_planificada[-1]
        vecinos = [
            (fila - 1, columna), (fila + 1, columna),
            (fila, columna - 1), (fila, columna + 1)
        ]
        disponibles = [
            (f, c) for f, c in vecinos
            if 0 <= f < 3 and 0 <= c < 3
            and (f, c) not in visitadas
        ]

        if disponibles:
            siguiente = random.choice(disponibles)
            ruta_planificada.append(siguiente)
            visitadas.add(siguiente)
        else:
            pendientes = [p for p in casillas if p not in visitadas]
            siguiente = pendientes[0]
            ruta_planificada.append(siguiente)
            visitadas.add(siguiente)

    # 2. Ejecución del recorrido con control de tiempo y cronómetro
    start_time = time.time()
    max_time_seconds = 30.0
    completed_successfully = False
    paso_global = 1

    for destino in ruta_planificada:
        # Verificar límite de tiempo
        if time.time() - start_time > max_time_seconds:
            print(f"\n[!] Tiempo límite excedido ({max_time_seconds} segundos).")
            break

        # Desplazarse casilla por casilla hacia el destino de la serpiente
        while tuple(env.agent_pos) != destino:
            percept_pos, percept_status = env.get_percept()
            
            # Determinar siguiente paso de movimiento
            if percept_pos[0] < destino[0]:
                accion = 'Down'
            elif percept_pos[0] > destino[0]:
                accion = 'Up'
            elif percept_pos[1] < destino[1]:
                accion = 'Right'
            elif percept_pos[1] > destino[1]:
                accion = 'Left'
            else:
                break
                
            env.execute_action(accion)
            env.render(step=paso_global, action=accion)
            paso_global += 1

        # Al llegar a la casilla de la serpiente, comprobar si necesita limpieza ('Suck')
        percept_pos, percept_status = env.get_percept()
        if percept_status == 1:
            env.execute_action('Suck')
            env.render(step=paso_global, action='Suck')
            paso_global += 1

        # Verificar si todo está limpio
        if env.is_completely_clean():
            print("¡Entorno 3x3 completamente limpio!")
            completed_successfully = True
            break

    # Resultados y métricas finales
    total_time = time.time() - start_time
    env.print_movement_summary()
    print(f"\n  Tiempo total de ejecución: {total_time:.2f} segundos")

    if not completed_successfully:
        print("\n  [ESTADO] Tarea no completada")

    plt.ioff()
    plt.show()