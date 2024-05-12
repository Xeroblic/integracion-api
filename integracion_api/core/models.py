from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authentication import TokenAuthentication

class TipoUsuario(models.Model):
    id_tipo_usuario = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.nombre

class UsuarioPersonalizado(AbstractUser):
    id_tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, null=False)
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        elif self.password != UsuarioPersonalizado.objects.get(pk=self.pk).password:
            self.set_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    nombre = models.CharField(max_length=300)
    precio_neto = models.IntegerField()
    fecha = models.DateField(auto_now_add=True)
    stock = models.IntegerField()
    imagen_url = models.CharField(max_length=500)
    
class Estado(models.Model):
    ESTADOS= [(1, 'Aceptado'), 
              (2, 'En proceso'), 
              (3, 'Enviado'),  
              (4, 'Finalizado'), 
              (5, 'Reembolsado'), 
              (6, 'Pendiente de pago')]
    id_estado = models.AutoField(choices=ESTADOS,primary_key=True)
    nombre = models.CharField( max_length=50)

    def __str__(self):
        return self.nombre    
    
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, null=False)
    subtotal = models.IntegerField(null=True)
    iva = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    fecha = models.DateField(auto_now_add=True, null=False)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=False)

class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False)
    cantidad = models.IntegerField()
    
    class Meta:
        unique_together = (('pedido', 'producto'),)

class MetodoPago(models.Model):
    id_metodo_pago = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class EstadoPago(models.Model):
    id_estado_pago = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=False)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, null=False)
    estado_pago = models.ForeignKey(EstadoPago, on_delete=models.CASCADE, null=False)
    monto = models.IntegerField()
    fecha = models.DateField(auto_now_add=True)

class Transaccion(models.Model):
    id_transaccion = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=False)
    cliente = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, null=False)
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, null=False)
    fecha = models.DateField(auto_now_add=True)
    
