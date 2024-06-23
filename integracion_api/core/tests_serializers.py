from core.models import *
from core.serializers import * 
from django.test import TestCase
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token

#test unitarios para los serializadores

class TipoUsuarioSerializerTestCase(TestCase):
    def setUp(self):
        self.tipo_usuario_data = {
            'nombre': 'Administrador',
        }

    def test_tipo_usuario_serializer_valid(self):
        data = {
            'nombre': 'Usuario Regular',
        }
        serializer = TipoUsuarioPostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_tipo_usuario_serializer_save(self):
        data = self.tipo_usuario_data
        serializer = TipoUsuarioPostSerializer(data=data)
        if serializer.is_valid():
            tipo_usuario = serializer.save()
            self.assertIsNotNone(tipo_usuario.id_tipo_usuario)
            self.assertEqual(tipo_usuario.nombre, self.tipo_usuario_data['nombre'])
        else:
            self.fail("Serializer no valido")
            
    def test_tipo_usuario_invalid(self):
        invalid_data = self.tipo_usuario_data.copy()
        invalid_data['nombre'] = None
        serializer = TipoUsuarioPostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_tipo_usuario_serializer_update(self):
        tipo_usuario = TipoUsuario.objects.create(**self.tipo_usuario_data)
        update_data = {'nombre': "Usuario avanzado" }
        serializer = TipoUsuarioPostSerializer(tipo_usuario, data=update_data, partial=True)
        if serializer.is_valid():
            updated_tipo_usuario = serializer.save()
            self.assertEqual(updated_tipo_usuario.nombre, update_data['nombre'])
        else:
            self.fail("Serializer no valido")

    def test_tipo_usuario_delete(self):
        tipo_usuario = TipoUsuario.objects.create(**self.tipo_usuario_data)
        tipo_usuario_id = tipo_usuario.id_tipo_usuario
        tipo_usuario.delete()
        self.assertFalse(TipoUsuario.objects.filter(id_tipo_usuario=tipo_usuario_id).exists())

    def test_get_tipo_usuario_data(self):
        tipo_usuario = TipoUsuario.objects.create(**self.tipo_usuario_data)
        serializer = TipoUsuarioSerializer(tipo_usuario)
        expected_data = self.tipo_usuario_data.copy()
        expected_data['id_tipo_usuario'] = tipo_usuario.id_tipo_usuario 
        self.assertEqual(serializer.data['nombre'], expected_data['nombre'])

