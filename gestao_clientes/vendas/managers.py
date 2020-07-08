from django.db import models
from django.db.models import Sum, F, FloatField, Min, Max, Avg, Count

class VendaManager(models.Manager):
    def media(self):
        return self.all().aggregate(Avg('valor'))['valor__avg']

    def media_desc(self):
        return self.all().aggregate(Avg('desconto'))['desconto__avg']

    def pedido_menor_valor(self):
        return self.all().aggregate(Min('valor'))['valor__min']

    def pedido_maior_valor(self):
        return self.all().aggregate(Max('valor'))['valor__max']

    def quantidade_de_pedidos(self):
        return self.all().aggregate(Count('id'))['id__count']

    def quantidade_de_pedidos_com_nfe(self):
        return self.filter(nfe_emitida=True).aggregate(Count('id'))['id__count']