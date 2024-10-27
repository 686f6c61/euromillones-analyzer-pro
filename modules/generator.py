import pandas as pd
import numpy as np
from tabulate import tabulate
import random
from datetime import datetime

class CombinationGenerator:
    def __init__(self, df):
        self.df = df
        self.numeros_posibles = list(range(1, 51))
        self.estrellas_posibles = list(range(1, 13))

    def generate_statistical(self, num_combinations=1):
        """Genera combinaciones basadas en estadísticas históricas."""
        print("\n📊 GENERANDO COMBINACIÓN ESTADÍSTICA")
        
        # Calcular frecuencias
        numeros = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros.extend(self.df[col].tolist())
        freq = pd.Series(numeros).value_counts()
        
        # Normalizar frecuencias como pesos
        weights = [freq.get(n, 0) + 1 for n in self.numeros_posibles]  # +1 para evitar peso 0
        
        combinaciones = []
        for _ in range(num_combinations):
            # Seleccionar números con probabilidad ponderada
            numeros_seleccionados = []
            nums_disponibles = self.numeros_posibles.copy()
            pesos = weights.copy()
            
            for _ in range(5):
                if nums_disponibles:
                    idx = random.choices(range(len(nums_disponibles)), weights=pesos, k=1)[0]
                    numeros_seleccionados.append(nums_disponibles.pop(idx))
                    pesos.pop(idx)
            
            # Generar estrellas
            estrellas = []
            for col in ['e1', 'e2']:
                estrellas.extend(self.df[col].tolist())
            freq_estrellas = pd.Series(estrellas).value_counts()
            pesos_estrellas = [freq_estrellas.get(n, 0) + 1 for n in self.estrellas_posibles]
            
            estrellas_seleccionadas = random.choices(self.estrellas_posibles, 
                                                   weights=pesos_estrellas, k=2)
            
            combinaciones.append({
                'numeros': sorted(numeros_seleccionados),
                'estrellas': sorted(estrellas_seleccionadas)
            })
            
            print(f"\nCombinación {len(combinaciones)}:")
            print(f"🎱 Números: {' - '.join(map(str, sorted(numeros_seleccionados)))}")
            print(f"⭐ Estrellas: {' - '.join(map(str, sorted(estrellas_seleccionadas)))}")
        
        return combinaciones

    def generate_balanced(self, num_combinations=1):
        """Genera combinaciones equilibradas basadas en patrones."""
        print("\n⚖️ GENERANDO COMBINACIÓN EQUILIBRADA")
        
        def is_balanced(numbers):
            # Verificar paridad
            pares = sum(1 for n in numbers if n % 2 == 0)
            if not 2 <= pares <= 3:
                return False
            
            # Verificar distribución por decenas
            decenas = [(n-1)//10 for n in numbers]
            if len(set(decenas)) < 3:
                return False
            
            # Verificar suma total
            suma = sum(numbers)
            if not 100 <= suma <= 150:
                return False
            
            # Verificar distancia entre números
            numbers = sorted(numbers)
            for i in range(len(numbers)-1):
                if numbers[i+1] - numbers[i] <= 1:  # Evitar consecutivos
                    return False
            
            return True

        combinaciones = []
        for _ in range(num_combinations):
            while True:
                numeros = sorted(random.sample(self.numeros_posibles, 5))
                if is_balanced(numeros):
                    break
            
            # Generar estrellas (una par y una impar)
            estrellas = []
            while len(estrellas) < 2:
                estrella = random.choice(self.estrellas_posibles)
                if not estrellas or (estrella % 2) != (estrellas[0] % 2):
                    estrellas.append(estrella)
            
            combinaciones.append({
                'numeros': numeros,
                'estrellas': sorted(estrellas)
            })
            
            print(f"\nCombinación {len(combinaciones)}:")
            print(f"🎱 Números: {' - '.join(map(str, numeros))}")
            print(f"⭐ Estrellas: {' - '.join(map(str, sorted(estrellas)))}")
            
            # Mostrar características de la combinación
            print("\nCaracterísticas:")
            print(f"- Números pares: {sum(1 for n in numeros if n % 2 == 0)}")
            print(f"- Suma total: {sum(numeros)}")
            print(f"- Decenas diferentes: {len(set((n-1)//10 for n in numeros))}")
        
        return combinaciones

    def generate_custom(self, forced_numbers=None, forbidden_numbers=None, num_combinations=1):
        """Genera combinaciones con restricciones personalizadas."""
        print("\n🎯 GENERANDO COMBINACIÓN PERSONALIZADA")
        
        forced_numbers = forced_numbers or []
        forbidden_numbers = forbidden_numbers or []
        
        numeros_disponibles = [n for n in self.numeros_posibles 
                             if n not in forbidden_numbers]
        
        combinaciones = []
        for _ in range(num_combinations):
            # Incluir números forzados
            numeros = forced_numbers.copy()
            
            # Completar con números aleatorios
            nums_faltantes = 5 - len(numeros)
            nums_adicionales = random.sample([n for n in numeros_disponibles 
                                           if n not in numeros], nums_faltantes)
            numeros.extend(nums_adicionales)
            
            # Generar estrellas
            estrellas = sorted(random.sample(self.estrellas_posibles, 2))
            
            combinaciones.append({
                'numeros': sorted(numeros),
                'estrellas': estrellas
            })
            
            print(f"\nCombinación {len(combinaciones)}:")
            print(f"🎱 Números: {' - '.join(map(str, sorted(numeros)))}")
            print(f"⭐ Estrellas: {' - '.join(map(str, estrellas))}")
        
        return combinaciones

    def generate_smart(self, num_combinations=1):
        """Genera combinaciones inteligentes mezclando diferentes estrategias."""
        print("\n🧠 GENERANDO COMBINACIÓN INTELIGENTE")
        
        # Obtener números calientes (frecuentes recientemente)
        ultimos_sorteos = self.df.head(20)
        numeros_recientes = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros_recientes.extend(ultimos_sorteos[col].tolist())
        freq_reciente = pd.Series(numeros_recientes).value_counts()
        
        # Obtener números históricos
        numeros_historicos = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros_historicos.extend(self.df[col].tolist())
        freq_historica = pd.Series(numeros_historicos).value_counts()
        
        combinaciones = []
        for i in range(num_combinations):
            # Mezclar diferentes estrategias
            if i % 3 == 0:  # Cada tercera combinación es más arriesgada
                # 2 números calientes, 2 fríos, 1 aleatorio
                calientes = freq_reciente.head(10).index.tolist()
                frios = freq_reciente.tail(10).index.tolist()
                numeros = (random.sample(calientes, 2) + 
                         random.sample(frios, 2) + 
                         [random.choice(self.numeros_posibles)])
            else:
                # 3 números con buena frecuencia histórica, 2 aleatorios
                buenos = freq_historica.head(20).index.tolist()
                numeros = (random.sample(buenos, 3) + 
                         random.sample(self.numeros_posibles, 2))
            
            # Asegurar que no hay repetidos
            numeros = sorted(list(set(numeros)))
            while len(numeros) < 5:
                nuevo = random.choice(self.numeros_posibles)
                if nuevo not in numeros:
                    numeros.append(nuevo)
            
            # Generar estrellas inteligentemente
            estrellas_hist = []
            for col in ['e1', 'e2']:
                estrellas_hist.extend(self.df[col].tolist())
            freq_estrellas = pd.Series(estrellas_hist).value_counts()
            
            # Una estrella frecuente, una menos frecuente
            estrellas = [
                freq_estrellas.head(6).index[random.randint(0, 5)],
                freq_estrellas.tail(6).index[random.randint(0, 5)]
            ]
            
            combinaciones.append({
                'numeros': sorted(numeros),
                'estrellas': sorted(estrellas)
            })
            
            print(f"\nCombinación {len(combinaciones)}:")
            print(f"🎱 Números: {' - '.join(map(str, sorted(numeros)))}")
            print(f"⭐ Estrellas: {' - '.join(map(str, sorted(estrellas)))}")
            
            # Análisis rápido de la combinación
            pares = sum(1 for n in numeros if n % 2 == 0)
            suma = sum(numeros)
            decenas = len(set((n-1)//10 for n in numeros))
            
            print("\nAnálisis:")
            print(f"- Balance par/impar: {pares}/{5-pares}")
            print(f"- Suma total: {suma}")
            print(f"- Decenas diferentes: {decenas}")
        
        return combinaciones

    def evaluate_combinations(self, combinations):
        """Evalúa un conjunto de combinaciones generadas."""
        print("\n📊 EVALUACIÓN DE COMBINACIONES")
        
        resultados = []
        for i, comb in enumerate(combinations, 1):
            # Calcular score basado en varios factores
            score = 0
            
            # Factor de frecuencia histórica
            numeros_hist = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros_hist.extend(self.df[col].tolist())
            freq_hist = pd.Series(numeros_hist).value_counts()
            
            freq_score = sum(freq_hist.get(n, 0)/len(self.df)*20 for n in comb['numeros'])
            score += freq_score
            
            # Factor de paridad
            pares = sum(1 for n in comb['numeros'] if n % 2 == 0)
            paridad_score = 10 if 2 <= pares <= 3 else 0
            score += paridad_score
            
            # Factor de suma
            suma = sum(comb['numeros'])
            suma_score = 10 if 100 <= suma <= 150 else 0
            score += suma_score
            
            # Factor de distribución
            decenas = len(set((n-1)//10 for n in comb['numeros']))
            distribucion_score = decenas * 5
            score += distribucion_score
            
            resultados.append([
                i,
                ' - '.join(map(str, comb['numeros'])),
                ' - '.join(map(str, comb['estrellas'])),
                round(score, 2)
            ])
        
        print("\nResumen de combinaciones:")
        print(tabulate(resultados,
                      headers=['#', 'Números', 'Estrellas', 'Score'],
                      tablefmt='pretty'))
        
        # Recomendar mejor combinación
        mejor = max(resultados, key=lambda x: x[3])
        print(f"\n🌟 Combinación recomendada: #{mejor[0]}")
        print(f"Score: {mejor[3]}/100")
        
        # Explicación detallada del cálculo del score
        print("\nExplicación del cálculo del score:")
        print(f"1. Frecuencia histórica: {freq_score:.2f} puntos")
        print("   (Basado en la frecuencia de aparición de cada número en sorteos anteriores)")
        print(f"2. Balance par/impar: {paridad_score} puntos")
        print(f"   (10 puntos si hay 2 o 3 números pares, 0 en caso contrario)")
        print(f"3. Suma total: {suma_score} puntos")
        print(f"   (10 puntos si la suma está entre 100 y 150, 0 en caso contrario)")
        print(f"4. Distribución por decenas: {distribucion_score} puntos")
        print(f"   (5 puntos por cada decena diferente representada)")
        print(f"\nScore total: {freq_score:.2f} + {paridad_score} + {suma_score} + {distribucion_score} = {score:.2f}")
