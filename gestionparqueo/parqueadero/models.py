from django.db import models

class Parking(models.Model):
    """
    Esta clase se encarga de almacenar la ubicación, tipo, estado de ocupación y el vehículo asociado al parqueadero.
    Hereda de models.Model de Django.

    Atributos:
        ubicacion (str): La ubicación del parqueadero.
        tipo (str): El tipo de vehículo que puede estacionar en el parqueadero.
        ocupado (bool): Indica si el parqueadero está ocupado o no.
        vehiculo (Vehiculo): El vehículo asociado al parqueadero.
    """
    ubicacion = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50)
    ocupado = models.BooleanField(default=False)
    vehiculo = models.OneToOneField('Vehiculo', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.ubicacion}'
    
class Vehiculo(models.Model):
    """
    Esta clase se encarga de almacenar la placa, tipo, parqueadero asociado, hora de ingreso y referencia al siguiente vehículo en la lista enlazada.
    Hereda de models.Model de Django. 

    Atributos:
        placa (str): La placa del vehículo.
        tipo (str): El tipo de vehículo.
        parqueadero (Parking): El parqueadero asociado al vehículo.
        hora_ingreso (datetime): La hora de ingreso del vehículo.
        siguiente (Vehiculo): Referencia al siguiente vehículo en la lista enlazada.
    """
    placa = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50)
    parqueadero = models.OneToOneField('Parking', on_delete=models.SET_NULL, null=True, blank=True, related_name='parqueadero_asociado')
    hora_ingreso = models.DateTimeField(null=True, blank=True)
    siguiente = None

    def __str__(self):
        return f'{self.placa}'


