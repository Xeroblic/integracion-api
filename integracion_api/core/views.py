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
