from django.urls import path
from .views import persons_list
from .views import persons_new
from .views import persons_update
from .views import persons_delete
from .views import api

# Based Class View
from .views import PersonList, PersonDetail, PersonCreate, PersonUpdate, PersonDelete, ProdutoBulk, ApiCbv

urlpatterns = [
    path('list/', persons_list, name="person_list"),
    path('new/', persons_new, name="person_new"),
    path('update/<int:id>/', persons_update, name="persons_update"),
    path('delete/<int:id>/', persons_delete, name="persons_delete"),
    path('person_list/', PersonList.as_view(), name='person_list_cbv'),
    path('person_detail/<int:pk>/', PersonDetail.as_view(), name='person_deitail'),
    path('person_create/', PersonCreate.as_view(), name="person_create"),
    path('person_update/<int:pk>/', PersonUpdate.as_view(), name='person_update'),
    path('person_delete/<int:pk>/', PersonDelete.as_view(), name='person_delete'),
    path('person_bulk/', ProdutoBulk.as_view(), name="person_bulk"),
    path('api/', api, name="api_fbv"),
    path('api_cbv/', ApiCbv.as_view(), name='api_cbv'),
]