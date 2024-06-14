from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Customuser
from rest_framework import generics
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
import string
import random
from rest_framework import status
from django.core.mail import send_mail
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .models import Product
from .models import Usermember
from .serializers import ProductSerializer
from django.db.utils import IntegrityError
from .serializers import  UsermemberSerializer

# class Client(viewsets.ModelViewSet):
#     queryset = Customuser.objects.all()
#     serializer_class = UserSerializer

#     def perform_create(self, serializer):
#         user = serializer.save()
#         random_password = ''.join(random.choices(string.digits, k=6))
#         user.set_password(random_password)
#         user.save()
#         send_mail(
#             'Welcome!',
#             'Thank you for registering.Your password is:'+random_password,
#             settings.EMAIL_HOST_USER,
#             [user.email],
#             fail_silently=False,
#         )
@api_view(['POST'])
def Client(request):
    if request.method == 'POST':
        customuser_serializer = UserSerializer(data=request.data)
        if customuser_serializer.is_valid():
            customuser_instance = customuser_serializer.save()
            
            # Assuming you want to create a Usermember instance upon registration
            usermember_data = {
                'user': customuser_instance.id,
                'is_approve': False  # Default value as per your model
            }
            usermember_serializer = UsermemberSerializer(data=usermember_data)
            if usermember_serializer.is_valid():
                usermember_serializer.save()
            
            return Response(customuser_serializer.data, status=status.HTTP_201_CREATED)
        return Response(customuser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = Customuser.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
               'sucess'
            })

        else:
            return Response({'error': 'Invalid credentials'}, status=400)
@api_view(['POST'])
def add_product(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
          
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
@api_view(['GET'])
def unapproved_users(request):
    if request.method == 'GET':
        unapproved_users = Usermember.objects.filter(is_approve=False)
       
        serializer = UsermemberSerializer(unapproved_users, many=True)
        print("Unapproved Users QuerySet:", unapproved_users)
        return Response(serializer.data)
    