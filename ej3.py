"""
Ejercicio 3 
Objetos dentro de Objetos y alguna lista. 

Cree una clase Videojuego, que contenga como atributo de instancia título, genero, lanzamiento y un mensaje que se creó el Videojuego. 
Modifique el método string de la clase y muestre el titulo y la fecha de lanzamiento. 
Cree una clase catalogo que contenga una lista de Videojuegos. 
Cree los métodos necesarios para agregar, mostrar y eliminar Videojuegos en el catálogo. 
"""

# Clase Videojuego
class Videojuego:
    def __init__(self, titulo, genero, lanzamiento):
        self.titulo = titulo
        self.genero = genero
        self.lanzamiento = lanzamiento
        print(f"Se creó el videojuego: {self.titulo}")

    def __str__(self):
        return f"{self.titulo} (Lanzamiento: {self.lanzamiento})"

# Clase Catálogo
class Catalogo:
    def __init__(self):
        self.videojuegos = []

    def agregar(self, videojuego):
        self.videojuegos.append(videojuego)
        print(f"Se agregó '{videojuego.titulo}' al catálogo.")

    def mostrar(self):
        if not self.videojuegos:
            print("El catálogo está vacío.")
        else:
            print("Videojuegos en el catálogo:")
            for juego in self.videojuegos:
                print(f"- {juego}")

    def eliminar(self, titulo):
        for juego in self.videojuegos:
            if juego.titulo.lower() == titulo.lower():
                self.videojuegos.remove(juego)
                print(f"Se eliminó '{titulo}' del catálogo.")
                return
        print(f"No se encontró el videojuego '{titulo}' en el catálogo.")


# Crear algunos videojuegos
juego1 = Videojuego("The Legend of Zelda", "Aventura", 1986)
juego2 = Videojuego("Minecraft", "Sandbox", 2011)
juego3 = Videojuego("DOOM", "Shooter", 1993)

# Crear catálogo y operar sobre él
mi_catalogo = Catalogo()
mi_catalogo.agregar(juego1)
mi_catalogo.agregar(juego2)
mi_catalogo.agregar(juego3)

mi_catalogo.mostrar()

mi_catalogo.eliminar("Minecraft")
mi_catalogo.mostrar()

mi_catalogo.eliminar("FIFA")
