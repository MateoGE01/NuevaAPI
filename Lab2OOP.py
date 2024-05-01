"""
Caso de estudio: Gestión de parqueadero con listas enlazadas
Para este laboratorio cada equipo deberá desarrollar un programa que facilite la gestión de vehículos en un parqueadero. 
El parqueadero cuenta con 3 pisos, cada piso con una capacidad para 120 motocicletas y 80 autos. 
Adicionalmente, en cada piso hay 10 espacios para personas de movilidad reducida. 

Requerimientos Funcionales:
1.	El sistema de ingreso al parqueadero es automatizado y en su entrada hay un tablero digital con un mapa que 
permite visualizar los espacios disponibles. 

2.	Cuando un vehículo ingresa, se registra su placa y cuando se ubica en el parqueadero, se asocia con la posición 
del parqueadero, de manera que este espacio debe aparece como “ocupado”. Nota: la nomenclatura del parqueadero debe 
representar su ubicación, por ejemplo, P2A8 representa el parqueadero del piso 2, fila A, puesto 8.

3.	La ubicación en que se ha parqueado un vehículo se puede simular con una asignación aleatoria del parqueadero. 
Si el vehículo registra que tiene movilidad reducida, entonces se le asignará este tipo de parqueadero. 
Se debe validar que, si un parqueadero está ocupado, no se puede asignar a otro auto.
 
4.	El administrador del parqueadero podrá consultar dónde está parqueado un vehículo y cuáles son los vehículos 
de cada piso. 

5.	Se debe registrar la hora de ingreso y de salida del vehículo para calcular el monto a pagar. 
El precio es de $2000 por hora, o fracción. Cuando el vehículo sale del parqueadero, debe pagar y su registro será eliminado de las listas.

Requerimientos de programación:
1.	Se pueden utilizar las estructuras de datos disponibles en Python, sin embargo, se debe definir al menos un 
TAD nuevo.

2.	El programa debe manejar al menos tres listas: 
a.	Lista con los registros de las placas de vehículos que van ingresando.
b.	Lista con el parqueadero asignado.
c.	Lista con la hora de ingreso.

"""
import random
from datetime import datetime

class Parqueadero:
    def __init__(self, ubicacion, tipo):
        self.ubicacion = ubicacion
        self.tipo = tipo
        self.ocupado = False
        self.vehiculo = None
        
class Vehiculo:
    def __init__(self, placa, tipo):
        self.placa = placa
        self.tipo = tipo
        self.parqueadero = None
        self.hora_ingreso = None
        self.siguiente = None

    
