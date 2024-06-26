from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  add_product


from .views import Client, LoginView
from . import views
from .views import user_data_view
from .views import ProductListView
from .views import CartViewSet
from rest_framework_simplejwt import views as jwt_views



router = DefaultRouter()
# router.register(r'products', ProductListView, basename='product')
router.register(r'cart', CartViewSet, basename='cart')


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
    path('signin/', LoginView.as_view(), name='signin'),
    # path('cart/', CartViewSet.as_view({'post': 'create', 'get': 'list'}), name='cart'),
    path('token/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
     path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh')
]
    

   
    
    
    
  
    

    
   

