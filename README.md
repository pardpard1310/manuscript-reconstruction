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

## Estructura del repositorio:

Este repositorio organiza el código y los datos utilizados en el proyecto de **Reconstrucción Multimodal de Manuscritos Históricos mediante Visual-Text Completion basado en Transformers**. A continuación, se describe cada carpeta y archivo que contiene el repositorio.

#### **data/**
Contiene los archivos de datos necesarios para entrenar y evaluar los modelos, organizados según el estado de los manuscritos.

- **`originals/`**: Contiene los manuscritos originales sin modificar. Estos archivos sirven como base para aplicar las diferentes técnicas de preprocesamiento, como la degradación y segmentación.
- **`cropped/`**: Manuscritos de los cuales se han recortado los bordes no deseados. Este paso es útil para eliminar áreas irrelevantes de las imágenes, como márgenes o bordes de la página.
- **`degraded/`**: Manuscritos con degradación artificial aplicada. Este conjunto de datos sintéticos simula daños como comeduras de polilla y otros deterioros, lo cual es crucial para entrenar los modelos en condiciones realistas de desgaste.
- **`segmented/`**: Manuscritos que han pasado por la segmentación por líneas después de la degradación. Aquí se almacenan las imágenes de los manuscritos que ya han sido procesados tanto por la degradación como por la segmentación de texto.

#### **scripts/**
Contiene los scripts funcionales que implementan las diferentes etapas del proyecto, desde la preparación de los datos hasta la evaluación de los modelos.

- **`degradation.py`**: Script que aplica degradación artificial a los manuscritos. Este script incluye técnicas como la comedura de polilla y otros efectos para simular deterioro de las imágenes.
- **`crop_borders.py`**: Script que recorta los bordes no deseados de las imágenes de los manuscritos, eliminando áreas fuera del área de interés para el procesamiento posterior.
- **`segmentation.py`**: Implementación del pipeline de segmentación de manuscritos históricos en líneas de texto. Este script extrae las líneas de los manuscritos para facilitar su procesamiento.
- **`ocr_model.py`**: Modelo OCR basado en Transformers para reconocer y extraer el texto de los manuscritos. Este modelo es ajustado mediante *fine-tuning* para obtener mejores resultados en el reconocimiento de texto.
- **`text_completion.py`**: Script para el modelo secuencia-a-secuencia que completa texto en los manuscritos deteriorados, utilizando *tokens <MASK>* para representar partes faltantes del texto.
- **`evaluate.py`**: Contiene los scripts para evaluar el desempeño de los modelos, utilizando métricas como CER (Character Error Rate), WER (Word Error Rate), IoU (Intersection over Union), y mAP (Mean Average Precision).

#### **models/**
Esta carpeta contiene los modelos entrenados, organizados en subcarpetas según el tipo de modelo.

- **`ocr_model/`**: Modelos entrenados para el reconocimiento óptico de caracteres (OCR) basados en Transformers.
- **`text_completion_model/`**: Modelos entrenados para el completado de texto en los manuscritos deteriorados.

#### **api/**
Contiene el código para la API que expone las funcionalidades de los algoritmos implementados, permitiendo a los usuarios acceder a los resultados de los modelos de una manera más interactiva.

- **`app.py`**: Código de la API que presenta los resultados obtenidos a partir de los algoritmos de segmentación, OCR y completado de texto. Puede incluir rutas para cargar las imágenes, procesarlas y devolver los resultados visuales o textuales.

#### **results/**
Almacena los resultados obtenidos a partir de los algoritmos, tanto en términos de evaluación cuantitativa como de visualización de los datos procesados.

- **`evaluation/`**: Carpeta donde se almacenan los resultados de las evaluaciones, como gráficos y métricas que muestran el desempeño de los modelos (ej., CER, WER, IoU, mAP).
- **`visualizations/`**: Contiene imágenes y visualizaciones de los resultados, como ejemplos de segmentación, reconocimiento de texto (OCR) y completado de texto en los manuscritos.

#### **README.md**
Archivo de documentación principal del proyecto. Contiene una descripción general del proyecto, los objetivos, la estructura del repositorio, instrucciones para instalar las dependencias, ejecutar los scripts y reproducir los resultados.

#### **LICENSE**
Archivo que especifica la licencia bajo la cual se distribuye el código del proyecto. Esto es importante si deseas compartir tu código con otros y aclarar los términos bajo los cuales puede ser usado, modificado y distribuido.

#### **requirements.txt**
Archivo que contiene las dependencias necesarias para ejecutar el proyecto, como OpenCV, Transformers, TensorFlow, PyTorch, entre otras. Este archivo permite a otros usuarios instalar todas las librerías requeridas de manera sencilla utilizando el comando `pip install -r requirements.txt`.

## Requisitos

Este proyecto depende de las siguientes librerías y herramientas:
OpenCV para procesamiento de imágenes.
Transformers de Hugging Face para modelos de NLP.
TensorFlow o PyTorch para la implementación y entrenamiento de los modelos.
