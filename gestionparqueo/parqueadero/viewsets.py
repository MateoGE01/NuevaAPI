from .serializers import ParqueaderoSerializer, VehiculoSerializer, SistemaSerializer
from .models import Parking, Vehiculo, Sistema
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

class ParqueaderoViewSet(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParqueaderoSerializer


class VehiculoViewSet(viewsets.ModelViewSet):  
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class SistemaViewSet(viewsets.ModelViewSet):    
    queryset = Sistema.objects.all()
    serializer_class = SistemaSerializer

    #Este método se encarga de crear todos los parqueaderos del sistema y también añadirlos en el endpoint de Parking
    def create(self, request, *args, **kwargs):
        if Sistema.objects.exists():
            return Response({"detail": "Ya existe un sistema de parqueo"}, status = status.HTTP_400_BAD_REQUEST)
        
        sistema = Sistema.objects.create()
        parqueaderos = sistema.parqueaderos_lista()
        for parqueadero in parqueaderos:
            parqueadero.save()
            sistema.parqueaderos.add(parqueadero)
        
        serializer = self.get_serializer(sistema)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    

    #Simplemente para ver como funciona cada elemento de la lista de sistemas que se denominan parqueaderos
    @action(detail=False, methods=['GET'])
    def mostrar_parqueadero(self, request):
        sistema = Sistema.objects.first()
        parqueaderos = sistema.parqueaderos.all()
        lista_autos = []
        for parqueadero in parqueaderos:
            if parqueadero.tipo == 'Auto':
                lista_autos.append(parqueadero.ubicacion)
        
        return Response(lista_autos, status = status.HTTP_200_OK)