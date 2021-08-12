from django.shortcuts import render, get_object_or_404
from restaurante.models import Mesa, Comanda
from collections import namedtuple

from restaurante.models import Categoria, ItemCardapio
from django.db.models import Count, Q

from garcom.models import Tarefa


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


def solicita_atendimento(request, slug):
    mesa = get_object_or_404(Mesa, slug=slug)

    try:
        comanda = Comanda.objects.get(mesa=mesa, status='aberta')
    except Comanda.DoesNotExist:
        comanda = None

    if comanda:
        # Já existe comanda aberta para a mesa que fez a solicitação

        # Verifica se existe solicitação de atendimento pendente para a mesa
        # exceto entrega
        try:
            tarefa = Tarefa.objects.get(~Q(tipo='entrega'), mesa=mesa, status='pendente')
            if tarefa.tipo != 'prim_atendimento':
                tarefa.tipo = 'atendimento'
                tarefa.save()
        except Tarefa.DoesNotExist:
            tarefa = Tarefa.objects.create(
                tipo='atendimento',
                mesa=mesa
            )
    else:
        # nessa caso, não existe comanda aberta para a mesa

        # abre uma nova comanda para a mesa
        comanda = Comanda.objects.create(mesa=mesa)
        # cria uma nova tarefa de primeiro atendimento para a mesa
        tarefa = Tarefa.objects.create(
            tipo='prim_atendimento',
            mesa=mesa
        )
    return render(
        request,
        'clientes/solicitacao.html',
        {
            'mesa':mesa,
            'tarefa':tarefa,
        }
    )

def solicita_fechamento(request, slug):
    mesa = get_object_or_404(Mesa, slug=slug)

    try:
        tarefa = Tarefa.objects.get(~Q(tipo='entrega'), mesa=mesa, status='pendente')
        if tarefa.tipo != 'prim_atendimento':
            tarefa.tipo = 'fechamento'
            tarefa.save()
    except Tarefa.DoesNotExist:
        tarefa = Tarefa.objects.create(
            tipo='fechamento',
            mesa=mesa
        )
    return render(
        request,
        'clientes/solicitacao.html',
        {
            'mesa':mesa,
            'tarefa':tarefa,
        }
    )
