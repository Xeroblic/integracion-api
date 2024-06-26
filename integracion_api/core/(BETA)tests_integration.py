


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