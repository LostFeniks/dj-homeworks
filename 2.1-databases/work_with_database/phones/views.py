from django.shortcuts import render, redirect, get_object_or_404
from .models import Phone


def index(request):
    # Перенаправление с главной страницы на каталог
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'

    # Получаем параметр сортировки из запроса
    sort = request.GET.get('sort')

    # Загружаем все телефоны
    phones = Phone.objects.all()

    # Применяем сортировку, если указано
    if sort == 'name':
        phones = phones.order_by('name')
    elif sort == 'min_price':
        phones = phones.order_by('price')
    elif sort == 'max_price':
        phones = phones.order_by('-price')

    context = {
        'phones': phones,
        'sort': sort,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'

    # Получаем конкретный телефон по slug или возвращаем 404
    phone = get_object_or_404(Phone, slug=slug)

    context = {
        'phone': phone
    }
    return render(request, template, context)

