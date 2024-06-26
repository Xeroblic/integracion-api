import random
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import viewsets
from core.models import *
from core.serializers import * 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from base64 import b64decode
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import generics
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


#obtener token si un usuario existe, si no le crea uno
class ObtainTokenView(APIView):
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Falta el encabezado de autorización'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            auth_type, auth_token = auth_header.split(' ')
            auth_string = b64decode(auth_token).decode('utf-8')
            username, password = auth_string.split(':')
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
    serializer_class = PagoSerializer
    
    @property
    def allowed_methods(self):
        return ['GET']
   
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class transaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer
    
    @property
    def allowed_methods(self):
        return ['GET']

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class informeVentaMensual(generics.ListAPIView):
    """
    Vista para obtener todos los pedidos del mes actual y el total de ventas del mes.
    """
    serializer_class = TransaccionSerializer
    
    @property
    def allowed_methods(self):
        return ['GET']
    
    def get_queryset(self):
        month = self.kwargs.get('month')
        if not 1 <= int(month) <= 12:
            raise Http404("El mes proporcionado no es válido.")
        
        first_day_of_month = timezone.now().replace(month=int(month), day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        return Transaccion.objects.filter(Q(pago__estado_pago__id_estado_pago=0) & Q(pedido__fecha__gte=first_day_of_month) & Q(pedido__fecha__lte=last_day_of_month))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Serializar las transacciones
        serializer = self.get_serializer(queryset, many=True)

        # Calcular el total de ventas del mes
        total_ventas_mes = queryset.aggregate(Sum('pedido__total'))['pedido__total__sum']

        return Response({
            'mes': f'Mes {self.kwargs.get("month")} del {timezone.now().year}',
            'total_ventas_mes': total_ventas_mes,
            'transacciones': serializer.data
        })

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProductosMasVendidosView(generics.ListAPIView):
    """
    Vista para obtener los productos más vendidos del mes actual.
    """
    serializer_class = ProductoSerializer
    
    @property
    def allowed_methods(self):
        return ['GET']

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

def payment(request, pedido_id):
    pedido = Pedido.objects.get(id_pedido=pedido_id)
    
    #comprobar si existe un pago para el pedido
    if Pago.objects.filter(pedido=pedido).exists():
        return HttpResponse('Este pedido ya tiene un pago asociado.', status=400)

    # Preparas los parámetros para la API
    params = {
        "buy_order": str(pedido.id_pedido),
        "session_id": str(random.randint(100000, 999999)),
        "amount": pedido.total,
        "return_url": "http://127.0.0.1:8000/verify_transaction"
    }
    
    headers = {
        "Tbk-Api-Key-Id": "597055555532",
        "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        "Content-Type": "application/json"
    }

    # Haces la llamada a la API
    response = requests.post('https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions', headers=headers, json=params)

    # Si la respuesta es exitosa, obtienes el token y renderizas la página de pago
    if response.status_code == 200:
        token = response.json()['token']
        return render(request, 'payment.html', {'token': token, 'message': 'Proceder al pago', 'submit': 'Pagar'})
    else:
        print(response.text)
        return HttpResponseBadRequest()

@csrf_exempt
def verify_transaction(request):
    if request.method == 'POST':
        response = request.POST

        return render(request, 'response.html', {'response': response})
    elif request.method == 'GET':
        # Capturas el token de la URL
        token = request.GET.get('token_ws')

        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"
        headers = {
            "Tbk-Api-Key-Id": "597055555532",
            "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            "Content-Type": "application/json"
        }
        
        response = requests.put(url, headers=headers)
        
        # Crear un pago
        response_data = response.json()
        pago_data = {
            'pedido': response_data['buy_order'],
            'metodo_pago': response_data['payment_type_code'],
            'monto': response_data['amount'],
            'estado_pago': response_data['response_code'],
            'fecha' : datetime.strptime(response_data['transaction_date'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        }
        serializer = PagoPostSerializer(data=pago_data)
        if serializer.is_valid():
            pago = serializer.save()
        else:
            return HttpResponseBadRequest(serializer.errors)

        #crear la transaccion
        transaccion_data = {
            'pedido': pago.pedido.id_pedido,
            'cliente': pago.pedido.usuario.id,
            'pago': pago.id_pago,
        }
        transaccion_serializer = TransaccionPostSerializer(data=transaccion_data)
        if transaccion_serializer.is_valid():
            transaccion_serializer.save()
        else:
            raise serializers.ValidationError(transaccion_serializer.errors)
        
        return render(request, 'response.html', {'response': 'Pago exitoso.'})
    else:
        return HttpResponseBadRequest()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class reporteEstrategiasYVentasView(generics.ListAPIView):
    """
    Vista para obtener los productos que no se han vendido en el mes actual.
    """
    serializer_class = ProductoSerializer

    @property
    def allowed_methods(self):
        return ['GET']

    def get_queryset(self):
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Obtener los productos vendidos este mes
        productos_vendidos_este_mes = DetallePedido.objects.filter(pedido__fecha__gte=first_day_of_month).values('producto').annotate(ventas=Count('producto'))

        # Crear un diccionario con los productos vendidos y sus ventas
        ventas_productos = {item['producto']: item['ventas'] for item in productos_vendidos_este_mes}

        # Obtener todos los productos
        todos_los_productos = Producto.objects.all()

        # Agregar el conteo de ventas a cada producto
        for producto in todos_los_productos:
            producto.ventas = ventas_productos.get(producto.id_producto, 0)

        # Filtrar los productos que no se han vendido este mes
        productos_no_vendidos_este_mes = [producto for producto in todos_los_productos if producto.ventas == 0]

        return productos_no_vendidos_este_mes
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Serializar los productos
        productos_serializados = []
        for producto in queryset:
            serializer = self.get_serializer(producto)
            producto_serializado = serializer.data
            producto_serializado['ventas'] = producto.ventas
            productos_serializados.append(producto_serializado)

        return Response({
            'productos_sin_ventas': productos_serializados
        })

