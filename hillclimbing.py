import random
from knapsack import KnapsackProblem

# --- 1. SIMPLE HILL CLIMBING ---
# Basado en la técnica más sencilla de optimización combinatoria.
def simple_hill_climbing(problema, MAX=100):
    t = 0
    s = problema.generar_solucion_aleatoria()
    
    while t < MAX:
        r = None # r es nuestra posible mejor solución.

        # Simulación de greedy_tweak: buscamos la primera mejora disponible
        indices = list(range(problema.n))
        random.shuffle(indices)
        
        for i in indices:
            vecino = s.copy()
            vecino[i] = 1 - vecino[i] # indagar por el vecino
            # Si r existe tal que c(r) es mejor que c(s)
            if problema.evaluar(vecino)["valor_total"] > problema.evaluar(s)["valor_total"]:
                r = vecino
                break
        
        if r is None: # Si r = vacia, terminamos
            break
            
        s = r
        t += 1
    return s

# --- 2. STOCHASTIC HILL CLIMBING ---
# Utiliza un enfoque aleatorio para seleccionar movimientos.
def stochastic_hill_climbing(problema, MAX=500):
    t = 0
    s = problema.generar_solucion_aleatoria()
    
    while t < MAX:
        # random_tweak: retorna una solución aleatoria r en la vecindad N(s)
        i = random.randint(0, problema.n - 1)
        r = s.copy()
        r[i] = 1 - r[i]
        
        # Si la nueva solución es mejor, se acepta el movimiento
        if problema.evaluar(r)["valor_total"] > problema.evaluar(s)["valor_total"]:
            s = r
            
        t += 1
    return s

# --- 3. STEEPEST ASCENT HILL CLIMBING ---
# Selecciona al mejor entre un número 'n' de vecinos considerados.
def steepest_ascent_hill_climbing(problema, n_vecinos=10, MAX=100):
    t = 0
    s = problema.generar_solucion_aleatoria()
    
    while t < MAX:
        # r := tweak(copy(s)) - candidato inicial
        i_rand = random.randint(0, problema.n - 1)
        r = s.copy()
        r[i_rand] = 1 - r[i_rand]
        
        # Evaluamos n-1 vecinos adicionales para encontrar el "máximo ascenso"
        for _ in range(n_vecinos - 1):
            w = s.copy()
            idx = random.randint(0, problema.n - 1)
            w[idx] = 1 - w[idx]
            
            if problema.evaluar(w)["valor_total"] > problema.evaluar(r)["valor_total"]:
                r = w
        
        # Solo nos movemos si el mejor vecino hallado supera a la solución actual
        if problema.evaluar(r)["valor_total"] > problema.evaluar(s)["valor_total"]:
            s = r
            
        t += 1
    return s

# --- 4. RANDOM RESTART HILL CLIMBING ---
# Utiliza reinicios desde soluciones aleatorias para escapar de óptimos locales.
def random_restart_hill_climbing(problema, MAX_RESTARTS=10, ITER_INTERNAS=50):
    t = 0
    s = problema.generar_solucion_aleatoria()
    best = s.copy() # Mantiene la mejor solución global
    
    while t < MAX_RESTARTS:
        # Búsqueda local por un intervalo de tiempo/iteraciones
        actual = s.copy()
        for _ in range(ITER_INTERNAS):
            i = random.randint(0, problema.n - 1)
            vecino = actual.copy()
            vecino[i] = 1 - vecino[i]
            
            if problema.evaluar(vecino)["valor_total"] > problema.evaluar(actual)["valor_total"]:
                actual = vecino
        
        # Si la solución del ciclo es mejor que la mejor histórica, actualizamos
        if problema.evaluar(actual)["valor_total"] > problema.evaluar(best)["valor_total"]:
            best = actual
            
        # Seleccionamos una nueva solución inicial aleatoria para el siguiente reinicio
        s = problema.generar_solucion_aleatoria()
        t += 1
        
    return best

# Creamos el problema
mochila = KnapsackProblem()

print(f"Resultados para {mochila}:")
print("-" * 50)

# Ejecución de variantes
resultados = [
    ("Simple", simple_hill_climbing(mochila)),
    ("Stochastic", stochastic_hill_climbing(mochila)),
    ("Steepest", steepest_ascent_hill_climbing(mochila)),
    ("Restart", random_restart_hill_climbing(mochila))
]

for nombre, sol in resultados:
    info = mochila.evaluar(sol)
    valor, peso = info["valor_total"], info["peso_total"]
    print(f"{nombre:15} | Valor: {valor:4} | Peso: {peso:3}")