from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import viewsets
from core.models import *
from core.serializers import * 
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework import generics


# Create your views here.
class userViewSet(viewsets.ModelViewSet):
    queryset = UsuarioPersonalizado.objects.all()
    serializer_class = UserSerializer
