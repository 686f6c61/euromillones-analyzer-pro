import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

class DataLoader:
    def __init__(self):
        self.filename = 'data/Euromillones - 2004 a 2024.csv'
        self.required_columns = ['FECHA', 'COMB. GANADORA', 'ESTRELLAS']
        self.df = None

    def load_data(self):
        """Carga y prepara los datos del CSV."""
        try:
            print("\n📂 Cargando datos del Euromillones...")
            
            # Verificar que existe el archivo
            if not os.path.exists(self.filename):
                raise FileNotFoundError(f"No se encuentra el archivo {self.filename}")

            # Cargar CSV
            self.df = pd.read_csv(self.filename)
            
            # Verificar estructura básica
            self._verify_data_structure()
            
            # Preparar y limpiar datos
            self.df = self._prepare_data()
            
            print("✅ Datos cargados y preparados correctamente")
            print(f"📊 Total de sorteos analizados: {len(self.df)}")
            print(f"📅 Rango de fechas: {self.df['fecha'].min().strftime('%d-%m-%Y')} "
                  f"a {self.df['fecha'].max().strftime('%d-%m-%Y')}")
            
            return self.df

        except Exception as e:
            print(f"\n❌ Error al cargar datos: {str(e)}")
            sys.exit(1)

    def _verify_data_structure(self):
        """Verifica la estructura básica del CSV."""
        # Verificar columnas necesarias
        for col in self.required_columns:
            if col not in self.df.columns:
                raise ValueError(f"Columna requerida '{col}' no encontrada en el CSV")

        # Verificar que hay datos
        if len(self.df) == 0:
            raise ValueError("El archivo CSV está vacío")

    def _prepare_data(self):
        """Prepara y limpia los datos."""
        # Copiar DataFrame para no modificar el original
        df = self.df.copy()

        # Renombrar columnas
        df.columns = ['fecha', 'n1', 'n2', 'n3', 'n4', 'n5', 'unnamed', 'e1', 'e2']
        
        # Eliminar columna innecesaria
        df = df.drop('unnamed', axis=1)

        # Convertir fecha a datetime
        df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y', errors='coerce')

        # Ordenar por fecha descendente (más reciente primero)
        df = df.sort_values('fecha', ascending=False)

        # Verificar y convertir números a int
        num_columns = ['n1', 'n2', 'n3', 'n4', 'n5', 'e1', 'e2']
        for col in num_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Eliminar filas con datos faltantes
        df = df.dropna()

        # Verificar rangos válidos
        self._verify_number_ranges(df)

        return df

    def _verify_number_ranges(self, df):
        """Verifica que los números están en rangos válidos."""
        # Verificar números principales (1-50)
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            invalid = df[~df[col].between(1, 50)]
            if len(invalid) > 0:
                raise ValueError(f"Encontrados números fuera de rango (1-50) en columna {col}")

        # Verificar estrellas (1-12)
        for col in ['e1', 'e2']:
            invalid = df[~df[col].between(1, 12)]
            if len(invalid) > 0:
                raise ValueError(f"Encontradas estrellas fuera de rango (1-12) en columna {col}")

    def get_data_info(self):
        """Retorna información básica sobre los datos cargados."""
        if self.df is None:
            return "No hay datos cargados"

        info = {
            'total_sorteos': len(self.df),
            'fecha_inicio': self.df['fecha'].min(),
            'fecha_fin': self.df['fecha'].max(),
            'dias_total': (self.df['fecha'].max() - self.df['fecha'].min()).days,
            'numeros_unicos': len(set(self.df[['n1', 'n2', 'n3', 'n4', 'n5']].values.ravel())),
            'estrellas_unicas': len(set(self.df[['e1', 'e2']].values.ravel()))
        }

        return info

    def get_time_ranges(self):
        """Retorna rangos de tiempo predefinidos para análisis."""
        if self.df is None:
            return None

        ultima_fecha = self.df['fecha'].max()
        
        ranges = {
            'ultimo_mes': self.df[self.df['fecha'] > (ultima_fecha - pd.DateOffset(months=1))],
            'ultimo_trimestre': self.df[self.df['fecha'] > (ultima_fecha - pd.DateOffset(months=3))],
            'ultimo_semestre': self.df[self.df['fecha'] > (ultima_fecha - pd.DateOffset(months=6))],
            'ultimo_año': self.df[self.df['fecha'] > (ultima_fecha - pd.DateOffset(years=1))],
            'ultimos_10': self.df.head(10)
        }

        return ranges

    def get_clean_numbers(self):
        """Retorna arrays limpios de números y estrellas."""
        if self.df is None:
            return None

        numbers = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            numbers.extend(self.df[col].tolist())

        stars = []
        for col in ['e1', 'e2']:
            stars.extend(self.df[col].tolist())

        return {
            'numbers': np.array(numbers),
            'stars': np.array(stars)
        }

    def validate_combination(self, numbers, stars):
        """Valida una combinación de números y estrellas."""
        # Verificar longitud
        if len(numbers) != 5:
            return False, "Debe proporcionar 5 números"
        if len(stars) != 2:
            return False, "Debe proporcionar 2 estrellas"

        # Verificar rangos
        if not all(1 <= n <= 50 for n in numbers):
            return False, "Los números deben estar entre 1 y 50"
        if not all(1 <= s <= 12 for s in stars):
            return False, "Las estrellas deben estar entre 1 y 12"

        # Verificar duplicados
        if len(set(numbers)) != 5:
            return False, "No puede haber números duplicados"
        if len(set(stars)) != 2:
            return False, "No puede haber estrellas duplicadas"

        return True, "Combinación válida"

    def export_data(self, filename, format='csv'):
        """Exporta los datos en diferentes formatos."""
        if self.df is None:
            return False, "No hay datos para exportar"

        try:
            if format == 'csv':
                self.df.to_csv(filename, index=False)
            elif format == 'excel':
                self.df.to_excel(filename, index=False)
            elif format == 'json':
                self.df.to_json(filename, orient='records', date_format='iso')
            else:
                return False, "Formato no soportado"

            return True, f"Datos exportados correctamente a {filename}"
        except Exception as e:
            return False, f"Error al exportar: {str(e)}"

    def get_data_quality_report(self):
        """Genera un reporte de calidad de los datos."""
        if self.df is None:
            return "No hay datos para analizar"

        report = {
            'registros_totales': len(self.df),
            'valores_faltantes': self.df.isnull().sum().to_dict(),
            'duplicados': len(self.df) - len(self.df.drop_duplicates()),
            'rango_fechas': {
                'inicio': self.df['fecha'].min(),
                'fin': self.df['fecha'].max(),
                'dias_faltantes': self._get_missing_dates()
            },
            'validacion_numeros': self._validate_number_consistency(),
            'validacion_estrellas': self._validate_star_consistency()
        }

        return report

    def _get_missing_dates(self):
        """Identifica fechas faltantes en la serie temporal."""
        fecha_completa = pd.date_range(
            start=self.df['fecha'].min(),
            end=self.df['fecha'].max(),
            freq='D'
        )
        fechas_sorteos = set(self.df['fecha'].dt.date)
        fechas_esperadas = set(fecha_completa.date)
        return sorted(fechas_esperadas - fechas_sorteos)

    def _validate_number_consistency(self):
        """Valida la consistencia de los números."""
        issues = []
        for col in ['n1', 'n2', 'n3', 'n4', 'n5']:
            # Verificar rango
            out_of_range = self.df[~self.df[col].between(1, 50)]
            if len(out_of_range) > 0:
                issues.append(f"Números fuera de rango en {col}: {len(out_of_range)} registros")

            # Verificar duplicados en la misma combinación
            for other_col in ['n1', 'n2', 'n3', 'n4', 'n5']:
                if col != other_col:
                    duplicates = self.df[self.df[col] == self.df[other_col]]
                    if len(duplicates) > 0:
                        issues.append(f"Números duplicados entre {col} y {other_col}: {len(duplicates)} registros")

        return issues

    def _validate_star_consistency(self):
        """Valida la consistencia de las estrellas."""
        issues = []
        for col in ['e1', 'e2']:
            # Verificar rango
            out_of_range = self.df[~self.df[col].between(1, 12)]
            if len(out_of_range) > 0:
                issues.append(f"Estrellas fuera de rango en {col}: {len(out_of_range)} registros")

            # Verificar duplicados en la misma combinación
            for other_col in ['e1', 'e2']:
                if col != other_col:
                    duplicates = self.df[self.df[col] == self.df[other_col]]
                    if len(duplicates) > 0:
                        issues.append(f"Estrellas duplicadas entre {col} y {other_col}: {len(duplicates)} registros")

        return issues
