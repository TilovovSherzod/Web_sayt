"""
Kontekst protsessorlari
"""
from .models import Kategoriya

def kategoriyalar(request):
    """Barcha sahifalarda kategoriyalarni ko'rsatish uchun kontekst protsessor"""
    return {
        'barcha_kategoriyalar': Kategoriya.objects.all()
    }

