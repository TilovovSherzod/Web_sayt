"""
Asosiy ilova URL konfiguratsiyasi
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.asosiy, name='asosiy'),
    path('maxsulot/<int:maxsulot_id>/', views.maxsulot_tafsilotlari, name='maxsulot_tafsilotlari'),
    path('savat/', views.savat, name='savat'),
    path('savatga-qoshish/', views.savatga_qoshish, name='savatga_qoshish'),
    path('savat-yangilash/', views.savat_yangilash, name='savat_yangilash'),
    path('savat-tozalash/', views.savat_tozalash, name='savat_tozalash'),
    path('buyurtma-yaratish/', views.buyurtma_yaratish, name='buyurtma_yaratish'),
    path('buyurtma-tasdiqlandi/<int:buyurtma_id>/', views.buyurtma_tasdiqlandi, name='buyurtma_tasdiqlandi'),
    path('buyurtmalarim/', views.buyurtmalarim, name='buyurtmalarim'),
]

