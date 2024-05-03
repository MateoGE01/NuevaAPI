from django.db import models
import random
from rest_framework.response import Response
from rest_framework import status

class Parking(models.Model):
    ubicacion = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50)
    ocupado = models.BooleanField(default=False)
    vehiculo = models.OneToOneField('Vehiculo', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.ubicacion}'
    
class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50)
    parqueadero = models.OneToOneField('Parking', on_delete=models.SET_NULL, null=True, blank=True, related_name='parqueadero_asociado')
    hora_ingreso = models.DateTimeField(null=True, blank=True)
    siguiente = None

    def __str__(self):
        return f'{self.placa}'


class sistema_parqueo:
    
    def __init__(self):
        self.head = None

    #Crea todos los parqueaderos que son 210 por piso y 630 en total, es decir, 21 parqueaderos por fila(podían ser más o menos filas, pero yo escogí 10 por pisos)
    def parqueaderos_lista(self):
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
        parqueaderos_disponibles = Parking.objects.filter(tipo=tipo, ocupado=False).order_by('?')

        if parqueaderos_disponibles.exists():
            return parqueaderos_disponibles.first()
        
    def asignar_parqueadero(self, vehiculo):
        parqueadero = self.parqueadero_disponible(vehiculo.tipo)

        parqueadero.ocupado = True
        parqueadero.vehiculo = vehiculo
        parqueadero.save()
        vehiculo.parqueadero = parqueadero
        vehiculo.save()        

    def ingreso(self, placa, tipo):
        nuevo_vehiculo = Vehiculo(placa=placa, tipo=tipo)
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