from .serializers import ParqueaderoSerializer, VehiculoSerializer, ParqueaderoResumenSerializer
from .models import Parking, Vehiculo, sistema_parqueo
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime


class ParqueaderoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Parqueadero.

    Este ViewSet proporciona las siguientes funcionalidades:
    - Obtener la lista de parqueaderos disponibles.
    - Registrar el ingreso de un vehículo.
    - Consultar la ubicación de un vehículo en el parqueadero.
    - Consultar los vehículos en cada piso del parqueadero.
    - Registrar la salida de un vehículo y calcular el monto a pagar.


    """
    queryset = Parking.objects.all()
    serializer_class = ParqueaderoSerializer
    sistema = sistema_parqueo()

    def create(self, request):
        """
        Crea los parqueaderos.

        Este método solo puede ser ejecutado una vez. Si se desea volver a crear los parqueaderos,
        se deben eliminar todos los parqueaderos existentes.

        Returns:
            Una respuesta HTTP con el estado HTTP 201 CREATED si los parqueaderos se crearon
            exitosamente.

        Raises:
            Response: Una respuesta HTTP con el estado HTTP 400 BAD REQUEST si los parqueaderos ya
            han sido creados.
        """
        if Parking.objects.exists():
            return Response({"detail":"Los parqueaderos ya han sido creados. Elimine todos los parqueaderos si desea usar este método."}, status=status.HTTP_400_BAD_REQUEST)
        self.sistema.parqueaderos_lista()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def parqueaderos_disponibles(self, request):
        """
        Obtiene la lista de parqueaderos disponibles.

        Returns:
            Una respuesta HTTP con el estado HTTP 200 OK y la lista de parqueaderos disponibles en
            el cuerpo de la respuesta.
        """
        parqueaderos_disponibles = Parking.objects.filter(ocupado=False)
        serializer = ParqueaderoResumenSerializer(parqueaderos_disponibles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['POST'])
    def ingreso_vehiculo(self, request):
        """
        Registra el ingreso de un vehículo al parqueadero.

        Args:
            request: La solicitud HTTP que contiene los datos del vehículo a ingresar.

        Returns:
            Una respuesta HTTP con el estado HTTP 201 CREATED si el vehículo se ingresó
            exitosamente.

        Raises:
            Response: Una respuesta HTTP con el estado HTTP 400 BAD REQUEST si alguno de los datos
            del vehículo es inválido o si no hay parqueaderos disponibles.
        """
        placa = request.data['placa']
        tipo = request.data['tipo']
        hora_ingreso_str = request.data['hora_ingreso']

        try:
            hora_ingreso = datetime.strptime(hora_ingreso_str, '%H:%M')
        except:
            return Response({"detail":"Hora de ingreso no válida. Debe ser en formato HH:MM."}, status=status.HTTP_400_BAD_REQUEST)
        
        if tipo not in ["Auto", "Motocicleta", "Movilidad Reducida"]:
            return Response({"detail":"Tipo de vehiculo no válido. Debe ser Auto, Motocicleta, Movilidad Reducida"}, status=status.HTTP_400_BAD_REQUEST)
        if Vehiculo.objects.filter(placa=placa).exists():
            return Response({"detail":"El vehiculo ya se encuentra en el parqueadero."}, status=status.HTTP_400_BAD_REQUEST)    
        if self.sistema.parqueadero_disponible(tipo) == None:
            return Response({"detail":"No hay parqueaderos disponibles."}, status=status.HTTP_400_BAD_REQUEST)
        
        self.sistema.ingreso(placa, tipo, hora_ingreso)
        return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['GET'])
    def consultar_ubicacion_VH(self, request):
        """
        Consulta la ubicación de un vehículo en el parqueadero.

        Args:
            request: La solicitud HTTP que contiene la placa del vehículo a consultar.

        Returns:
            Una respuesta HTTP con el estado HTTP 200 OK y la ubicación del vehículo en el cuerpo
            de la respuesta.

        Raises:
            Response: Una respuesta HTTP con el estado HTTP 400 BAD REQUEST si el vehículo no se
            encuentra en el parqueadero.
        """
        placa = request.query_params['placa']
        vehiculo_ubicacion = self.sistema.consultar_ubicacion_vehiculo(placa)
        print(vehiculo_ubicacion)
        if vehiculo_ubicacion == None:
            return Response({"detail":"El vehiculo no se encuentra en el parqueadero."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(vehiculo_ubicacion, status=status.HTTP_200_OK)  

    @action(detail=False, methods=['GET'])
    def consultar_vehiculos_piso(self, request):
        """
        Consulta los vehículos en cada piso del parqueadero.

        Returns:
            Una respuesta HTTP con el estado HTTP 200 OK y la lista de vehículos en cada piso del
            parqueadero en el cuerpo de la respuesta.

        Raises:
            Response: Una respuesta HTTP con el estado HTTP 400 BAD REQUEST si no hay vehículos en
            el parqueadero.
        """
        if Parking.objects.filter(ocupado=True).exists() == False:
            return Response({"detail":"No hay vehiculos en el parqueadero."}, status=status.HTTP_400_BAD_REQUEST)
        
        vehiculos_piso = self.sistema.consultar_vehiculos_piso()
        return Response(vehiculos_piso, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def salida_vehiculo(self, request):
        """
        Registra la salida de un vehículo y calcula el monto a pagar.

        Args:
            request: La solicitud HTTP que contiene la placa y la hora de salida del vehículo.

        Returns:
            Una respuesta HTTP con el estado HTTP 200 OK y el monto a pagar en el cuerpo de la
            respuesta.

        Raises:
            Response: Una respuesta HTTP con el estado HTTP 400 BAD REQUEST si el vehículo no se
            encuentra en el parqueadero o si la hora de salida es inválida.
        """
        placa = request.query_params['placa']
        hora_salida_str = request.query_params['hora_salida']

        try:
            hora_salida = datetime.strptime(hora_salida_str, '%H:%M')
        except:
            return Response({"detail":"Hora de salida no válida. Debe ser en formato HH:MM."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Vehiculo.objects.filter(placa=placa).exists():
            return Response({"detail":"El vehiculo no se encuentra en el parqueadero."}, status=status.HTTP_400_BAD_REQUEST)

        vehiculo_monto = self.sistema.salida(placa, hora_salida)
       
        return Response(vehiculo_monto, status=status.HTTP_200_OK)

class VehiculoViewSet(viewsets.ModelViewSet):  
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer