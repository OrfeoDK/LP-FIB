# Práctica Logo3D

Este documento describe los pasos necesarios para llevar a cabo la ejecución de la práctica de compiladores y Python.

## Instalación

Primeramente se ha de instalar [Python3](https://www.python.org/downloads/):

Después, para comprobar que se ha instalado PIP, utiliza el comando:

```bash
pip help
```

Para instalar las librerias necesarias, entra en la carpeta donde tengas el proyecto haciendo cd en la consola y utiliza el siguiente comando:

### UNIX

```bash
python -m pip install -r requirements.txt
```

### WINDOWS

```bash
py -m pip install -r requirements.txt
```

A continuación, descarga el .jar de [ANTLR 4.9.2](https://www.antlr.org/download.html) y sigue las siguientes indicaciones según tu sistema operativo:

### UNIX

0- Instala Java (versión 1.7 o mayor)

1- Guarda antlr-4.9.2-complete.jar en un sitio racional como /usr/local/lib

2- Añadelo a tu CLASSPATH:

```bash
export CLASSPATH=".:/usr/local/lib/antlr-4.9.2-complete.jar:$CLASSPATH"
```

3- Crea aliases para la ANTLR Tool, y TestRig:

```bash
alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.9.2-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
alias grun='java -Xmx500M -cp "/usr/local/lib/antlr-4.9.2-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'
```

### WINDOWS

0- Instala Java (versión 1.7 o mayor)

1- Guarda antlr-4.9.2-complete.jar en tu directorio para librerias 3rd party de Java, como C:\Javalib

2- Añade antlr-4.9.2-complete.jar a tu CLASSPATH, ya sea:

- Permanentemente: Usando System Properties dialog > Environment variables > Create or append to CLASSPATH variable
- Temporalmente con el comando:

```bash
SET CLASSPATH=.;C:\Javalib\antlr-4.9.2-complete.jar;%CLASSPATH%
```

3- Crea comandos cortos convenientes para la ANTLR Tool, and TestRig usando los comandos doskey:

```bash
doskey antlr4=java org.antlr.v4.Tool $*
doskey grun =java org.antlr.v4.gui.TestRig $*
```

## Generar archivos ANTLR

Para generar los archivos necesarios con ANTLR situate en la carpeta donde se ubica el proyecto y utiliza el comando:

```bash
antlr4 -Dlanguage=Python3 -no-listener -visitor logo3d.g
```

## Ejecución

Crea un archivo .l3d y escribe ahí el programa en Logo3D que quieras ejecutar.
En la linea de comandos, situate en la carpeta donde se encuentra el proyecto.

Para ejecutar tu programa desde la función main utiliza el comando:

```bash
python3 logo3d.py nom_programa.l3d
```

Para ejecutar tu programa desde un procedimiento en concreto con sus respectivos parámetros utiliza el comando:

```bash
python3 logo3d.py nom_programa.l3d nom_procedimiento param1 param2 etc.
```

## Autor

- Moisés Campillo
