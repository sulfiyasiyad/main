from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  LoginView,add_product
from.views import ProductViewSet

from .views import Client
from . import views


router = DefaultRouter()
# router.register(r'users', Client)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('add-product/', add_product, name='add_product'),
    path('users/', Client, name='Client'),
    path('unapproved-users/', views.unapproved_users, name='unapproved-users'),
    
   

]