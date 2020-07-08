from django.contrib import admin
from .models import Venda, ItemDoPedido

# Criando Actions Personalizadas para o form admim do Django
from .actions_personalizadas import criando_actions_personalizadas_nfe_emitida, criando_actions_personalizadas_nfe_nao_emitida


class ItemPedidoInline(admin.TabularInline):
    model = ItemDoPedido
    extra = 1

# class ItemPedidoInline(admin.StackedInline):
#     model = ItemDoPedido
#     extra = 1


class VendaAdmin(admin.ModelAdmin):
    list_filter = ('pessoa__doc', )
    list_display = ('id', 'pessoa', 'nfe_emitida', 'desconto', 'get_total')
    fields = ['numero', 'desconto', 'impostos', 'pessoa', 'nfe_emitida', 'status', 'valor',]
    #raw_id_fields = ('pessoa',)
    autocomplete_fields = ('pessoa',)
    readonly_fields = ('valor', )
    #filter_vertical = ['produtos']
    #filter_horizontal = ['produtos']
    search_fields = ('id', 'pessoa__first_name', 'pessoa__doc__num_doc')
    inlines = [ItemPedidoInline]

    def get_total(self, obj):
        if obj.valor:
            return obj.calcular_total()

    get_total.short_description = 'Valor total'

    # def get_total(self, obj: Venda):
    #     return obj.get_total()
    # get_total.short_description = 'Valor total'

    # Passando as actions personalizadas criadas
    actions = [
        criando_actions_personalizadas_nfe_emitida,
        criando_actions_personalizadas_nfe_nao_emitida,
    ]


admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemDoPedido)