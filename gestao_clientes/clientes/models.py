from django.core.mail import send_mail, mail_admins, send_mass_mail
# Para envio de emails com html
from django.template.loader import render_to_string
from django.db import models
from decouple import config


class Documento(models.Model):
    num_doc = models.CharField(max_length=50)

    def __str__(self):
        return self.num_doc


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=5, decimal_places=2)
    bio = models.TextField()
    photo = models.ImageField(upload_to='clients_photos', null=True, blank=True)
    doc = models.OneToOneField(Documento, null=True, blank=True, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        permissions = (
            ('deletar_clientes', 'Deletar Clientes'),
        )
        unique_together = (("first_name", "telefone"), )


    @property
    def nome_completo(self):
        return self.first_name + " " + self.last_name

    # Enviando email assim que salvar
    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)

        # data = {'cliente': self.first_name}
        # plain_text = render_to_string('clientes/emails/novo_cliente.txt', data)
        # html_email = render_to_string('clientes/emails/novo_cliente.html', data)
        #
        # # Email Simples
        # # send_mail(
        # #     'Enviando email pelo Django - Novo Cliente',
        # #     'O cliente %s foi cadastrado com sucesso ' % self.first_name,
        # #     config('EMAIL_HOST_USER'),
        # #     ['o.ollyver@yahoo.com.br'],
        # #     fail_silently=False,
        # # )
        #
        # # Email Com HTML
        # send_mail(
        #     'Enviando email pelo Django - Novo Cliente Cadastrado',
        #     plain_text,
        #     config('EMAIL_HOST_USER'),
        #     ['o.ollyver@yahoo.com.br'],
        #     html_message=html_email,
        #     fail_silently=False,
        # )
        #
        # # Enviando email para os Admim que estão caqdastrados em settings na const ADMIN
        # mail_admins(
        #     'Enviando email pelo Django Para os Admins - Novo Cliente Cadastrado',
        #     plain_text,
        #     html_message=html_email,
        # )
        #
        # # Enviando emails em massa
        # message1 = ('01 - Envio de Emails em Massa Pelo Django', 'MENSAGEM 01 - Envio de Emails em Massa Pelo Django', config('EMAIL_HOST_USER'), [config('EMAIL_HOST_USER'), 'o.ollyver@yahoo.com.br'])
        # message2 = ('02 - Envio de Emails em Massa Pelo Django', 'MENSAGEM 02 - Envio de Emails em Massa Pelo Django', config('EMAIL_HOST_USER'), ['ollyver.ottoboni@amcom.com.br'])
        # send_mass_mail((message1, message2), fail_silently=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name





