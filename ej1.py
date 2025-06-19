"""
Ejercicio 1 
Arranquemos viendo un poco de variables y funciones. 

Tenemos 4 puntos que corresponden a dos coordenadas (x,y) que forman la diagonal de un rectángulo. 
Define el método Distancia, cuyos parámetros sean otro par de coordenadas y que calcule la distancia entre los dos puntos y la muestre por pantalla. 
Calcular la altura del rectángulo 
Calcular la base del rectángulo 
Calcular el área del rectángulo 
Cado uno de estos cálculos en una función distinta y mostrar los resultados. 

"""

import math

# Función para calcular la distancia entre dos puntos (x1, y1) y (x2, y2)
def distancia(p1, p2):
    d = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    print(f"Distancia entre {p1} y {p2}: {d}")
    return d

# Función para calcular la altura del rectángulo (diferencia en Y)
def altura(p1, p2):
    h = abs(p2[1] - p1[1])
    print(f"Altura del rectángulo: {h}")
    return h

# Función para calcular la base del rectángulo (diferencia en X)
def base(p1, p2):
    b = abs(p2[0] - p1[0])
    print(f"Base del rectángulo: {b}")
    return b

# Función para calcular el área del rectángulo
def area(p1, p2):
    b = base(p1, p2)
    h = altura(p1, p2)
    a = b * h
    print(f"Área del rectángulo: {a}")
    return a

# Ejemplo con dos puntos que definen la diagonal de un rectángulo
punto1 = (2, 3)
punto2 = (7, 9)

# Llamadas a las funciones
distancia(punto1, punto2)
altura(punto1, punto2)
base(punto1, punto2)
area(punto1, punto2)
