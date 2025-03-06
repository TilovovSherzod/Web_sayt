"""
Asosiy ilova modellari
"""
from django.db import models
from django.contrib.auth.models import User


class Kategoriya(models.Model):
    """Maxsulot kategoriyasi modeli"""
    nomi = models.CharField(max_length=100)  # Kategoriya nomi
    rasm = models.ImageField(upload_to='kategoriyalar/', null=True, blank=True)  # Kategoriya rasmi
    yaratilgan_sana = models.DateTimeField(auto_now_add=True)  # Yaratilgan sana

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Maxsulot(models.Model):
    """Maxsulot modeli"""
    nomi = models.CharField(max_length=200)  # Maxsulot nomi
    tavsif = models.TextField()  # Maxsulot tavsifi
    narx = models.DecimalField(max_digits=10, decimal_places=2)  # Maxsulot narxi
    chegirma_narx = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Chegirma narxi
    rasm = models.ImageField(upload_to='maxsulotlar/')  # Maxsulot rasmi
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE,
                                   related_name='maxsulotlar')  # Kategoriyaga bog'lanish
    mavjud = models.BooleanField(default=True)  # Maxsulot mavjudligi
    yaratilgan_sana = models.DateTimeField(auto_now_add=True)  # Yaratilgan sana

    def __str__(self):
        return self.nomi

    class Meta:
        verbose_name = "Maxsulot"
        verbose_name_plural = "Maxsulotlar"


class Savat(models.Model):
    """Foydalanuvchi savati modeli"""
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                      blank=True)  # Foydalanuvchiga bog'lanish
    sessiya_id = models.CharField(max_length=100, null=True,
                                  blank=True)  # Sessiya ID (ro'yxatdan o'tmagan foydalanuvchilar uchun)
    yaratilgan_sana = models.DateTimeField(auto_now_add=True)  # Yaratilgan sana

    def __str__(self):
        return f"Savat #{self.id}"

    class Meta:
        verbose_name = "Savat"
        verbose_name_plural = "Savatlar"

    @property
    def jami_narx(self):
        """Savatdagi barcha maxsulotlarning umumiy narxini hisoblash"""
        return sum(item.jami_narx for item in self.savatlar.all())

    @property
    def maxsulotlar_soni(self):
        """Savatdagi maxsulotlar sonini hisoblash"""
        return sum(item.miqdor for item in self.savatlar.all())


class SavatMaxsulot(models.Model):
    """Savatdagi maxsulot modeli"""
    savat = models.ForeignKey(Savat, on_delete=models.CASCADE, related_name='savatlar')  # Savatga bog'lanish
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)  # Maxsulotga bog'lanish
    miqdor = models.PositiveIntegerField(default=1)  # Maxsulot miqdori

    def __str__(self):
        return f"{self.maxsulot.nomi} ({self.miqdor})"

    class Meta:
        verbose_name = "Savat maxsuloti"
        verbose_name_plural = "Savat maxsulotlari"

    @property
    def jami_narx(self):
        """Maxsulot narxini miqdorga ko'paytirish"""
        if self.maxsulot.chegirma_narx:
            return self.maxsulot.chegirma_narx * self.miqdor
        return self.maxsulot.narx * self.miqdor


class Buyurtma(models.Model):
    """Buyurtma modeli"""
    HOLAT_TANLOVLARI = (
        ('kutilmoqda', 'Kutilmoqda'),
        ('tasdiqlangan', 'Tasdiqlangan'),
        ('yuborilgan', 'Yuborilgan'),
        ('yetkazilgan', 'Yetkazilgan'),
        ('bekor_qilingan', 'Bekor qilingan'),
    )

    TOLOV_USULI_TANLOVLARI = (
        ('naqd', 'Naqd pul'),
        ('karta', 'Karta orqali'),
    )

    foydalanuvchi = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                      blank=True)  # Foydalanuvchiga bog'lanish
    ism = models.CharField(max_length=100)  # Buyurtmachi ismi
    familiya = models.CharField(max_length=100)  # Buyurtmachi familiyasi
    telefon = models.CharField(max_length=20)  # Telefon raqami
    manzil = models.TextField()  # Yetkazib berish manzili
    tolov_usuli = models.CharField(max_length=20, choices=TOLOV_USULI_TANLOVLARI, default='naqd')  # To'lov usuli
    holat = models.CharField(max_length=20, choices=HOLAT_TANLOVLARI, default='kutilmoqda')  # Buyurtma holati
    jami_narx = models.DecimalField(max_digits=10, decimal_places=2)  # Buyurtma umumiy narxi
    yaratilgan_sana = models.DateTimeField(auto_now_add=True)  # Yaratilgan sana
    yangilangan_sana = models.DateTimeField(auto_now=True)  # Yangilangan sana

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.ism} {self.familiya}"

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"


class BuyurtmaMaxsulot(models.Model):
    """Buyurtmadagi maxsulot modeli"""
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE,
                                 related_name='buyurtma_maxsulotlari')  # Buyurtmaga bog'lanish
    maxsulot = models.ForeignKey(Maxsulot, on_delete=models.CASCADE)  # Maxsulotga bog'lanish
    miqdor = models.PositiveIntegerField(default=1)  # Maxsulot miqdori
    narx = models.DecimalField(max_digits=10, decimal_places=2)  # Sotib olingan narx

    def __str__(self):
        return f"{self.maxsulot.nomi} ({self.miqdor})"

    class Meta:
        verbose_name = "Buyurtma maxsuloti"
        verbose_name_plural = "Buyurtma maxsulotlari"

    @property
    def jami_narx(self):
        """Maxsulot narxini miqdorga ko'paytirish"""
        return self.narx * self.miqdor

