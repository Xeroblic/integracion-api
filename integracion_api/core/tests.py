import requests
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import *
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from base64 import b64encode
from rest_framework.test import APIRequestFactory
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
# Create your tests here.

class TestIntegracionEndpoints(APITestCase):
    def setUp(self):
        # Crear usuario para autenticación
        tipo_usuario, created = TipoUsuario.objects.get_or_create(id_tipo_usuario=1) 
        self.user = UsuarioPersonalizado.objects.create_user(username='testuser', password='testpassword', id_tipo_usuario=tipo_usuario)
        self.auth_string = b64encode(f'testuser:testpassword'.encode('utf-8')).decode('utf-8')
        
    def test_usuario_existe(self):
        # Intentar recuperar el usuario por su nombre de usuario
        user_exists = UsuarioPersonalizado.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists, "Test user not created in DB")
    
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


class ObtainTokenViewTest(TestCase):
    def setUp(self):
        tipo_usuario, created = TipoUsuario.objects.get_or_create(id_tipo_usuario=1) 
        self.client = APIClient()
        self.user = UsuarioPersonalizado.objects.create_user(username='testuser', password='testpassword',id_tipo_usuario=tipo_usuario)
        self.userBypass = UsuarioPersonalizado.objects.get(username='testuser')
        self.url = reverse('get-token')  

    def test_missing_authorization_header(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_authorization_header(self):
        self.client.credentials(HTTP_AUTHORIZATION='Basic abc123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        
class UserViewTest(TestCase):
    def setUp(self):
        tipo_usuario, created = TipoUsuario.objects.get_or_create(id_tipo_usuario=1) 
        self.client = APIClient()
        self.user = UsuarioPersonalizado.objects.create_user(username='testuser', password='testpassword',id_tipo_usuario=tipo_usuario)
        self.token = Token.objects.create(user=self.user)
        self.url = reverse('usuario-list')  
    
    def test_missing_authorization_header(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_users(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = {
            'username': 'testuser2',
            'password': 'testpassword2',
            'id_tipo_usuario': 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = {
            'username': 'testuser2',
            'password': 'testpassword2',
            'id_tipo_usuario': 1
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_get_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.url + '1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    