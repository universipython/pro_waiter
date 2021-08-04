from django.urls import path
from . import views

urlpatterns = [
    path('mesa/<slug:slug>/', views.mesa_cliente, name="mesa-cliente"),
    path('cardapio/<slug:slug>/', views.cardapio_cliente,
         name='cardapio-cliente'),
]
