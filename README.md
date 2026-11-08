## Medicion Termica De Procesadores

## 1. Descripción del proyecto
Este proyecto analiza cómo se genera y se transfiere el calor dentro de un procesador durante tareas de alto rendimiento. Para ello, utiliza un modelo matemático de conducción térmica en una dimensión y un programa desarrollado en Python.

## 2. Objetivo
Estudiar la distribución de temperatura, el flujo de calor y el gradiente térmico en una región del procesador mediante ecuaciones físicas y simulaciones computacionales.

## 3. Herramientas utilizadas
- **Python:** desarrollo del modelo.
- **NumPy:** cálculos numéricos.
- **Matplotlib:** generación de gráficas.
- **CSV:** almacenamiento de los resultados.

## 4. Modelo matemático
Se utiliza la ecuación de conducción de calor con generación interna de energía:

\\[
k\\frac{d^2\\theta}{dx^2}+\\dot q'''=0
\\]

Donde:
- \\(k\\): conductividad térmica del silicio.
- \\(\\theta\\): incremento relativo de temperatura.
- \\(\\dot q'''\\): generación volumétrica de calor.
- \\(x\\): posición dentro del material.

El modelo permite calcular el perfil de temperatura, el gradiente térmico, el flujo de calor y el incremento máximo de temperatura.

## 5. Parámetros utilizados
El procesador de referencia es el Intel Core i7-13700. Se emplean datos técnicos del fabricante y valores supuestos para representar una región activa del chip:

- Potencia local: 10 W.
- Área: 20 mm².
- Espesor del silicio: 0,37 mm.
- Conductividad térmica: 122,04 W/(m·K).
- Incertidumbre relativa de la conductividad: 5 %.

Estos valores forman parte de un modelo simplificado y no son mediciones directas del procesador.

## 6. Análisis de incertidumbre
El programa realiza **10 simulaciones con una semilla fija (2026)**. En cada escenario varían ligeramente la potencia, el área, el espesor y la conductividad térmica para observar cómo cambian los resultados.

Las simulaciones ofrecen un rango exploratorio de resultados; no constituyen un intervalo de confianza estadístico.

## 7. Resultados
El programa genera gráficas y un archivo CSV para observar:
- Distribución del incremento de temperatura.
- Gradiente térmico.
- Flujo de calor.
- Variaciones entre los 10 escenarios simulados.

## 8. Cómo ejecutar el programa
1. Instalar Python.
2. Instalar las bibliotecas necesarias:

```bash
pip install numpy matplotlib
```

3. Abrir la terminal en la carpeta del proyecto.
4. Ejecutar:

```bash
python modelo_termico_tema13_10_simulaciones.py
```

5. Consultar la carpeta `resultados`, donde se guardan las gráficas y los datos.

## 9. Limitaciones
El modelo considera conducción de calor en una dimensión, estado estacionario y generación uniforme de energía. No representa todo el sistema de refrigeración del procesador ni calcula su temperatura real de funcionamiento. Por tanto, sus resultados son aproximaciones teóricas.

## 10. Conclusión
El proyecto muestra cómo las matemáticas, la física y la programación permiten estudiar la disipación térmica en los procesadores. Las simulaciones ayudan a comprender cómo los cambios en las propiedades y dimensiones del material afectan la transferencia de calor.

## 11. Referencias principales
- Intel. *Intel Core i7-13700 Processor Specifications*.
- Bergman et al. (2011). *Fundamentals of Heat and Mass Transfer*.
- Shanks et al. (1963). *Thermal Conductivity of Silicon from 300 to 1400°K*.
- Harris et al. (2020). *Array Programming with NumPy*.
- Hunter (2007). *Matplotlib: A 2D Graphics Environment*.
- JCGM (2008). *Evaluation of Measurement Data: Monte Carlo Method*.
"""
