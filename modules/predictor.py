import pandas as pd
import numpy as np
from tabulate import tabulate
from datetime import datetime, timedelta

class Predictor:
    def __init__(self, df):
        self.df = df

    def get_hot_numbers(self):
        print("\n🔥 NÚMEROS CALIENTES")
        
        ranges = [20, 50, 100, len(self.df)]
        labels = ["últimos 20 sorteos", "últimos 50 sorteos", "últimos 100 sorteos", "toda la serie histórica"]
        
        for range_size, label in zip(ranges, labels):
            print(f"\n{label.capitalize()}:")
            
            # Seleccionar el rango de sorteos
            df_range = self.df.head(range_size)
            
            # Contar frecuencias
            numeros = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros.extend(df_range[col].tolist())
            
            freq = pd.Series(numeros).value_counts()
            total_apariciones = len(numeros)
            
            # Calcular tendencias
            freq_total = pd.Series(self.df[['n1', 'n2', 'n3', 'n4', 'n5']].values.ravel()).value_counts()
            
            # Preparar resultados
            resultados = []
            for num, count in freq.head(10).items():
                porcentaje = (count / range_size) * 100
                freq_esperada = (freq_total[num] / len(self.df)) * range_size
                tendencia = ((count - freq_esperada) / freq_esperada) * 100
                
                resultados.append([
                    num,
                    count,
                    f"{porcentaje:.1f}",
                    f"{tendencia:+.2f}%"
                ])
            
            # Mostrar tabla
            print(tabulate(resultados,
                           headers=['Número', 'Apariciones', '% Sorteos', 'Tendencia'],
                           tablefmt='pretty'))

    def get_cold_numbers(self):
        """Analiza números que llevan mucho tiempo sin salir."""
        print("\n❄️ NÚMEROS FRÍOS")
        
        ranges = [20, 50, 100, len(self.df)]
        labels = ["últimos 20 sorteos", "últimos 50 sorteos", "últimos 100 sorteos", "toda la serie histórica"]
        
        for range_size, label in zip(ranges, labels):
            print(f"\n{label.capitalize()}:")
            
            # Seleccionar el rango de sorteos
            df_range = self.df.head(range_size)
            
            # Contar frecuencias
            numeros = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros.extend(df_range[col].tolist())
            
            freq = pd.Series(numeros).value_counts()
            total_apariciones = len(numeros)
            
            # Calcular tendencias
            freq_total = pd.Series(self.df[['n1', 'n2', 'n3', 'n4', 'n5']].values.ravel()).value_counts()
            
            # Preparar resultados
            resultados = []
            for num in range(1, 51):  # Consideramos todos los números posibles
                count = freq.get(num, 0)
                porcentaje = (count / range_size) * 100
                freq_esperada = (freq_total.get(num, 0) / len(self.df)) * range_size
                tendencia = ((count - freq_esperada) / freq_esperada) * 100 if freq_esperada > 0 else 0
                
                resultados.append([
                    num,
                    count,
                    f"{porcentaje:.1f}",
                    f"{tendencia:+.2f}%"
                ])
            
            # Ordenar por frecuencia ascendente y tomar los 10 menos frecuentes
            resultados.sort(key=lambda x: x[1])
            resultados = resultados[:10]
            
            # Mostrar tabla
            print(tabulate(resultados,
                           headers=['Número', 'Apariciones', '% Sorteos', 'Tendencia'],
                           tablefmt='pretty'))

    def analyze_patterns(self):
        """Analiza patrones en los últimos sorteos."""
        print("\n🔄 ANÁLISIS DE PATRONES RECIENTES")
        
        ultimos_sorteos = self.df.head(10)
        
        # Analizar paridad
        pares_impares = []
        for _, row in ultimos_sorteos.iterrows():
            numeros = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            pares = sum(1 for n in numeros if n % 2 == 0)
            impares = 5 - pares
            pares_impares.append([pares, impares])
        
        patron_paridad = pd.DataFrame(pares_impares).mode().iloc[0]
        print(f"Patrón de paridad más común: {patron_paridad[0]} pares, {patron_paridad[1]} impares")
        
        # Analizar distribución por decenas
        decenas_dist = []
        for _, row in ultimos_sorteos.iterrows():
            numeros = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            decenas = [(n-1)//10 for n in numeros]
            decenas_dist.append(pd.Series(decenas).value_counts())
        
        print("\nDistribución típica por decenas:")
        decenas_promedio = pd.DataFrame(decenas_dist).mean()
        for dec, valor in decenas_promedio.items():
            print(f"Decena {dec*10+1}-{(dec+1)*10}: {valor:.1f} números")

    def predict_next_draw(self):
        try:
            print("\n🎯 PREDICCIÓN PRÓXIMO SORTEO")
            
            print("Obteniendo números más frecuentes...")
            numeros_frecuentes = self._get_most_frequent_numbers(5)
            print(f"Números más frecuentes: {numeros_frecuentes}")
            
            print("Obteniendo estrellas más frecuentes...")
            estrellas_frecuentes = self._get_most_frequent_stars(2)
            print(f"Estrellas más frecuentes: {estrellas_frecuentes}")
            
            print("Ajustando paridad...")
            numeros_ajustados = self._adjust_parity(numeros_frecuentes)
            print(f"Números después de ajustar paridad: {numeros_ajustados}")
            
            print("Ajustando suma...")
            numeros_ajustados = self._adjust_sum(numeros_ajustados)
            print(f"Números después de ajustar suma: {numeros_ajustados}")
            
            print("Ajustando distribución de decenas...")
            numeros_predichos = self._adjust_decades_distribution(numeros_ajustados)
            print(f"Números después de ajustar distribución de decenas: {numeros_predichos}")
            
            # Ordenar los números y estrellas
            numeros_predichos.sort()
            estrellas_frecuentes.sort()
            
            print("\nNúmeros predichos:")
            print(" - ".join(map(str, numeros_predichos)))
            print("\nEstrellas predichas:")
            print(" - ".join(map(str, estrellas_frecuentes)))
            
            print("\nAnálisis de la predicción:")
            self._analizar_prediccion(numeros_predichos, estrellas_frecuentes)
        
        except Exception as e:
            print(f"Se produjo un error durante la predicción: {str(e)}")
            import traceback
            traceback.print_exc()

    def _get_most_frequent_numbers(self, n):
        numeros = self.df[['n1', 'n2', 'n3', 'n4', 'n5']].values.ravel()
        return pd.Series(numeros).value_counts().head(n).index.tolist()

    def _get_most_frequent_stars(self, n):
        estrellas = self.df[['e1', 'e2']].values.ravel()
        return pd.Series(estrellas).value_counts().head(n).index.tolist()

    def _adjust_parity(self, numbers):
        pares = sum(1 for n in numbers if n % 2 == 0)
        impares = 5 - pares
        ideal_pares = 2  # Asumimos que lo ideal es tener 2 pares y 3 impares
        
        if pares > ideal_pares:
            # Reemplazar pares por impares
            for i, n in enumerate(numbers):
                if n % 2 == 0 and pares > ideal_pares:
                    numbers[i] = self._get_next_odd_frequent(numbers)
                    pares -= 1
        elif pares < ideal_pares:
            # Reemplazar impares por pares
            for i, n in enumerate(numbers):
                if n % 2 != 0 and pares < ideal_pares:
                    numbers[i] = self._get_next_even_frequent(numbers)
                    pares += 1
        
        return numbers

    def _adjust_sum(self, numbers):
        suma_actual = sum(numbers)
        suma_ideal = 150  # Asumimos que la suma ideal es 150
        intentos = 0
        max_intentos = 100  # Limitamos el número de intentos para evitar bucles infinitos
        
        print(f"Suma actual: {suma_actual}, Suma ideal: {suma_ideal}")
        
        while suma_actual != suma_ideal and intentos < max_intentos:
            if suma_actual < suma_ideal:
                # Reemplazar el número más pequeño por uno más grande
                min_index = numbers.index(min(numbers))
                nuevo_numero = self._get_next_larger_frequent(numbers)
                if nuevo_numero:
                    numbers[min_index] = nuevo_numero
                else:
                    print("No se pudo encontrar un número más grande.")
                    break
            else:
                # Reemplazar el número más grande por uno más pequeño
                max_index = numbers.index(max(numbers))
                nuevo_numero = self._get_next_smaller_frequent(numbers)
                if nuevo_numero:
                    numbers[max_index] = nuevo_numero
                else:
                    print("No se pudo encontrar un número más pequeño.")
                    break
            
            suma_actual = sum(numbers)
            intentos += 1
            print(f"Intento {intentos}: Nueva suma = {suma_actual}")
        
        if intentos == max_intentos:
            print(f"Se alcanzó el máximo de intentos. Suma final: {suma_actual}")
        elif suma_actual == suma_ideal:
            print(f"Se logró la suma ideal de {suma_ideal}")
        else:
            print(f"No se pudo alcanzar la suma ideal. Suma final: {suma_actual}")
        
        return numbers

    def _adjust_decades_distribution(self, numbers):
        decenas = [(n-1)//10 for n in numbers]
        dec_dist = pd.Series(decenas).value_counts()
        
        ideal_dist = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1}  # Distribución ideal
        
        for dec, count in dec_dist.items():
            while count > ideal_dist[dec]:
                # Reemplazar un número de esta decena por uno de una decena menos representada
                for i, n in enumerate(numbers):
                    if (n-1)//10 == dec:
                        numbers[i] = self._get_number_from_underrepresented_decade(numbers)
                        break
                count -= 1
        
        return numbers

    def _get_next_odd_frequent(self, exclude):
        numeros = self.df[['n1', 'n2', 'n3', 'n4', 'n5']].values.ravel()
        freq = pd.Series(numeros).value_counts()
        for n in freq.index:
            if n % 2 != 0 and n not in exclude:
                return n

    def _get_next_even_frequent(self, exclude):
        numeros = self.df[['n1', 'n2', 'n3', 'n4', 'n5']].values.ravel()
        freq = pd.Series(numeros).value_counts()
        for n in freq.index:
            if n % 2 == 0 and n not in exclude:
                return n

    def _get_next_larger_frequent(self, exclude):
        numeros = self.df[['n1', 'n2', 'n3', 'n4', 'n5']].values.ravel()
        freq = pd.Series(numeros).value_counts()
        for n in freq.index:
            if n > max(exclude) and n not in exclude:
                return n
        return None  # Retorna None si no se encuentra un número más grande

    def _get_next_smaller_frequent(self, exclude):
        numeros = self.df[['n1', 'n2', 'n3', 'n4', 'n5']].values.ravel()
        freq = pd.Series(numeros).value_counts()
        for n in reversed(freq.index):
            if n < min(exclude) and n not in exclude:
                return n
        return None  # Retorna None si no se encuentra un número más pequeño

    def _get_number_from_underrepresented_decade(self, exclude):
        numeros = self.df[['n1', 'n2', 'n3', 'n4', 'n5']].values.ravel()
        freq = pd.Series(numeros).value_counts()
        decenas_actuales = [(n-1)//10 for n in exclude]
        for n in freq.index:
            if (n-1)//10 not in decenas_actuales and n not in exclude:
                return n

    def _analizar_prediccion(self, numeros, estrellas):
        # Analizar paridad
        pares = sum(1 for n in numeros if n % 2 == 0)
        impares = 5 - pares
        print(f"Paridad: {pares} pares, {impares} impares")
        
        # Analizar suma
        suma = sum(numeros)
        print(f"Suma de los números: {suma}")
        
        # Analizar distribución por decenas
        decenas = [(n-1)//10 for n in numeros]
        dec_dist = pd.Series(decenas).value_counts().sort_index()
        print("Distribución por decenas:")
        for dec in range(5):
            print(f"  {dec}0-{dec}9: {dec_dist.get(dec, 0)}")
        
        # Analizar estrellas
        print(f"Suma de las estrellas: {sum(estrellas)}")

    def evaluate_combination(self, numbers, stars):
        """Evalúa una combinación específica."""
        print("\n📊 EVALUACIÓN DE LA COMBINACIÓN")
        
        # Comparar con números calientes
        hot_nums = set(self.get_hot_numbers())
        hot_matches = set(numbers) & hot_nums
        
        # Comparar con números fríos
        cold_nums = set(self.get_cold_numbers())
        cold_matches = set(numbers) & cold_nums
        
        print(f"\nNúmeros calientes incluidos: {len(hot_matches)}")
        print(f"Números fríos incluidos: {len(cold_matches)}")
        
        # Calcular score
        score = (len(hot_matches) * 20 + len(cold_matches) * 15)
        print(f"\nScore de la combinación: {score}/100")
        
        if score >= 75:
            print("✅ Combinación muy prometedora")
        elif score >= 50:
            print("📊 Combinación con potencial medio")
        else:
            print("⚠️ Combinación con bajo potencial histórico")
        
        return score

