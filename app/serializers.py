from .models import Customuser
from .models import Product
from .models import Usermember

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
        fields = ['username', 'password']


  

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
# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'product', 'quantity']
#         read_only_fields = ['user']
        