"""
Ejercicio 2 
Funciones y un poco de POO. 

Crea una clase llamada Punto con sus dos coordenadas X y Y. 
Añade un método constructor para crear puntos, si no se recibe una coordenada, su valor será cero. 
Redefine el método string para que al imprimir por pantalla el punto aparezca en formato (X,Y) 
Define el método Cuadrante que indique a qué cuadrante pertenece el punto: 
 

Define el método Vector, cuyos parámetros sean otro par de coordenadas y que calcule el vector que une los dos puntos. 
 

Define el método Distancia, cuyos parámetros sean otro par de coordenadas y que calcule la distancia entre los dos puntos y la muestre por pantalla. 
 
PROTIP: En Python, la función raíz cuadrada se debe importar del módulo math y se llama sqrt(). 
"""

import math

class Punto:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def cuadrante(self):
        if self.x == 0 and self.y == 0:
            return "El punto está en el origen"
        elif self.x == 0:
            return "El punto está sobre el eje Y"
        elif self.y == 0:
            return "El punto está sobre el eje X"
        elif self.x > 0 and self.y > 0:
            return "Primer cuadrante"
        elif self.x < 0 and self.y > 0:
            return "Segundo cuadrante"
        elif self.x < 0 and self.y < 0:
            return "Tercer cuadrante"
        elif self.x > 0 and self.y < 0:
            return "Cuarto cuadrante"

    def vector(self, otro):
        dx = otro.x - self.x
        dy = otro.y - self.y
        print(f"Vector desde {self} hasta {otro}: ({dx}, {dy})")
        return (dx, dy)

    def distancia(self, otro):
        d = math.sqrt((otro.x - self.x) ** 2 + (otro.y - self.y) ** 2)
        print(f"Distancia entre {self} y {otro}: {d}")
        return d

# Ejemplo de uso
p1 = Punto(3, 4)
p2 = Punto(-2, 5)

print(f"Punto 1: {p1}")
print(f"Punto 2: {p2}")

print(p1.cuadrante())
print(p2.cuadrante())

p1.vector(p2)
p1.distancia(p2)
