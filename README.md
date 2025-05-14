# Descripción
Este repositorio contiene el código y los scripts desarrollados para la reconstrucción multimodal de manuscritos históricos, centrado en la completación visual-textual basada en Transformers. El objetivo principal de este proyecto es recuperar texto de manuscritos deteriorados utilizando técnicas avanzadas de visión por computadora y procesamiento de lenguaje natural (NLP).

## El proyecto está estructurado en cinco objetivos clave:

#### **Degradación artificial de manuscritos digitales:** 
  Se crea un conjunto de datos sintéticos aplicando degradaciones controladas a imágenes de manuscritos originales.

#### **Segmentación de manuscritos históricos:** 
  Implementación de un pipeline para segmentar las líneas de texto en las imágenes de los manuscritos.

#### **Reconocimiento de texto (OCR):**
  Desarrollo de un modelo OCR basado en Transformers, ajustado mediante fine-tuning.

#### **Completado textual:**
  Implementación de un modelo secuencia-a-secuencia para completar textos deteriorados utilizando tokens <MASK>.

#### **API para presentación de resultados:**
  Desarrollo de una API que permite acceder y visualizar los resultados de los algoritmos implementados, incluyendo segmentación y completado de texto.

Los scripts incluidos en este repositorio están diseñados para facilitar la replicación del proyecto, y los modelos entrenados se encuentran en el directorio correspondiente. Además, se proporcionan herramientas para evaluar el rendimiento de los modelos utilizando métricas como CER, WER, IoU y mAP.

## Propósito del repositorio

Este repositorio documenta paso a paso el desarrollo de cada componente del sistema, desde la simulación del daño hasta la presentación final de los resultados. Está organizado por objetivos específicos, donde cada carpeta contiene sus scripts, modelos y resultados correspondientes.


## Estructura del repositorio:

Este repositorio organiza el código y los datos utilizados en el proyecto de **Reconstrucción Multimodal de Manuscritos Históricos mediante Visual-Text Completion basado en Transformers**. A continuación, se describe cada carpeta y archivo que contiene el repositorio.

```
manuscript-reconstruction/
├── data/                       # Resultados generados del preprocesamiento y degradación
├── O1_degradacion-artificial/ # Scripts para degradación artificial de manuscritos
├── O2_segmentacion-lineas/    # Scripts para segmentación de líneas en manuscritos
├── O3_modelo-OCR-transformer/ # Fine-tuning del modelo OCR basado en Transformers
├── O4_completado-textual/     # Completado de texto dañado con modelos seq2seq
├── O5_api-visualizacion/      # Visualización e interacción mediante API
└── README.md                  # Descripción general del repositorio
```


## Objetivos del proyecto

1. **Diseñar una estrategia de degradación artificial** que permita simular daños reales en manuscritos históricos mediante técnicas de procesamiento de imágenes.
2. **Segmentar los manuscritos deteriorados** extrayendo automáticamente las líneas de texto presentes en cada imagen.
3. **Reconocer texto deteriorado** mediante un modelo OCR ajustado (fine-tuning) a partir de Transformers.
4. **Completar texto faltante** utilizando un modelo secuencia-a-secuencia basado en aprendizaje profundo.
5. **Desarrollar una API** que permita a los usuarios explorar visualmente los resultados del sistema de reconstrucción.


## Cómo navegar este repositorio

- Cada carpeta `O1_`, `O2_`, etc., contiene su propio `README.md` con instrucciones específicas de ejecución, scripts utilizados y resultados esperados.
- La carpeta `data/` contiene los resultados intermedios generados, organizados por etapa.
- La documentación general y dependencias se especifican en este README principal y en `requirements.txt`.


## Requisitos

Este proyecto fue desarrollado en Python 3.8+ y requiere las siguientes librerías:

OpenCV para procesamiento de imágenes.
Transformers de Hugging Face para modelos de NLP.
TensorFlow o PyTorch para la implementación y entrenamiento de los modelos.

Instalación recomendada:

```bash
pip install -r requirements.txt
```


Este repositorio está en evolución continua como parte del desarrollo de la tesis, y se actualizará conforme se avance en la implementación y validación de los módulos.
