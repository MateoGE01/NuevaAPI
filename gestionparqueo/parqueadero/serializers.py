from .models import Parking, Vehiculo
from rest_framework import serializers
    
class VehiculoSerializer(serializers.ModelSerializer):
    parqueadero = serializers.StringRelatedField()
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo', 'parqueadero', 'hora_ingreso']
        

    def to_representation(self, instance):
            representation = super().to_representation(instance)
            hora_ingreso = instance.hora_ingreso.strftime("%H:%M")
            representation['hora_ingreso'] = hora_ingreso

            
            return representation 
       
class ParqueaderoResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['ubicacion', 'tipo']
        depth = 1

class ParqueaderoSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSerializer(read_only=True)

    class Meta:
        model = Parking
        fields = ['ubicacion', 'tipo', 'ocupado', 'vehiculo']
        read_only_fields = ['ubicacion', 'tipo', 'ocupado', 'vehiculo']
        depth = 1