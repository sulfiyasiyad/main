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

from rest_framework.decorators import api_view

from .models import Usermember
from .serializers import ProductSerializer
from django.contrib.auth.decorators import login_required

from .serializers import  UsermemberSerializer
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import Product
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CartSerializer
from .models import Cart








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


    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        return JsonResponse({'user_type': user.user_type}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)




@api_view(['POST'])
def add_product(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
          
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


   
@api_view(['GET'])
def unapproved_users(request):
    if request.method == 'GET':
        unapproved_users = Usermember.objects.filter(is_approve=False)
       
        serializer = UsermemberSerializer(unapproved_users, many=True)
        print("Unapproved Users QuerySet:", unapproved_users)
        return Response(serializer.data)
@api_view(['PATCH'])
def accept_user(request, pk):
    try:
        user_member = Usermember.objects.get(pk=pk)
    except Usermember.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user_member.is_approve = True
    user_member.save()
    random_password = get_random_string(length=6, allowed_chars='0123456789')
    
    # Update user's password
    user = user_member.user
    user.password = make_password(random_password)
    user.save()
    send_mail(
            'Welcome!',
            'Thank you for registering.Your password is:'+random_password,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
    )
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def decline_user(request, pk):
    try:
        user_member = Usermember.objects.get(pk=pk)
    except Usermember.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user_member.user.delete()  # Delete the associated user
    user_member.delete()  # Delete the user member
    return Response(status=status.HTTP_204_NO_CONTENT)
# @api_view(['GET'])
# def user_data_view(request):
#     user = request.user
#     print(user)
#     return JsonResponse({'username': user.username, 'email': user.email}, status=200)
api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_data_view(request):
    user = request.user
    print(user)
    return JsonResponse({'error': 'sucess'}, status=200)

# class ProductListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)
class ProductListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = Customuser.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,  # Include the username in the response
            })
        return Response({"error": "Invalid credentials"}, status=400)
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    print(serializer_class)
    permission_classes = [AllowAny]
    
  

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart_item, created = Cart.objects.get_or_create(
            user=self.request.user,
            product=serializer.validated_data['product'],
            defaults={'quantity': serializer.validated_data['quantity']}
        )
        if not created:
            cart_item.quantity += serializer.validated_data['quantity']
            cart_item.save()
        return Response(CartSerializer(cart_item).data)
       