class sistema_parqueo:
    """
    Clase que representa un sistema de parqueo.

    Esta clase se encarga de administrar los parqueaderos, asignar y consultar ubicaciones de vehículos,
    y calcular el precio de estacionamiento.

    Atributos:
        head: El primer vehículo en la lista enlazada de vehículos ingresados al sistema.
    """
    def __init__(self):
        self.head = None

    def parqueaderos_lista(self):
        """
        Crea todos los parqueaderos disponibles en el sistema. Que son 210 por piso y 630 en total, es decir, 
        21 parqueaderos por fila(podían ser más o menos filas, se escogio 10 por pisos).
        """
        for piso in range(1, 4):
            for fila in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
                for puesto in range(1, 13):
                    Parking(ubicacion=f"P{piso}{fila}{puesto}", tipo="Motocicleta").save()
                for puesto in range(13, 21):
                    Parking(ubicacion=f"P{piso}{fila}{puesto}", tipo="Auto").save()
                for puesto in range(21, 22):
                    Parking(ubicacion=f"P{piso}{fila}{puesto}", tipo="Movilidad Reducida").save()    

    #Los siguientes 3 métodos cumplen punto 2 y 3
    def parqueadero_disponible(self, tipo):
        """
        Busca un parqueadero disponible del tipo especificado.
        El parqueadero se selecciona aleatoriamente de entre los parqueaderos disponibles.

        Args:
            tipo (str): El tipo de vehículo (Motocicleta, Auto, Movilidad Reducida).

        Returns:
            Parking: El parqueadero disponible del tipo especificado, o None si no hay ninguno disponible.
        """
        parqueaderos_disponibles = Parking.objects.filter(tipo=tipo, ocupado=False).order_by('?')

        if parqueaderos_disponibles.exists():
            return parqueaderos_disponibles.first()
        
    def asignar_parqueadero(self, vehiculo):
        """
        Asigna un parqueadero a un vehículo.
        El parqueadero asignado se marca como ocupado y se guarda el vehículo en el parqueadero.

        Args:
            vehiculo (Vehiculo): El vehículo al que se le asignará un parqueadero.
        """
        parqueadero = self.parqueadero_disponible(vehiculo.tipo)

        parqueadero.ocupado = True
        parqueadero.vehiculo = vehiculo
        parqueadero.save()
        vehiculo.parqueadero = parqueadero
        vehiculo.save()        

    def ingreso(self, placa, tipo, hora):
        """
        Registra el ingreso de un vehículo al sistema.
        Es como el método Insert de una lista enlazada, se crea un nuevo vehículo y se asigna un parqueadero.
        
        Args:
            placa (str): La placa del vehículo.
            tipo (str): El tipo de vehículo (Motocicleta, Auto, Movilidad Reducida).
            hora (datetime): La hora de ingreso del vehículo.
        """
        nuevo_vehiculo = Vehiculo(placa=placa, tipo=tipo, hora_ingreso=hora)
        nuevo_vehiculo.save()

        if self.head == None:
            self.head = nuevo_vehiculo
            self.asignar_parqueadero(self.head)
        else:
            current = self.head
            while current.siguiente != None:
                current = current.siguiente
            current.siguiente = nuevo_vehiculo
            self.asignar_parqueadero(current.siguiente)

    #Los siguientes 2 métodos cumplen punto 4
    def consultar_ubicacion_vehiculo(self, placa):
        """
        Consulta la ubicación de un vehículo en el sistema.
        Es como el método Search de una lista enlazada, se recorre cada nodo para encontrar el vehículo y su ubicación.

        Args:
            placa (str): La placa del vehículo.

        Returns:
            dict: Un diccionario con la placa del vehículo y su ubicación en el parqueadero.
        """
        current = self.head
        while current != None:
            if current.placa == placa:
                return {"placa": current.placa, "ubicacion": current.parqueadero.ubicacion}
            current = current.siguiente
    
    def consultar_vehiculos_piso(self):
        """
        Consulta los vehículos estacionados en cada piso del parqueadero.
        Se recorre cada nodo para encontrar los vehículos en cada piso.

        Returns:
            dict: Un diccionario con los pisos como claves y una lista de vehículos en cada piso como valores.
        """
        pisos = {}

        for piso in range(1, 4):
            pisos[f"Piso {piso}"] = []
            current = self.head
            while current != None:
                if current.parqueadero.ubicacion.startswith(f"P{piso}"):
                    pisos[f"Piso {piso}"].append({"placa": current.placa, "ubicacion": current.parqueadero.ubicacion})
                current = current.siguiente
        
        return pisos

    #Los siguientes 2 métodos cumplen el punto 5
    def salida(self, placa, hora_salida):
        """
        Registra la salida de un vehículo del sistema y calcula el monto a pagar.
        Es como el método Delete de una lista enlazada, pero calcula el precio a pagar.

        Args:
            placa (str): La placa del vehículo que sale.
            hora_salida (datetime): La hora de salida del vehículo.

        Returns:
            list: Una lista de diccionarios con la información de los vehículos que salieron, incluyendo la placa, hora de ingreso, hora de salida y monto a pagar.
        """
        lista_guarda_vehiculo = []
        current = self.head

        if (current != None) and (current.placa == placa):  
            current.parqueadero.ocupado = False
            current.parqueadero.vehiculo = None
            current.parqueadero.save()

            monto = self.calcular_precio(current.hora_ingreso, hora_salida)
            lista_guarda_vehiculo.append({"placa": current.placa, "hora_ingreso": current.hora_ingreso.strftime('%H:%M'), "hora_salida": hora_salida.strftime('%H:%M'), "monto": monto})
            vehiculo_eliminar = current
            self.head = current.siguiente
            vehiculo_eliminar.delete()
            current = None

        previous = None

        while (current != None):
            previous = current
            current = current.siguiente
            if current.placa == placa:
                current.parqueadero.ocupado = False
                current.parqueadero.vehiculo = None
                current.parqueadero.save()            
                
                monto = self.calcular_precio(current.hora_ingreso, hora_salida)
                lista_guarda_vehiculo.append({"placa": current.placa, "hora_ingreso": current.hora_ingreso.strftime('%H:%M'), "hora_salida": hora_salida.strftime('%H:%M'), "monto": monto})
                vehiculo_eliminar = current
                previous.siguiente = current.siguiente
                vehiculo_eliminar.delete()
                current = None

        return lista_guarda_vehiculo

    def calcular_precio(self, hora_entrada, hora_salida):
        """
        Calcula el monto a pagar por el tiempo de estacionamiento de un vehículo.

        Args:
            hora_entrada (datetime): La hora de ingreso del vehículo.
            hora_salida (datetime): La hora de salida del vehículo.

        Returns:
            float: El monto a pagar por el tiempo de estacionamiento.
        """
        diferencia = hora_salida - hora_entrada
        precio_hora = 2000
        costo_hora = (diferencia.seconds // 3600) * precio_hora
        costo_minuto = (diferencia.seconds % 3600 // 60) * (precio_hora / 60)
        return round(costo_hora + costo_minuto, 2)