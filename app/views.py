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
from .models import Product, Cart, CartItem
from .models import Usermember
from .serializers import ProductSerializer
from django.db.utils import IntegrityError
from .serializers import  UsermemberSerializer
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action



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


    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
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

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        product = self.get_object()
        cart, created = Cart.objects.get_or_create(user=request.user)
        print(cart)
        cart_product, created = CartItem.objects.get_or_create(cart=cart, product=product)

        return Response({'message': 'Product added to cart successfully.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_from_cart(self, request, pk=None):
        product = self.get_object()
        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart, product=product).delete()

        return Response({'message': 'Product removed from cart successfully.'}, status=status.HTTP_200_OK)
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
@login_required
def get_username(request):
    return Response({'username': request.user.username})


# class CartViewSet(viewsets.ModelViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

#     @action(detail=False, methods=['get'])
#     def get_user_cart(self, request):
#         user = request.user
#         cart, created = Cart.objects.get_or_create(user=user)
#         serializer = self.get_serializer(cart)
#         return Response(serializer.data)

#     @action(detail=True, methods=['post'])
#     def add_to_cart(self, request, pk=None):
#         user = request.user
#         cart, created = Cart.objects.get_or_create(user=user)
#         product_id = request.data.get('product_id')
#         quantity = request.data.get('quantity', 1)

#         product = Product.objects.get(id=product_id)
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#         if not created:
#             cart_item.quantity += int(quantity)
#             cart_item.save()

#         return Response({'status': 'product added to cart'})
