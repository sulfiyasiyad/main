from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


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











