from .models import Parking, Vehiculo, Sistema
from rest_framework import serializers

class ParqueaderoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['ubicacion', 'tipo', 'ocupado', 'vehiculo']
    
class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo', 'parqueadero', 'hora_ingreso']

class SistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sistema
        fields = ['parqueaderos']