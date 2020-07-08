from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout

# Based Class View
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views import View


class HomePageView(TemplateView):
    template_name = 'home3.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['minha_variavel'] = "Contexto injetado dentro da variável minha_variavel em home - views.py na class HomePageView(TemplateView):"
        return context


class MyView(View):
    def get(self, request, *args, **kwargs):
        response = render_to_response('home4.html')
        # setando Cookie
        response.set_cookie('cor', 'azul', max_age=10000)
        # lendo o Cookie
        meu_cookie = request.COOKIES.get('cor')
        print('Lendo o Cookie: ', meu_cookie)

        return response
        #return HttpResponse('Respondendo o método get em home - views.py na class MyView(View): ')
        # return render(request, 'home4.html')



# TODO: Refatorar para usar threads assim que possivel
def home(request):
    # Debugando em modo Hard
    # import pdb; pdb.set_trace()
    value1 = 10
    value2 = 20
    res = value1*value2
    return render(request, 'home.html', {'results': res})


# FIXME: Corrigir método
def my_logout(request):
    logout(request)
    return redirect('home')
