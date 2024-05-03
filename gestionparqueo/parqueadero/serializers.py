from .models import Parking, Vehiculo
from rest_framework import serializers

class ParqueaderoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['ubicacion', 'tipo', 'ocupado', 'vehiculo']
        read_only_fields = ['ubicacion', 'tipo', 'ocupado', 'vehiculo']
        depth = 1
    
class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo', 'parqueadero', 'hora_ingreso']
        depth = 1

class ParqueaderoResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['ubicacion', 'tipo']
        depth = 1