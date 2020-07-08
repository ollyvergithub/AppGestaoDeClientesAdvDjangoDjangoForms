from django.urls import path
from .views import home, my_logout, HomePageView, MyView
# Class Based Views
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', home, name="home"),
    path('logout/', my_logout, name="logout"),
    path('home2/', TemplateView.as_view(template_name='home2.html'), name="home2"),
    path('home3/', HomePageView.as_view(template_name='home3.html')),
    path('view/', MyView.as_view()),
]