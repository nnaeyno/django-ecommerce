from django.shortcuts import render


def main(request):
    return render(request, 'index.html')


def category(request, slug):
    return render(request, 'shop.html')


def product(request, slug):
    return render(request, 'shop-detail.html')


def contact(request):
    return render(request, 'contact.html')


def error(request):
    return render(request, '404.html')


def testimonial(request):
    return render(request, 'testimonial.html')