# JavaLexicalAnalyser

---
**Elaborado por:**
+ Bernardo Altamirano (167881)
+ Ivana Lucho (167028)
+ Andrea Padilla (166605)
+ América Castrejón (166414)
+ Alexis Calvillo (159702)
+ Maritrini García (151490)
---

## Introducción
El proyecto consiste en construir un sencillo reconocedor de declaraciones de variables de un lenguaje de programación. El programa debe leer los datos de entrada, una serie de declaraciones de variables y debe arrojar como resultado una serie de estadisticas relacionadas con las variables declaradas y sus tipos.

## Especificaciones generales

* El programa debe leer los datos de entrada de un archivo, el cual se le pasa por medio de la línea de comandos o se carga por medio de una  ventana de dialogo de abrir archivo.
* El programa debe utilizar expresiones regulares para realizar el analisis de la entrada. Puedes usar los paquetes o bibliotecas estandar de expresiones regulares de Python o Java.
* Tu programa debe reconocer todos los tipos de declaraciones de variables del lenguaje Java en su version 8.
* La salida del programa debe contener los siguientes datos:
    * Numero total de variables declaradas.
    * Numero total de tipos utilizados en las declaraciones encontradas.
    * Numero total de variables declaradas de cada tipo.
    * Numero total de variables inicializadas.
    * Numero total de variables de tipo arreglo.
    * Clasificacion de todos los nombres de variables por tipo declarado.
* El formato de la salida es a libre eleccion, pero debe ser claro.

## Funcionamiento
Para evaluar las expresiones se definieron métodos distintos para cada tipo de dato que admite Java 8. La validación de las declaraciones se realizo usando expresiones regulares. Estos métodos pueden ser consultados en su archivo correspondiente:
* [float](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/DoubleFloat.py)
* [String](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/String.py)
* [boolean](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/boolean.py)
* [byte](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/byte.py)
* [char](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/char.py)
* [int](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/int.py)
* [long](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/long.py)
* [short](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/short.py)

El archivo que contiene las expresiones a evaluar está titulado como [`java-regex.txt`](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/java-regex.txt). El usuario puede modificar este archivo para evaluar las distintas declaraciones. Es importante notar que las distintas declaraciones están en un mismo renglón separadas por un `;`.

El archivo [`main.py`](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/main.py) es el que el usuario debe correr para utilizar el proyecto. Este último contiene las llamadas a los métodos que mencionamos anteriormente.

## Ejecución
Descargar el repositorio, colocarse sobre el archivo [`main.py`](https://github.com/bernyag/JavaLexicalAnalyser/blob/main/main.py) y correr el siguiente comando en el CLI:
   +`python3 main.py`
