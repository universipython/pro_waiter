from django.urls import path
from . import views

urlpatterns = [
    path('entrar/', views.LoginUsuario.as_view(), name='entrar'),
    
]
