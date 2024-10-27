# 🎰 Euromillones Analyzer Pro

Un analizador avanzado y completo de resultados del Euromillones con predicciones sofisticadas, estadísticas detalladas y un generador de combinaciones inteligente.

## ✨ Características Principales

- Análisis exhaustivo de resultados históricos del Euromillones
- Predicciones avanzadas basadas en múltiples modelos estadísticos
- Generador de combinaciones inteligente con parámetros personalizables
- Estadísticas profundas y visualizaciones interactivas
- Análisis temporal y detección de patrones complejos
- Interfaz de consola intuitiva y fácil de usar

## 🚀 Instalación y Configuración

1. Clona el repositorio:
   ```bash
   git clone https://github.com/686f6c61/euromillones-analyzer-pro.git
   cd euromillones-analyzer-pro
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Asegúrate de tener el archivo de datos `Euromillones - 2004 a 2024.csv` en el directorio `data/`.

## 🖥️ Uso del Programa

Ejecuta el programa principal:
```bash
python main.py
```

## 📁 Estructura Detallada del Proyecto

```
euromillones-analyzer-pro/
│
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Documentación
│
├── modules/                # Módulos del programa
│   ├── __init__.py         # Inicialización del paquete
│   ├── analyzer.py         # Análisis de datos
│   ├── data_loader.py      # Carga y preprocesamiento de datos
│   ├── generator.py        # Generador de combinaciones
│   ├── predictor.py        # Modelos de predicción
│   ├── statistics.py       # Análisis estadísticos
│   ├── visualizer.py       # Visualización de datos
│   └── helpers.py          # Funciones auxiliares
│
└── data/
    └── Euromillones - 2004 a 2024.csv  # Datos históricos
```

### 📊 Descripción Detallada de los Módulos

#### 🎮 main.py
Punto de entrada principal del programa. Gestiona la interfaz de usuario y coordina las llamadas a los diferentes módulos.

Funcionalidades clave:
- Menú principal interactivo
- Gestión de flujo del programa
- Manejo de errores y excepciones

#### 🔍 modules/analyzer.py
Realiza análisis profundos de los datos históricos del Euromillones.

Cálculos y análisis:
- Identificación de patrones en números y estrellas
- Análisis de secuencias y rachas
- Detección de correlaciones entre números
- Análisis de distribución de números por decenas
- Cálculo de la entropía de las combinaciones

#### 📥 modules/data_loader.py
Gestiona la carga, limpieza y preprocesamiento de los datos históricos.

Operaciones:
- Lectura y parsing del archivo CSV
- Limpieza de datos (manejo de valores nulos, formato de fechas)
- Creación de características adicionales (día de la semana, mes, año)
- Validación de integridad de los datos

#### 🎲 modules/generator.py
Genera combinaciones inteligentes basadas en diversos criterios estadísticos.

Métodos de generación:
- Combinaciones basadas en frecuencia histórica
- Generación de combinaciones equilibradas por decenas
- Combinaciones basadas en patrones identificados
- Generador personalizado con parámetros ajustables

#### 🔮 modules/predictor.py
Implementa modelos de predicción para futuros sorteos.

Modelos y técnicas:
- Predicción basada en frecuencias históricas
- Modelo de regresión logística para probabilidad de aparición
- Análisis de tendencias a corto y largo plazo
- Predicción de números calientes y fríos

#### 📈 modules/statistics.py
Realiza cálculos estadísticos avanzados sobre los datos históricos.

Análisis estadísticos:
- Estadísticas descriptivas (media, mediana, moda, desviación estándar)
- Análisis de frecuencia de números y estrellas
- Cálculo de probabilidades condicionales
- Análisis de varianza (ANOVA) para identificar tendencias significativas
- Tests de aleatoriedad y distribución

#### 📊 modules/visualizer.py
Genera visualizaciones gráficas de los datos y resultados de análisis.

Tipos de visualizaciones:
- Gráficos de frecuencia de números y estrellas
- Mapas de calor para correlaciones
- Gráficos de líneas para tendencias temporales
- Diagramas de caja para distribuciones de números

#### 🛠️ modules/helpers.py
Contiene funciones auxiliares utilizadas por otros módulos.

Funcionalidades:
- Formateo de datos para visualización
- Cálculos matemáticos comunes
- Funciones de validación y verificación

## 🔬 Funcionalidades Detalladas

### 📊 Análisis de Datos
- Frecuencia histórica de números y estrellas
- Identificación de patrones temporales (estacionalidad, tendencias)
- Análisis de rachas y secuencias consecutivas
- Correlaciones entre números y entre números y estrellas
- Análisis de la distribución de números por decenas y paridad

### 🔮 Predicciones
- Modelo de predicción basado en frecuencias históricas ponderadas
- Análisis de tendencias a corto (últimos 10 sorteos) y largo plazo
- Cálculo de probabilidades condicionales para combinaciones de números
- Identificación de números "calientes" (frecuentes recientemente) y "fríos" (poco frecuentes)
- Predicción de rangos probables para la suma de los números ganadores

### 🎲 Generador de Combinaciones
- Generación basada en estadísticas históricas con ponderación ajustable
- Creación de combinaciones equilibradas por decenas y paridad
- Opción para incluir o excluir números específicos
- Validación de combinaciones generadas contra patrones históricos
- Generador de combinaciones "contrarian" basado en números menos frecuentes

### 📈 Estadísticas Avanzadas
- Análisis de varianza (ANOVA) para identificar diferencias significativas entre períodos
- Cálculo de la entropía de las combinaciones ganadoras a lo largo del tiempo
- Análisis de componentes principales (PCA) para identificar factores subyacentes
- Tests de aleatoriedad (runs test, chi-cuadrado) para validar la distribución de números
- Análisis de Fourier para identificar ciclos o patrones periódicos en los resultados

## 🛠️ Uso Avanzado y Personalización

El Euromillones Analyzer Pro permite una amplia personalización de sus análisis y predicciones. Algunos ejemplos de uso avanzado incluyen:

- Ajuste de parámetros en el generador de combinaciones para favorecer ciertos patrones o distribuciones.
- Personalización de los modelos de predicción, como la modificación de los pesos en el análisis de frecuencias históricas.
- Creación de análisis personalizados combinando diferentes métricas y visualizaciones.

Para más detalles sobre cómo personalizar y extender las funcionalidades, consulta la documentación de cada módulo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas y apreciadas. Si deseas contribuir al proyecto:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu funcionalidad (`git checkout -b feature/AmazingFeature`).
3. Realiza tus cambios y haz commit (`git commit -m 'Add some AmazingFeature'`).
4. Push a la rama (`git push origin feature/AmazingFeature`).
5. Abre un Pull Request.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## ⚠️ Descargo de Responsabilidad

Este software se proporciona solo con fines educativos y de entretenimiento. No garantiza ganancias en la lotería y no debe ser utilizado como base para decisiones financieras. Juega responsablemente.
