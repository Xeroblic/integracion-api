from rest_framework.response import Response
from rest_framework import serializers
from core.models import * 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['id', 'username', 'email', 'password', 'first_name', 'telefono']
        extra_kwargs = {'password': {'write_only': True}}