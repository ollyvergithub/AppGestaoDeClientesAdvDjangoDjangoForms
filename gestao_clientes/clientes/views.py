from django.forms import model_to_dict
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Person
from produtos.models import Produto
from vendas.models import Venda
from .forms import PersonForm

# Based Class View
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy


# LoginRequiredMixin - é um mixin e serve para substituir @login_required
class PersonList(LoginRequiredMixin, ListView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Setando Sessions
        primeiro_acesso = self.request.session.get('primeiro_acesso', False)
        if not primeiro_acesso:
            context['message'] = 'Seja bem vindo ao seu primeiro acesso hoje'
            self.request.session['primeiro_acesso'] = True
        else:
            context['message'] = 'Você já acessou hoje hoje'

        return context

    def get_queryset(self):
        # Realizando a busca de clientes
        termo_de_busca = self.request.GET.get('pesquisa', None)

        if (termo_de_busca):
            persons = Person.objects.all()
            new_context = persons.filter(first_name__icontains=termo_de_busca) | persons.filter(last_name__icontains=termo_de_busca)
        else:
            order = self.request.GET.get('orderby', 'first_name')
            new_context = Person.objects.order_by(order)

        return new_context


class PersonDetail(LoginRequiredMixin, DetailView):
    model = Person
    # Injetando contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class PersonCreate(LoginRequiredMixin, CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']
    # success_url = '/clientes/person_list'
    success_url = reverse_lazy('person_list_cbv')


class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = Person
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']
    # success_url = '/clientes/person_list'
    success_url = reverse_lazy('person_list_cbv')

    # def get_success_url(self):
    #     success_url = reverse_lazy('person_list_cbv')


class PersonDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('clientes.deletar_clientes',)
    model = Person

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return HttpResponse("Sem permissao")
        return super().dispatch(request, *args, **kwargs)

    success_url = reverse_lazy('person_list_cbv')


class ProdutoBulk(LoginRequiredMixin, View):
    def get(self, request):
        produtos = ['Banana - Bulk', 'Maçã - Bulk', 'Laranja - Bulk', 'Pera - Bulk', 'Melancia - Bulk']
        lista_produtos = []

        for produto in produtos:
            p = Produto(descricao=produto, preco=10)
            lista_produtos.append(p)

        Produto.objects.bulk_create(lista_produtos)

        return HttpResponse('Funcionou')


def api(request):
    a = {'nome':'Ollyver', 'idade': 48, 'salario': 12000.00}
    mensagem = {'mensagem': "Erro Xpto"}
    lista = [1, 2, 3]

    produto = Produto.objects.last()
    #b = {'nome': produto.descricao, 'preco': produto.preco }
    b = model_to_dict(produto)

    l= []
    l.append({'endereco': 'Veio de clientes/views/def api'})
    produtos = Produto.objects.all()

    for produto in produtos:
        l.append(model_to_dict(produto))

    return JsonResponse(l, status=200, safe=False)


class ApiCbv(View):
    def get(self, request):
        data = {'nome': 'Ollyver', 'idade': 48, 'salario': 12000.58}
        produto = Produto.objects.last()
        b = model_to_dict(produto)

        l = []
        l.append({'endereco': 'Veio de clientes/views/class ApiCbv(View):'})
        produtos = Produto.objects.all()

        for produto in produtos:
            l.append(model_to_dict(produto))

        return JsonResponse(l, status=200, safe=False)

    def post(self):
        pass


@login_required
def persons_list(request):
    persons = Person.objects.all()
    return render(request, 'person.html', {'persons': persons})


@login_required
def persons_new(request):
    form = PersonForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):
    1/0
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})