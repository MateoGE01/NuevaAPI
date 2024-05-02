from django.db import models

class Parking(models.Model):
    ubicacion = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50)
    ocupado = models.BooleanField(default=False)
    vehiculo = models.OneToOneField('Vehiculo', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.ubicacion}|{self.tipo}|{self.ocupado}|{self.vehiculo}'
class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50)
    parqueadero = models.OneToOneField('Parking', on_delete=models.SET_NULL, null=True, blank=True, related_name='parqueadero_asociado')
    hora_ingreso = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.placa}|{self.tipo}|{self.parqueadero}|{self.hora_ingreso}'

class Sistema(models.Model):
    parqueaderos = models.ManyToManyField(Parking)

    def parqueaderos_lista(self):
        parqueaderos = [] 
        for piso in range(1, 4):
            for fila in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
                for puesto in range(1, 13):
                    parqueaderos.append(Parking(ubicacion=f"P{piso}{fila}{puesto}", tipo="Motocicleta"))
                for puesto in range(13, 21):
                    parqueaderos.append(Parking(ubicacion=f"P{piso}{fila}{puesto}", tipo="Auto"))
                for puesto in range(21, 22):
                    parqueaderos.append(Parking(ubicacion=f"P{piso}{fila}{puesto}", tipo="Movilidad Reducida"))     
                    
        return parqueaderos