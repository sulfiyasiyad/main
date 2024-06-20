from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  add_product
from.views import ProductViewSet,CustomerHomeView,CartView,AddToCartView

from .views import Client
from . import views


router = DefaultRouter()
# router.register(r'users', Client)
router.register(r'products', ProductViewSet)
# router.register(r'carts', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('login/', LoginView.as_view(), name='login'),
    path('add-product/', add_product, name='add_product'),
    path('users/', Client, name='Client'),
    path('unapproved-users/', views.unapproved_users, name='unapproved-users'),
    path('accept-user/<int:pk>/', views.accept_user, name='accept-user'),
    path('decline-user/<int:pk>/', views.decline_user, name='decline-user'),
    path('login/', views.login_view, name='login'),
    path('get_username/', views.get_username, name='get_username'),
    # path('carts/get_user_cart/', CartViewSet.as_view({'get': 'get_user_cart'}), name='get_user_cart'),
    # path('carts/<int:pk>/add_to_cart/', CartViewSet.as_view({'post': 'add_to_cart'}), name='add_to_cart'),
    
    path('customer/home/', CustomerHomeView.as_view(), name='customer_home'),
    path('cart/', CartView.as_view(), name='cart'),
     path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),



  
    

    
   

]