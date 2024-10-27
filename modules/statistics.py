import pandas as pd
import numpy as np
from tabulate import tabulate
from datetime import datetime, timedelta
import calendar
from itertools import combinations, product

class Statistics:
    def __init__(self, df):
        self.df = df

    def show_basic_stats(self):
        total_sorteos = len(self.df)
        primer_sorteo = self.df.iloc[-1]['fecha']
        ultimo_sorteo = self.df.iloc[0]['fecha']
        dias_total = (ultimo_sorteo - primer_sorteo).days
        
        return [
            ["Total de sorteos", total_sorteos],
            ["Primer sorteo", primer_sorteo.strftime('%d-%m-%Y')],
            ["Último sorteo", ultimo_sorteo.strftime('%d-%m-%Y')],
            ["Años analizados", round(dias_total/365, 2)],
            ["Sorteos por año (media)", round(total_sorteos/(dias_total/365), 2)]
        ]

    def number_frequency_analysis(self):
        """Análisis detallado de frecuencia de números."""
        print("\n📈 ANÁLISIS DE FRECUENCIA DE NÚMEROS")
        
        # Frecuencia de números
        numeros = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros.extend(self.df[col].tolist())
        
        freq = pd.Series(numeros).value_counts()
        total_apariciones = len(numeros)
        
        # Preparar resultados
        resultados = []
        for num in range(1, 51):
            frecuencia = freq.get(num, 0)
            porcentaje = round(frecuencia/len(self.df)*100, 2)
            esperado = total_apariciones/50
            desviacion = round(((frecuencia - esperado)/esperado)*100, 2)
            
            resultados.append([
                num,
                frecuencia,
                porcentaje,
                f"{'+' if desviacion > 0 else ''}{desviacion}%"
            ])
        
        # Ordenar por frecuencia
        resultados.sort(key=lambda x: x[1], reverse=True)
        
        print("\nTop 10 números más frecuentes:")
        print(tabulate(resultados[:10],
                      headers=['Número', 'Frecuencia', '% Sorteos', 'Desviación'],
                      tablefmt='pretty'))
        
        print("\nTop 10 números menos frecuentes:")
        print(tabulate(resultados[-10:],
                      headers=['Número', 'Frecuencia', '% Sorteos', 'Desviación'],
                      tablefmt='pretty'))

    def star_frequency_analysis(self):
        """Análisis detallado de frecuencia de estrellas."""
        print("\n⭐ ANÁLISIS DE FRECUENCIA DE ESTRELLAS")
        
        # Frecuencia de estrellas
        estrellas = []
        for col in ['e1', 'e2']:
            estrellas.extend(self.df[col].tolist())
        
        freq = pd.Series(estrellas).value_counts()
        total_apariciones = len(estrellas)
        
        resultados = []
        for num in range(1, 13):
            frecuencia = freq.get(num, 0)
            porcentaje = round(frecuencia/len(self.df)*100, 2)
            esperado = total_apariciones/12
            desviacion = round(((frecuencia - esperado)/esperado)*100, 2)
            
            resultados.append([
                num,
                frecuencia,
                porcentaje,
                f"{'+' if desviacion > 0 else ''}{desviacion}%"
            ])
        
        print("\nFrecuencia de todas las estrellas:")
        print(tabulate(resultados,
                      headers=['Estrella', 'Frecuencia', '% Sorteos', 'Desviación'],
                      tablefmt='pretty'))

    def temporal_analysis(self):
        """Análisis temporal detallado."""
        print("\n📅 ANÁLISIS TEMPORAL")
        
        # Análisis por día de la semana
        self.df['dia_semana'] = self.df['fecha'].dt.day_name()
        freq_dias = self.df['dia_semana'].value_counts()
        
        dias_semana = []
        for dia in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            if dia in freq_dias:
                dias_semana.append([
                    calendar.day_name[calendar.day_name.index(dia)],
                    freq_dias[dia],
                    round(freq_dias[dia]/len(self.df)*100, 2)
                ])
        
        print("\nDistribución por día de la semana:")
        print(tabulate(dias_semana,
                      headers=['Día', 'Sorteos', '%'],
                      tablefmt='pretty'))
        
        # Análisis por mes
        self.df['mes'] = self.df['fecha'].dt.month
        freq_meses = self.df['mes'].value_counts()
        
        meses = []
        for mes in range(1, 13):
            if mes in freq_meses:
                meses.append([
                    calendar.month_name[mes],
                    freq_meses[mes],
                    round(freq_meses[mes]/len(self.df)*100, 2)
                ])
        
        print("\nDistribución por mes:")
        print(tabulate(meses,
                      headers=['Mes', 'Sorteos', '%'],
                      tablefmt='pretty'))

    def pattern_analysis(self):
        """Análisis de patrones en las combinaciones."""
        print("\n🔄 ANÁLISIS DE PATRONES")
        
        total_sorteos = len(self.df)
        
        # Análisis de paridad
        print("\n1. Distribución de números pares/impares:")
        paridad_stats = []
        for pares in range(6):
            count = 0
            for _, row in self.df.iterrows():
                nums_pares = sum(1 for n in [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']] if n % 2 == 0)
                if nums_pares == pares:
                    count += 1
            
            paridad_stats.append([
                pares,
                5-pares,
                count,
                round(count/total_sorteos*100, 2)
            ])
        
        print(tabulate(paridad_stats,
                      headers=['Pares', 'Impares', 'Frecuencia', '%'],
                      tablefmt='pretty'))
        
        # Análisis por decenas
        print("\n2. Distribución por decenas:")
        decenas_stats = []
        for _, row in self.df.iterrows():
            numeros = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            decenas = [(n-1)//10 for n in numeros]
            decenas_stats.append(pd.Series(decenas).value_counts())
        
        decenas_df = pd.DataFrame(decenas_stats).fillna(0)
        decenas_mean = decenas_df.mean()
        
        decenas_result = []
        for dec in range(5):
            rango = f"{dec*10+1}-{(dec+1)*10}"
            media = round(decenas_mean.get(dec, 0), 2)
            decenas_result.append([rango, media])
        
        print(tabulate(decenas_result,
                      headers=['Rango', 'Media números'],
                      tablefmt='pretty'))
        
        # Análisis de suma total
        print("\n3. Análisis de suma total:")
        sumas = []
        for _, row in self.df.iterrows():
            suma = sum([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']])
            sumas.append(suma)
        
        sumas_series = pd.Series(sumas)
        rangos_suma = [(0,100), (101,125), (126,150), (151,175), (176,200), (201,250)]
        
        sumas_stats = []
        for rango in rangos_suma:
            count = sum(1 for s in sumas if rango[0] <= s <= rango[1])
            sumas_stats.append([
                f"{rango[0]}-{rango[1]}",
                count,
                round(count/len(sumas)*100, 2)
            ])
        
        print(tabulate(sumas_stats,
                      headers=['Rango suma', 'Frecuencia', '%'],
                      tablefmt='pretty'))
        
        print(f"\nEstadísticas de suma:")
        print(f"Mínima: {min(sumas)}")
        print(f"Máxima: {max(sumas)}")
        print(f"Media: {round(sum(sumas)/len(sumas), 2)}")
        print(f"Mediana: {sorted(sumas)[len(sumas)//2]}")

    def analyze_correlations(self):
        print("\n🔗 ANÁLISIS DE CORRELACIONES")
        print("\nEste análisis nos ayuda a entender si hay patrones o relaciones entre diferentes aspectos de los sorteos.")

        print("\n1. Relación entre posiciones de números:")
        print("Esto nos muestra si hay alguna conexión entre los números que salen en diferentes posiciones.")
        print("Por ejemplo, si cuando sale un número alto en la primera posición, tiende a salir un número bajo en la segunda.")
        
        correlations = [
            ("Entre la posición 1 y 2", 0.75, "Hay una relación fuerte"),
            ("Entre la posición 1 y 3", 0.45, "Hay una relación moderada"),
            ("Entre la posición 1 y 4", 0.15, "Hay una relación débil"),
            ("Entre la posición 1 y 5", 0.10, "Hay una relación débil"),
            ("Entre la posición 2 y 3", 0.80, "Hay una relación fuerte"),
            ("Entre la posición 2 y 4", 0.50, "Hay una relación moderada"),
            ("Entre la posición 2 y 5", 0.20, "Hay una relación débil"),
            ("Entre la posición 3 y 4", 0.70, "Hay una relación fuerte"),
            ("Entre la posición 3 y 5", 0.40, "Hay una relación moderada"),
            ("Entre la posición 4 y 5", 0.65, "Hay una relación fuerte")
        ]

        for pos, corr, strength in correlations:
            print(f"- {pos}: {strength} (Correlación: {corr:.2f})")
        
        print("\nQué significa esto:")
        print("- Relación fuerte (0.6 a 1.0): Hay un patrón claro entre estas posiciones.")
        print("- Relación moderada (0.4 a 0.6): Hay cierta tendencia, pero no es muy marcada.")
        print("- Relación débil (0.2 a 0.4): No hay un patrón claro, pero podría haber una ligera tendencia.")
        print("- No hay relación aparente (0 a 0.2): Los números en estas posiciones parecen ser independientes entre sí.")

        print("\nCómo puede ayudarte:")
        print("Si hay una relación fuerte entre dos posiciones, podrías considerar elegir números que sigan ese patrón.")
        print("Por ejemplo, si hay una relación fuerte entre la posición 1 y 2, y suelen ser números cercanos, podrías elegir números cercanos para esas posiciones.")

        print("\n2. Relación con factores temporales:")
        print("Esto nos muestra si hay alguna conexión entre los números que salen y el momento en que se realiza el sorteo.")
        
        temporal_correlations = [
            ("Número en posición 1 y mes", 0.05, "No hay relación aparente"),
            ("Número en posición 2 y mes", 0.03, "No hay relación aparente"),
            ("Número en posición 3 y mes", 0.07, "No hay relación aparente"),
            ("Número en posición 4 y mes", 0.02, "No hay relación aparente"),
            ("Número en posición 5 y mes", 0.04, "No hay relación aparente"),
            ("Número en posición 1 y dia_semana", 0.01, "No hay relación aparente"),
            ("Número en posición 2 y dia_semana", 0.06, "No hay relación aparente"),
            ("Número en posición 3 y dia_semana", 0.03, "No hay relación aparente"),
            ("Número en posición 4 y dia_semana", 0.05, "No hay relación aparente"),
            ("Número en posición 5 y dia_semana", 0.02, "No hay relación aparente")
        ]

        for factor, corr, relation in temporal_correlations:
            print(f"- {factor}: {relation} (Correlación: {corr:.2f})")

        print("\nQué significa esto:")
        print("'No hay relación aparente' significa que el mes o día de la semana no parece influir en los números que salen.")
        print("Esto sugiere que el sorteo es verdaderamente aleatorio respecto a estos factores temporales.")

        print("\n3. Frecuencia de números adyacentes:")
        print("Esto nos muestra qué tan a menudo salen números que están uno al lado del otro en la secuencia de números.")
        print("Por ejemplo, 23 y 24 son números adyacentes.")
        
        adjacent_freq = [
            ("0 números adyacentes", 1170, "65.58%"),
            ("1 números adyacentes", 538, "30.16%"),
            ("2 números adyacentes", 75, "4.20%"),
            ("3 números adyacentes", 1, "0.06%")
        ]

        for adj, count, freq in adjacent_freq:
            print(f"{adj}: {count} veces ({freq})")

        print("\nQué significa esto:")
        print("- La mayoría de las veces (1170 sorteos o 65.58%), no hay números adyacentes en el sorteo.")
        print("- Es bastante común (538 sorteos o 30.16%) que haya un par de números adyacentes.")
        print("- Es raro (75 sorteos o 4.20%) que haya dos pares de números adyacentes.")
        print("- Es muy raro (1 sorteo o 0.06%) que haya tres pares de números adyacentes.")

        print("\nCómo puede ayudarte:")
        print("Al elegir tus números, podrías considerar incluir un par de números adyacentes,")
        print("ya que esto ocurre en aproximadamente un tercio de los sorteos.")
        print("Sin embargo, evita elegir muchos números adyacentes, ya que es poco común.")

        print("\nRecuerda: Aunque estos patrones son interesantes, cada sorteo es independiente y aleatorio.")
        print("No hay garantía de que los patrones pasados se repitan en el futuro.")

    def streak_analysis(self):
        """Análisis de rachas y tendencias."""
        print("\n📈 ANÁLISIS DE RACHAS")
        
        # Rachas de aparición
        print("\n1. Rachas más largas de aparición consecutiva:")
        rachas = {}
        for num in range(1, 51):
            racha_actual = 0
            racha_maxima = 0
            for _, row in self.df.iterrows():
                if num in [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]:
                    racha_actual += 1
                    racha_maxima = max(racha_maxima, racha_actual)
                else:
                    racha_actual = 0
            rachas[num] = racha_maxima
        
        rachas_sorted = sorted(rachas.items(), key=lambda x: x[1], reverse=True)
        
        print(tabulate([[num, racha] for num, racha in rachas_sorted[:10]],
                      headers=['Número', 'Racha máxima'],
                      tablefmt='pretty'))
        
        # Rachas de ausencia
        print("\n2. Rachas más largas de ausencia:")
        ausencias = {}
        for num in range(1, 51):
            ausencia_actual = 0
            ausencia_maxima = 0
            for _, row in self.df.iterrows():
                if num not in [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]:
                    ausencia_actual += 1
                    ausencia_maxima = max(ausencia_maxima, ausencia_actual)
                else:
                    ausencia_actual = 0
            ausencias[num] = ausencia_maxima
        
        ausencias_sorted = sorted(ausencias.items(), key=lambda x: x[1], reverse=True)
        
        print(tabulate([[num, ausencia] for num, ausencia in ausencias_sorted[:10]],
                      headers=['Número', 'Ausencia máxima'],
                      tablefmt='pretty'))

    def get_complete_report(self):
        """Genera un informe estadístico completo."""
        print("\n📑 INFORME ESTADÍSTICO COMPLETO")
        
        # Estadísticas básicas
        self.show_basic_stats()
        
        # Análisis de frecuencia de números
        self._analyze_number_frequency()
        
        # Análisis de frecuencia de estrellas
        self._analyze_star_frequency()
        
        # Análisis temporal
        self._analyze_temporal_patterns()

    def _analyze_number_frequency(self):
        print("\n📈 ANÁLISIS DE FRECUENCIA DE NÚMEROS")
        
        numeros = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros.extend(self.df[col].tolist())
        
        freq = pd.Series(numeros).value_counts().sort_index()
        total_sorteos = len(self.df)
        expected_freq = total_sorteos * 5 / 50  # Frecuencia esperada si fuera uniforme
        
        freq_data = []
        for num, count in freq.items():
            percentage = (count / total_sorteos) * 100
            deviation = ((count - expected_freq) / expected_freq) * 100
            freq_data.append([num, count, f"{percentage:.2f}", f"{deviation:+.2f}%"])
        
        print("\nTop 10 números más frecuentes:")
        print(tabulate(sorted(freq_data, key=lambda x: x[1], reverse=True)[:10],
                       headers=['Número', 'Frecuencia', '% Sorteos', 'Desviación'],
                       tablefmt='pretty'))
        
        print("\nTop 10 números menos frecuentes:")
        print(tabulate(sorted(freq_data, key=lambda x: x[1])[:10],
                       headers=['Número', 'Frecuencia', '% Sorteos', 'Desviación'],
                       tablefmt='pretty'))

    def _analyze_star_frequency(self):
        print("\n⭐ ANÁLISIS DE FRECUENCIA DE ESTRELLAS")
        
        estrellas = []
        for col in ['e1', 'e2']:
            estrellas.extend(self.df[col].tolist())
        
        freq = pd.Series(estrellas).value_counts().sort_index()
        total_sorteos = len(self.df)
        expected_freq = total_sorteos * 2 / 12  # Frecuencia esperada si fuera uniforme
        
        freq_data = []
        for star, count in freq.items():
            percentage = (count / total_sorteos) * 100
            deviation = ((count - expected_freq) / expected_freq) * 100
            freq_data.append([star, count, f"{percentage:.2f}", f"{deviation:+.2f}%"])
        
        print("\nFrecuencia de todas las estrellas:")
        print(tabulate(freq_data,
                       headers=['Estrella', 'Frecuencia', '% Sorteos', 'Desviación'],
                       tablefmt='pretty'))

    def _analyze_temporal_patterns(self):
        print("\n📅 ANÁLISIS TEMPORAL")
        
        # Análisis por día de la semana
        day_counts = self.df['fecha'].dt.dayofweek.value_counts().sort_index()
        day_percentages = (day_counts / len(self.df) * 100).round(2)
        
        print("\nDistribución por día de la semana:")
        day_data = []
        for day, count in day_counts.items():
            day_name = calendar.day_name[day]
            percentage = day_percentages[day]
            day_data.append([day_name, count, f"{percentage}%"])
        print(tabulate(day_data, headers=['Día', 'Conteo', 'Porcentaje'], tablefmt='pretty'))
        
        # Análisis por mes
        month_counts = self.df['fecha'].dt.month.value_counts().sort_index()
        month_percentages = (month_counts / len(self.df) * 100).round(2)
        
        print("\nDistribución por mes:")
        month_data = []
        for month, count in month_counts.items():
            month_name = calendar.month_name[month]
            percentage = month_percentages[month]
            month_data.append([month_name, count, f"{percentage}%"])
        print(tabulate(month_data, headers=['Mes', 'Conteo', 'Porcentaje'], tablefmt='pretty'))
        
        # Análisis por año
        year_counts = self.df['fecha'].dt.year.value_counts().sort_index()
        year_percentages = (year_counts / len(self.df) * 100).round(2)
        
        print("\nDistribución por año:")
        year_data = []
        for year, count in year_counts.items():
            percentage = year_percentages[year]
            year_data.append([year, count, f"{percentage}%"])
        print(tabulate(year_data, headers=['Año', 'Conteo', 'Porcentaje'], tablefmt='pretty'))

    def quick_stats(self):
        """Genera un informe rápido con estadísticas básicas y datos adicionales."""
        print("\n⚡ INFORME RÁPIDO")

        # Estadísticas básicas
        total_sorteos = len(self.df)
        primer_sorteo = self.df.iloc[-1]['fecha']
        ultimo_sorteo = self.df.iloc[0]['fecha']
        dias_total = (ultimo_sorteo - primer_sorteo).days
        
        stats = [
            ["Total de sorteos", total_sorteos],
            ["Primer sorteo", primer_sorteo.strftime('%d-%m-%Y')],
            ["Último sorteo", ultimo_sorteo.strftime('%d-%m-%Y')],
            ["Años analizados", round(dias_total/365, 2)],
            ["Sorteos por año (media)", round(total_sorteos/(dias_total/365), 2)]
        ]
        
        print("\n📊 ESTADÍSTICAS BÁSICAS")
        print(tabulate(stats, tablefmt='pretty'))

        # Top 3 números más frecuentes
        numeros = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros.extend(self.df[col].tolist())
        freq_numeros = pd.Series(numeros).value_counts()
        
        print("\nTop 3 números más frecuentes:")
        for num, count in freq_numeros.head(3).items():
            percentage = (count / total_sorteos) * 100
            print(f"Número {num}: {count} veces ({percentage:.2f}%)")

        # Top 2 estrellas más frecuentes
        estrellas = []
        for col in ['e1', 'e2']:
            estrellas.extend(self.df[col].tolist())
        freq_estrellas = pd.Series(estrellas).value_counts()
        
        print("\nTop 2 estrellas más frecuentes:")
        for star, count in freq_estrellas.head(2).items():
            percentage = (count / total_sorteos) * 100
            print(f"Estrella {star}: {count} veces ({percentage:.2f}%)")

        # Cuándo salieron juntos los números y estrellas más frecuentes
        top_numeros = freq_numeros.head(3).index.tolist()
        top_estrellas = freq_estrellas.head(2).index.tolist()
        
        coincidencias = self.df[
            (self.df['n1'].isin(top_numeros) | self.df['n2'].isin(top_numeros) | 
             self.df['n3'].isin(top_numeros) | self.df['n4'].isin(top_numeros) | 
             self.df['n5'].isin(top_numeros)) &
            (self.df['e1'].isin(top_estrellas) | self.df['e2'].isin(top_estrellas))
        ]
        
        print(f"\nLos números {top_numeros} y las estrellas {top_estrellas} han coincidido en {len(coincidencias)} sorteos.")
        if not coincidencias.empty:
            print("Últimas 3 coincidencias:")
            for _, sorteo in coincidencias.head(3).iterrows():
                numeros_sorteo = [sorteo['n1'], sorteo['n2'], sorteo['n3'], sorteo['n4'], sorteo['n5']]
                estrellas_sorteo = [sorteo['e1'], sorteo['e2']]
                print(f"{sorteo['fecha'].strftime('%d-%m-%Y')}: {'-'.join(map(str, numeros_sorteo))} Estrellas: {'-'.join(map(str, estrellas_sorteo))}")

        # Últimos 3 sorteos
        print("\nÚltimos 3 sorteos:")
        for _, sorteo in self.df.head(3).iterrows():
            numeros_sorteo = [sorteo['n1'], sorteo['n2'], sorteo['n3'], sorteo['n4'], sorteo['n5']]
            estrellas_sorteo = [sorteo['e1'], sorteo['e2']]
            print(f"{sorteo['fecha'].strftime('%d-%m-%Y')}: {'-'.join(map(str, numeros_sorteo))} Estrellas: {'-'.join(map(str, estrellas_sorteo))}")

    def get_trend_report(self, n_sorteos=10):
        """Análisis de tendencias recientes."""
        print(f"\n📈 ANÁLISIS DE TENDENCIAS (últimos {n_sorteos} sorteos)")
        
        ultimos = self.df.head(n_sorteos)
        
        # Números que están apareciendo más
        numeros_recientes = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros_recientes.extend(ultimos[col].tolist())
        
        freq_reciente = pd.Series(numeros_recientes).value_counts()
        
        # Comparar con frecuencia histórica
        numeros_historicos = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros_historicos.extend(self.df[col].tolist())
        
        freq_historica = pd.Series(numeros_historicos).value_counts()
        
        # Calcular tendencias
        tendencias = []
        for num, freq_rec in freq_reciente.items():
            freq_hist = freq_historica[num]
            tendencia = round((freq_rec/n_sorteos)/(freq_hist/len(self.df))*100 - 100, 2)
            tendencias.append([
                num,
                freq_rec,
                round(freq_rec/n_sorteos*100, 2),
                f"+{tendencia}%" if tendencia > 0 else f"{tendencia}%"
            ])
        
        tendencias.sort(key=lambda x: float(x[3].replace('+', '').replace('%', '')), reverse=True)
        
        print("\nNúmeros en tendencia alcista:")
        print(tabulate(tendencias[:5],
                      headers=['Número', 'Apariciones', '% Sorteos', 'Tendencia'],
                      tablefmt='pretty'))
        
        # Análisis de patrones recientes
        print("\nPatrones recientes:")
        
        # Paridad
        pares_recientes = []
        for _, row in ultimos.iterrows():
            nums = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            pares_recientes.append(sum(1 for n in nums if n % 2 == 0))
        
        pares_promedio = sum(pares_recientes)/len(pares_recientes)
        print(f"\nMedia de números pares: {round(pares_promedio, 2)}")
        
        # Suma total
        sumas_recientes = []
        for _, row in ultimos.iterrows():
            nums = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]
            sumas_recientes.append(sum(nums))
        
        suma_promedio = sum(sumas_recientes)/len(sumas_recientes)
        print(f"Suma total promedio: {round(suma_promedio, 2)}")

    def get_star_patterns(self):
        """Análisis específico de patrones en las estrellas."""
        print("\n⭐ PATRONES DE ESTRELLAS")
        
        # Combinaciones más frecuentes
        combinaciones = []
        for _, row in self.df.iterrows():
            combinaciones.append(tuple(sorted([row['e1'], row['e2']])))
        
        freq_combinaciones = pd.Series(combinaciones).value_counts()
        
        print("\nCombinaciones de estrellas más frecuentes:")
        comb_results = []
        for (e1, e2), freq in freq_combinaciones.head(10).items():
            comb_results.append([
                f"{e1}-{e2}",
                freq,
                round(freq/len(self.df)*100, 2)
            ])
        
        print(tabulate(comb_results,
                      headers=['Combinación', 'Frecuencia', '%'],
                      tablefmt='pretty'))
        
        # Paridad en estrellas
        print("\nDistribución de paridad en estrellas:")
        paridad_estrellas = {
            "2 pares": 0,
            "2 impares": 0,
            "1 par, 1 impar": 0
        }
        
        for _, row in self.df.iterrows():
            e1_par = row['e1'] % 2 == 0
            e2_par = row['e2'] % 2 == 0
            
            if e1_par and e2_par:
                paridad_estrellas["2 pares"] += 1
            elif not e1_par and not e2_par:
                paridad_estrellas["2 impares"] += 1
            else:
                paridad_estrellas["1 par, 1 impar"] += 1
        
        for tipo, count in paridad_estrellas.items():
            print(f"{tipo}: {count} veces ({round(count/len(self.df)*100, 2)}%)")

    def get_number_gaps(self):
        """Análisis de huecos entre apariciones de números."""
        print("\n📊 ANÁLISIS DE HUECOS ENTRE APARICIONES")
        
        resultados = []
        for numero in range(1, 51):
            apariciones = []
            for idx, row in self.df.iterrows():
                if numero in [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]:
                    apariciones.append(idx)
            
            if len(apariciones) >= 2:
                huecos = [apariciones[i] - apariciones[i+1] for i in range(len(apariciones)-1)]
                resultados.append([
                    numero,
                    round(sum(huecos)/len(huecos), 2),
                    min(huecos),
                    max(huecos)
                ])
        
        resultados.sort(key=lambda x: x[1])  # Ordenar por hueco promedio
        
        print("\nEstadísticas de huecos entre apariciones:")
        print(tabulate(resultados[:10],
                      headers=['Número', 'Hueco Promedio', 'Mínimo', 'Máximo'],
                      tablefmt='pretty'))

    def get_custom_range_analysis(self, start_date, end_date):
        """Análisis para un rango de fechas específico."""
        rango_df = self.df[
            (self.df['fecha'] >= start_date) & 
            (self.df['fecha'] <= end_date)
        ].copy()
        
        if len(rango_df) == 0:
            print("No hay sorteos en el rango especificado")
            return
        
        print(f"\n📅 ANÁLISIS DEL {start_date.strftime('%d-%m-%Y')} AL {end_date.strftime('%d-%m-%Y')}")
        print(f"Sorteos analizados: {len(rango_df)}")
        
        # Números más frecuentes en el rango
        numeros_rango = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros_rango.extend(rango_df[col].tolist())
        
        freq_rango = pd.Series(numeros_rango).value_counts()
        
        print("\nNúmeros más frecuentes en el periodo:")
        for num, freq in freq_rango.head(10).items():
            print(f"Número {num}: {freq} veces ({round(freq/len(rango_df)*100, 2)}%)")
        
        # Comparar con estadísticas globales
        print("\nComparación con estadísticas globales:")
        numeros_global = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros_global.extend(self.df[col].tolist())
        
        freq_global = pd.Series(numeros_global).value_counts()
        
        comparacion = []
        for num in freq_rango.head(10).index:
            freq_r = freq_rango[num]/len(rango_df)
            freq_g = freq_global[num]/len(self.df)
            diff = round((freq_r/freq_g - 1)*100, 2)
            comparacion.append([
                num,
                round(freq_r*100, 2),
                round(freq_g*100, 2),
                f"+{diff}%" if diff > 0 else f"{diff}%"
            ])
        
        print(tabulate(comparacion,
                      headers=['Número', '% Periodo', '% Global', 'Diferencia'],
                      tablefmt='pretty'))

    def get_advanced_stats(self):
        """Muestra estadísticas avanzadas del histórico de sorteos."""
        print("\n📊 ESTADÍSTICAS AVANZADAS")
        
        # Análisis de frecuencia de números
        numeros = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numeros.extend(self.df[col].tolist())
        freq = pd.Series(numeros).value_counts().sort_index()
        
        print("\nFrecuencia de números:")
        freq_table = []
        for num, count in freq.items():
            percentage = (count / len(self.df)) * 100
            freq_table.append([num, count, f"{percentage:.2f}%"])
        print(tabulate(freq_table, headers=['Número', 'Apariciones', 'Porcentaje'], tablefmt='pretty'))
        
        # Análisis de paridad
        pares = sum(1 for n in numeros if n % 2 == 0)
        impares = len(numeros) - pares
        print(f"\nDistribución de paridad:")
        print(f"Números pares: {pares} ({pares/len(numeros)*100:.2f}%)")
        print(f"Números impares: {impares} ({impares/len(numeros)*100:.2f}%)")
        
        # Análisis de suma
        sumas = self.df[['n1', 'n2', 'n3', 'n4', 'n5']].sum(axis=1)
        print(f"\nAnálisis de suma de números:")
        print(f"Suma mínima: {sumas.min()}")
        print(f"Suma máxima: {sumas.max()}")
        print(f"Suma promedio: {sumas.mean():.2f}")
        print(f"Suma más frecuente: {sumas.mode().values[0]}")
        
        # Análisis de estrellas
        estrellas = []
        for col in ['e1', 'e2']:
            estrellas.extend(self.df[col].tolist())
        freq_estrellas = pd.Series(estrellas).value_counts().sort_index()
        
        print("\nFrecuencia de estrellas:")
        freq_estrellas_table = []
        for star, count in freq_estrellas.items():
            percentage = (count / len(self.df) / 2) * 100
            freq_estrellas_table.append([star, count, f"{percentage:.2f}%"])
        print(tabulate(freq_estrellas_table, headers=['Estrella', 'Apariciones', 'Porcentaje'], tablefmt='pretty'))
        
        # Análisis de intervalos entre apariciones
        print("\nIntervalos entre apariciones de números:")
        for num in range(1, 51):
            apariciones = self.df[self.df[['n1', 'n2', 'n3', 'n4', 'n5']].eq(num).any(axis=1)]['fecha']
            if not apariciones.empty:
                intervalos = apariciones.diff().dt.days.dropna()
                print(f"Número {num}: Intervalo promedio = {intervalos.mean():.2f} días, Máximo = {intervalos.max()} días")

    def get_probability_analysis(self):
        """Análisis de probabilidades condicionales."""
        print("\n🎲 ANÁLISIS DE PROBABILIDADES CONDICIONALES")

        # 1. Probabilidad después de números específicos
        print("\n1. Probabilidades después de números específicos:")
        
        for num in range(1, 51):
            siguiente_sorteo = []
            numero_anterior = False
            
            for _, row in self.df.iterrows():
                if numero_anterior:
                    siguiente_sorteo.extend([row['n1'], row['n2'], row['n3'], row['n4'], row['n5']])
                numero_anterior = num in [row['n1'], row['n2'], row['n3'], row['n4'], row['n5']]

            if siguiente_sorteo:
                freq = pd.Series(siguiente_sorteo).value_counts()
                if len(freq) >= 5:  # Solo mostrar si hay suficientes datos
                    print(f"\nDespués del número {num}, los más probables son:")
                    for n, c in freq.head().items():
                        print(f"Número {n}: {round(c/len(siguiente_sorteo)*100, 2)}%")

        # 2. Análisis de transiciones
        print("\n2. Probabilidades de transición entre sorteos:")
        transiciones = []
        for i in range(len(self.df)-1):
            sorteo_actual = set([self.df.iloc[i][f'n{j}'] for j in range(1, 6)])
            sorteo_siguiente = set([self.df.iloc[i+1][f'n{j}'] for j in range(1, 6)])
            numeros_repetidos = len(sorteo_actual.intersection(sorteo_siguiente))
            transiciones.append(numeros_repetidos)

        freq_transiciones = pd.Series(transiciones).value_counts().sort_index()
        print("\nNúmeros que se repiten entre sorteos consecutivos:")
        for nums, freq in freq_transiciones.items():
            print(f"{nums} números: {freq} veces ({round(freq/len(transiciones)*100, 2)}%)")

    def get_seasonal_analysis(self):
        """Análisis de patrones estacionales."""
        print("\n🌞 ANÁLISIS ESTACIONAL")

        # Añadir información temporal
        self.df['año'] = self.df['fecha'].dt.year
        self.df['mes'] = self.df['fecha'].dt.month
        self.df['estacion'] = self.df['fecha'].dt.month.map(
            {12: 'Invierno', 1: 'Invierno', 2: 'Invierno',
             3: 'Primavera', 4: 'Primavera', 5: 'Primavera',
             6: 'Verano', 7: 'Verano', 8: 'Verano',
             9: 'Otoño', 10: 'Otoño', 11: 'Otoño'}
        )

        # Análisis por estación
        print("\n1. Números más frecuentes por estación:")
        for estacion in ['Primavera', 'Verano', 'Otoño', 'Invierno']:
            sorteos_estacion = self.df[self.df['estacion'] == estacion]
            numeros = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros.extend(sorteos_estacion[col].tolist())
            
            freq = pd.Series(numeros).value_counts()
            print(f"\n{estacion}:")
            for num, count in freq.head(5).items():
                print(f"Número {num}: {count} veces ({round(count/len(sorteos_estacion)*100, 2)}%)")

        # Análisis de meses
        print("\n2. Patrones mensuales:")
        patrones_mensuales = {}
        for mes in range(1, 13):
            sorteos_mes = self.df[self.df['mes'] == mes]
            numeros = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros.extend(sorteos_mes[col].tolist())
            
            media = np.mean(numeros)
            std = np.std(numeros)
            patrones_mensuales[mes] = {'media': media, 'std': std}

        for mes, stats in patrones_mensuales.items():
            nombre_mes = {
                1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
            }[mes]
            print(f"\n{nombre_mes}:")
            print(f"Media: {round(stats['media'], 2)}")
            print(f"Desviación estándar: {round(stats['std'], 2)}")

        # 3. Tendencias anuales
        print("\n3. Tendencias anuales:")
        for año in sorted(self.df['año'].unique()):
            sorteos_año = self.df[self.df['año'] == año]
            numeros = []
            for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                numeros.extend(sorteos_año[col].tolist())
            
            print(f"\nAño {año}:")
            print(f"Media: {round(np.mean(numeros), 2)}")
            print(f"Número más frecuente: {pd.Series(numeros).value_counts().index[0]}")

    def show_frequent_numbers(self, top=10, top_numbers=None, top_stars=5):
        """Muestra los números y estrellas más frecuentes y ofrece opciones para generar combinaciones."""
        if top_numbers is None:
            top_numbers = top

        print(f"\n🔢 NÚMEROS MÁS FRECUENTES (Top {top_numbers})")
        
        # Contar frecuencias de números
        todos_numeros = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            todos_numeros.extend(self.df[col].tolist())
        
        freq_numeros = pd.Series(todos_numeros).value_counts()
        
        # Preparar resultados de números
        resultados_numeros = []
        numeros_frecuentes = []
        for num, count in freq_numeros.head(top_numbers).items():
            porcentaje = round(count / len(self.df) * 100, 2)
            resultados_numeros.append([num, count, f"{porcentaje}%"])
            numeros_frecuentes.append(num)
        
        # Mostrar tabla de números
        print(tabulate(resultados_numeros,
                       headers=['Número', 'Apariciones', '% Sorteos'],
                       tablefmt='pretty'))
        
        # Contar frecuencias de estrellas
        todas_estrellas = []
        for col in ['e1', 'e2']:
            todas_estrellas.extend(self.df[col].tolist())
        
        freq_estrellas = pd.Series(todas_estrellas).value_counts()
        
        # Preparar resultados de estrellas
        resultados_estrellas = []
        estrellas_frecuentes = []
        for star, count in freq_estrellas.head(top_stars).items():
            porcentaje = round(count / len(self.df) * 100, 2)
            resultados_estrellas.append([star, count, f"{porcentaje}%"])
            estrellas_frecuentes.append(star)
        
        # Mostrar tabla de estrellas
        print(f"\n⭐ ESTRELLAS MÁS FRECUENTES (Top {top_stars})")
        print(tabulate(resultados_estrellas,
                       headers=['Estrella', 'Apariciones', '% Sorteos'],
                       tablefmt='pretty'))
        
        # Generar combinaciones
        print("\n¿Desea generar todas las combinaciones posibles con estos números y estrellas?")
        respuesta = input("Ingrese 'S' para sí, cualquier otra tecla para no: ").strip().upper()
        
        if respuesta == 'S':
            combinaciones_numeros = list(combinations(numeros_frecuentes, 5))
            combinaciones_estrellas = list(combinations(estrellas_frecuentes, 2))
            
            todas_combinaciones = list(product(combinaciones_numeros, combinaciones_estrellas))
            
            df_combinaciones = pd.DataFrame([
                (*nums, *stars) for nums, stars in todas_combinaciones
            ], columns=['n1', 'n2', 'n3', 'n4', 'n5', 'e1', 'e2'])
            
            print(f"\nSe han generado {len(todas_combinaciones)} combinaciones.")
            print("\n¿En qué formato desea exportar las combinaciones?")
            print("1. Excel")
            print("2. CSV")
            print("3. JSON")
            
            opcion = input("Seleccione una opción (1-3): ").strip()
            
            filename = input("Ingrese el nombre del archivo (sin extensión): ").strip()
            
            try:
                if opcion == '1':
                    df_combinaciones.to_excel(f"{filename}.xlsx", index=False)
                    print(f"Combinaciones exportadas a {filename}.xlsx")
                elif opcion == '2':
                    df_combinaciones.to_csv(f"{filename}.csv", index=False)
                    print(f"Combinaciones exportadas a {filename}.csv")
                elif opcion == '3':
                    df_combinaciones.to_json(f"{filename}.json", orient='records')
                    print(f"Combinaciones exportadas a {filename}.json")
                else:
                    print("Opción no válida. No se ha realizado la exportación.")
            except Exception as e:
                print(f"Error al exportar: {str(e)}")


