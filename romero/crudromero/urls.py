from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('', views.inicio, name='inicio'),
    path('getuserdata/', views.get_data, name='api-get'),
    path('ver-todo/<str:text>', views.ver_todo, name='ver_todo'),
    path('ver/<str:id>', views.vista, name='vista'),
]
