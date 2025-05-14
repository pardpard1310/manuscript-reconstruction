
# Objetivo 1 — Simulación de degradación artificial en manuscritos históricos

Este módulo implementa un conjunto de scripts para generar un **dataset sintético de manuscritos deteriorados**, con el fin de simular daños reales como inclinación del texto, bordes innecesarios y huecos causados por insectos (túneles de polilla). Este dataset es utilizado posteriormente en tareas de restauración textual y visual.

---

## Objetivo específico

**Diseñar una estrategia de degradación artificial para manuscritos digitales.**

---

## Estructura

```
O1_degradacion-artificial/
├── 1_preprocesamiento/          # Preparación de imágenes base
│   ├── deskew_text_lines.py     # Corrige la inclinación del texto
│   └── crop_manuscript_region.py # Recorta los bordes innecesarios
│
├── 2_simulacion-huecos/         # Simulación del daño físico
│   └── simulate_wormholes.py    # Aplica túneles de polilla sobre la imagen
│
└── README.md                    # Este archivo
```

---

## Descripción de scripts

### `deskew_text_lines.py`
Corrige automáticamente la inclinación del texto en manuscritos, estimando el mejor ángulo de rotación mediante proyección horizontal. Las imágenes alineadas se utilizan como base para los siguientes pasos.

### `crop_manuscript_region.py`
Recorta el contenido relevante del manuscrito eliminando márgenes innecesarios. Usa contornos detectados automáticamente y permite ajuste manual en caso necesario.

### `simulate_wormholes.py`
Simula túneles de polilla (daño físico) de forma realista, con bordes suaves y profundidad visual. Se genera una imagen con daño en color y una versión binarizada en blanco y negro optimizada para OCR.

---

## Resultado esperado

- **R1.** Script funcional y parametrizable para aplicar degradaciones artificiales en manuscritos digitales.
- **R2.** Conjunto de datos sintéticos con manuscritos deteriorados generado mediante el script.

---

## Ejecución

Los scripts no dependen de argumentos por consola, pero puedes modificar directamente las rutas al final de cada archivo `.py`. Se recomienda ejecutarlos en este orden:

1. `deskew_text_lines.py` – enderezar texto
2. `crop_manuscript_region.py` – recortar contenido útil
3. `simulate_wormholes.py` – aplicar degradación visual

---

## Notas

- Las imágenes generadas por estos scripts se almacenan en la carpeta `data/`, organizada por tipo (alineadas, recortadas, degradadas).
- Este objetivo representa la **fase inicial del pipeline** completo para la reconstrucción multimodal de manuscritos.

---

## Requisitos

- Python 3.8+
- OpenCV
- NumPy

Puedes instalar dependencias ejecutando:

```bash
pip install -r ../../requirements.txt
```

---
