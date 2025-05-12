# Difusión en Imágenes mediante EDPs

Este repositorio contiene la implementación de modelos de difusión para el tratamiento de imágenes basado en ecuaciones en derivadas parciales (EDPs). Incluye tanto difusión isotrópica como modelos de difusión anisotrópica de Perona-Malik, con dos tipos de funciones de difusión.

---

## Estructura del proyecto

| Archivo                         | Descripción                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| `ecuacionDelCalor_vect.py`     | Aplica la ecuación del calor (difusión isotrópica) a una imagen.           |
| `peronaMalik_exp.py`           | Difusión anisotrópica de Perona-Malik con función de difusión exponencial. |
| `peronaMalik_frac.py`          | Difusión anisotrópica de Perona-Malik con función fraccional (racional).   |
| `script_heat.sh`               | Ejecuta múltiples pruebas con la ecuación del calor sobre una imagen.      |
| `script_prueba_tfg.sh`         | Ejecuta todos los métodos con distintas configuraciones. Llama también a `script_heat.sh`. |
| `Imagenes_prueba/`             | Carpeta donde deben colocarse las imágenes originales a procesar.          |
| `resultados/`                  | Carpeta donde se guardan automáticamente los resultados generados.         |
| `requirements.txt`             | Lista de dependencias necesarias para ejecutar los scripts.                |

---

## Ejecución manual

### Difusión isotrópica (ecuación del calor)

```bash
python3 ecuacionDelCalor_vect.py r t imagen.png resultados/ [--pasos] [--nomostrar]
```

- `r`: paso de tiempo (por ejemplo, `0.25`)
- `t`: tiempo total de evolución (por ejemplo, `10`)
- `imagen.png`: ruta de la imagen de entrada (debe estar en `Imagenes_prueba/`)
- `resultados/`: carpeta de salida
- `--pasos`: (opcional) muestra los pasos intermedios
- `--nomostrar`: (opcional) no muestra la imagen al finalizar

### Difusión anisotrópica de Perona-Malik

#### Función exponencial

```bash
python3 peronaMalik_exp.py iteraciones K imagen.png resultados/ [--nomostrar]
```

#### Función fraccional

```bash
python3 peronaMalik_frac.py iteraciones K imagen.png resultados/ [--nomostrar]
```

- `iteraciones`: número de pasos del algoritmo (por ejemplo, `100`)
- `K`: parámetro de sensibilidad (por ejemplo, `10`)
- `imagen.png`: imagen de entrada
- `resultados/`: carpeta donde se guardará la imagen procesada
- `--nomostrar`: (opcional) no muestra el resultado por pantalla

---

## Ejecución automática por lotes

### `script_heat.sh`

Procesa una imagen específica usando la ecuación del calor con distintos valores de `r` y `t`. Puedes modificar la ruta de la imagen en el script si deseas usar otra.

```bash
bash script_heat.sh
```

### `script_prueba_tfg.sh`

Ejecuta todos los métodos (calor, Perona-Malik exponencial y fraccional) con varias combinaciones de parámetros sobre una imagen fija. También llama al script `script_heat.sh` al final.

```bash
bash script_prueba_tfg.sh
```

> **Nota:** Asegúrate de tener las imágenes en la carpeta `Imagenes_prueba/` y que los scripts `.sh` tienen permisos de ejecución:  
> 
> ```bash
> chmod +x script_heat.sh script_prueba_tfg.sh
> ```

---

## Requisitos

El entorno requiere Python 3 y las siguientes librerías:

- `numpy===1.24.4`
- `matplotlib===3.7.2`
- `opencv-python===4.8.0.76`
- `imageio===2.31.1`

Instala todas las dependencias con:

```bash
pip install -r requirements.txt
```

---

## Ejemplo de uso rápido

```bash
# Procesar una imagen con la ecuación del calor
python3 ecuacionDelCalor_vect.py 0.25 10 Imagenes_prueba/imagen.png resultados/

# Procesar la misma imagen con Perona-Malik (exp)
python3 peronaMalik_exp.py 100 10 Imagenes_prueba/imagen.png resultados/

# Procesar con Perona-Malik (fraccional)
python3 peronaMalik_frac.py 100 10 Imagenes_prueba/imagen.png resultados/
```

---

## Autor

Este proyecto ha sido desarrollado como parte del Trabajo de Fin de Grado (TFG) sobre ecuaciones en derivadas parciales aplicadas al procesamiento de imágenes.