class UserSerializerTestCase(TestCase):
    def setUp(self):
        # Primero, crea una instancia de TipoUsuario
        self.tipo_usuario = TipoUsuario.objects.create(nombre='testTU')  # Asegúrate de incluir los campos requeridos por el modelo TipoUsuario
        self.user = UsuarioPersonalizado.objects.create_user(username='testuser', password='testpassword', email='test@example.com', id_tipo_usuario=self.tipo_usuario)
        self.serializer = UserSerializer(instance=self.user)
        self.user_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'password': 'newpassword',
            'id_tipo_usuario': self.tipo_usuario  # Asigna directamente la instancia de TipoUsuario
        }

    def test_user_serializer_valid(self):
        # Prueba para verificar que el serializer es válido con datos correctos
        unique_username = f'{self.user.username}_{get_random_string(20)}'
        instance_data = {
            'id': self.user.id,  
            'username': unique_username,
            'email': self.user.email,
            'password': self.user.password,
            'id_tipo_usuario': self.user.id_tipo_usuario.id_tipo_usuario
        }
        serializer = UserSerializer(data=instance_data)
        self.assertTrue(serializer.is_valid())

    def test_user_serializer_save(self):
        # Prueba para verificar que el serializer guarda correctamente el usuario
        serializer = UserSerializer(data=self.user_data)
        if serializer.is_valid():
            user = serializer.save()
            self.assertIsNotNone(user.pk)  # Verificar que el usuario se ha guardado correctamente
            self.assertTrue(Token.objects.filter(user=user).exists())  # Verificar que se creó un token para el usuario

    def test_get_user_data(self):
        user = UsuarioPersonalizado.objects.get(username='testuser')
        serializer = UserSerializer(user)
        #comprobaremos si existe el testuser creado en el setup
        expected_data = {
            'username': self.user.username,
            'email': self.user.email,
            'id_tipo_usuario': self.user.id_tipo_usuario
        }
        self.assertEqual(serializer.data['username'], expected_data['username'])
        self.assertEqual(serializer.data['email'], expected_data['email'])
        self.assertEqual(serializer.data['id_tipo_usuario'], self.user.id_tipo_usuario.id_tipo_usuario)
    
    def test_user_serializer_invalid(self):
        # Prueba para verificar el comportamiento con datos inválidos
        invalid_data = {
            'username': '',
            'password': 'short',  
            'email': 'notanemail', 
            'id_tipo_usuario': None  
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertGreater(len(serializer.errors), 0, "Debería haber errores de validación")
    
    def test_user_serializer_update(self):
        updated_user = self.serializer.update(self.user, self.user_data)
        self.assertEqual(updated_user.username, self.user_data['username'])
        self.assertEqual(updated_user.email, self.user_data['email'])

    def test_user_delete(self):
        user_id = self.user.id
        self.user.delete()
        self.assertFalse(UsuarioPersonalizado.objects.filter(id=user_id).exists())

class ProductoSerializerTestCase(TestCase):
    def setUp(self):
        self.producto_data = {
            'sku': 'SKU123',
            'marca': 'MarcaX',
            'nombre': 'ProductoX',
            'precio_neto': 100,
            'stock': 10,
            'imagen_url': 'http://example.com/imagen.jpg'
        }

    def test_producto_serializer_valid(self):
        data = {
            'sku': 'SKU124',
            'marca': 'MarcaY',
            'nombre': 'ProductoY',
            'precio_neto': 200,
            'stock': 20,
            'imagen_url': 'http://example.com/imagen2.jpg'
        }
        serializer = ProductoPostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_producto_serializer_save(self):
        data = self.producto_data
        serializer = ProductoPostSerializer(data=data)
        if serializer.is_valid():
            producto = serializer.save()
            self.assertIsNotNone(producto.id_producto)
            for field in self.producto_data:
                self.assertEqual(getattr(producto, field), self.producto_data[field])
        else:
            self.fail("Serializer no valido")

    def test_producto_serializer_update(self):
        producto = Producto.objects.create(**self.producto_data)
        update_data = {'stock': 10}
        serializer = ProductoPostSerializer(producto, data=update_data, partial=True)
        if serializer.is_valid():
            updated_producto = serializer.save()
            self.assertEqual(updated_producto.stock, update_data['stock'])
        else: 
            self.fail("Serializer no valido")

    def test_producto_serializer_stock(self):
        # comprobar validación de stock
        invalid_data = self.producto_data.copy()
        invalid_data['stock'] = -10 
        serializer = ProductoPostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_producto_delete(self):
        producto = Producto.objects.create(**self.producto_data)
        producto_id = producto.id_producto
        producto.delete()
        self.assertFalse(Producto.objects.filter(id_producto=producto_id).exists())

    def test_get_producto_data(self):
        producto = Producto.objects.create(**self.producto_data)
        serializer = ProductoSerializer(producto)
        expected_data = self.producto_data.copy()
        expected_data['id_producto'] = producto.id_producto  # Asumiendo que se espera el id en la respuesta
        self.assertEqual(serializer.data['sku'], expected_data['sku'])
        self.assertEqual(serializer.data['marca'], expected_data['marca'])
        self.assertEqual(serializer.data['nombre'], expected_data['nombre'])
        self.assertEqual(serializer.data['precio_neto'], expected_data['precio_neto'])
        self.assertEqual(serializer.data['stock'], expected_data['stock'])
        self.assertEqual(serializer.data['imagen_url'], expected_data['imagen_url'])

class PedidoSerializerTestCase(TestCase):
    def setUp(self):
        # Crear instancias de UsuarioPersonalizado y Estado para usar en la creación de Pedido
        tipo_usuario = TipoUsuario.objects.create(nombre="Tipo de prueba")
        self.usuario = UsuarioPersonalizado.objects.create(username="usuario_test", password="password123", id_tipo_usuario=tipo_usuario)
        self.estado = Estado.objects.create(id_estado=1, nombre="Aceptado")
        self.pedido_data = {
            'usuario': self.usuario,
            'fecha': '2023-01-01',
            'estado': self.estado
        }
        
    def test_pedido_serializer_valid(self):
        self.data = {
            'usuario' : 1,
            'fecha' : '2023-01-01',
            'estado' : 1
        }
        serializer = PedidoPostSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_pedido_serializer_save(self):
        serializer = PedidoPostSerializer(data=self.pedido_data)
        if serializer.is_valid():
            pedido = serializer.save()
            self.assertIsNotNone(pedido.id_pedido)
            self.assertEqual(pedido.usuario, self.usuario)
            self.assertEqual(pedido.estado, self.estado)

    def test_pedido_serializer_update(self):
        pedido = Pedido.objects.create(**self.pedido_data)
        update_data = {'subtotal': 2000, 'iva': 320, 'total': 2320}
        serializer = PedidoSerializer(pedido, data=update_data, partial=True)
        if serializer.is_valid():
            updated_pedido = serializer.save()
            self.assertEqual(updated_pedido.subtotal, update_data['subtotal'])
            self.assertEqual(updated_pedido.iva, update_data['iva'])
            self.assertEqual(updated_pedido.total, update_data['total'])

    # Se manda un objeto invalido al post serializer para comprobar que no permite la entrada de datos
    def test_pedido_serializer_invalid(self):
        invalid_data = self.pedido_data.copy()
        serializer = PedidoPostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_pedido_delete(self):
        pedido = Pedido.objects.create(**self.pedido_data)
        pedido_id = pedido.id_pedido
        pedido.delete()
        self.assertFalse(Pedido.objects.filter(id_pedido=pedido_id).exists())
    
    def test_get_pedido_data(self):
        pedido = Pedido.objects.create(**self.pedido_data)
        serializer = PedidoSerializer(pedido)
        expected_data = {
            'usuario': self.usuario,
            'fecha': '2023-01-01',
            'estado': self.estado
        }
        self.assertEqual(serializer.data['usuario']['id'], expected_data['usuario'].id)
        self.assertEqual(serializer.data['fecha'], expected_data['fecha'])
        self.assertEqual(serializer.data['estado']['id_estado'], expected_data['estado'].id_estado)

class DetallePedidoSerializerTestCase(TestCase):
    def setUp(self):
        # Crear instancias necesarias para los tests, como Pedido, Producto, etc.
        self.tipo_usuario = TipoUsuario.objects.create(nombre="Tipo de prueba")
        self.usuario = UsuarioPersonalizado.objects.create(username="usuario_test", password="password123", id_tipo_usuario=self.tipo_usuario)
        self.estado = Estado.objects.create(nombre="Aceptado")
        self.pedido = Pedido.objects.create(usuario=self.usuario, fecha='2023-01-01', estado=self.estado, subtotal=0, iva=0, total=0)
        self.producto = Producto.objects.create(sku="SKU123", marca="MarcaX", nombre="ProductoX", precio_neto=100, stock=10, imagen_url="http://example.com/imagen.jpg")

        self.detalle_pedido_data = {
            'pedido': self.pedido,
            'producto': self.producto,
            'cantidad': 5
        }   

    def test_detalle_pedido_serializer_valid(self):
        data = {
            'pedido': self.pedido.id_pedido,
            'producto': self.producto.id_producto,
            'cantidad': 2
        }
        serializer = DetallePedidoPostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_detalle_pedido_serializer_save(self):
        data = {
            'pedido': self.pedido.id_pedido,
            'producto': self.producto.id_producto,
            'cantidad': self.detalle_pedido_data['cantidad']
        }
        serializer = DetallePedidoPostSerializer(data=data)
        if serializer.is_valid():
            detalle_pedido = serializer.save()
            self.assertIsNotNone(detalle_pedido.id_detalle_pedido)
            self.assertEqual(detalle_pedido.pedido, self.pedido)
            self.assertEqual(detalle_pedido.producto, self.producto)
            self.assertEqual(detalle_pedido.cantidad, self.detalle_pedido_data['cantidad'])
        else:
            self.fail("Serializer no valido")

    def test_detalle_pedido_serializer_update(self):
        detalle_pedido = DetallePedido.objects.create(**self.detalle_pedido_data)
        update_data = {'producto': 1, 'cantidad': 3}
        serializer = DetallePedidoPostSerializer(detalle_pedido, data=update_data, partial=True)
        if serializer.is_valid():
            updated_detalle_pedido = serializer.save()
            self.assertEqual(updated_detalle_pedido.cantidad, update_data['cantidad'])

    def test_detalle_pedido_serializer_stock(self):
        # comprobar validación de stock
        invalid_data = {
            'pedido': self.pedido.id_pedido,
            'producto': self.producto.id_producto,
            'cantidad': 20
        }
        serializer = DetallePedidoPostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_detalle_pedido_delete(self):
        detalle_pedido = DetallePedido.objects.create(**self.detalle_pedido_data)
        detalle_pedido_id = detalle_pedido.id_detalle_pedido
        detalle_pedido.delete()
        self.assertFalse(DetallePedido.objects.filter(id_detalle_pedido=detalle_pedido_id).exists())

    def test_get_detalle_pedido_data(self):
        detalle_pedido = DetallePedido.objects.create(**self.detalle_pedido_data)
        serializer = DetallePedidoSerializer(detalle_pedido)
        expected_data = {
            'pedido': self.pedido.id_pedido,
            'producto': self.producto.id_producto,
            'cantidad': self.detalle_pedido_data['cantidad']
        }
        self.assertEqual(serializer.data['pedido'], expected_data['pedido'])
        self.assertEqual(serializer.data['producto'], expected_data['producto'])
        self.assertEqual(serializer.data['cantidad'], expected_data['cantidad'])

class EstadoSerializerTestCase(TestCase):
    def setUp(self):
        self.estado_data = {
            'nombre': 'Estado de prueba'
        }

    def test_estado_serializer_valid(self):
        data = {
            'nombre': 'Estado de prueba'
        }
        serializer = EstadoPostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_estado_serializer_save(self):
        data = self.estado_data
        serializer = EstadoPostSerializer(data=data)
        if serializer.is_valid():
            estado = serializer.save()
            self.assertIsNotNone(estado.id_estado)
            self.assertEqual(estado.nombre, self.estado_data['nombre'])
        else:
            self.fail("Serializer no valido")

    def test_estado_serializer_invalid(self):
        invalid_data = self.estado_data.copy()
        invalid_data['nombre'] = None
        serializer = EstadoPostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_estado_serializer_update(self):
        estado = Estado.objects.create(**self.estado_data)
        update_data = {'nombre': "Estado actualizado" }
        serializer = EstadoPostSerializer(estado, data=update_data, partial=True)
        if serializer.is_valid():
            updated_estado = serializer.save()
            self.assertEqual(updated_estado.nombre, update_data['nombre'])
        else:
            self.fail("Serializer no valido")

    def test_estado_delete(self):
        estado = Estado.objects.create(**self.estado_data)
        estado_id = estado.id_estado
        estado.delete()
        self.assertFalse(Estado.objects.filter(id_estado=estado_id).exists())

    def test_get_estado_data(self):
        estado = Estado.objects.create(**self.estado_data)
        serializer = EstadoSerializer(estado)
        expected_data = self.estado_data.copy()
        expected_data['id_estado'] = estado.id_estado 
        self.assertEqual(serializer.data['nombre'], expected_data['nombre'])

class MetodoPagoSerializerTestCase(TestCase):
    def setUp(self):
        self.metodo_pago_data = {
            'nombre': 'Metodo de prueba'
        }

    def test_metodo_pago_serializer_valid(self):
        data = {
            'nombre': 'Metodo de prueba'
        }
        serializer = MetodoPagoPostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_metodo_pago_serializer_save(self):
        data = self.metodo_pago_data
        serializer = MetodoPagoPostSerializer(data=data)
        if serializer.is_valid():
            metodo_pago = serializer.save()
            self.assertIsNotNone(metodo_pago.id_metodo_pago)
            self.assertEqual(metodo_pago.nombre, self.metodo_pago_data['nombre'])
        else:
            self.fail("Serializer no valido")

    def test_metodo_pago_serializer_invalid(self):
        invalid_data = self.metodo_pago_data.copy()
        invalid_data['nombre'] = None
        serializer = MetodoPagoPostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_metodo_pago_serializer_update(self):
        metodo_pago = MetodoPago.objects.create(**self.metodo_pago_data)
        update_data = {'nombre': "Metodo actualizado" }
        serializer = MetodoPagoPostSerializer(metodo_pago, data=update_data, partial=True)
        if serializer.is_valid():
            updated_metodo_pago = serializer.save()
            self.assertEqual(updated_metodo_pago.nombre, update_data['nombre'])
        else:
            self.fail("Serializer no valido")

    def test_metodo_pago_delete(self):
        metodo_pago = MetodoPago.objects.create(**self.metodo_pago_data)
        metodo_pago_id = metodo_pago.id_metodo_pago
        metodo_pago.delete()
        self.assertFalse(MetodoPago.objects.filter(id_metodo_pago=metodo_pago_id).exists())

    def test_get_metodo_pago_data(self):
        metodo_pago = MetodoPago.objects.create(**self.metodo_pago_data)
        serializer = MetodoPagoSerializer(metodo_pago)
        expected_data = self.metodo_pago_data.copy()
        expected_data['id_metodo_pago'] = metodo_pago.id_metodo_pago 
        self.assertEqual(serializer.data['nombre'], expected_data['nombre'])

class EstadoPagoSerializerTestCase(TestCase):
    def setUp(self):
        self.estado_pago_data = {
            'id_estado_pago': 1,
            'nombre': 'Estado de pago de prueba'
        }

    def test_estado_pago_serializer_valid(self):
        data = {
            'id_estado_pago': 1,
            'nombre': 'Estado de pago de prueba'
        }
        serializer = EstadoPagoPostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_estado_pago_serializer_save(self):
        data = self.estado_pago_data
        serializer = EstadoPagoPostSerializer(data=data)
        if serializer.is_valid():
            estado_pago = serializer.save()
            self.assertEqual(estado_pago.nombre, self.estado_pago_data['nombre'])
        else:
            self.fail("Serializer no valido")

    def test_estado_pago_serializer_invalid(self):
        invalid_data = self.estado_pago_data.copy()
        invalid_data['nombre'] = None
        serializer = EstadoPagoPostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_estado_pago_serializer_update(self):
        estado_pago = EstadoPago.objects.create(**self.estado_pago_data)
        update_data = {'nombre': "Estado de pago actualizado" }
        serializer = EstadoPagoPostSerializer(estado_pago, data=update_data, partial=True)
        if serializer.is_valid():
            updated_estado_pago = serializer.save()
            self.assertEqual(updated_estado_pago.id_estado_pago, self.estado_pago_data['id_estado_pago'])
            self.assertEqual(updated_estado_pago.nombre, update_data['nombre'])
        else:
            self.fail("Serializer no valido")

    def test_estado_pago_delete(self):
        estado_pago = EstadoPago.objects.create(**self.estado_pago_data)
        estado_pago_id = estado_pago.id_estado_pago
        estado_pago.delete()
        self.assertFalse(EstadoPago.objects.filter(id_estado_pago=estado_pago_id).exists())

    def test_get_estado_pago_data(self):
        estado_pago = EstadoPago.objects.create(**self.estado_pago_data)
        serializer = EstadoPagoSerializer(estado_pago)
        expected_data = self.estado_pago_data.copy()
        expected_data['id_estado_pago'] = estado_pago.id_estado_pago 
        self.assertEqual(serializer.data['nombre'], expected_data['nombre'])

class PagoSerializerTestCase(TestCase):
    def setUp(self):
        self.tipo_usuario = TipoUsuario.objects.create(nombre="Tipo de prueba")
        self.usuario = UsuarioPersonalizado.objects.create(username="usuario_test", password="password123", id_tipo_usuario=self.tipo_usuario)
        self.estado = Estado.objects.create(nombre="Aceptado")
        self.pedido = Pedido.objects.create(usuario=self.usuario, fecha='2023-01-01', estado=self.estado)
        self.metodo_pago = MetodoPago.objects.create(id_metodo_pago=1, nombre="Metodo de prueba", descripcion="Descripcion de prueba")
        self.estado_pago = EstadoPago.objects.create(id_estado_pago=1, nombre="Aceptado")
        self.pago_data = {
            'pedido': self.pedido,
            'metodo_pago': self.metodo_pago,
            'estado_pago': self.estado_pago,
            'fecha': '2023-01-01',
            'monto': 100,
        }
        self.valid_data = {
            'pedido': self.pedido.id_pedido,
            'metodo_pago': self.metodo_pago.id_metodo_pago,
            'estado_pago': self.estado_pago.id_estado_pago,
            'fecha': '2023-01-01',
            'monto': 100
        }

    def test_pago_serializer_valid(self):
        serializer = PagoPostSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_pago_serializer_save(self):
        serializer = PagoPostSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)   
        if serializer.is_valid():
            pago = serializer.save()
            self.assertIsNotNone(pago.id_pago)
            self.assertEqual(pago.pedido, self.pedido)
            self.assertEqual(pago.metodo_pago.nombre, self.metodo_pago.nombre)
            self.assertEqual(pago.estado_pago, self.estado_pago)
        else:
            self.fail("Serializer no valido")

    def test_pago_serializer_update(self):
        pago = Pago.objects.create(**self.pago_data)
        update_data = {'estado_pago': 1}
        serializer = PagoPostSerializer(pago, data=update_data, partial=True)
        if serializer.is_valid():
            updated_pago = serializer.save()
            self.assertEqual(updated_pago.estado_pago.id_estado_pago, update_data['estado_pago'])
        else:
            self.fail("Serializer no valido")

    def test_pago_serializer_invalid(self):
        invalid_data = self.valid_data.copy()
        invalid_data['fecha'] = None
        serializer = PagoPostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_pago_delete(self):
        pago = Pago.objects.create(**self.pago_data)
        pago_id = pago.id_pago
        pago.delete()
        self.assertFalse(Pago.objects.filter(id_pago=pago_id).exists())

    def test_get_pago_data(self):
        pago = Pago.objects.create(**self.pago_data)
        serializer = PagoSerializer(pago)
        expected_data = {
            'pedido': self.pedido.id_pedido,
            'metodo_pago': self.metodo_pago.id_metodo_pago,
            'estado_pago': self.estado_pago.id_estado_pago,
            'fecha': '2023-01-01',
            'monto': 100
        }
        self.assertEqual(serializer.data['pedido']['id_pedido'], expected_data['pedido'])
        self.assertEqual(int(serializer.data['metodo_pago']['id_metodo_pago']), expected_data['metodo_pago']) #int porque es string
        self.assertEqual(serializer.data['estado_pago']['id_estado_pago'], expected_data['estado_pago'])
        self.assertEqual(serializer.data['fecha'], expected_data['fecha'])
        self.assertEqual(serializer.data['monto'], expected_data['monto'])

