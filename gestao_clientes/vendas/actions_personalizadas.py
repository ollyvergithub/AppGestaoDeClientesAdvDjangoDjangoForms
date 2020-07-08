from django.http import HttpResponseNotFound

def criando_actions_personalizadas_nfe_emitida(modeladmin, request, queryset):
    if request.user.has_perm('vendas.setar_nfe'):
        queryset.update(nfe_emitida=True)
    else:
        return HttpResponseNotFound('<h1>Sem permissao</h1>')
criando_actions_personalizadas_nfe_emitida.short_description = "Action Personalizada - Nfe Emitida"


def criando_actions_personalizadas_nfe_nao_emitida(modeladmin, request, queryset):
    queryset.update(nfe_emitida=False)
criando_actions_personalizadas_nfe_nao_emitida.short_description = "Action Personalizada - Nfe Não Emitida"