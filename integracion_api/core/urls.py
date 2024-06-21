from django.urls import path, include
from rest_framework import routers
from core.views import *
from core.serializers import *

router = routers.DefaultRouter()
router.register('usuario', userViewSet, basename='usuario')
router.register('tipo_usuario', tipoUsuarioViewSet, basename='tipo_usuario')
router.register('producto', productoViewSet, basename='producto')
router.register('pedido', pedidoViewSet, basename='pedido')
router.register('detalle_pedido', detallePedidoViewSet, basename='detalle_pedido')
router.register('estado', estadoViewSet, basename='estado')
router.register('metodo_pago', metodoViewSet, basename='metodo_pago')
router.register('estado_pago', estadoPagoViewSet, basename='estado_pago')
router.register('transaccion', transaccionViewSet, basename='transaccion')
router.register('pago', pagoViewSet, basename='pago')

urlpatterns = [
    path('', include(router.urls)),
    path('get-token/', ObtainTokenView.as_view(), name='get-token'),
    path('pedidos/<int:pk>/', PedidoDetailView.as_view(), name='pedido-detail'),
    path('informe_ventas_mensual/<int:month>/', informeVentaMensual.as_view(), name='informe_ventas_mensual'),
    path('reporte_productos_vendidos/', ProductosMasVendidosView.as_view(), name='reporte_productos_vendidos'),
    #TODO: Reporte estrategia de ventas y promociones
    path('payment/<int:pedido_id>/', payment, name='payment'),
    path('verify_transaction', verify_transaction, name='verify_transaction'),
    path('reporte_estrategia_ventas/', reporteEstrategiasYVentasView.as_view(), name='reporte_estrategia_ventas'),
]