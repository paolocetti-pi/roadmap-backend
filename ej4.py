"""
Ejercicio 4 
Veamos un poco de herencia y polimorfismo. 

1) Crea una superclase llamada Vehículo cuyos atributos sean Color y Ruedas. Redefine el método str para que devuelva por pantalla: 
Color: {El color del vehículo}, {Cantidad de ruedas} ruedas. 

Crea una subclase llamada Carro y agrega los atributos Velocidad, Cilindraje. Redefine el método str para que devuelva por pantalla 
Color: {El color del vehículo}, {Velocidad} Km/h, {Cantidad de ruedas} ruedas, {Cilindraje} cc". 

2) Extiende las subclases siguiendo el siguiente esquema: 
 
PROTIP: Utiliza la función super() 

Crea al menos un objeto de cada subclase y añádelos a una lista llamada Vehículos. 
Define una función llamada catalogar() que reciba un argumento optativo ruedas. La idea es que muestre únicamente los vehículos cuyo número de ruedas coincida con el valor del argumento. Debe mostrar el siguiente mensaje solo si se envía el argumento ruedas: 
Se han encontrado {} vehículos con {} ruedas: 
"""

# Superclase Vehículo
class Vehiculo:
    def __init__(self, color, ruedas):
        self.color = color
        self.ruedas = ruedas

    def __str__(self):
        return f"Color: {self.color}, {self.ruedas} ruedas"

# Subclase Carro
class Carro(Vehiculo):
    def __init__(self, color, ruedas, velocidad, cilindraje):
        super().__init__(color, ruedas)
        self.velocidad = velocidad
        self.cilindraje = cilindraje

    def __str__(self):
        return f"Color: {self.color}, {self.velocidad} Km/h, {self.ruedas} ruedas, {self.cilindraje} cc"
    
class Camioneta(Carro):
    def __init__(self, color, ruedas, velocidad, cilindraje, carga):
        super().__init__(color, ruedas, velocidad, cilindraje)
        self.carga = carga

    def __str__(self):
        return (f"Color: {self.color}, {self.velocidad} Km/h, {self.ruedas} ruedas, "
                f"{self.cilindraje} cc, Carga: {self.carga} Kg")


class Bicicleta(Vehiculo):
    def __init__(self, color, ruedas, tipo):
        super().__init__(color, ruedas)
        self.tipo = tipo  # urbana / deportiva

    def __str__(self):
        return f"Color: {self.color}, {self.ruedas} ruedas, Tipo: {self.tipo}"


class Motocicleta(Bicicleta):
    def __init__(self, color, ruedas, tipo, velocidad, cilindraje):
        super().__init__(color, ruedas, tipo)
        self.velocidad = velocidad
        self.cilindraje = cilindraje

    def __str__(self):
        return (f"Color: {self.color}, {self.velocidad} Km/h, {self.ruedas} ruedas, "
                f"{self.cilindraje} cc, Tipo: {self.tipo}")
    

def catalogar(vehiculos, ruedas=None):
    if ruedas is not None:
        filtrados = [v for v in vehiculos if v.ruedas == ruedas]
        print(f"Se han encontrado {len(filtrados)} vehículos con {ruedas} ruedas:")
        for v in filtrados:
            print(f"- {v}")
    else:
        for v in vehiculos:
            print(f"- {v}")


# Crear objetos de cada subclase
vehiculo1 = Vehiculo("Rojo", 4)
carro1 = Carro("Azul", 4, 160, 2000)
camioneta1 = Camioneta("Negro", 4, 120, 3000, 800)
bicicleta1 = Bicicleta("Verde", 2, "urbana")
moto1 = Motocicleta("Gris", 2, "deportiva", 220, 600)

# Lista de vehículos
vehiculos = [vehiculo1, carro1, camioneta1, bicicleta1, moto1]

# Mostrar todos
print("Todos los vehículos:")
catalogar(vehiculos)

# Mostrar filtrados por ruedas
print("\nVehículos con 2 ruedas:")
catalogar(vehiculos, ruedas=2)

