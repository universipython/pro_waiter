from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Mesa(models.Model):

    numero = models.CharField(max_length=3, unique=True)
    slug = models.SlugField(max_length=8, blank=True, unique=True)

    def __str__(self):
        return f"Mesa {self.numero}"

    def save(self, *args, **kwargs):
        self.slug_save()
        super(Mesa, self).save(*args, **kwargs)

    def slug_save(self):
        if not self.slug:
            self.slug = get_random_string(8)
            slug_is_wrong = True
            while slug_is_wrong:
                slug_is_wrong = False
                other_objs_with_slug = type(self).objects.filter(slug=self.slug)
                if len(other_objs_with_slug) > 0:
                    slug_is_wrong = True
                if slug_is_wrong:
                    self.slug = get_random_string(8)

    def get_absolute_url(self):
        return reverse('mesa-cliente', args=[self.slug])

    def get_menu_url(self):
        return reverse('cardapio-cliente', args=[self.slug])


class Comanda(models.Model):
    OPCOES_STATUS = (
            ('aberta', 'Aberta'),
            ('fechada', 'Fechada'),
    )
    codigo = models.SlugField(max_length=8, blank=True, unique=True)
    mesa = models.ForeignKey(Mesa, null=True, on_delete=models.SET_NULL)
    abertura = models.DateTimeField(auto_now_add=True)
    fechamento = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=7, choices=OPCOES_STATUS, default='aberta')
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.slug_save()
        super(Comanda, self).save(*args, **kwargs)

    def slug_save(self):
        if not self.codigo:
            self.codigo = get_random_string(8)
            slug_is_wrong = True
            while slug_is_wrong:
                slug_is_wrong=False
                other_objs_with_slug = type(self).objects.filter(codigo=self.codigo)
                if len(other_objs_with_slug) > 0:
                    slug_is_wrong = True
                if slug_is_wrong:
                    self.codigo = get_random_string(8)

    def atualiza_total(self):
        itens = ItemPedido.objects.filter(comanda=self)
        novo_total = 0.00
        for item in itens:
            novo_total +=  float(item.preco)
        self.valor_total = novo_total
        self.save()

    def __str__(self):
        return f"Comanda {self.codigo}"


class Categoria(models.Model):
    nome = models.CharField(max_length=55)
    descricao = models.TextField(blank=True)
    ordem = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('ordem', 'nome')

    def __str__(self):
        return self.nome


class ItemCardapio(models.Model):
    item = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    ativo = models.BooleanField(default=True)
    necessita_preparo = models.BooleanField(default=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.item


class ItemPedido(models.Model):
    OPCOES_STATUS = (
            ('preparo', 'Em Preparo'),
            ('pronto', 'Pronto'),
            ('entregue', 'Entregue'),
    )
    item = models.ForeignKey(ItemCardapio, on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    comanda = models.ForeignKey(Comanda, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=OPCOES_STATUS, default="preparo")
    obs = models.TextField(blank=True)
    hr_pedido = models.DateTimeField(auto_now_add=True)
    hr_entregue = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('hr_pedido', 'item')

    def pedido_pronto(self):
        if self.status == "preparo":
            self.status = "pronto"
            self.save()

    def entregar_pedido(self):
        self.status = "entregue"
        self.hr_entregue = timezone.now()
        self.save()

    def __str__(self):
        return self.item.item
