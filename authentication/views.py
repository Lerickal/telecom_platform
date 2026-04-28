from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data['username']
        password= request.data['password']

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user':{
                'id': user.id,
                'username': user.get_username(),
                'email': user.get_email_field_name()
            }
        })

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.usernane,
            'email': user.email
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message', 'Logged out.'})

def login_page(request):
    return render(request, 'authentication/login.html')