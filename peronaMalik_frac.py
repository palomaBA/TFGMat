import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from imageio.v2 import imread
import time
import cv2 as cv

def anisofrac(inimage_path, iterations, K):
    # Load grayscale image and convert to float
    outimage = imread(inimage_path, pilmode='L').astype(np.float64)
    m, n = outimage.shape

    # Discretization parameters
    deltax = 1 / (m - 1)
    deltay = 1 / (n - 1)
    deltamin = min(deltax, deltay)
    deltat = (deltamin ** 2) / 4  # Stability condition

    sx = deltat / (deltax ** 2)
    sy = deltat / (deltay ** 2)

    for _ in range(iterations):
        # South and east differences
        diffY1 = np.zeros_like(outimage)
        diffY1[:-1, :] = outimage[1:, :] - outimage[:-1, :]

        diffX1 = np.zeros_like(outimage)
        diffX1[:, :-1] = outimage[:, 1:] - outimage[:, :-1]

        # North and west differences
        diffY2 = np.zeros_like(outimage)
        diffY2[1:, :] = -diffY1[:-1, :]

        diffX2 = np.zeros_like(outimage)
        diffX2[:, 1:] = -diffX1[:, :-1]

        # Fractional conductivity function
        g1 = 1 / (1 + ((np.sqrt((diffX1/deltax)**2 + (diffY1/deltay)**2)) / (K/deltamin))**2)
        fluxY1 = diffY1 * g1
        fluxX1 = diffX1 * g1

        g2 = 1 / (1 + ((np.sqrt((diffX2/deltax)**2 + (diffY2/deltay)**2)) / (K/deltamin))**2)
        fluxY2 = diffY2 * g2
        fluxX2 = diffX2 * g2

        # Update image
        outimage += sy * (fluxY1 + fluxY2) + sx * (fluxX1 + fluxX2)

    return outimage

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Difusión anisotrópica (Perona-Malik) con función fraccional')
    parser.add_argument('iterations', type=int, help='número de iteraciones')
    parser.add_argument('K', type=int, help='Parametro K')
    parser.add_argument('inimage', type=str, help='Nombre de la foto')
    parser.add_argument('output_dir', type=str, help='Donde se guardará el resultado')
    parser.add_argument('--nomostrar', action='store_true', help='No mostrar la imagen')
    args = parser.parse_args()
    
    start = time.time()
    result = anisofrac(args.inimage, args.iterations, args.K)
    end = time.time()
    print(f"Tiempo de procesamiento: {end - start:.6f} segundos")
    
    # Mostrar el resultado clipeado a [0, 255]
    result_disp = np.clip(result, 0, 255).astype(np.uint8)
    if not args.nomostrar:
        plt.imshow(result_disp, cmap='gray')
        plt.axis('off')
        plt.title("Imagen procesada (función fraccional)")
        plt.show()
    
    # Guardar el resultado
    base = os.path.basename(args.inimage)
    name, ext = os.path.splitext(base)
    
    final_output_path = os.path.join(args.output_dir, f"PeronaMalik_Frac_K{args.K}_it{args.iterations}{ext}")
    cv.imwrite(final_output_path, result_disp)
    print(f"Imagen final guardada: {final_output_path}\n")