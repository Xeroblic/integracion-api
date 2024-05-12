from django.urls import path, include
from rest_framework import routers
from core.views import *
from core.serializers import *

router = routers.DefaultRouter()
router.register('usuario', userViewSet)
router.register('tipo_usuario', tipoUsuarioViewSet)
router.register('producto', productoViewSet)
router.register('pedido', pedidoViewSet)
router.register('detalle_pedido', detallePedidoViewSet)
router.register('estado', estadoViewSet)
# router.register('carrito', CarritoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get-token/', ObtainTokenView.as_view(), name='get-token'),
    path('pedidos/<int:pk>/', PedidoDetailView.as_view(), name='pedido-detail'),
]