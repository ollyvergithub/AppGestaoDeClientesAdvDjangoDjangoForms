from django.contrib import admin
from django.utils.html import format_html
from .models import Person, Documento

class ListandoClientes(admin.ModelAdmin):
    # Monta a ordem de exibição dos campos
    # fields = ['doc', ('first_name', 'last_name'), ('age', 'salary'), 'bio', 'photo']
    fieldsets = (
        ('Dados Pessoais', {
            'fields': (('first_name', 'last_name'), 'telefone', 'age', 'bio')
        }),

        ('Dados Complementares', {
            'classes': ('collapse',),
            'fields': ('doc', 'salary', 'photo')
        }),
    )
    list_display = ('id', 'first_name', 'last_name', 'telefone', 'age', 'salary', 'doc', 'thumbnail')
    list_display_links = ('id', 'first_name',)

    # Filtros
    list_filter = ('age', 'salary',)
    search_fields = ('first_name', 'age',)

    list_editable = ('age', 'salary',)
    list_per_page = 10
    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px"/>'.format(obj.photo.url))

    thumbnail.short_description = "Foto do Cliente"


admin.site.register(Person, ListandoClientes)
admin.site.register(Documento)

