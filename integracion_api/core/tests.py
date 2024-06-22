from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import *
from core.serializers import * 
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from base64 import b64encode
from django.utils.crypto import get_random_string
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

# Create your tests here.

# class TestIntegracionEndpoints(APITestCase):
#     def setUp(self):
#         # Crear usuario para autenticación
#         tipo_usuario, created = TipoUsuario.objects.get_or_create(id_tipo_usuario=1) 
#         self.user = UsuarioPersonalizado.objects.create_user(username='testuser', password='testpassword', id_tipo_usuario=tipo_usuario)
#         self.auth_string = b64encode(f'testuser:testpassword'.encode('utf-8')).decode('utf-8')
        
#     def test_usuario_existe(self):
#         # Intentar recuperar el usuario por su nombre de usuario
#         user_exists = UsuarioPersonalizado.objects.filter(username='testuser').exists()
#         self.assertTrue(user_exists, "Test user not created in DB")
    
    # def test_get_token(self):
    #     url = reverse('get-token')
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Basic {self.auth_string}')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_pedido_detail(self):
    #     # Asumiendo que ya existe un pedido con id=1
    #     url = reverse('pedido-detail', args=[1])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # Verificar contenido de la respuesta

    # # Añadir más métodos de test para otros endpoints siguiendo el patrón anterior

    # def tearDown(self):
    #     # Limpiar datos si es necesario
    #     pass


# class ObtainTokenViewTest(TestCase):
#     def setUp(self):
#         tipo_usuario, created = TipoUsuario.objects.get_or_create(id_tipo_usuario=1) 
#         self.client = APIClient()
#         self.user = UsuarioPersonalizado.objects.create_user(username='testuser', password='testpassword',id_tipo_usuario=tipo_usuario)
#         self.userBypass = UsuarioPersonalizado.objects.get(username='testuser')
#         self.url = reverse('get-token')  

#     def test_missing_authorization_header(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_invalid_authorization_header(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Basic abc123')
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_invalid_credentials(self):
    #     self.client2.auth = HTTPBasicAuth('testuser', 'testpassword')
    #     self.client2.headers.update({'x-test': 'true'})
    #     response = self.client2.get('http://127.0.0.1:8000/get-token/')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_valid_credentials(self):
    #     # Codificar las credenciales en base64
    #     self.client.force_authenticate(user=self.userBypass, token=None)
    #     response = self.client.get(self.url)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue('token' in response.data)
        
# class UserViewTest(TestCase):
#     def setUp(self):
#         tipo_usuario, created = TipoUsuario.objects.get_or_create(id_tipo_usuario=1) 
#         self.client = APIClient()
#         self.user = UsuarioPersonalizado.objects.create_user(username='testuser', password='testpassword',id_tipo_usuario=tipo_usuario)
#         self.token = Token.objects.create(user=self.user)
#         self.url = reverse('usuario-list')  
    
#     def test_missing_authorization_header(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
#     def test_get_users(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    
#     def test_create_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         data = {
#             'username': 'testuser2',
#             'password': 'testpassword2',
#             'id_tipo_usuario': 1
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
#     def test_update_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         data = {
#             'username': 'testuser2',
#             'password': 'testpassword2',
#             'id_tipo_usuario': 1
#         }
#         response = self.client.put(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
#     def test_delete_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
#     def test_get_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         response = self.client.get(self.url + '1/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    
# class PedidoViewTest(TestCase):
#     def setUp(self):
#         tipo_usuario, created = TipoUsuario.objects.get_or_create(id_tipo_usuario=1) 
#         self.client = APIClient()
#         self.user = UsuarioPersonalizado.objects.create_user(username='testuser', password='testpassword',id_tipo_usuario=tipo_usuario)
#         self.user_id = self.user.id
#         self.estado = Estado.objects.create(nombre='Estado de prueba')
#         self.estado_id = self.estado.id_estado
#         self.token = Token.objects.create(user=self.user)
#         self.url = reverse('pedido-list')  
    
#     def test_missing_authorization_header(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
#     def test_create_pedido(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         data = {
#             'usuario': self.user_id,
#             'fecha': '2022-01-01',
#             'estado': self.estado_id
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
#     def test_get_pedidos(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    
#     def test_update_pedido(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         data = {
#             'usuario': self.user_id,
#             'fecha': '2022-01-02',
#             'estado': self.estado_id
#         }
#         response = self.client.put(self.url, data)
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
#     def test_get_pedido(self):
#         self.test_create_pedido()
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         url = f'{self.url}1/'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    
#     def test_delete_pedido(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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

