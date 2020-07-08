from django.db import models
from django.db.models import Sum, F, FloatField, Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from clientes.models import Person
from produtos.models import Produto
from .managers import VendaManager


class Venda(models.Model):
    # Model Choice
    ABERTA = "AB"
    FECHADA = "FC"
    PROCESSANDO = "PC"
    DESCONHECIDO = "DC"

    STATUS = (
        (ABERTA, "Aberta"),
        (FECHADA, "Fechada"),
        (PROCESSANDO, "Processando"),
        (DESCONHECIDO, "Desconhecido"),
    )
    status = models.CharField(choices=STATUS, default=DESCONHECIDO, null=True, max_length=2)
    numero = models.CharField(max_length=7)
    valor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    impostos = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pessoa = models.ForeignKey(Person, null=True, blank=True, on_delete=models.PROTECT)
    nfe_emitida = models.BooleanField(default=False)

    objects = VendaManager()

    class Meta:
        permissions = (
            ('setar_nfe', 'Usuário pode alterar parametro nfe'),
            ('ver_dashboard', 'Pode visualizar o dashboard'),
            ('permissao3', 'Permissao 3'),
        )

    def get_raw_vendas(self):
        return Venda.objects.raw('select * from vendas_venda where id= %s', [18])

    def calcular_total(self):
        total = self.itemdopedido_set.all().aggregate(
            tot_pedido=Sum((F('quantidade') * F('produto__preco')) - F('desconto'), output_field=FloatField())
        )['tot_pedido'] or 0

        total = total - float(self.impostos) - float(self.desconto)

        self.valor = total
        Venda.objects.filter(id=self.id).update(valor=total)
        return self.valor

    def __str__(self):
        return self.numero


class ItemDoPedido(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens dos Pedidos"
        unique_together = (
            ("venda", "produto"),
        )

    def __str__(self):
        return f"{self.venda.numero} - {self.produto.descricao} ({self.quantidade})"


@receiver(post_save, sender=Venda)
def update_vendas_total(sender, instance: Venda, **kwargs):
    instance.calcular_total()