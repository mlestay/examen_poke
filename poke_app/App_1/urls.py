from django.urls import path
from App_1 import views

urlpatterns = [
    path('', views.index),
    path('/index', views.registro),
    path('App_1/pokes', views.registro),
    path('index', views.login),
    path('pokes',views.perfil),
    path('pokes', views.me_gusta),
    path('index', views.me_gusta),
    path('pokes', views.add_poke),
    path('pokes', views.lista_usuarios),
    path('loggout', views.logout),

]
