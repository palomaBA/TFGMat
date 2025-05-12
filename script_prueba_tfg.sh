#!/bin/bash
# Script para procesar múltiples imágenes con Perona-Malik

# Directorio donde se encuentran las imágenes
input_dir="Imagenes_prueba"  # Cambia esta ruta según dónde tengas tus imágenes

# Directorio base donde se guardarán los resultados
output_base="resultados"

# Habilitar globbing sin resultados y sin importar mayúsculas/minúsculas
shopt -s nullglob
shopt -s nocaseglob

# Definir arrays con distintos parámetros para pruebas
iterations_values=(50 80 150 500 800 1000)                   
K_values=(4 7 10 15 25)      

#r_values=(0.1)
#t_values=(10)
#K_values=(10)

# Recorre cada imagen con extensión jpg, jpeg o png en el directorio de entrada
#for img in "$input_dir"/*.{jpg,jpeg,png}; do
img="$input_dir/imagen_gris_ruido_gaussiano.png"
    # Verificar que la imagen exista
    [ -e "$img" ] || continue

    # Obtener el nombre base sin extensión
    base=$(basename "$img")
    name="${base%.*}"
    
    # Crear la carpeta de salida para esta imagen
    output_dir="$output_base/$name"
    mkdir -p "$output_dir"
    
    # Copiar la imagen original a la carpeta de resultados
    cp "$img" "$output_dir/${name}_original.${base##*.}"
    echo "Procesando la imagen: $img"
    
    # Ejecutar peronaMalik_vect.py con cada combinación de parámetros
    for it in "${iterations_values[@]}"; do
        
        for K in "${K_values[@]}"; do
            echo "Ejecutando peronaMalik_exp.py con iterations=$it, K=$K"
            # Ejecutar el script de Perona-Malik con los parámetros actuales
            python3 peronaMalik_exp.py "$it" "$K" "$img" "$output_dir" --nomostrar
            echo "Ejecutando peronaMalik_frac.py con iterations=$it, K=$K"
            # Ejecutar el script de Perona-Malik con los parámetros actuales
            python3 peronaMalik_frac.py "$it" "$K" "$img" "$output_dir" --nomostrar
        done
        
    done
#done

./script_heat.sh
