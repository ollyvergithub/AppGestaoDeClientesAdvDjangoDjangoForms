Gestão de Clientes
========

App Gestão de Clientes Avançado. Django e Django Forms

License: MIT

Versão: 1.0

### App utilizando os recursos avançados do Framework

* Class Based Views;
* Sistema de Templates;
* CustomTemplateTags;
* CustomFilters;
* Customização do Admin;
* Django ORM;
* Utilizando o sistema de permissoes do Django;
* Cookies e Sessões;
* Middlewares;
* Managers;
* Envio de emails simples, com HTML e em Massa;
* Login com redes sociais;
* Criação de APIs com Django;
* Tests;
* Configurando e utilizando Logs;

### Para desenvolver

I)  Clone o repositório.
```console
$ git clone https://github.com/ollyvergithub/AppGestaoDeClientesAdvDjangoDjangoForms.git
```

II)  Crie um Virtualenv com Python 3.6
```console
$ python -m venv venv
```

III.  Ative o Virtualenv.
```console
$ source venv/bin/activate
```

IV.  Instale as dependências.
```console
$ pip install -r requirements-dev.txt
```

V.  Configure a instância com o .env
```console
$ cp .env_sample .env
```

VI.  Rode as migrações
```console
$ python manage.py migrate
```

VII.  Execute os testes.
```console
$ python manage.py test
```