import pandas as pd
import numpy as np
from tabulate import tabulate
import os
from datetime import datetime
import math

class Visualizer:
    def __init__(self):
        self.colors = {
            'header': '\033[95m',
            'blue': '\033[94m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'end': '\033[0m',
            'bold': '\033[1m'
        }
        
        self.symbols = {
            'ball': '🔵',
            'star': '⭐',
            'chart': '📊',
            'up': '↑',
            'down': '↓',
            'right': '→',
            'warning': '⚠️',
            'check': '✅',
            'cross': '❌',
            'info': 'ℹ️'
        }

    def clear_screen(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_title(self, text):
        """Muestra un título formateado."""
        width = 60
        print("\n" + "=" * width)
        print(f"{self.colors['bold']}{text.center(width)}{self.colors['end']}")
        print("=" * width + "\n")

    def show_frequency_matrix(self, numbers, max_number=50):
        """Muestra una matriz visual de frecuencias."""
        print("\nMatriz de Frecuencias:")
        
        # Calcular frecuencias
        freq = pd.Series(numbers).value_counts()
        max_freq = freq.max()
        
        # Crear matriz
        matrix = []
        row = []
        for i in range(1, max_number + 1):
            count = freq.get(i, 0)
            intensity = int((count / max_freq) * 8)
            # Usar diferentes caracteres para representar intensidad
            char = " ▁▂▃▄▅▆▇█"[intensity]
            row.append(f"{i:2d}{char}")
            if i % 10 == 0:
                matrix.append(row)
                row = []
        if row:
            matrix.append(row + ['  '] * (10 - len(row)))

        # Mostrar matriz
        for row in matrix:
            print(" ".join(row))
        
        print("\nIntensidad: menor ▁▂▃▄▅▆▇█ mayor")

    def show_heat_calendar(self, df, year=None):
        """Muestra un calendario de calor con la frecuencia de números."""
        if year is None:
            year = df['fecha'].max().year

        df_year = df[df['fecha'].dt.year == year].copy()
        df_year['month'] = df_year['fecha'].dt.month
        df_year['day'] = df_year['fecha'].dt.day

        print(f"\nCalendario de sorteos {year}:")
        
        months = {
            1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr',
            5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Ago',
            9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
        }

        for month in range(1, 13):
            month_data = df_year[df_year['month'] == month]
            print(f"\n{months[month]}: ", end='')
            for day in range(1, 32):
                if day in month_data['day'].values:
                    print('█', end='')
                else:
                    print('·', end='')

    def show_trend_graph(self, numbers, window=10):
        """Muestra un gráfico de tendencia para un número específico."""
        freq = pd.Series(numbers).rolling(window=window).mean()
        
        max_val = freq.max()
        min_val = freq.min()
        height = 10
        width = 50

        print(f"\nTendencia (ventana móvil de {window} sorteos):")
        
        # Normalizar y crear gráfico
        for i in range(height-1, -1, -1):
            line = ''
            for val in freq[-width:]:
                if pd.isna(val):
                    char = ' '
                else:
                    normalized = (val - min_val) / (max_val - min_val) * height
                    char = '█' if normalized >= i else ' '
                line += char
            print(f"{line}")

        # Eje X
        print('─' * width)

    def show_number_distribution(self, numbers, bins=5):
        """Muestra la distribución de números en formato ASCII."""
        freq = pd.Series(numbers).value_counts().sort_index()
        max_freq = freq.max()
        bin_size = 50 // bins
        
        print("\nDistribución de números:")
        
        for i in range(bins):
            start = i * bin_size + 1
            end = min((i + 1) * bin_size, 50)
            bin_count = freq[start:end+1].sum()
            bar_length = int((bin_count / max_freq) * 40)
            print(f"{start:2d}-{end:2d} |{'█' * bar_length} {bin_count}")

    def show_combination_analysis(self, combination, historical_data):
        """Muestra un análisis visual de una combinación."""
        numbers = combination['numbers']
        stars = combination['stars']
        
        print("\nAnálisis de Combinación:")
        print("Números:", end=' ')
        for num in sorted(numbers):
            freq = sum(1 for row in historical_data if num in row)
            if freq > len(historical_data) * 0.2:  # Alta frecuencia
                print(f"{self.colors['green']}{num}{self.colors['end']}", end=' ')
            elif freq < len(historical_data) * 0.1:  # Baja frecuencia
                print(f"{self.colors['red']}{num}{self.colors['end']}", end=' ')
            else:
                print(num, end=' ')
        
        print("\nEstrellas:", end=' ')
        for star in sorted(stars):
            print(f"{self.symbols['star']}{star}", end=' ')

    def show_statistical_summary(self, data):
        """Muestra un resumen estadístico visual."""
        print("\nResumen Estadístico:")
        
        # Estadísticas básicas
        stats = {
            'Media': np.mean(data),
            'Mediana': np.median(data),
            'Desv. Est.': np.std(data),
            'Mín': min(data),
            'Máx': max(data)
        }
        
        max_label = max(len(k) for k in stats.keys())
        for label, value in stats.items():
            bar_length = int((value - min(data)) / (max(data) - min(data)) * 30)
            print(f"{label.rjust(max_label)}: {value:6.2f} |{'█' * bar_length}")

    def show_pattern_analysis(self, numbers):
        """Muestra un análisis visual de patrones."""
        print("\nAnálisis de Patrones:")
        
        # Matriz de distancias
        sorted_nums = sorted(numbers)
        print("\nMatriz de distancias entre números:")
        for i in range(len(sorted_nums)):
            for j in range(len(sorted_nums)):
                dist = abs(sorted_nums[i] - sorted_nums[j])
                if i == j:
                    print(" · ", end='')
                else:
                    print(f"{dist:2d}", end=' ')
            print()

    def create_progress_bar(self, current, total, width=50):
        """Crea una barra de progreso."""
        percent = current / total
        filled = int(width * percent)
        bar = '█' * filled + '▒' * (width - filled)
        return f"[{bar}] {percent:.1%}"

    def show_comparison_chart(self, data1, data2, label1, label2):
        """Muestra un gráfico comparativo de dos conjuntos de datos."""
        max_val = max(max(data1), max(data2))
        width = 30
        
        print(f"\nComparación {label1} vs {label2}:")
        for i in range(len(data1)):
            val1 = int((data1[i] / max_val) * width)
            val2 = int((data2[i] / max_val) * width)
            
            print(f"{i+1:2d} | {'█' * val1}{' ' * (width-val1)} | {'█' * val2}")
        
        print(f"{'-' * (width*2+7)}")
        print(f"    {label1.center(width)} {label2.center(width)}")

    def show_probability_meter(self, probability):
        """Muestra un medidor visual de probabilidad."""
        width = 40
        filled = int(width * probability)
        
        print("\nProbabilidad:")
        print(f"[{'█' * filled}{'▒' * (width-filled)}] {probability:.1%}")
        
        if probability > 0.7:
            print(f"{self.symbols['check']} Alta probabilidad")
        elif probability > 0.4:
            print(f"{self.symbols['info']} Probabilidad media")
        else:
            print(f"{self.symbols['warning']} Baja probabilidad")

    def show_time_series(self, data, dates, title="Serie Temporal"):
        """Muestra una serie temporal en ASCII."""
        print(f"\n{title}")
        
        # Normalizar datos para visualización
        height = 10
        min_val = min(data)
        max_val = max(data)
        range_val = max_val - min_val
        
        normalized = [(x - min_val) / range_val * height for x in data]
        
        # Crear gráfico
        for h in range(height, -1, -1):
            line = ""
            for val in normalized:
                if val >= h:
                    line += "█"
                else:
                    line += " "
            print(line)
        
        # Eje temporal
        print("-" * len(data))
        
        # Mostrar fechas importantes
        if len(dates) > 2:
            print(f"{dates[0].strftime('%m/%y')} {' ' * (len(data)-12)} {dates[-1].strftime('%m/%y')}")

    def show_last_draws(self, df, n=5):
        """Muestra los últimos N sorteos."""
        print(f"\n📅 ÚLTIMOS {n} SORTEOS")
        
        ultimos = df.head(n)
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
