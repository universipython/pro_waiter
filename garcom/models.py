from django.db import models
from django.conf import settings
from django.utils import timezone

from restaurante.models import Mesa, ItemPedido

class Tarefa(models.Model):

    OPCOES_TIPO = (
        ('prim_atendimento', 'Primeiro Atendimento'),
        ('atendimento', 'Atendimento'),
        ('fechamento', 'Fechamento'),
        ('entrega', 'Entrega')
    )

    OPCOES_STATUS = (
        ('pendente', 'Pendente'),
        ('concluido', 'Concluido'),
    )

    tipo = models.CharField(max_length=16, choices=OPCOES_TIPO)
    garcom = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=9, choices=OPCOES_STATUS, default='pendente')
    hr_criacao = models.DateTimeField(auto_now_add=True)
    hr_atendimento = models.DateTimeField(null=True, blank=True)
    mesa = models.ForeignKey(Mesa, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f"{self.get_tipo_display()} na mesa {self.mesa.numero}"


    def atender_tarefa(self, garcom):
        self.garcom = garcom
        self.status = 'concluido'
        self.hr_atendimento = timezone.now()
        self.save()


class Entrega(models.Model):
    pedido = models.OneToOneField(ItemPedido, on_delete=models.CASCADE)
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE)
