#!/bin/bash

# Guarda el directorio actual
current_dir=$(pwd)

#Limpia la base de datos
rm ../db/lacosa.sqlite
python3 ../db/database.py

# Mueve los archivos .py a la carpeta superior
mv *.py ..

# Entra a la carpeta superior
cd ..

# Ejecuta pytest en todos los archivos .py
pytest -v

# Mueve nuevamente los archivos .py a la carpeta original
mv *.py "$current_dir"

# Vuelve a la carpeta de test
cd "$current_dir"

#Devuelve main y defintitions al directorio original
mv main.py ..
mv definitions.py ..



