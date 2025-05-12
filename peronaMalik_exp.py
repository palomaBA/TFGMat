import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from imageio.v2 import imread
import time
import cv2 as cv

def anisoexp(inimage_path, iterations, K):
    """Función que aplica la difusión anisotrópica de Perona-Malik a una imagen.
    
    Attributes:
        inimage_path (str): Ruta de la imagen a procesar.
        iterations (int): Número de iteraciones.
        K (float): Parámetro K para la difusión.
    Returns:
        numpy.ndarray: Imagen procesada.
    """
    # Cargar imagen en escala de grises y convertir a float
    outimage = imread(inimage_path, pilmode='L').astype(np.float64)
    m, n = outimage.shape

    # Parámetros de discretización
    deltax = 1 / (m - 1)
    deltay = 1 / (n - 1)
    deltamin = min(deltax, deltay)
    deltat = (deltamin ** 2) / 4

    sx = deltat / (deltax ** 2)
    sy = deltat / (deltay ** 2)

    for _ in range(iterations):
        # Diferencias hacia el sur y el este
        diffY1 = np.zeros_like(outimage)
        diffY1[:-1, :] = outimage[1:, :] - outimage[:-1, :]

        diffX1 = np.zeros_like(outimage)
        diffX1[:, :-1] = outimage[:, 1:] - outimage[:, :-1]

        # Diferencias hacia el norte y el oeste
        diffY2 = np.zeros_like(outimage)
        diffY2[1:, :] = -diffY1[:-1, :]

        diffX2 = np.zeros_like(outimage)
        diffX2[:, 1:] = -diffX1[:, :-1]

        # Conductividad exponencial
        g1 = np.exp(-((1 / ((K / deltamin) ** 2)) * ((diffX1 / deltax) ** 2 + (diffY1 / deltay) ** 2)))
        fluxY1 = diffY1 * g1
        fluxX1 = diffX1 * g1

        g2 = np.exp(-((1 / ((K / deltamin) ** 2)) * ((diffX2 / deltax) ** 2 + (diffY2 / deltay) ** 2)))
        fluxY2 = diffY2 * g2
        fluxX2 = diffX2 * g2

        # Actualización de la imagen
        outimage += sy * (fluxY1 + fluxY2) + sx * (fluxX1 + fluxX2)


    return outimage


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Difusión anisotrópica (Perona-Malik)')
    parser.add_argument('iterations', type=int, help='número de iteraciones')
    parser.add_argument('K', type=int, help='Parametro K')
    parser.add_argument('inimage', type=str, help='Nombre de la foto')
    parser.add_argument('output_dir', type=str, help='Donde se guardará el resultado')
    parser.add_argument('--nomostrar', action='store_true', help='No mostrar la imagen')
    args = parser.parse_args()

    
    start = time.time()
    result = anisoexp(args.inimage, args.iterations, args.K)
    end = time.time()
    print(f"Tiempo de procesamiento: {end - start:.6f} segundos")
    
    # Mostrar el resultado clipeado a [0, 255]
    result_disp = np.clip(result, 0, 255).astype(np.uint8)
    if not args.nomostrar:
        plt.imshow(result_disp, cmap='gray')
        plt.axis('off')
        plt.title("Imagen procesada")
        plt.show()
    
    # Guardar el resultado
    base = os.path.basename(args.inimage)
    name, ext = os.path.splitext(base)

    
    final_output_path = os.path.join(args.output_dir, f"PeronaMalik_Exp_K{args.K}_it{args.iterations}{ext}")
    cv.imwrite(final_output_path, result_disp)
    print(f"Imagen final guardada: {final_output_path}\n")
    
