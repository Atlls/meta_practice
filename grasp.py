import random
from knapsack import KnapsackProblem

def fase_construccion(problema, alpha):
    """
    Construye una solución desde cero usando una Lista Restringida de Candidatos (RCL).
    """

    def funcion_voraz_g(objeto):
        # g(i) = valor / peso (beneficio por unidad de peso)
        return objeto["valor"] / objeto["peso"]

    solucion = [0] * problema.n
    peso_actual = 0
    
    # 1. Identificar candidatos (objetos que aún caben en la mochila)
    candidatos = list(range(problema.n))
    
    while candidatos:
        # Filtrar candidatos que ya no caben por peso
        candidatos = [i for i in candidatos if peso_actual + problema.objetos[i]["peso"] <= problema.peso_maximo]
        if not candidatos:
            break
            
        # 2. Evaluar candidatos usando la función voraz 'g' (Valor / Peso) [cite: 114]
        # g representa la calidad de cada objeto
        costos = [funcion_voraz_g(problema.objetos[i]) for i in candidatos]
        
        g_min = min(costos)
        g_max = max(costos)
        
        # 3. Definir el umbral de calidad basado en alpha 
        # Si alpha = 0 -> umbral = g_max (Totalmente voraz)
        # Si alpha = 1 -> umbral = g_min (Totalmente aleatorio)
        umbral = g_max - alpha * (g_max - g_min)
        
        # 4. Crear la RCL (Lista Restringida de Candidatos) 
        # Objetos cuyo beneficio es >= umbral
        rcl = [candidatos[i] for i in range(len(candidatos)) if costos[i] >= umbral]
        
        # 5. Selección aleatoria de la RCL 
        elegido = random.choice(rcl)
        
        # 6. Añadir a la solución y actualizar estado (Adaptación)
        solucion[elegido] = 1
        peso_actual += problema.objetos[elegido]["peso"]
        candidatos.remove(elegido)
        
    return solucion

def busqueda_local(problema, solucion_inicial):
    """
    Refina la solución construida buscando un óptimo local (Hill Climbing Simple). [cite: 1, 9]
    """
    mejor_sol = solucion_inicial.copy()
    mejor_val = problema.evaluar(mejor_sol)['valor_total']
    
    # Ese while está como medio trivial.
    mejorando = True
    while mejorando:
        mejorando = False
        indices = list(range(problema.n))
        random.shuffle(indices)
        
        for i in indices:
            vecino = mejor_sol.copy()
            vecino[i] = 1 - vecino[i] # Intentar meter o sacar un objeto
            
            val_vecino = problema.evaluar(vecino)['valor_total']
            if val_vecino > mejor_val:
                mejor_sol = vecino
                mejor_val = val_vecino
                mejorando = True
                break
    return mejor_sol

def grasp(problema, max_iter=20, alpha=0.3):
    """
    Esquema principal de GRASP. [cite: 2]
    """
    s_best = [0] * problema.n
    v_best = 0
    
    print(f"--- Iniciando GRASP (iteraciones={max_iter}, alpha={alpha}) ---")
    
    for i in range(max_iter):
        # Fase 1: Construcción [cite: 1, 2]
        s = fase_construccion(problema, alpha)
        
        # Fase 2: Búsqueda Local [cite: 1, 2]
        s_local = busqueda_local(problema, s)
        v_local = problema.evaluar(s_local)['valor_total']
        
        # Actualizar la mejor solución global encontrada [cite: 2]
        if v_local > v_best:
            s_best = s_local
            v_best = v_local
            print(f"Iteración {i}: Nuevo mejor valor = {v_best}")
            
    return s_best, v_best

if __name__ == "__main__":
    p = KnapsackProblem(load_from_file="k10.txt") # Cargar instancia desde archivo
    
    mejor_sol, mejor_val = grasp(p, max_iter=1000, alpha=0.85)
    
    print("\n--- RESULTADO FINAL ---")
    print(f"Mejor Valor: {mejor_val}")
    print(f"Valor Óptimo: {p.optimo}")
    print(f"Configuración: {mejor_sol}")