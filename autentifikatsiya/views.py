"""
Autentifikatsiya ilova ko'rinishlari
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

from .models import Profil
from asosiy.views import savat_olish


def royxatdan_otish(request):
    """Ro'yxatdan o'tish sahifasi"""
    if request.user.is_authenticated:
        return redirect('asosiy')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Parollarni tekshirish
        if password != password_confirm:
            messages.error(request, "Parollar mos kelmadi")
            return render(request, 'autentifikatsiya/royxatdan_otish.html')

        # Foydalanuvchi mavjudligini tekshirish
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud")
            return render(request, 'autentifikatsiya/royxatdan_otish.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro'yxatdan o'tgan")
            return render(request, 'autentifikatsiya/royxatdan_otish.html')

        # Foydalanuvchi yaratish
        user = User.objects.create_user(username=username, email=email, password=password)

        # Profil yaratish
        Profil.objects.create(foydalanuvchi=user)

        # Sessiya savatini foydalanuvchiga bog'lash
        sessiya_savat = savat_olish(request)
        if sessiya_savat.sessiya_id and not sessiya_savat.foydalanuvchi:
            sessiya_savat.foydalanuvchi = user
            sessiya_savat.sessiya_id = None
            sessiya_savat.save()

        # Foydalanuvchini tizimga kiritish
        login(request, user)
        messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
        return redirect('asosiy')

    return render(request, 'autentifikatsiya/royxatdan_otish.html')


def kirish(request):
    """Tizimga kirish sahifasi"""
    if request.user.is_authenticated:
        return redirect('asosiy')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Foydalanuvchini tekshirish
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Foydalanuvchini tizimga kiritish
            login(request, user)

            # Sessiya savatini foydalanuvchiga bog'lash
            sessiya_savat = savat_olish(request)
            if sessiya_savat.sessiya_id and not sessiya_savat.foydalanuvchi:
                # Foydalanuvchining mavjud savatini tekshirish
                foydalanuvchi_savat = None
                try:
                    foydalanuvchi_savat = user.savat_set.get(foydalanuvchi=user)
                except:
                    pass

                if foydalanuvchi_savat:
                    # Sessiya savatidagi maxsulotlarni foydalanuvchi savatiga ko'chirish
                    for savat_maxsulot in sessiya_savat.savatlar.all():
                        savat_maxsulot.savat = foydalanuvchi_savat
                        savat_maxsulot.save()
                    sessiya_savat.delete()
                else:
                    # Sessiya savatini foydalanuvchiga bog'lash
                    sessiya_savat.foydalanuvchi = user
                    sessiya_savat.sessiya_id = None
                    sessiya_savat.save()

            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect('asosiy')
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri")

    return render(request, 'autentifikatsiya/kirish.html')


def chiqish(request):
    """Tizimdan chiqish"""
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz!")
    return redirect('asosiy')


@login_required
def profil(request):
    """Foydalanuvchi profili sahifasi"""
    user = request.user

    # Profil mavjud emasligini tekshirish va yaratish
    try:
        profil = user.profil
    except:
        profil = Profil.objects.create(foydalanuvchi=user)

    if request.method == 'POST':
        # Profil ma'lumotlarini yangilash
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        profil.telefon = request.POST.get('telefon', '')
        profil.manzil = request.POST.get('manzil', '')

        # Profil rasmini yangilash
        if 'rasm' in request.FILES:
            profil.rasm = request.FILES['rasm']

        profil.save()

        messages.success(request, "Profil muvaffaqiyatli yangilandi!")
        return redirect('profil')

    return render(request, 'autentifikatsiya/profil.html', {
        'user': user,
        'profil': profil,
    })


# JWT API uchun ko'rinishlar
def token_olish(request):
    """Admin uchun JWT token olish"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            refresh = RefreshToken.for_user(user)

            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return JsonResponse({'error': 'Noto\'g\'ri ma\'lumotlar yoki huquqlar yetarli emas'}, status=401)

    return render(request, 'autentifikatsiya/token_olish.html')

