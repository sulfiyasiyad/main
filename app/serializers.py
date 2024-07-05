from .models import Customuser
from .models import Product
from .models import Usermember,OrderItem,Orders


from rest_framework import serializers
from .models import Cart

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
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name= serializers.CharField(source='user.last_name', read_only=True)
   


    class Meta:
        model = Usermember
        fields = ['id', 'user', 'is_approve', 'username','email','user_type','first_name','last_name'] 
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields  = ['product', 'quantity']
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'user', 'cart', 'total_price', 'address', 'district', 'pin_code']
class OrderSerializer(serializers.ModelSerializer):
    cart_items = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = [
            'id', 'user', 'first_name', 'last_name', 'username', 'email',
            'address', 'country', 'district', 'pincode', 'total_price',
            'delivery_method', 'tracking_id', 'estimated_delivery_date', 'created_at', 'cart_items'
        ]
       
        read_only_fields = ['user', 'total_price', 'created_at', 'cart_items']
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
