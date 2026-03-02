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
    def __init__(self, num_objetos=20, peso_maximo=100, seed=42):
        random.seed(seed)
        self.peso_maximo = peso_maximo
        self.objetos = [
            {
                "id": i, 
                "valor": random.randint(10, 100), 
                "peso": random.randint(1, 20)
            } for i in range(num_objetos)
        ]
        self.n = num_objetos

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