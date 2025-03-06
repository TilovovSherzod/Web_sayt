"""
Autentifikatsiya ilova URL konfiguratsiyasi
"""
from django.urls import path
from . import views

urlpatterns = [
    path('royxatdan-otish/', views.royxatdan_otish, name='royxatdan_otish'),
    path('kirish/', views.kirish, name='kirish'),
    path('chiqish/', views.chiqish, name='chiqish'),
    path('profil/', views.profil, name='profil'),
    path('token/', views.token_olish, name='token_olish'),
]

