import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import time
import os

def difusion_isotropica(r, t, nb_foto, pasos=False, nomostrar=False):
    """Función que aplica la ecuación del calor a una imagen.

    Attributes:
        r (float): Paso de tiempo.
        t (float): Tiempo total de difusión.
        nb_foto (str): Nombre de la imagen a procesar.
        pasos (bool): Si True, muestra los pasos intermedios.
        nomostrar (bool): Si True, no muestra la imagen final.
    Returns:
        numpy.ndarray: Imagen procesada.
    """
    print("Empieza el programa")
    print("Bordes estáticos")
    if pasos:
        print("Mostrando pasos")
    
    # Leer la imagen
    foto = cv.imread(nb_foto, cv.IMREAD_GRAYSCALE)
    if foto is None:
        print("Error al leer la imagen")
        return
    
    print(foto.shape)
    print(foto.dtype)
    
    plt.figure()
    if not pasos:
        filas = 1
        columnas = 2
    else:
        columnas = 2
        filas = 1 + int(t / 2)
    
    plt.subplot(filas, columnas, 1)
    plt.imshow(foto, cmap='gray')
    plt.title('T=0')
    plt.axis('off')
    
    # Convertir a float32 para cálculos
    foto = foto.astype(np.float32)
    foto2 = np.copy(foto)

    # Crear máscaras para aplicar el operador de Laplace
    kernel = np.array([[0, r, 0],
                       [r, 1 - 4 * r, r],
                       [0, r, 0]], dtype=np.float32)
    
    start_time=time.time()
    aux = 1
    
    for k in np.arange(0, t + r, r):
        print(f"Paso: {int(k / r)} de {int(t / r)}")
        # Usar convolución 2D para actualizar la imagen
        foto2 = cv.filter2D(foto2, -1, kernel, borderType=cv.BORDER_REFLECT)

        if pasos and k >= aux:
            plt.subplot(filas, columnas, int(1 + aux))
            plt.imshow(foto2, cmap='gray')
            plt.title(f'T={aux}')
            plt.axis('off')
            aux += 1

    end_time=time.time()
    print(f"Tiempo del algoritmo: {end_time - start_time:.6f} segundos")
    if not pasos:
        plt.subplot(filas, columnas, 2)
        plt.imshow(foto2, cmap='gray')
        plt.title(f'T={t}')
        plt.axis('off')
    if not nomostrar:
        plt.show()

    return foto2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ecuación del calor')
    parser.add_argument('r', type=float, help='Paso de tiempo')
    parser.add_argument('t', type=float, help='Tiempo')
    parser.add_argument('nb_foto', type=str, help='Nombre de la foto')
    parser.add_argument('output_dir', type=str, help='Directorio donde se guardará el resultado')
    parser.add_argument('--pasos', action='store_true', help='Muestra los pasos intermedios')
    parser.add_argument('--nomostrar', action='store_true', help='No mostrar la imagen')
    args = parser.parse_args()

    if args.t <= 0:
        print('El tiempo debe ser mayor que 0')
        sys.exit(1)
    if args.nb_foto is None:
        print('Falta el nombre de la foto')
        sys.exit(1)
    
    resultado = difusion_isotropica(args.r, args.t, args.nb_foto, args.pasos, args.nomostrar)
    
    if resultado is not None:
        # Guardar la imagen final en el output_dir
        base = os.path.basename(args.nb_foto)
        name, ext = os.path.splitext(base)
        output_path = os.path.join(args.output_dir, f"Calor_r{args.r}_t{args.t}{ext}")
        resultado_norm = np.clip(resultado, 0, 255).astype(np.uint8)
        cv.imwrite(output_path, resultado_norm)
        print(f"Imagen final guardada: {output_path}")