class Sistema:
    def __init__(self) -> None:
        self.head = None
        self.parqueaderos = self.parqueaderos_lista()
        
    def parqueaderos_lista(self):#Crea todos los parqueaderos
        parqueaderos = [] 
        for piso in range(1, 4):
            for fila in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
                for puesto in range(1, 13):#LLega hasta 12, motocicletas
                    parqueaderos.append(Parqueadero(f"P{piso}{fila}{puesto}", "Motocicleta"))
                for puesto in range(13, 21):#Llega hasta 8#autos
                    parqueaderos.append(Parqueadero(f"P{piso}{fila}{puesto}", "Auto"))
                for puesto in range(21, 22):
                    parqueaderos.append(Parqueadero(f"P{piso}{fila}{puesto}", "Movilidad Reducida"))     
                    
        return parqueaderos
    

    def parqueadero_disponible(self, tipo):#CUMPLE PUNTO 3. Verifica si hay parqueaderos disponibles para el tipo de vehiculo que ingresará
        parqueaderos_disponibles = []
        for parqueadero in self.parqueaderos:
            if parqueadero.tipo == tipo and parqueadero.ocupado == False:
                parqueaderos_disponibles.append(parqueadero)
        
        if parqueaderos_disponibles != []:#Si hay parqueaderos disponibles
            return random.choice(parqueaderos_disponibles)
        else:
            print("No hay parqueaderos disponibles")
            
    def asignar_parqueadero(self, vehiculo):#Asigna un parqueadero a un vehiculo, pero verifica que no esté ocupado
        parqueadero = self.parqueadero_disponible(vehiculo.tipo)
        parqueadero.ocupado = True
        parqueadero.vehiculo = vehiculo
        vehiculo.parqueadero = parqueadero
        
                
    def ingreso(self, placa, tipo, hora):#Ingreso de vehiculo, es como el método Insert de LinkedList
        if self.head == None:
            self.head = Vehiculo(placa, tipo)#El primer vehiculo que ingrese se considerará el self.head
            self.asignar_parqueadero(self.head)
            self.head.hora_ingreso = datetime.strptime(hora, "%H:%M") 
        else:
            current = self.head
            while current.siguiente:
                current = current.siguiente
            current.siguiente = Vehiculo(placa, tipo)
            self.asignar_parqueadero(current.siguiente)
            current.siguiente.hora_ingreso = datetime.strptime(hora, "%H:%M")
            
    #CUMPLE PUNTO 4        
    def consultar_ubicacion_vehiclo(self, placa):#Es como el Search de LinkedList
        current = self.head
        while current != None:
            if current.placa == placa:
                return current.parqueadero.ubicacion
            current = current.siguiente
    
    def consultar_vehiculos_piso(self):
        for piso in range(1, 4):
            print(f"Piso {piso}:")
            current = self.head
            while current != None:
                if current.parqueadero.ubicacion.startswith(f"P{piso}"):
                    print(f"Vehiculo {current.placa} en {current.parqueadero.ubicacion}")
                current = current.siguiente
    
    #CUMPLE PUNTO 5
    def salida(self, placa, hora_salida):#Es como el Delete de LinkedList, pero con la diferencia que se calcula el precio a pagar
        current = self.head
        if (current != None) and (current.placa == placa):#Si el vehiculo a salir es el primero
            current.parqueadero.ocupado = False
            current.parqueadero.vehiculo = None
            current.parqueadero = None
            self.head = current.siguiente
            self.calcular_precio(current.placa, current.hora_ingreso, hora_salida)#Calcula el precio a pagar
            current = None
            return
        
        previous = None
        while (current != None):#Si el vehiculo a salir no es el primero
            previous = current
            current = current.siguiente
            if current.placa == placa:
                current.parqueadero.ocupado = False
                current.parqueadero.vehiculo = None
                current.parqueadero = None
                previous.siguiente = current.siguiente
                self.calcular_precio(current.placa, current.hora_ingreso, hora_salida)#Calcula el precio a pagar
                current = None

    def calcular_precio(self, placa, hora_entrada, hora_salida):#Calcula el precio a pagar por el tiempo que estuvo el vehiculo en el parqueadero
        hora_salida = datetime.strptime(hora_salida, "%H:%M")
        diferencia = hora_salida - hora_entrada
        precio_hora = 2000
        costo_hora = (diferencia.seconds // 3600) * precio_hora
        costo_minuto = (diferencia.seconds % 3600 // 60) * (precio_hora / 60)
        monto = round(costo_hora + costo_minuto, 2)
        print(f"El monto a pagar es de ${monto} para el vehiculo {placa}")

    #CUMPLE PUNTO 1
    def mostrar_parqueaderos_disponibles(self):#Es para mostar los parqueaderos disponibles
        print("Parqueaderos disponibles:")
        for parqueadero in self.parqueaderos:
            if parqueadero.ocupado == False:
                print(f"Parqueadero {parqueadero.ubicacion} tipo {parqueadero.tipo}")  
    
    #Es para mostrar los parqueaderos ocupados, no es un requerimiento, pero es útil para verificar que el programa funciona
    def mostrar_parqueaderos_ocupados(self):
            ocupados = []
            for parqueadero in self.parqueaderos:
                if parqueadero.ocupado:
                    ocupados.append(parqueadero)
            for parqueadero in ocupados:
                print(f"Parqueadero {parqueadero.ubicacion} tipo {parqueadero.tipo} ocupado por {parqueadero.vehiculo.placa}")
    
                           
    #Es para imprimir los parqueaderos, me sirve para verificar que están todos los parqueaderos        
    def imprimir_parqueaderos(self):
        for piso in range(1, 4):
            print(f"Piso {piso}:")
            for fila in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
                parqueaderos_fila = [parqueadero for parqueadero in self.parqueaderos if parqueadero.ubicacion.startswith(f"P{piso}{fila}")]
                fila_str = f"Fila {fila}: "
                for parqueadero in parqueaderos_fila:
                    if parqueadero.ocupado:
                        fila_str += "OC "
                    else:
                        fila_str += f"{parqueadero.ubicacion} "
                print(fila_str)

if __name__ == "__main__":
    hola = Sistema()
    hola.ingreso("ABC123", "Auto", "07:40") #Punto 2 y por dentro cumple el 3
    hola.ingreso("DEF456", "Auto", "08:00") 
    hola.ingreso("GHI789", "Auto", "09:00")
    hola.ingreso("JKL012", "Auto", "10:00")
    hola.salida("ABC123", "09:23") #Punto 5
    #hola.mostrar_parqueaderos_ocupados() #Para verificar que el programa funciona
    hola.consultar_vehiculos_piso() #Punto 4
    #hola.mostrar_parqueaderos_disponibles()   Punto 1, son bastantes así que para evitar llenar toda la terminal lo mantengo comentado