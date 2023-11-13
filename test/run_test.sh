#!/bin/bash

# Guarda el directorio actual
current_dir=$(pwd)

# Mueve los archivos .py a la carpeta superior
mv *.py ..

# Entra a la carpeta superior
cd ..

# Ejecuta pytest en todos los archivos .py
pytest -v

# Vuelve al directorio original
cd "$current_dir"

# Mueve nuevamente los archivos .py a la carpeta original
mv *.py "$current_dir"
