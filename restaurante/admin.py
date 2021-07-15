from django.contrib import admin
from .models import Mesa, Comanda, Categoria, ItemCardapio, ItemPedido
# Register your models here.
admin.site.register(Mesa)
admin.site.register(Comanda)
admin.site.register(Categoria)
admin.site.register(ItemCardapio)
admin.site.register(ItemPedido)
