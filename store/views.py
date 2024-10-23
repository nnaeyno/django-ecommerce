from django.shortcuts import render, get_object_or_404

from store.models import Category, Product


def main(request):
    return render(request, 'index.html')


def category(request, slug):
    if slug:
        selected_category = get_object_or_404(Category, slug=slug)
        subcategories = selected_category.get_children()
        products = Product.objects.filter(categories=selected_category)
    else:
        selected_category = None
        subcategories = Category.objects.filter(parent__isnull=True)
        products = Product.objects.all()

    context = {
        'category': selected_category,
        'subcategories': subcategories,
        'products': products,
    }

    return render(request, 'shop.html', context)


def product(request, slug):
    return render(request, 'shop-detail.html')


def contact(request):
    return render(request, 'contact.html')


def error(request):
    return render(request, '404.html')


def testimonial(request):
    return render(request, 'testimonial.html')