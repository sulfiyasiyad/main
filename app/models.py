from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class Customuser(AbstractUser):
    user_type=models.IntegerField(default=1)
   
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name











