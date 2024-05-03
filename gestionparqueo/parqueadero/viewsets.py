from .serializers import ParqueaderoSerializer, VehiculoSerializer, ParqueaderoResumenSerializer
from .models import Parking, Vehiculo, sistema_parqueo
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


class ParqueaderoViewSet(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParqueaderoSerializer
    sistema = sistema_parqueo()

    #Se crean los parqueaderos
    def create(self, request):
        if Parking.objects.exists():
            return Response({"detail":"Los parqueaderos ya han sido creados. Elimine todos los parqueaderos si desea usar este método."}, status=status.HTTP_400_BAD_REQUEST)
        self.sistema.parqueaderos_lista()
        return Response(status=status.HTTP_201_CREATED)

    #Cumple punto 1
    @action(detail=False, methods=['GET'])
    def parqueaderos_disponibles(self, request):
        parqueaderos_disponibles = Parking.objects.filter(ocupado=False)
        serializer = ParqueaderoResumenSerializer(parqueaderos_disponibles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    #Cumple punto 2 y 3
    @action(detail=False, methods=['POST'])
    def ingreso_vehiculo(self, request):
        placa = request.data['placa']
        tipo = request.data['tipo']

        self.sistema.ingreso(placa, tipo)

        return Response(status=status.HTTP_201_CREATED)
    

class VehiculoViewSet(viewsets.ModelViewSet):  
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer