from django.shortcuts import render, get_object_or_404
from restaurante.models import Mesa, Comanda
from collections import namedtuple


def mesa_cliente(request, slug):
    mesa = get_object_or_404(Mesa, slug=slug)
    Pedidos = namedtuple("Pedidos", ['prontos', 'em_preparo', 'entregues'])
    pedidos = None
    try:
        comanda = Comanda.objects.get(mesa=mesa, status="aberta")
        pedidos_prontos = comanda.itempedido_set.filter(status="pronto")
        pedidos_em_preparo = comanda.itempedido_set.filter(status="preparo")
        pedidos_entregues = comanda.itempedido_set.filter(status="entregue")
        pedidos = Pedidos(
                    pedidos_prontos,
                    pedidos_em_preparo,
                    pedidos_entregues
        )
    except Comanda.DoesNotExist:
        comanda = None
    return render(
                  request,
                  'clientes/mesa_cliente.html',
                  {'mesa':mesa, 'comanda':comanda, 'pedidos':pedidos}
    )
