from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroViewSet
from .views import UserRegisterView
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register(r'entries', RegistroViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('login/', views.user_login, name='login'),
    path('create_entry/', views.create_entry, name='create_entry'),
    path('user_register/', views.user_register, name='user_register'),
]