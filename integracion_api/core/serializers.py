from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import * 

class TipoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUsuario
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # id_tipo_usuario = TipoUsuarioSerializer(required=True)
    class Meta:
        model = UsuarioPersonalizado
        fields = ['id', 'username', 'email', 'password', 'id_tipo_usuario']
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self, **kwargs):
        user = super().save(**kwargs)
        Token.objects.create(user=user)
        return user

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

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class EstadoPostSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(required=True)
    class Meta:
        model = Estado
        fields = ['nombre']
    
class PedidoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    estado = EstadoSerializer()
    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoPostSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(required=True)
    
    class Meta:
        model = Pedido
        fields = ['usuario', 'fecha', 'estado']

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'
    

class DetallePedidoPostSerializer(serializers.ModelSerializer):
    cantidad = serializers.IntegerField(required=True)
    
    class Meta:
        model = DetallePedido
        fields = ['pedido', 'producto', 'cantidad']
        
    def validate(self, data):
        producto = data['producto']
        cantidad = data['cantidad']

        if producto.stock < cantidad:
            raise serializers.ValidationError({'message': 'Producto agotado'})

        return data
        
    def create(self, validated_data):
        producto = validated_data['producto']
        cantidad = validated_data['cantidad']
        
        producto.stock -= cantidad
        producto.save()

        detalle_pedido = DetallePedido.objects.create(**validated_data)

        # Recuperar el pedido asociado
        pedido = detalle_pedido.pedido

        # Calcular el subtotal, iva y total
        subtotal = sum(detalle.producto.precio_neto * detalle.cantidad for detalle in DetallePedido.objects.filter(pedido=pedido))
        iva = subtotal * 0.19
        total = subtotal + iva

        # Guardar los valores calculados en el pedido
        pedido.subtotal = subtotal
        pedido.iva = iva
        pedido.total = total
        pedido.save()

        return detalle_pedido

        
class ProductoCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad']