class TransaccionSerializerTest(TestCase):
    def setUp(self):
        self.tipo_usuario = TipoUsuario.objects.create(nombre="Tipo de prueba")
        self.usuario = UsuarioPersonalizado.objects.create(username="usuario_test", password="password123", id_tipo_usuario=self.tipo_usuario)
        self.usuario_update = UsuarioPersonalizado.objects.create(username="usuario_test_update", password="password123", id_tipo_usuario=self.tipo_usuario)
        self.estado = Estado.objects.create(nombre="Aceptado")
        self.pedido = Pedido.objects.create(usuario=self.usuario, fecha='2023-01-01', estado=self.estado)
        self.metodo_pago = MetodoPago.objects.create(id_metodo_pago=1, nombre="Metodo de prueba", descripcion="Descripcion de prueba")
        self.estado_pago = EstadoPago.objects.create(id_estado_pago=1, nombre="Aceptado")
        self.pago = Pago.objects.create(pedido=self.pedido, metodo_pago=self.metodo_pago, estado_pago=self.estado_pago, fecha='2023-01-01', monto=100)
        self.transaccion_data = {
            'id_transaccion': 1,
            'pedido': self.pedido,
            'cliente': self.usuario,
            'pago': self.pago
        }
        self.transaccion_valid = {
            'id_transaccion': 1,
            'pedido': self.pago.pedido.id_pedido,
            'cliente': self.pago.pedido.usuario.id,
            'pago': self.pago.id_pago
        }
        
    def test_transaccion_serializer_valid(self):
        serializer = TransaccionPostSerializer(data=self.transaccion_valid)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
    def test_transaccion_serializer_save(self):
        serializer = TransaccionPostSerializer(data=self.transaccion_valid)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        if serializer.is_valid():
            transaccion = serializer.save()
            self.assertIsNotNone(transaccion.pago.id_pago)
            self.assertEqual(transaccion.pedido, self.pedido)
            self.assertEqual(transaccion.cliente, self.usuario)
            self.assertEqual(transaccion.pago, self.pago)
        else:
            self.fail("Serializer no valido")
            
    def test_transaccion_serializer_update(self):
        transaccion = Transaccion.objects.create(**self.transaccion_data)
        update_data = {
            'cliente': self.usuario_update.id,
        }
        serializer = TransaccionPostSerializer(transaccion, data=update_data, partial=True)
        if serializer.is_valid():
            updated_transaccion = serializer.save()
            self.assertEqual(updated_transaccion.cliente.id, update_data['cliente'])
        else:
            self.fail("Serializer no valido")

    def test_transaccion_serializer_invalid(self):
        invalid_data = self.transaccion_valid.copy()
        invalid_data['pedido'] = None
        serializer = TransaccionPostSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_transaccion_delete(self):
        transaccion = Transaccion.objects.create(**self.transaccion_data)
        transaccion_id = transaccion.id_transaccion
        transaccion.delete()
        self.assertFalse(Transaccion.objects.filter(id_transaccion=transaccion_id).exists())

    def test_get_transaccion_data(self):
        transaccion = Transaccion.objects.create(**self.transaccion_data)
        serializer = TransaccionSerializer(transaccion)
        expected_data = {
            'pago': transaccion.pago.id_pago,
            'cliente': transaccion.cliente.id,
            'pedido': transaccion.pedido.id_pedido
        }
        self.assertEqual(serializer.data['pago']['id_pago'], expected_data['pago'])
        self.assertEqual(serializer.data['cliente']['id'], expected_data['cliente'])
        self.assertEqual(serializer.data['pedido']['id_pedido'], expected_data['pedido'])

