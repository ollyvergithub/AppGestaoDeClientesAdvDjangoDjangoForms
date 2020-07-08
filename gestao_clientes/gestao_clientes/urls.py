from django.contrib import admin
from django.urls import path, include
from clientes import urls as clientes_urls
from home import urls as home_urls
from produtos import urls as produtos_urls
from vendas import urls as vendas_urls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include(home_urls)),
    path('clientes/', include(clientes_urls)),
    path('produtos/', include(produtos_urls)),
    path('vendas/', include(vendas_urls)),
    path('login/', auth_views.login, name='login'),
    path('', include('django.contrib.auth.urls')),

    # Customização do admin
    #path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),

    # `allauth` needs this from django
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# instalando Debug Tool Bar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Personalizando cabeçalhos
admin.site.site_header = "Gestão de Clientes - Alterado em gestao_clientes - urls"
admin.site.index_title = "Gestão de Clientes Administração - Alterado em gestao_clientes - urls"
admin.site.site_title = "Seja bem vindo ao Gestão de Clientes - Alterado em gestao_clientes - urls"

