"""
Euromillones Analysis Package
----------------------------
Un paquete completo para el análisis de resultados del Euromillones.

Módulos:
    - analyzer: Análisis detallado de datos
    - data_loader: Carga y preparación de datos
    - generator: Generación de combinaciones
    - predictor: Predicciones y probabilidades
    - statistics: Análisis estadísticos
    - visualizer: Visualización de datos
    - helpers: Funciones de utilidad
"""

from .analyzer import DataAnalyzer
from .data_loader import DataLoader
from .generator import CombinationGenerator
from .predictor import Predictor
from .statistics import Statistics
from .visualizer import Visualizer
from .helpers import Helpers

__version__ = '1.0.0'
__author__ = 'Tu Nombre'
__email__ = 'tu@email.com'

# Configuración del paquete
PACKAGE_CONFIG = {
    'max_numbers': 50,
    'max_stars': 12,
    'combination_size': 5,
    'stars_size': 2,
    'min_number': 1,
    'default_analysis_period': 10,
    'date_format': '%d-%m-%Y',
    'csv_filename': 'Euromillones - 2004 a 2024.csv'
}

# Mapeo de nombres de día
WEEKDAY_NAMES = {
    0: 'Lunes',
    1: 'Martes',
    2: 'Miércoles',
    3: 'Jueves',
    4: 'Viernes',
    5: 'Sábado',
    6: 'Domingo'
}

# Mapeo de nombres de mes
MONTH_NAMES = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Septiembre',
    10: 'Octubre',
    11: 'Noviembre',
    12: 'Diciembre'
}

# Mapeo de estaciones
SEASONS = {
    12: 'Invierno', 1: 'Invierno', 2: 'Invierno',
    3: 'Primavera', 4: 'Primavera', 5: 'Primavera',
    6: 'Verano', 7: 'Verano', 8: 'Verano',
    9: 'Otoño', 10: 'Otoño', 11: 'Otoño'
}

# Códigos de colores ANSI
COLORS = {
    'header': '\033[95m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'end': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

# Símbolos Unicode
SYMBOLS = {
    'ball': '🔵',
    'star': '⭐',
    'chart': '📊',
    'up': '↑',
    'down': '↓',
    'right': '→',
    'warning': '⚠️',
    'check': '✅',
    'cross': '❌',
    'info': 'ℹ️',
    'calendar': '📅',
    'money': '💰',
    'graph': '📈',
    'magnifier': '🔍',
    'dice': '🎲',
    'crystal_ball': '🔮',
    'clipboard': '📋',
    'save': '💾',
    'time': '⏰'
}

# Configuración de formato de tablas
TABLE_FORMATS = {
    'default': 'pretty',
    'minimal': 'simple',
    'markdown': 'pipe',
    'grid': 'grid'
}

def get_version():
    """Retorna la versión actual del paquete."""
    return __version__

def get_config():
    """Retorna la configuración actual del paquete."""
    return PACKAGE_CONFIG

def get_color(name):
    """Retorna un código de color ANSI por nombre."""
    return COLORS.get(name, '')

def get_symbol(name):
    """Retorna un símbolo Unicode por nombre."""
    return SYMBOLS.get(name, '')

def format_weekday(day_number):
    """Formatea el número de día a nombre."""
    return WEEKDAY_NAMES.get(day_number, '')

def format_month(month_number):
    """Formatea el número de mes a nombre."""
    return MONTH_NAMES.get(month_number, '')

def get_season(month):
    """Retorna la estación del año para un mes dado."""
    return SEASONS.get(month, '')

# Función de inicialización del paquete
def initialize():
    """Inicializa el paquete y verifica las dependencias."""
    required_packages = [
        'pandas',
        'numpy',
        'tabulate'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        raise ImportError(
            "Faltan las siguientes dependencias: " + 
            ", ".join(missing_packages) +
            ". Instálalas usando pip install <package>"
        )
    
    return True

# Verificar dependencias al importar el paquete
initialize()