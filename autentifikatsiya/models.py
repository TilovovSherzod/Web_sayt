"""
Autentifikatsiya ilova modellari
"""
from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):
    """Foydalanuvchi profili modeli"""
    foydalanuvchi = models.OneToOneField(User, on_delete=models.CASCADE,
                                         related_name='profil')  # Foydalanuvchiga bog'lanish
    telefon = models.CharField(max_length=20, blank=True, null=True)  # Telefon raqami
    manzil = models.TextField(blank=True, null=True)  # Manzil
    rasm = models.ImageField(upload_to='profillar/', blank=True, null=True)  # Profil rasmi

    def __str__(self):
        return self.foydalanuvchi.username

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

