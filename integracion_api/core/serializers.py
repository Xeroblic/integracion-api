from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import * 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['id', 'username', 'email', 'password', 'id_tipo_usuario']
        extra_kwargs = {'password': {'write_only': True}}
    def save(self, **kwargs):
        user = super().save(**kwargs)
        Token.objects.create(user=user)
        return user

class TipoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUsuario
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class TipoUsuarioPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUsuario
        fields = ['nombre']

class ProductoPostSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(required=True)
    marca = serializers.CharField(required=True)
    nombre = serializers.CharField(required=True)
    stock = serializers.IntegerField(required=True)
    precio_neto = serializers.IntegerField(required=True)
    imagen_url = serializers.CharField(required=True)

    class Meta:
        model = Producto
        fields = ['sku', 'marca', 'nombre', 'stock', 'precio_neto', 'imagen_url']
    
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoPostSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(required=True)
    id_estado = serializers.IntegerField(required=True)
    class Meta:
        model = Pedido
        fields = ['id_usuario', 'fecha', 'id_estado']

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

class DetallePedidoPostSerializer(serializers.ModelSerializer):
    #make required 'cantidad', 'fecha'
    cantidad = serializers.IntegerField(required=True)
    fecha = serializers.DateTimeField(required=True)
    
    class Meta:
        model = DetallePedido
        fields = ['id_pedido', 'id_producto', 'cantidad', 'fecha']
        
class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class EstadoPostSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=True)
    class Meta:
        model = Estado
        fields = ['nombre']