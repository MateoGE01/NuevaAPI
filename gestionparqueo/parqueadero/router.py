from rest_framework import routers
from parqueadero.viewsets import ParqueaderoViewSet, VehiculoViewSet

router = routers.DefaultRouter()
router.register(r'parqueadero', ParqueaderoViewSet)
router.register(r'vehiculo', VehiculoViewSet)
