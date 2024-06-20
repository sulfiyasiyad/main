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


  

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['id', 'name', 'price', 'description','specification','quantity']
    # def create(self, validated_data):
    #     pro= Product.objects.create_pro(
    #         name=validated_data['name'],
    #         price=validated_data['price'],
    
    #         description=validated_data['description'],
    #         specification=validated_data['specification'],
    #         quantity=validated_data['quantity'],
            
    #     )
    #     return pro
class UsermemberSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Usermember
    #     fields = '__all__'
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)


    class Meta:
        model = Usermember
        fields = ['id', 'user', 'is_approve', 'username','email'] 
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'cart']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

