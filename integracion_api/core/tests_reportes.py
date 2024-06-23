from unittest import mock
from django.test import TestCase
from django.utils import timezone
from core.models import *
from core.views import ProductosMasVendidosView, reporteEstrategiasYVentasView, informeVentaMensual
from rest_framework.test import APIRequestFactory

class ReporteEstrategiasYVentasViewTest(TestCase):
    def setUp(self):
        # Configuración de productos y detalles de pedido
        self.producto_data = {
            'sku': 'SKU123',
            'marca': 'MarcaX',
            'nombre': 'producto_vendido',
            'precio_neto': 100,
            'stock': 10,
            'imagen_url': 'http://example.com/imagen.jpg'
        }
        self.producto_data_no_vendido = {
            'sku': 'SKU123',
            'marca': 'MarcaX',
            'nombre': 'producto_no_vendido',
            'precio_neto': 100,
            'stock': 10,
            'imagen_url': 'http://example.com/imagen.jpg'
        }
        
        self.producto_vendido = Producto.objects.create(**self.producto_data)
        self.producto_no_vendido = Producto.objects.create(**self.producto_data_no_vendido)
        
        tipo_usuario = TipoUsuario.objects.create(nombre="Tipo de prueba")
        self.usuario = UsuarioPersonalizado.objects.create(username="usuario_test", password="password123", id_tipo_usuario=tipo_usuario)
        self.estado = Estado.objects.create(id_estado=1, nombre="Aceptado")
        self.pedido_data = {
            'usuario': self.usuario,
            'fecha': timezone.now().date(),
            'estado': self.estado
        }
        self.pedido = Pedido.objects.create(**self.pedido_data)
        self.detalle_pedido = DetallePedido.objects.create(producto=self.producto_vendido, cantidad=1, pedido=self.pedido)
        
        # falsa peticion para cumplir el request de las views.
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/fake-url') 
        self.view = reporteEstrategiasYVentasView()
        
        self.view.kwargs = {}  
        self.view.format_kwarg = None  
        self.view.request = mock.Mock()

        # Llamada al método list de la vista y almacenamiento de la respuesta para su uso en los tests
        self.response = self.view.list(self.view.request)

    def test_respuesta_correcta(self):
        queryset = self.view.get_queryset()
        self.assertIn(self.producto_no_vendido, queryset)
        self.assertNotIn(self.producto_vendido, queryset)

    def test_list(self):
        productos_sin_ventas = self.response.data['productos_sin_ventas']
        self.assertTrue(any(producto['nombre'] == "producto_no_vendido" for producto in productos_sin_ventas))
        self.assertFalse(any(producto['nombre'] == "producto_vendido" for producto in productos_sin_ventas))
    
    def test_respuesta_inicial(self):
        self.assertIn('productos_sin_ventas', self.response.data)

    def test_tipo_de_datos_respuesta(self):
        self.assertIsInstance(self.response.data, dict)

    def test_cantidad_de_productos(self):
        self.assertEqual(len(self.response.data['productos_sin_ventas']), 1)
    
    def test_campos_minimos(self):
        productos_sin_ventas = self.response.data['productos_sin_ventas']
        self.assertIn('id_producto', productos_sin_ventas[0])
        self.assertIn('sku', productos_sin_ventas[0])
        self.assertIn('nombre', productos_sin_ventas[0])
        self.assertIn('marca', productos_sin_ventas[0])
        self.assertIn('precio_neto', productos_sin_ventas[0])
        self.assertIn('fecha', productos_sin_ventas[0])
        self.assertIn('stock', productos_sin_ventas[0])
        self.assertIn('imagen_url', productos_sin_ventas[0])
        self.assertIn('ventas', productos_sin_ventas[0])

