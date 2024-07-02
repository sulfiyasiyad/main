from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  add_product


from .views import Client
from . import views
from .views import user_data_view
from .views import ProductListView,HomeView,ProductViewLogin
# from .views import CartViewSet
from rest_framework_simplejwt import views as jwt_views



router = DefaultRouter()
# router.register(r'products', ProductListView, basename='product')
# router.register(r'cart', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
    # path('login/', LoginView.as_view(), name='login'),
    
    path('add-product/', add_product, name='add_product'),
    path('users/', Client, name='Client'),
    path('unapproved-users/', views.unapproved_users, name='unapproved-users'),
    path('accept-user/<int:pk>/', views.accept_user, name='accept-user'),
    path('decline-user/<int:pk>/', views.decline_user, name='decline-user'),
    path('login/', views.login_view, name='login'),
    # path('userdata/', views.user_data_view, name='user_data'),
    path('userdata/', user_data_view, name='user-data'),
    path('products/', ProductListView.as_view(), name='product-list'),
    # path('signin/', LoginView.as_view(), name='signin'),
    # path('add/', AddToCartView.as_view(), name='add-to-cart'),
   
    
    path('home/',HomeView.as_view(), name ='home'),
    path('product/', ProductViewLogin.as_view(), name='product'),
    path('add-to-cart/<int:product_id>/',views.add_to_cart, name='add-to-cart'),
    path('view-cart/', views.view_cart, name='view-cart'),
]
    

   
    
    
    
  
    

    
   

