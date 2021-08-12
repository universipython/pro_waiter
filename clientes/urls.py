from django.urls import path
from . import views

urlpatterns = [
    path('mesa/<slug:slug>/', views.mesa_cliente, name="mesa-cliente"),
    path('cardapio/<slug:slug>/', views.cardapio_cliente,
         name='cardapio-cliente'),
    path('solicitacao-atendimento/<slug:slug>/', views.solicita_atendimento,
         name="solicita-atendimento"),
    path('solicitacao-fechamento/<slug:slug>/', views.solicita_fechamento,
         name='solicita-fechamento'),
]