class ProductosMasVendidosViewTests(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas
        self.producto_data = {
            'sku': 'SKU123',
            'marca': 'MarcaX',
            'nombre': 'producto_vendido',
            'precio_neto': 100,
            'stock': 10,
            'imagen_url': 'http://example.com/imagen.jpg'
        }
        self.producto_data_no_vendido = {
            'sku': 'SKU123',
            'marca': 'MarcaX',
            'nombre': 'producto_no_vendido',
            'precio_neto': 100,
            'stock': 10,
            'imagen_url': 'http://example.com/imagen.jpg'
        }
        
        self.producto_vendido = Producto.objects.create(**self.producto_data)
        self.producto_no_vendido = Producto.objects.create(**self.producto_data_no_vendido)
        
        tipo_usuario = TipoUsuario.objects.create(nombre="Tipo de prueba")
        self.usuario = UsuarioPersonalizado.objects.create(username="usuario_test", password="password123", id_tipo_usuario=tipo_usuario)
        self.estado = Estado.objects.create(id_estado=1, nombre="Aceptado")
        self.pedido_data = {
            'usuario': self.usuario,
            'fecha': timezone.now().date(),
            'estado': self.estado
        }
        self.pedido = Pedido.objects.create(**self.pedido_data)
        self.detalle_pedido = DetallePedido.objects.create(producto=self.producto_vendido, cantidad=1, pedido=self.pedido)

        self.factory = APIRequestFactory()
        self.request = self.factory.get('/fake-url') 
        self.view = ProductosMasVendidosView()
        self.view.request = self.request
        self.view.request = mock.Mock()
        
        self.view.kwargs = {}  
        self.view.format_kwarg = None  
        
        self.response = self.view.list(self.view.request)

    def test_respuesta_correcta(self):
        queryset = self.view.get_queryset()
        self.assertEqual(self.detalle_pedido.cantidad, queryset[0]['veces_vendido'])

    def test_list(self):
        productos_mas_vendidos = self.response.data['productos_mas_vendidos_este_mes']
        self.assertTrue(any(producto['nombre'] == "producto_vendido" for producto in productos_mas_vendidos))
        self.assertFalse(any(producto['nombre'] == "producto_no_vendido" for producto in productos_mas_vendidos))
    
    def test_respuesta_inicial(self):
        self.assertIn('productos_mas_vendidos_este_mes', self.response.data)

    def test_tipo_de_datos_respuesta(self):
        self.assertIsInstance(self.response.data, dict)

    def test_cantidad_de_productos(self):
        self.assertEqual(len(self.response.data['productos_mas_vendidos_este_mes']), 1)
    
    def test_campos_minimos(self):
        productos_mas_vendidos = self.response.data['productos_mas_vendidos_este_mes']
        self.assertIn('id_producto', productos_mas_vendidos[0])
        self.assertIn('sku', productos_mas_vendidos[0])
        self.assertIn('nombre', productos_mas_vendidos[0])
        self.assertIn('marca', productos_mas_vendidos[0])
        self.assertIn('precio_neto', productos_mas_vendidos[0])
        self.assertIn('fecha', productos_mas_vendidos[0])
        self.assertIn('stock', productos_mas_vendidos[0])
        self.assertIn('imagen_url', productos_mas_vendidos[0])
        self.assertIn('veces_vendido', productos_mas_vendidos[0])
        self.assertIn('total_productos_vendidos', productos_mas_vendidos[0])

class InformeVentasMensualViewTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas
        self.producto_data = {
            'sku': 'SKU123',
            'marca': 'MarcaX',
            'nombre': 'producto_vendido',
            'precio_neto': 100,
            'stock': 10,
            'imagen_url': 'http://example.com/imagen.jpg'
        }
        self.producto_data_no_vendido = {
            'sku': 'SKU123',
            'marca': 'MarcaX',
            'nombre': 'producto_no_vendido',
            'precio_neto': 100,
            'stock': 10,
            'imagen_url': 'http://example.com/imagen.jpg'
        }
        
        self.producto_vendido = Producto.objects.create(**self.producto_data)
        self.producto_no_vendido = Producto.objects.create(**self.producto_data_no_vendido)
        
        tipo_usuario = TipoUsuario.objects.create(nombre="Tipo de prueba")
        self.usuario = UsuarioPersonalizado.objects.create(username="usuario_test", password="password123", id_tipo_usuario=tipo_usuario)
        self.estado = Estado.objects.create(id_estado=1, nombre="Aceptado")
        self.pedido_data = {
            'usuario': self.usuario,
            'fecha': timezone.now().date(),
            'estado': self.estado
        }
        self.pedido = Pedido.objects.create(**self.pedido_data)
        self.detalle_pedido = DetallePedido.objects.create(producto=self.producto_vendido, cantidad=1, pedido=self.pedido)
        self.metodo_pago = MetodoPago.objects.create(id_metodo_pago=1, nombre="Metodo de prueba", descripcion="Descripcion de prueba")
        self.estado_pago = EstadoPago.objects.create(id_estado_pago=0, nombre="Aceptado")
        self.pago = Pago.objects.create(pedido=self.pedido, metodo_pago=self.metodo_pago, estado_pago=self.estado_pago, fecha=timezone.now().date(), monto=100)
        self.transaccion_data = {
            'id_transaccion': 1,
            'pedido': self.pedido,
            'cliente': self.usuario,
            'pago': self.pago
        }
         
        self.transaccion = Transaccion.objects.create(**self.transaccion_data)
        
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/fake-url') 
        self.view = informeVentaMensual()
        self.view.request = self.request
        self.view.request = mock.Mock()
        
        self.view.kwargs = {'month': timezone.now().month}  
        self.view.format_kwarg = None  
        
        self.response = self.view.list(self.view.request)

    def test_retornar_respuesta(self):
        queryset = self.view.get_queryset()
        self.assertTrue(queryset.exists())

    def test_list(self):
        transacciones = self.response.data['transacciones']
        self.assertTrue(any(transaccion['id_transaccion'] == self.transaccion_data['id_transaccion'] for transaccion in transacciones))
        
    def test_respuesta_inicial(self):
        self.assertIn('transacciones', self.response.data)
        self.assertIn('total_ventas_mes', self.response.data)
        self.assertIn('mes', self.response.data)
        
    def test_tipo_de_datos_respuesta(self):
        self.assertIsInstance(self.response.data, dict)
    
    def test_campos_minimos(self):
        transacciones = self.response.data['transacciones']
        self.assertIn('id_transaccion', transacciones[0])
        self.assertIn('pedido', transacciones[0])
        self.assertIn('cliente', transacciones[0])
        self.assertIn('pago', transacciones[0])
    
    def test_comprobar_mes(self):
        self.assertIsNot(self.view.kwargs['month'], timezone.now().month - 1)
        self.assertIsNot(self.view.kwargs['month'], timezone.now().month + 1)
        self.assertEqual(self.view.kwargs['month'], timezone.now().month)
    
        