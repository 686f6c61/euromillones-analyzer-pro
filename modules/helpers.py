import os
import sys
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tabulate import tabulate
import random

class Helpers:
    @staticmethod
    def clear_screen():
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def format_number(number, decimals=2):
        """Formatea números para mostrar."""
        if isinstance(number, (int, float)):
            if number == int(number):
                return str(int(number))
            return f"{number:.{decimals}f}"
        return str(number)

    @staticmethod
    def format_percentage(value, decimals=2):
        """Formatea porcentajes."""
        return f"{value:.{decimals}f}%"

    @staticmethod
    def format_date(date):
        """Formatea fechas."""
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return date
        return date.strftime('%d-%m-%Y')

    @staticmethod
    def get_date_ranges():
        """Retorna rangos de fechas predefinidos."""
        today = datetime.now()
        ranges = {
            'ultima_semana': (today - timedelta(days=7), today),
            'ultimo_mes': (today - timedelta(days=30), today),
            'ultimo_trimestre': (today - timedelta(days=90), today),
            'ultimo_semestre': (today - timedelta(days=180), today),
            'ultimo_año': (today - timedelta(days=365), today),
        }
        return ranges

    @staticmethod
    def validate_date_range(start_date, end_date):
        """Valida un rango de fechas."""
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%d-%m-%Y')
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%d-%m-%Y')
            
            if start_date > end_date:
                return False, "La fecha de inicio debe ser anterior a la fecha final"
            if end_date > datetime.now():
                return False, "La fecha final no puede ser futura"
            
            return True, "Rango de fechas válido"
        except ValueError:
            return False, "Formato de fecha inválido (debe ser DD-MM-YYYY)"

    @staticmethod
    def get_progress_bar(current, total, width=50):
        """Genera una barra de progreso."""
        percent = current / total
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {percent:.1%}"

    @staticmethod
    def format_time_ago(date):
        """Formatea tiempo transcurrido."""
        if not date:
            return "fecha desconocida"
        
        now = datetime.now()
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return date

        diff = now - date
        days = diff.days

        if days == 0:
            return "hoy"
        elif days == 1:
            return "ayer"
        elif days < 7:
            return f"hace {days} días"
        elif days < 30:
            weeks = days // 7
            return f"hace {weeks} semana{'s' if weeks != 1 else ''}"
        elif days < 365:
            months = days // 30
            return f"hace {months} mes{'es' if months != 1 else ''}"
        else:
            years = days // 365
            return f"hace {years} año{'s' if years != 1 else ''}"

    @staticmethod
    def format_large_number(number):
        """Formatea números grandes."""
        if number < 1000:
            return str(number)
        elif number < 1000000:
            return f"{number/1000:.1f}K"
        else:
            return f"{number/1000000:.1f}M"

    @staticmethod
    def is_prime(n):
        """Verifica si un número es primo."""
        if n < 2:
            return False
        for i in range(2, int(np.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def is_fibonacci(n):
        """Verifica si un número pertenece a la secuencia de Fibonacci."""
        def is_perfect_square(x):
            s = int(np.sqrt(x))
            return s * s == x
        
        return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)

    @staticmethod
    def generate_random_combination():
        """Genera una combinación aleatoria válida."""
        numbers = sorted(random.sample(range(1, 51), 5))
        stars = sorted(random.sample(range(1, 13), 2))
        return {'numbers': numbers, 'stars': stars}

    @staticmethod
    def save_to_file(data, filename, format='json'):
        """Guarda datos en un archivo."""
        try:
            if format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, default=str)
            elif format == 'txt':
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            return True, f"Datos guardados en {filename}"
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"

    @staticmethod
    def load_from_file(filename, format='json'):
        """Carga datos desde un archivo."""
        try:
            if format == 'json':
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            elif format == 'txt':
                with open(filename, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            return None, f"Error al cargar: {str(e)}"

    @staticmethod
    def create_table(data, headers=None, format='pretty'):
        """Crea una tabla formateada."""
        return tabulate(data, headers=headers, tablefmt=format)

    @staticmethod
    def validate_number_range(number, min_val, max_val):
        """Valida que un número esté en un rango."""
        try:
            num = int(number)
            if min_val <= num <= max_val:
                return True, num
            return False, f"El número debe estar entre {min_val} y {max_val}"
        except ValueError:
            return False, "Debe introducir un número válido"

    @staticmethod
    def get_combinations(numbers, r):
        """Genera todas las combinaciones posibles de r elementos."""
        def combinations_helper(arr, r):
            if r == 0:
                return [[]]
            if len(arr) < r:
                return []
            
            result = []
            # Incluir el primer elemento
            first = arr[0]
            rest = arr[1:]
            com_with_first = combinations_helper(rest, r-1)
            for com in com_with_first:
                result.append([first] + com)
            
            # No incluir el primer elemento
            result.extend(combinations_helper(rest, r))
            return result
        
        return combinations_helper(sorted(numbers), r)

    @staticmethod
    def analyze_sequence(numbers):
        """Analiza una secuencia de números."""
        if not numbers:
            return {}
        
        sorted_nums = sorted(numbers)
        diffs = [sorted_nums[i+1] - sorted_nums[i] for i in range(len(sorted_nums)-1)]
        
        return {
            'min': min(numbers),
            'max': max(numbers),
            'mean': np.mean(numbers),
            'median': np.median(numbers),
            'std': np.std(numbers),
            'range': max(numbers) - min(numbers),
            'consecutive_count': sum(1 for d in diffs if d == 1),
            'max_gap': max(diffs),
            'gaps': diffs
        }

    @staticmethod
    def get_number_properties(n):
        """Retorna propiedades de un número."""
        properties = {
            'is_even': n % 2 == 0,
            'is_prime': Helpers.is_prime(n),
            'is_fibonacci': Helpers.is_fibonacci(n),
            'factors': [i for i in range(1, n + 1) if n % i == 0],
            'square': n * n,
            'sqrt': np.sqrt(n),
            'binary': bin(n)[2:],
            'decade': (n - 1) // 10,
            'divisible_by_5': n % 5 == 0,
            'divisible_by_10': n % 10 == 0
        }
        return properties

    @staticmethod
    def format_combination(numbers, stars):
        """Formatea una combinación de Euromillones."""
        nums = ' - '.join(map(str, sorted(numbers)))
        stars_str = ' - '.join(map(str, sorted(stars)))
        return f"Números: {nums} | Estrellas: {stars_str}"

    @staticmethod
    def get_memory_usage():
        """Retorna el uso de memoria del proceso."""
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # en MB

    @staticmethod
    def log_error(error, log_file='error.log'):
        """Registra un error en el archivo de log."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_msg = f"[{timestamp}] {str(error)}\n"
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(error_msg)
            return True
        except Exception:
            return False

    @staticmethod
    def get_valid_input(prompt, input_type=str, validator=None):
        """
        Solicita entrada al usuario y la valida.
        
        :param prompt: El mensaje para mostrar al usuario.
        :param input_type: El tipo de dato esperado (str, int, float, etc.).
        :param validator: Una función opcional para validación adicional.
        :return: La entrada validada del usuario.
        """
        while True:
            try:
                user_input = input_type(input(prompt))
                if validator:
                    if validator(user_input):
                        return user_input
                    else:
                        print("Entrada inválida. Por favor, intente de nuevo.")
                else:
                    return user_input
            except ValueError:
                print(f"Por favor, ingrese un valor de tipo {input_type.__name__}.")
