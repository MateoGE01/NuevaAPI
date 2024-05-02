from rest_framework import routers
from parqueadero.viewsets import ParqueaderoViewSet, VehiculoViewSet, SistemaViewSet

router = routers.DefaultRouter()
router.register(r'parqueadero', ParqueaderoViewSet)
router.register(r'vehiculo', VehiculoViewSet)
router.register(r'sistema', SistemaViewSet)