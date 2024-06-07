from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  LoginView

from .views import Client

router = DefaultRouter()
router.register(r'users', Client)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),

]