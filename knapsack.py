import random

class KnapsackProblem:
    """
    Clase que representa el problema de la mochila (knapsack problem).
    Cada objeto tiene un valor y un peso, y el objetivo es maximizar el valor total sin exceder un peso máximo.
    La solución se representa como una lista de 0s y 1s, donde 1 indica que el objeto está incluido en la mochila y 0 que no lo está.

    Para indagar en un vecino, se puede baragear los índices de los
    objetos y cambiar el estado de inclusión (0 a 1 o viceversa) para generar
    vecina una nueva solución vecina candidata. 
    """
    def __init__(self, num_objetos: int =20,
                       seed: int =42,
                       load_from_file: str = None,
                       save_to_file: str = None):
        """
        Inicializa una instancia de `KnapsackProblem`.

        Parámetros:
        - num_objetos (int): número de objetos a generar aleatoriamente cuando no se carga desde archivo. Por defecto 20.
        - seed (int): semilla para el generador pseudoaleatorio. Por defecto 42.
        - load_from_file (str | None): nombre de archivo (relativo a la carpeta `knapsack_casos/`) desde el cual cargar un caso. Si se proporciona, se ignoran `num_objetos` y `seed`.
        - save_to_file (str | None): ruta de salida para guardar el caso generado. Si se proporciona, se escribirá el caso en la ruta indicada.

        Comportamiento:
        - Si `load_from_file` no es None, se llama a `cargar_desde_archivo` y se inicializa el problema a partir del contenido del archivo.
        - Si no, se generan `num_objetos` objetos aleatorios (con `valor` y `peso`), se calcula la capacidad (`peso_maximo`) y se obtiene el óptimo real mediante programación dinámica.
        """
        if load_from_file:
            tupla_objetos, peso_maximo, optimo = self.cargar_desde_archivo(load_from_file)
            self.objetos = [{"id": i, "valor": tupla[0], "peso": tupla[1]} for i, tupla in enumerate(tupla_objetos)]
            self.n = len(self.objetos)
            self.peso_maximo = peso_maximo
            self.optimo = optimo

        else:
            random.seed(seed)
            self.objetos = [
                {
                    "id": i, 
                    "valor": random.randint(50, 100), # Jian Dong 2021
                    "peso": random.randint(5, 20) # Jian Dong 2021
                } for i in range(num_objetos)
            ]
            self.n = num_objetos
            beta = 0.75 # Jian Dong 2021
            self.peso_maximo = round(beta * sum(obj["peso"] for obj in self.objetos))
            self.optimo = self.resolver_por_programacion_dinamica()
            if save_to_file:
                self.guardar_a_archivo(save_to_file)
    
    def guardar_a_archivo(self, ruta):
        """
        Guarda el caso actual en un archivo con el siguiente formato de líneas:

        Línea 1: peso máximo (int)
        Línea 2: valor óptimo (int)
        Línea 3: pesos de los objetos separados por comas
        Línea 4: valores de los objetos separados por comas

        Parámetros:
        - ruta (str): ruta del archivo donde se escribirá el caso. La función no añade prefijos; pase la ruta completa o relativa deseada.
        """
        with open(ruta, 'w') as f:
            f.write(f"{self.peso_maximo}\n")
            f.write(f"{self.optimo}\n")
            pesos = ','.join(str(obj["peso"]) for obj in self.objetos)
            valores = ','.join(str(obj["valor"]) for obj in self.objetos)
            f.write(f"{pesos}\n")
            f.write(f"{valores}\n")

    def cargar_desde_archivo(self, ruta):
        """
        Carga un caso desde la carpeta `knapsack_casos/`.

        El archivo esperado debe tener 4 líneas con el formato:
        1) peso máximo (int)
        2) valor óptimo (int)
        3) pesos de los objetos separados por comas
        4) valores de los objetos separados por comas

        Parámetros:
        - ruta (str): nombre de archivo relativo dentro de `knapsack_casos/` (por ejemplo 'k100.txt'). La función antepone internamente 'knapsack_casos/'.

        Retorna:
        - objetos (list of tuples): lista de tuplas (valor, peso)
        - peso_maximo (int)
        - optimo (int)
        """
        ruta = 'knapsack_casos/' + ruta
        with open(ruta, 'r') as f:
            lineas = f.readlines()
            peso_maximo = int(lineas[0].strip())
            optimo = int(lineas[1].strip())
            pesos = list(map(int, lineas[2].strip().split(',')))
            valores = list(map(int, lineas[3].strip().split(',')))
            objetos = list(zip(valores, pesos))
        return objetos, peso_maximo, optimo

    def resolver_por_programacion_dinamica(self) -> int:
        """
        Implementación del algoritmo de la mochila 0-1 usando PD.
        Calcula el valor óptimo real (Opt).
        """
        W = self.peso_maximo
        n = self.n
        # Creamos una matriz de (n+1) x (W+1) iniciada en 0
        # dp[i][w] guardará el valor máximo usando i objetos y peso w
        dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

        for i in range(1, n + 1):
            peso_i = self.objetos[i-1]["peso"]
            valor_i = self.objetos[i-1]["valor"]
            for w in range(W + 1):
                if peso_i <= w:
                    # Decisión: Max(No meter objeto, Meter objeto)
                    dp[i][w] = max(dp[i-1][w], dp[i-1][w - peso_i] + valor_i)
                else:
                    dp[i][w] = dp[i-1][w]
        
        return dp[n][W]

    def evaluar(self, solucion):
        """
        Calcula el fitness de una solución (lista de 0s y 1s).
        Retorna (valor_total, peso_total).
        """
        peso_total = sum(self.objetos[i]["peso"] for i in range(self.n) if solucion[i] == 1)
        valor_total = sum(self.objetos[i]["valor"] for i in range(self.n) if solucion[i] == 1)
        
        # Penalización severa si excede el peso
        if peso_total > self.peso_maximo:
            return {"valor_total": 0, "peso_total": peso_total}
        
        return {"valor_total": valor_total, "peso_total": peso_total}

    def generar_solucion_aleatoria(self):
        return [random.randint(0, 1) for _ in range(self.n)]

    def __str__(self):
        return f"Problema Mochila: {self.n} objetos | Capacidad: {self.peso_maximo}"
    
if __name__ == "__main__":
    pass
    # d = 1500
    # p = KnapsackProblem(num_objetos=d, save_to_file=f"knapsack_casos/k{d}.txt")