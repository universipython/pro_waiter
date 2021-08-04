from django.shortcuts import render, get_object_or_404
from restaurante.models import Mesa, Comanda
from collections import namedtuple

from restaurante.models import Categoria, ItemCardapio
from django.db.models import Count, Q


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


def cardapio_cliente(request, slug):
    mesa = get_object_or_404(Mesa, slug=slug)
    categorias = Categoria.objects. \
                annotate(ativos=Count('itemcardapio', \
                                      filter=Q(itemcardapio__ativo=True))). \
                                      filter(ativos__gt=0)
    itens_sem_categoria = ItemCardapio.objects.filter(categoria__isnull=True,
                                                      ativo=True)
    return render(request, 'clientes/cardapio_cliente.html',
                  {'mesa':mesa,
                   'categorias':categorias,
                   'itens_sem_categoria':itens_sem_categoria})
