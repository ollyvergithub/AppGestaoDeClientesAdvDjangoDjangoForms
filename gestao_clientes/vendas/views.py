import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Venda, ItemDoPedido
from .forms import ItemPedidoForm, ItemDoPedidoModelForm
import logging

logger = logging.getLogger('django')


class DashboardView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('vendas.ver_dashboard'):
            return HttpResponse("Sem permissão")

        # Se tiver permissão, segue o fluxo normal
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        # Utilizando as managers criadas em managers.py
        data = {}
        data['media'] = Venda.objects.media()
        data['media_desc'] = Venda.objects.media_desc()
        data['media_desc'] = round(float(data['media_desc']), 2)
        data['min'] = Venda.objects.pedido_menor_valor()
        data['max'] = Venda.objects.pedido_maior_valor()
        data['n_ped'] = Venda.objects.quantidade_de_pedidos()
        data['n_ped_nfe'] = Venda.objects.quantidade_de_pedidos_com_nfe()
        return render(request, 'vendas/dashboard.html', data)


class ListaVendas(View):
    def get(self, request):
        # Trabalhando com logs, que está setado em settings.py
        logger.debug("Acessaram a listagem de vendas")
        try:
            1/0
        except Exception as e:
            time = datetime.datetime.now()
            # logger.error(str(e))
            logger.exception("Log de exception: " + time.strftime("%Y-%m-%d %H:%M:%S") + " - " + str(request.user))
            logger.error("Log de error: " + time.strftime("%Y-%m-%d %H:%M:%S") + " - " + str(request.user))

        vendas = Venda.objects.all()
        count_vendas = vendas.count()

        # implementando get_raw_vendas que está em models
        v = Venda.objects.last()
        raw_vendas = v.get_raw_vendas()

        return render(request, 'vendas/lista-vendas.html', {'vendas': vendas, 'count_vendas': count_vendas, 'raw_vendas': raw_vendas})


class NovoPedido(View):

    def get(self, request):
        return render(request, 'vendas/novo-pedido.html')

    def post(self, request):
        data = {}

        data['form_item'] = ItemPedidoForm()
        data['numero'] = request.POST['numero']
        data['desconto'] = float(request.POST['desconto'].replace(',', '.'))
        data['venda_id'] = request.POST['venda_id']

        if data['venda_id']:
            venda = Venda.objects.get(id=data['venda_id'])
            venda.desconto = data['desconto']
            venda.numero = data['numero']
            venda.save()
        else:
            venda = Venda.objects.create(
                numero=data['numero'],
                desconto=data['desconto']
            )

        itens = venda.itemdopedido_set.all()
        data['venda'] = venda
        data['itens'] = itens

        return render(request, 'vendas/novo-pedido.html', data)


class NovoItemPedido(View):

    def get(self, request, pk):
        pass

    def post(self, request, venda):
        data = {}

        item = ItemDoPedido.objects.create(
            produto_id=request.POST['produto_id'], quantidade=request.POST['quantidade'],
            desconto=request.POST['desconto'], venda_id=venda
        )

        data['item'] = item
        data['form_item'] = ItemPedidoForm()
        data['numero'] = item.venda.numero
        data['desconto'] = item.venda.desconto
        data['venda'] = item.venda
        data['itens'] = item.venda.itemdopedido_set.all()

        return render(
            request, 'vendas/novo-pedido.html', data
        )


class EditPedido(View):
    def get(self, request, venda):
        data = {}
        venda = Venda.objects.get(id=venda)
        data['form_item'] = ItemPedidoForm()
        data['numero'] = venda.numero
        data['desconto'] = float(venda.desconto)
        data['venda'] = venda
        data['itens'] = venda.itemdopedido_set.all()

        return render(
            request, 'vendas/novo-pedido.html', data
        )


class DeletePedido(View):
    def get(self, request, venda):
        venda = Venda.objects.get(id=venda)
        return render(request, 'vendas/delete-pedido-confirm.html', {'venda': venda})

    def post(self, request, venda):
        venda = Venda.objects.get(id=venda)
        venda.delete()
        return redirect('lista-vendas')


class DeleteItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        return render(request, 'vendas/delete-itempedido-confirm.html', {'item_pedido': item_pedido})

    def post(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        venda_id = item_pedido.venda_id
        item_pedido.delete()
        return redirect('edit-pedido', venda=venda_id)


class EditItemPedido(View):
    def get(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        form = ItemDoPedidoModelForm(instance=item_pedido)
        return render(request, 'vendas/edit-itempedido.html', {'item_pedido': item_pedido, 'form': form})

    def post(self, request, item):
        item_pedido = ItemDoPedido.objects.get(id=item)
        item_pedido.desconto = request.POST['desconto']
        item_pedido.quantidade = request.POST['quantidade']

        item_pedido.save()

        venda_id = item_pedido.venda_id
        return redirect('edit-pedido', venda=venda_id)



