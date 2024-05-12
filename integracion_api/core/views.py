from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import viewsets
from core.models import *
from core.serializers import * 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from base64 import b64decode
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import generics
from django.utils import timezone
from django.db.models import Sum, Count

#obtener token si un usuario existe, si no le crea uno
class ObtainTokenView(APIView):
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Falta el encabezado de autorización'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            auth_type, auth_string = auth_header.split(' ')
            username, password = b64decode(auth_string).decode('utf-8').split(':')
        except ValueError:
            return Response({'error': 'Encabezado de autorización inválido'},
                            status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Credenciales inválidas'},
                            status=status.HTTP_403_FORBIDDEN)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class userViewSet(viewsets.ModelViewSet):
    queryset = UsuarioPersonalizado.objects.all()
    serializer_class = UserSerializer
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class tipoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = TipoUsuario.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TipoUsuarioPostSerializer
        return TipoUsuarioSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class productoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductoPostSerializer
        return ProductoSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class pedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PedidoPostSerializer
        return PedidoSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class detallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DetallePedidoPostSerializer
        return DetallePedidoSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class estadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EstadoPostSerializer
        return EstadoSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PedidoDetailView(generics.RetrieveAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        detalles_pedido = DetallePedido.objects.filter(pedido=instance)
        detalles_serializer = DetallePedidoSerializer(detalles_pedido, many=True)

        return Response({
            'pedido': serializer.data,
            'detalles_pedido': detalles_serializer.data
        })

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class metodoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MetodoPagoPostSerializer
        return MetodoPagoSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class estadoPagoViewSet(viewsets.ModelViewSet):
    queryset = EstadoPago.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EstadoPagoPostSerializer
        return EstadoPagoSerializer
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class pagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PagoPostSerializer
        return PagoSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class transaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransaccionPostSerializer
        return TransaccionSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ReporteBodegaView(generics.ListAPIView):
    """
    Vista para obtener todos los pedidos del mes actual y el total de ventas del mes.
    """
    serializer_class = PedidoSerializer

    def get_queryset(self):
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        return Pedido.objects.filter(fecha__gte=first_day_of_month)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Serializar los pedidos
        serializer = self.get_serializer(queryset, many=True)

        # Calcular el total de ventas del mes
        total_ventas_mes = queryset.aggregate(Sum('total'))['total__sum']

        return Response({
            'pedidos': serializer.data,
            'total_ventas_mes': total_ventas_mes
        })

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProductosMasVendidosView(generics.ListAPIView):
    """
    Vista para obtener los productos más vendidos del mes actual.
    """
    serializer_class = ProductoSerializer

    def get_queryset(self):
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        detalles_pedido = DetallePedido.objects.filter(pedido__fecha__gte=first_day_of_month)

        # Obtener los productos más vendidos del mes actual
        productos_mas_vendidos = detalles_pedido.values('producto').annotate(veces_vendido=Count('producto'), total_productos_vendidos=Sum('cantidad')).order_by('-veces_vendido')

        # Obtener los IDs de los productos más vendidos y las veces que se vendieron
        productos_mas_vendidos_info = [{'id_producto': item['producto'], 'veces_vendido': item['veces_vendido'], 'total_productos_vendidos': item['total_productos_vendidos']} for item in productos_mas_vendidos]

        # Devolver la información de los productos más vendidos
        return productos_mas_vendidos_info

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Serializar los productos
        productos_serializados = []
        for producto_info in queryset:
            producto = Producto.objects.get(id_producto=producto_info['id_producto'])
            serializer = self.get_serializer(producto)
            producto_serializado = serializer.data
            producto_serializado['veces_vendido'] = producto_info['veces_vendido']
            producto_serializado['total_productos_vendidos'] = producto_info['total_productos_vendidos']
            productos_serializados.append(producto_serializado)

        return Response({
            'productos_mas_vendidos_este_mes': productos_serializados
        })
        