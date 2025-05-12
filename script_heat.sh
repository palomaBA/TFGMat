#!/bin/bash
# Script para procesar múltiples imágenes con la ecuación del calor

# Directorio donde se encuentran las imágenes de prueba
input_dir="Imagenes_prueba"  # Cambia esta ruta si es necesario

# Directorio base para guardar los resultados
output_base="resultados"

# Habilitar globbing sin resultados y manejo de mayúsculas/minúsculas
shopt -s nullglob
shopt -s nocaseglob

# Definir arrays con distintos parámetros para pruebas
r_values=(0.1 0.25 0.5)         
t_values=(3 10 20 50 100)    

# Recorre cada imagen con extensión jpg, jpeg o png
#for img in "$input_dir"/*.{jpg,jpeg,png}; do
img="$input_dir/imagen_gris_ruido_gaussiano.png"
    [ -e "$img" ] || continue

    base=$(basename "$img")
    name="${base%.*}"
    
    # Crear la carpeta de salida para esta imagen
    output_dir="$output_base/$name"
    if [ ! -d "$output_dir" ]; then
        mkdir -p "$output_dir"
    fi
    
    # Copiar la imagen original a la carpeta de resultados
    original_img="$output_dir/${name}_original.${base##*.}"
    if [ ! -f "$original_img" ]; then
        cp "$img" "$original_img"
    fi

    echo "Procesando la imagen: $img"
    
    # Ejecutar ecuacionCalor_vect.py con cada combinación de parámetros
    for r in "${r_values[@]}"; do
        for t in "${t_values[@]}"; do
            echo "Ejecutando ecuacionCalor_vect.py con r=$r, t=$t"
            # Ejecutar el script de la ecuación del calor con los parámetros actuales
            python3 ecuacionDelCalor_vect.py "$r" "$t" "$img" "$output_dir" --nomostrar
        done
    done
#done
