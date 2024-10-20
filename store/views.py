from django.shortcuts import render


def main(request):
    return render(request, 'index.html')


def category(request):
    return render(request, 'shop.html')


def product(request):
    return render(request, 'shop-detail.html')


def contact(request):
    return render(request, 'contact.html')