import pandas as pd
import numpy as np
from tabulate import tabulate
from datetime import datetime, timedelta
import calendar
import seaborn as sns
import matplotlib.pyplot as plt

class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def analyze_number(self, number):
        """Análisis detallado de un número específico."""
        print(f"\n📊 ANÁLISIS DEL NÚMERO {number}")
        
        # Frecuencia total
        frecuencia = sum((self.df[col] == number).sum() for col in ['n1', 'n2', 'n3', 'n4', 'n5'])
        porcentaje = round(frecuencia/len(self.df)*100, 2)
        print(f"\nFrecuencia total: {frecuencia} apariciones ({porcentaje}% de los sorteos)")

        # Última aparición
        ultima_aparicion = None
        for _, row in self.df.iterrows():
            if number in [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]:
                ultima_aparicion = row['fecha']
                break
        
        if ultima_aparicion:
            dias_sin_salir = (self.df.iloc[0]['fecha'] - ultima_aparicion).days
            print(f"Última aparición: {ultima_aparicion.strftime('%d-%m-%Y')} ({dias_sin_salir} días)")

        # Posiciones más frecuentes
        posiciones = []
        for pos in ['n1', 'n2', 'n3', 'n4', 'n5']:
            freq = (self.df[pos] == number).sum()
            if freq > 0:
                posiciones.append([pos, freq])
        
        print("\nPosiciones más frecuentes:")
        print(tabulate(posiciones, headers=['Posición', 'Frecuencia'], tablefmt='pretty'))

    def analyze_combination(self, numbers, stars):
        """Análisis completo de una combinación."""
        print("\n🔍 ANÁLISIS DE COMBINACIÓN")
        print(f"\nNúmeros: {' - '.join(map(str, sorted(numbers)))}")
        print(f"Estrellas: {' - '.join(map(str, sorted(stars)))}")

        self._analyze_frequency(numbers, stars)
        self._analyze_patterns(numbers)
        self._analyze_historical(numbers, stars)
        return self._calculate_score(numbers, stars)

    def _analyze_frequency(self, numbers, stars):
        """Análisis de frecuencia de números y estrellas."""
        print("\n1️⃣ ANÁLISIS DE FRECUENCIA")
        
        # Análisis de números
        results = []
        for num in numbers:
            freq = sum((self.df[col] == num).sum() for col in ['n1', 'n2', 'n3', 'n4', 'n5'])
            porcentaje = round(freq/len(self.df)*100, 2)
            results.append([num, freq, porcentaje])
        
        print("\nFrecuencia de números:")
        print(tabulate(results, 
                      headers=['Número', 'Apariciones', '% Sorteos'],
                      tablefmt='pretty'))

        # Análisis de estrellas
        star_results = []
        for star in stars:
            freq = sum((self.df[col] == star).sum() for col in ['e1', 'e2'])
            porcentaje = round(freq/len(self.df)*100, 2)
            star_results.append([star, freq, porcentaje])
        
        print("\nFrecuencia de estrellas:")
        print(tabulate(star_results,
                      headers=['Estrella', 'Apariciones', '% Sorteos'],
                      tablefmt='pretty'))

    def _analyze_patterns(self, numbers):
        """Análisis de patrones en la combinación."""
        print("\n2️⃣ ANÁLISIS DE PATRONES")
        
        # Paridad
        pares = sum(1 for n in numbers if n % 2 == 0)
        impares = len(numbers) - pares
        print(f"\nParidad: {pares} pares, {impares} impares")
        
        # Distribución por decenas
        decenas = [(n-1)//10 for n in numbers]
        dec_dist = pd.Series(decenas).value_counts()
        
        print("\nDistribución por decenas:")
        for dec in range(5):
            count = dec_dist.get(dec, 0)
            rango = f"{dec*10+1}-{(dec+1)*10}"
            print(f"{rango}: {count} números")
        
        # Suma total
        suma = sum(numbers)
        print(f"\nSuma total: {suma}")
        if 100 <= suma <= 150:
            print("✅ Suma en rango óptimo")
        else:
            print("⚠️ Suma fuera del rango típico ganador")
        
        # Consecutivos
        nums_sorted = sorted(numbers)
        consecutivos = sum(1 for i in range(len(nums_sorted)-1) 
                         if nums_sorted[i+1] - nums_sorted[i] == 1)
        print(f"\nNúmeros consecutivos: {consecutivos}")

    def _analyze_historical(self, numbers, stars):
        """Análisis histórico de la combinación."""
        print("\n3️⃣ ANÁLISIS HISTÓRICO")
        
        # Verificar si la combinación ha salido antes
        combinaciones_similares = 0
        coincidencias_maximas = 0
        fecha_similar = None
        
        for _, row in self.df.iterrows():
            nums_sorteo = set([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']])
            nums_check = set(numbers)
            coincidencias = len(nums_check & nums_sorteo)
            
            if coincidencias > coincidencias_maximas:
                coincidencias_maximas = coincidencias
                fecha_similar = row['fecha']
            
            if coincidencias >= 4:
                combinaciones_similares += 1

        print(f"\nMáximas coincidencias encontradas: {coincidencias_maximas} números")
        if fecha_similar:
            print(f"Fecha: {fecha_similar.strftime('%d-%m-%Y')}")
        
        if combinaciones_similares > 0:
            print(f"\nCombinaciones similares (4+ números): {combinaciones_similares}")

    def _calculate_score(self, numbers, stars):
        """Calcula un score para la combinación."""
        score = 0
        
        # Factor de frecuencia
        for num in numbers:
            freq = sum((self.df[col] == num).sum() for col in ['n1', 'n2', 'n3', 'n4', 'n5'])
            score += min(freq/len(self.df)*100, 20)  # Máximo 20 puntos por número
        
        # Factor de paridad
        pares = sum(1 for n in numbers if n % 2 == 0)
        if 2 <= pares <= 3:
            score += 10
        
        # Factor de suma
        suma = sum(numbers)
        if 100 <= suma <= 150:
            score += 10
        
        # Factor de distribución por decenas
        decenas = pd.Series([(n-1)//10 for n in numbers]).value_counts()
        if len(decenas) >= 3:  # Números bien distribuidos
            score += 10
        
        # Normalizar score
        score = min(100, score)
        
        print(f"\n📈 SCORE FINAL: {round(score, 2)}/100")
        
        if score >= 75:
            print("🌟 Combinación muy prometedora")
        elif score >= 50:
            print("✅ Combinación aceptable")
        else:
            print("⚠️ Combinación con baja probabilidad histórica")
        
        return round(score, 2)

    def analyze_last_draws(self, n=10):
        """Analiza los últimos N sorteos."""
        print(f"\n📅 ÚLTIMOS {n} SORTEOS")
        
        ultimos = self.df.head(n)
        results = []
        
        for _, row in ultimos.iterrows():
            numeros = sorted([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']])
            estrellas = sorted([row['e1'], row['e2']])
            results.append([
                row['fecha'].strftime('%d-%m-%Y'),
                ' - '.join(map(str, numeros)),
                ' - '.join(map(str, estrellas))
            ])
        
        print(tabulate(results,
                      headers=['Fecha', 'Números', 'Estrellas'],
                      tablefmt='pretty'))

    def get_statistics(self):
        """Retorna estadísticas generales."""
        stats = {
            'total_sorteos': len(self.df),
            'primer_sorteo': self.df.iloc[-1]['fecha'].strftime('%d-%m-%Y'),
            'ultimo_sorteo': self.df.iloc[0]['fecha'].strftime('%d-%m-%Y')
        }
        
        # Números más frecuentes
        todos_numeros = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            todos_numeros.extend(self.df[col].tolist())
        
        freq = pd.Series(todos_numeros).value_counts()
        stats['numero_mas_frecuente'] = freq.index[0]
        stats['numero_menos_frecuente'] = freq.index[-1]
        
        return stats

    def analyze_monthly_trends(self):
        """Analiza tendencias mensuales."""
        print("\n📊 TENDENCIAS MENSUALES")
        
        self.df['mes'] = self.df['fecha'].dt.month
        monthly_counts = self.df.groupby('mes').size().reset_index(name='conteo')
        monthly_counts['mes'] = monthly_counts['mes'].apply(lambda x: calendar.month_abbr[x])
        
        print(tabulate(monthly_counts, headers=['Mes', 'Número de sorteos'], tablefmt='pretty'))
        
        # Análisis de números por mes
        numeros_por_mes = {}
        for mes in range(1, 13):
            sorteos_mes = self.df[self.df['mes'] == mes]
            numeros_mes = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros_mes.extend(sorteos_mes[col].tolist())
            
            total_numeros = len(numeros_mes)
            freq = pd.Series(numeros_mes).value_counts()
            top_5 = freq.head(5)
            
            numeros_por_mes[calendar.month_abbr[mes]] = [
                (num, count, round(count/total_numeros*100, 2))
                for num, count in top_5.items()
            ]
        
        print("\nNúmeros más frecuentes por mes:")
        headers = ['Mes', 'Top 5 números (Número, Apariciones, % del mes)']
        data = [
            (mes, ', '.join([f"{num}({count}, {pct}%)" for num, count, pct in info]))
            for mes, info in numeros_por_mes.items()
        ]
        print(tabulate(data, headers=headers, tablefmt='pretty'))

    def analyze_seasonal_trends(self):
        """Analiza tendencias por estaciones."""
        print("\n🌞 ANÁLISIS POR ESTACIONES")
        
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Invierno'
            elif month in [3, 4, 5]:
                return 'Primavera'
            elif month in [6, 7, 8]:
                return 'Verano'
            else:
                return 'Otoño'
        
        self.df['estacion'] = self.df['fecha'].dt.month.apply(get_season)
        seasonal_counts = self.df.groupby('estacion').size().reset_index(name='conteo')
        
        print(tabulate(seasonal_counts, headers=['Estación', 'Número de sorteos'], tablefmt='pretty'))
        
        # Análisis de números por estación
        numeros_por_estacion = {}
        for estacion in ['Primavera', 'Verano', 'Otoño', 'Invierno']:
            numeros_estacion = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros_estacion.extend(self.df[self.df['estacion'] == estacion][col].tolist())
            total_numeros = len(numeros_estacion)
            freq = pd.Series(numeros_estacion).value_counts().head(5)
            numeros_por_estacion[estacion] = [
                (num, count, round(count/total_numeros*100, 2))
                for num, count in freq.items()
            ]
        
        print("\nNúmeros más frecuentes por estación:")
        headers = ['Estación', 'Top 5 números (Número, Apariciones, % de la estación)']
        data = [
            (estacion, ', '.join([f"{num}({count}, {pct}%)" for num, count, pct in info]))
            for estacion, info in numeros_por_estacion.items()
        ]
        print(tabulate(data, headers=headers, tablefmt='pretty'))

    def compare_current_vs_previous_year(self):
        """Compara el año actual con el anterior."""
        print("\n📅 COMPARACIÓN AÑO ACTUAL VS ANTERIOR")
        
        current_year = datetime.now().year
        df_current = self.df[self.df['fecha'].dt.year == current_year]
        df_previous = self.df[self.df['fecha'].dt.year == current_year - 1]
        
        def get_top_numbers(df):
            numeros = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros.extend(df[col].tolist())
            total_numeros = len(numeros)
            freq = pd.Series(numeros).value_counts().head(10)
            return [(num, count, round(count/total_numeros*100, 2)) for num, count in freq.items()]
        
        top_current = get_top_numbers(df_current)
        top_previous = get_top_numbers(df_previous)
        
        print(f"Top 10 números más frecuentes en {current_year}:")
        for num, count, pct in top_current:
            print(f"Número {num}: {count} apariciones ({pct}%)")
        
        print(f"\nTop 10 números más frecuentes en {current_year-1}:")
        for num, count, pct in top_previous:
            print(f"Número {num}: {count} apariciones ({pct}%)")
        
        common_numbers = set([num for num, _, _ in top_current]) & set([num for num, _, _ in top_previous])
        print(f"\nNúmeros comunes en ambos años: {', '.join(map(str, common_numbers))}")

    def analyze_weekday_trends(self):
        """Analiza tendencias por día de la semana."""
        print("\n📆 ANÁLISIS POR DÍA DE LA SEMANA")
        
        self.df['dia_semana'] = self.df['fecha'].dt.dayofweek
        weekday_counts = self.df.groupby('dia_semana').size().reset_index(name='conteo')
        weekday_counts['dia_semana'] = weekday_counts['dia_semana'].apply(lambda x: calendar.day_name[x])
        
        print(tabulate(weekday_counts, headers=['Día', 'Número de sorteos'], tablefmt='pretty'))
        
        # Análisis de números por día de la semana
        numeros_por_dia = {}
        for dia in range(7):
            numeros_dia = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros_dia.extend(self.df[self.df['dia_semana'] == dia][col].tolist())
            total_numeros = len(numeros_dia)
            freq = pd.Series(numeros_dia).value_counts().head(5)
            numeros_por_dia[calendar.day_name[dia]] = [
                (num, count, round(count/total_numeros*100, 2))
                for num, count in freq.items()
            ]
        
        print("\nNúmeros más frecuentes por día de la semana:")
        headers = ['Día', 'Top 5 números (Número, Apariciones, % del día)']
        data = [
            (dia, ', '.join([f"{num}({count}, {pct}%)" for num, count, pct in info]))
            for dia, info in numeros_por_dia.items()
        ]
        print(tabulate(data, headers=headers, tablefmt='pretty'))

    def analyze_patterns(self):
        """Analiza patrones en los resultados históricos."""
        print("\n🔄 ANÁLISIS DE PATRONES")
        
        # Analizar paridad
        pares_impares = []
        for _, row in self.df.iterrows():
            numeros = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            pares = sum(1 for n in numeros if n % 2 == 0)
            impares = 5 - pares
            pares_impares.append([pares, impares])
        
        df_paridad = pd.DataFrame(pares_impares, columns=['Pares', 'Impares'])
        patron_paridad = df_paridad.mode().iloc[0]
        print(f"Patrón de paridad más común: {patron_paridad['Pares']} pares, {patron_paridad['Impares']} impares")
        
        # Distribución de paridad
        dist_paridad = df_paridad.value_counts(normalize=True) * 100
        print("\nDistribución de paridad:")
        for (pares, impares), porcentaje in dist_paridad.items():
            print(f"{pares} pares, {impares} impares: {porcentaje:.2f}%")

        # Analizar distribución por decenas
        decenas_dist = []
        for _, row in self.df.iterrows():
            numeros = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            decenas = [(n-1)//10 for n in numeros]
            decenas_dist.append(pd.Series(decenas).value_counts())
        
        print("\nDistribución promedio por decenas:")
        decenas_promedio = pd.DataFrame(decenas_dist).mean().sort_values(ascending=False)
        for dec, valor in decenas_promedio.items():
            print(f"Decena {dec*10+1}-{(dec+1)*10}: {valor:.2f} números")

        # Analizar suma total
        sumas = self.df[['n1', 'n2', 'n3', 'n4', 'n5']].sum(axis=1)
        print(f"\nSuma total promedio: {sumas.mean():.2f}")
        print(f"Rango de suma más común: {sumas.mode().values[0]}")
        
        # Analizar números consecutivos
        def contar_consecutivos(numeros):
            return sum(1 for i in range(len(numeros)-1) if numeros[i+1] - numeros[i] == 1)
        
        consecutivos = self.df.apply(lambda row: contar_consecutivos(sorted([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']])), axis=1)
        print("\nFrecuencia de números consecutivos:")
        freq_consecutivos = consecutivos.value_counts(normalize=True) * 100
        for n_consec, porcentaje in freq_consecutivos.sort_index().items():
            print(f"{n_consec} consecutivos: {porcentaje:.2f}%")

    def analyze_correlations(self):
        """Analiza correlaciones entre números y otros factores de forma comprensible."""
        print("\n🔗 ANÁLISIS DE CORRELACIONES")
        
        # Preparar datos
        numeros = pd.DataFrame()
        for i in range(1, 6):
            numeros[f'n{i}'] = self.df[f'n{i}']
        
        # Correlación entre números
        corr_matrix = numeros.corr()
        
        print("\nRelación entre posiciones de números:")
        for i in range(1, 6):
            for j in range(i+1, 6):
                corr = corr_matrix.loc[f'n{i}', f'n{j}']
                interpretacion = self.interpretar_correlacion(corr)
                print(f"- Entre la posición {i} y {j}: {interpretacion}")
        
        # Correlación con factores temporales
        numeros['mes'] = self.df['fecha'].dt.month
        numeros['dia_semana'] = self.df['fecha'].dt.dayofweek
        
        corr_temporal = numeros.corr()[['mes', 'dia_semana']].iloc[:-2]
        
        print("\nRelación con factores temporales:")
        for factor in ['mes', 'dia_semana']:
            for i in range(1, 6):
                corr = corr_temporal.loc[f'n{i}', factor]
                interpretacion = self.interpretar_correlacion(corr)
                print(f"- Número en posición {i} y {factor}: {interpretacion}")
        
        # Análisis de números adyacentes
        def numeros_adyacentes(row):
            nums = sorted([row[f'n{i}'] for i in range(1, 6)])
            return sum(1 for i in range(len(nums)-1) if nums[i+1] - nums[i] == 1)
        
        numeros['adyacentes'] = self.df.apply(numeros_adyacentes, axis=1)
        
        print("\nFrecuencia de números adyacentes:")
        freq_adyacentes = numeros['adyacentes'].value_counts(normalize=True) * 100
        for n_adj, porcentaje in freq_adyacentes.sort_index().items():
            print(f"{n_adj} números adyacentes: {porcentaje:.2f}%")
        
        # Visualización simplificada
        self.visualizar_correlaciones_simplificadas(corr_matrix)

    def interpretar_correlacion(self, valor):
        """Interpreta el valor de correlación de forma comprensible."""
        if abs(valor) < 0.1:
            return "No hay relación aparente"
        elif abs(valor) < 0.3:
            return "Hay una relación débil"
        elif abs(valor) < 0.5:
            return "Hay una relación moderada"
        else:
            return "Hay una relación fuerte"

    def visualizar_correlaciones_simplificadas(self, corr_matrix):
        """Crea una visualización muy simplificada de las relaciones entre posiciones."""
        plt.figure(figsize=(10, 8))
        
        # Crear una matriz de texto para las relaciones
        relaciones = np.array([[self.simplificar_correlacion(val) for val in row] for row in corr_matrix.values])
        
        # Crear un mapa de colores personalizado
        colors = {'Fuerte +': '#1a9850', 'Moderada +': '#91cf60', 'Débil +': '#d9ef8b',
                  'Sin relación': '#ffffbf',
                  'Débil -': '#fee08b', 'Moderada -': '#fc8d59', 'Fuerte -': '#d73027'}
        
        # Convertir la matriz de texto a una matriz numérica para la visualización
        num_matrix = np.array([[list(colors.keys()).index(val) for val in row] for row in relaciones])
        
        plt.imshow(num_matrix, cmap=plt.cm.RdYlGn, aspect='auto', vmin=-3, vmax=3)
        
        # Añadir texto a cada celda
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                plt.text(j, i, relaciones[i, j], ha="center", va="center", color="black", fontweight='bold')
        
        plt.title('Relación entre las posiciones de los números', fontsize=16)
        plt.xlabel('Posición del número', fontsize=12)
        plt.ylabel('Posición del número', fontsize=12)
        
        # Personalizar los ticks de los ejes
        positions = ['1ª', '2ª', '3ª', '4ª', '5ª']
        plt.xticks(range(len(positions)), positions)
        plt.yticks(range(len(positions)), positions)
        
        # Añadir una leyenda personalizada
        handles = [plt.Rectangle((0,0),1,1, color=color) for color in colors.values()]
        plt.legend(handles, colors.keys(), title="Fuerza de la relación", 
                   loc='center left', bbox_to_anchor=(1, 0.5))
        
        plt.tight_layout()
        plt.show()

    def simplificar_correlacion(self, valor):
        """Simplifica el valor de correlación para la visualización."""
        if abs(valor) < 0.1:
            return "Sin relación"
        elif abs(valor) < 0.3:
            return "Débil +" if valor > 0 else "Débil -"
        elif abs(valor) < 0.5:
            return "Moderada +" if valor > 0 else "Moderada -"
        else:
            return "Fuerte +" if valor > 0 else "Fuerte -"

    def analyze_stars(self):
        """Analiza las estrellas en los resultados del Euromillones."""
        print("\n⭐ ANÁLISIS DE ESTRELLAS")
        
        # Frecuencia de las estrellas
        estrellas = []
        for col in ['e1', 'e2']:
            estrellas.extend(self.df[col].tolist())
        
        freq_estrellas = pd.Series(estrellas).value_counts().sort_index()
        total_sorteos = len(self.df)
        
        print("\nFrecuencia de aparición de las estrellas:")
        datos_estrellas = []
        for estrella, freq in freq_estrellas.items():
            porcentaje = (freq / (total_sorteos * 2)) * 100
            datos_estrellas.append([estrella, freq, f"{porcentaje:.2f}%"])
        
        print(tabulate(datos_estrellas, 
                       headers=['Estrella', 'Apariciones', '% de Sorteos'],
                       tablefmt='pretty'))

        # Combinaciones más frecuentes de estrellas
        combinaciones = self.df.groupby(['e1', 'e2']).size().sort_values(ascending=False)
        
        print("\nCombinaciones de estrellas más frecuentes:")
        datos_combinaciones = []
        for (e1, e2), freq in combinaciones.head(10).items():
            porcentaje = (freq / total_sorteos) * 100
            datos_combinaciones.append([f"{e1} - {e2}", freq, f"{porcentaje:.2f}%"])
        
        print(tabulate(datos_combinaciones, 
                       headers=['Combinación', 'Apariciones', '% de Sorteos'],
                       tablefmt='pretty'))

        # Análisis de tendencias recientes
        ultimos_sorteos = self.df.head(20)
        estrellas_recientes = []
        for col in ['e1', 'e2']:
            estrellas_recientes.extend(ultimos_sorteos[col].tolist())
        
        freq_recientes = pd.Series(estrellas_recientes).value_counts()
        
        print("\nTendencias recientes de estrellas (últimos 20 sorteos):")
        datos_recientes = []
        for estrella in range(1, 13):
            freq_reciente = freq_recientes.get(estrella, 0)
            freq_total = freq_estrellas.get(estrella, 0)
            tendencia = ((freq_reciente / 40) / (freq_total / (total_sorteos * 2)) - 1) * 100
            datos_recientes.append([estrella, freq_reciente, f"{tendencia:+.2f}%"])
        
        print(tabulate(datos_recientes, 
                       headers=['Estrella', 'Apariciones Recientes', 'Tendencia'],
                       tablefmt='pretty'))

        # Visualización de la frecuencia de las estrellas
        plt.figure(figsize=(12, 6))
        freq_estrellas.plot(kind='bar')
        plt.title('Frecuencia de aparición de las estrellas')
        plt.xlabel('Estrella')
        plt.ylabel('Número de apariciones')
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()
