from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class Customuser(AbstractUser):
    user_type=models.IntegerField(default=1)
    pancard = models.CharField(max_length=10, unique=True)
    is_approve=models.BooleanField(default=False)
   
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    specification=models.TextField()
    quantity=models.IntegerField()

    def __str__(self):
        return self.name
class Usermember(models.Model):
    user=models.ForeignKey(Customuser,on_delete=models.CASCADE,null=True)
    is_approve=models.BooleanField(default=False)
    user_type=models.IntegerField(default=1)
    

    
    def __str__(self):
        return f"{self.user.username} - Approved: {self.is_approve}"
class Cart(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Orders(models.Model):
    DELIVERY_METHOD_CHOICES = [
        ('road', 'Road'),
        ('airline', 'Airline'),
        ('ship', 'Ship')
    ]
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    country = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    cart_items = models.ManyToManyField(CartItem)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHOD_CHOICES)
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'






