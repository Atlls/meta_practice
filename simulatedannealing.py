import math
import random
from knapsack import KnapsackProblem

def simulated_annealing(problema, T_inicial=100.0, alpha=0.95, L=50, T_final=0.01):
    """
    Implementación de Simulated Annealing para el Problema de la Mochila.
    
    Parámetros (Decisiones Genéricas):
    - T_inicial: Temperatura de inicio.
    - alpha: Factor de enfriamiento (regla de dedo: 0.8 a 0.99).
    - L: Longitud de la cadena (iteraciones por temperatura [iteraciones internas]).
    - T_final: Temperatura de parada (congelación).
    """
    
    # 1. Solución inicial
    s_actual = problema.generar_solucion_aleatoria()
    v_actual = problema.evaluar(s_actual)['valor_total']
    
    # Memoria a largo plazo (el mejor absoluto hallado)
    best_s = s_actual.copy()
    best_v = v_actual
    
    T = T_inicial
    
    print(f"--- Iniciando Simulated Annealing (T={T_inicial}, alpha={alpha}) ---")
    
    while T > T_final:
        for _ in range(L):
            # 2. Generar vecino (tweak)
            i = random.randint(0, problema.n - 1)
            vecino = s_actual.copy()
            vecino[i] = 1 - vecino[i]
            
            v_vecino = problema.evaluar(vecino)['valor_total']
            
            # 3. Calcular diferencia de energía (Costo)
            # En maximización, delta es (Nuevo - Viejo). 
            # Si delta > 0, el vecino es mejor.
            delta = v_vecino - v_actual
            
            if delta > 0:
                # El vecino es mejor, lo aceptamos siempre
                s_actual = vecino
                v_actual = v_vecino
                # Actualizar el récord histórico
                if v_actual > best_v:
                    best_s = s_actual.copy()
                    best_v = v_actual
            else:
                # El vecino es PEOR. Calculamos probabilidad de aceptación
                # P = e^(delta / T)
                probabilidad = math.exp(delta / T)
                
                if random.random() < probabilidad:
                    # Aceptamos una solución peor para escapar de óptimos locales
                    s_actual = vecino
                    v_actual = v_vecino
        
        # 4. Esquema de enfriamiento
        T = T * alpha
        
    return best_s, best_v

if __name__ == "__main__":
    p = KnapsackProblem(num_objetos=20, peso_maximo=100)
    
    # Ejemplo con parámetros configurables
    mejor_sol, mejor_val = simulated_annealing(
        p, 
        T_inicial=200.0, # Un poco trivial aumentarlo porque se usa tambien en la reducción de temperatura.
        alpha=0.5, # Existen varias maneras de enfriar, por ahora tenemos la geométrica, TODO: Hacer las otras dos.
        L=100, # Aumentarlo generalmente mejora la calidad de la solución.
        T_final=0.1
    )
    
    print("\n--- RESULTADO FINAL ---")
    print(f"Mejor Valor alcanzado: {mejor_val}")
    print(f"Configuración de bits: {mejor_sol}")