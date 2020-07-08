from django.test import TestCase
from vendas.models import Venda, ItemDoPedido
from produtos.models import Produto


class VendaTestCase(TestCase):
    def setUp(self):
        self.venda = Venda.objects.create(numero=555, desconto=10, status="AB")
        self.produto = Produto.objects.create(descricao='Produto criaco com test', preco=10)

    def test_verifica_num_vendas(self):
        assert Venda.objects.all().count() == 1

    def test_valor_venda(self):
        """ Verifica valor total da venda """
        ItemDoPedido.objects.create(
            venda= self.venda,
            produto=self.produto,
            quantidade=10,
            desconto=8
        )
        assert self.venda.valor >= 1

    def test_item_incluido_lista_itens(self):
        item = ItemDoPedido.objects.create(
            venda=self.venda,
            produto=self.produto,
            quantidade=1,
            desconto=0
        )
        self.assertIn(item, self.venda.itemdopedido_set.all())

    def test_nota_fiscal_emitida(self):
        self.assertFalse(self.venda.nfe_emitida)

    def test_checa_status(self):
        self.venda.status = 'PC'
        self.venda.save()
        self.assertEqual(self.venda.status, 'AB')


