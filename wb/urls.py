from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('nova_empresa', views.nova_empresa, name='nova_empresa'),
    path('questionario', views.questionario, name='questionario'),
    path('respostas', views.respostas, name='respostas'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('loginview', views.loginview, name='loginview'),
    path('sair', views.sair, name='sair'),
    path('esqueceuasenha', views.esqueceuasenha, name='esqueceuasenha'),
    path('boaspraticas', views.boaspraticas, name='boaspraticas'),
    path('boaspraticasdetalhada/<int:pk>/', views.boaspraticasdetalhada, name='boaspraticasdetalhada'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)