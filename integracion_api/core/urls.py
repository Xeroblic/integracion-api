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
router.register('metodo_pago', metodoViewSet)
router.register('estado_pago', estadoPagoViewSet)
router.register('pago', pagoViewSet)
router.register('transaccion', transaccionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get-token/', ObtainTokenView.as_view(), name='get-token'),
    path('pedidos/<int:pk>/', PedidoDetailView.as_view(), name='pedido-detail'),
    path('reporte_bodega/', ReporteBodegaView.as_view(), name='reporte_bodega'),
    path('reporte_productos_vendidos/', ProductosMasVendidosView.as_view(), name='reporte_productos_vendidos'),
    #TODO: Reporte de ventas, basados en transacciones.
    path('payment/<int:pedido_id>/', payment, name='payment'),
    path('verify_transaction', verify_transaction, name='verify_transaction'),
]