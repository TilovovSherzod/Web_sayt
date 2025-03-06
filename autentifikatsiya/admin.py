"""
Admin panel konfiguratsiyasi
"""
from django.contrib import admin
from .models import Profil

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    """Profil admin konfiguratsiyasi"""
    list_display = ('foydalanuvchi', 'telefon')
    search_fields = ('foydalanuvchi__username', 'foydalanuvchi__email', 'telefon')

