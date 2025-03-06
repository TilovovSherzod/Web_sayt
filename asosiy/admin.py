"""
Admin panel konfiguratsiyasi
"""
from django.contrib import admin
from .models import Kategoriya, Maxsulot, Savat, SavatMaxsulot, Buyurtma, BuyurtmaMaxsulot


@admin.register(Kategoriya)
class KategoriyaAdmin(admin.ModelAdmin):
    """Kategoriya admin konfiguratsiyasi"""
    list_display = ('nomi', 'yaratilgan_sana')
    search_fields = ('nomi',)


class SavatMaxsulotInline(admin.TabularInline):
    """Savat maxsulotlarini ko'rsatish uchun inline"""
    model = SavatMaxsulot
    extra = 0


@admin.register(Savat)
class SavatAdmin(admin.ModelAdmin):
    """Savat admin konfiguratsiyasi"""
    list_display = ('id', 'foydalanuvchi', 'yaratilgan_sana', 'jami_narx', 'maxsulotlar_soni')
    inlines = [SavatMaxsulotInline]


@admin.register(Maxsulot)
class MaxsulotAdmin(admin.ModelAdmin):
    """Maxsulot admin konfiguratsiyasi"""
    list_display = ('nomi', 'kategoriya', 'narx', 'chegirma_narx', 'mavjud', 'yaratilgan_sana')
    list_filter = ('kategoriya', 'mavjud')
    search_fields = ('nomi', 'tavsif')


class BuyurtmaMaxsulotInline(admin.TabularInline):
    """Buyurtma maxsulotlarini ko'rsatish uchun inline"""
    model = BuyurtmaMaxsulot
    extra = 0
    readonly_fields = ('maxsulot', 'miqdor', 'narx')


@admin.register(Buyurtma)
class BuyurtmaAdmin(admin.ModelAdmin):
    """Buyurtma admin konfiguratsiyasi"""
    list_display = ('id', 'ism', 'familiya', 'telefon', 'holat', 'tolov_usuli', 'jami_narx', 'yaratilgan_sana')
    list_filter = ('holat', 'tolov_usuli')
    search_fields = ('ism', 'familiya', 'telefon')
    readonly_fields = ('jami_narx',)
    inlines = [BuyurtmaMaxsulotInline]

    def get_readonly_fields(self, request, obj=None):
        """Tahrirlash mumkin bo'lmagan maydonlarni belgilash"""
        if obj:  # Agar buyurtma mavjud bo'lsa
            return self.readonly_fields + ('foydalanuvchi', 'ism', 'familiya', 'telefon', 'manzil', 'tolov_usuli')
        return self.readonly_fields

