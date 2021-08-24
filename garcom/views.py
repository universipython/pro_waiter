from django.shortcuts import render
from .models import Tarefa


def painel_view(request):
    entregas = Tarefa.objects.filter(tipo='entrega')
    prim_atendimentos = Tarefa.objects.filter(tipo='prim_atendimento')
    atendimentos = Tarefa.objects.filter(tipo='atendimento')
    fechamentos = Tarefa.objects.filter(tipo='fechamento')
    qtdd_atendimentos = prim_atendimentos.count() + atendimentos.count()
    print(prim_atendimentos)
    context = {
        'entregas':entregas,
        'prim_atendimentos':prim_atendimentos,
        'atendimentos':atendimentos,
        'fechamentos':fechamentos,
        'qtdd_atendimentos':qtdd_atendimentos,
    }

    return render(request, 'garcom/home.html', context)
