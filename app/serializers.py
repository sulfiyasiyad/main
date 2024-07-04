from .models import Customuser
from .models import Product
from .models import Usermember
from .models import Orders
from .models import OrderItem

from rest_framework import serializers
from .models import Cart, CartItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['username', 'first_name', 'last_name', 'email', 'pancard', 'user_type']
    def create(self, validated_data):
        user = Customuser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
    
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            pancard=validated_data['pancard'],
            user_type=validated_data['user_type'],
        )
        return user
    def validate_email(self, value):
        if Customuser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['username', 'password','user_type']


  

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
   
class UsermemberSerializer(serializers.ModelSerializer):
   
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)


    class Meta:
        model = Usermember
        fields = ['id', 'user', 'is_approve', 'username','email'] 
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields  = ['product', 'quantity']
# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Orders
#         fields = ['id', 'user', 'cart', 'total_price', 'address', 'district', 'pin_code']
class OrderSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True)  # Use CartSerializer for nested representation

    class Meta:
        model = Orders
        fields = ['user', 'cart', 'total_price', 'address', 'district', 'pin_code']

    def create(self, validated_data):
        cart_data = validated_data.pop('cart')  # Extract cart data
        order = Orders.objects.create(**validated_data)
        
        for item_data in cart_data:
            # Create each Cart object associated with the order
            Cart.objects.create(order=order, **item_data)
        
        return order