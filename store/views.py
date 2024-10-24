from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from store.models import Category, Product


def main(request):
    return render(request, 'index.html')


def category(request, slug=None):
    if slug:
        selected_category = get_object_or_404(Category, slug=slug)
        subcategories = selected_category.get_children()
        products = Product.objects.filter(categories=selected_category)
    else:
        selected_category = None
        subcategories = Category.objects.filter(parent__isnull=True)
        products = Product.objects.all()

    context = search(request, products, selected_category, subcategories)
    return render(request, 'shop.html', context)


def search(request, products, selected_category, subcategories):
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query)  # | Q(description__icontains=query)
        )

    context = {
        'category': selected_category,
        'subcategories': subcategories,
        'products': products,
        'query': query,
    }
    return context


def product(request, slug):
    return render(request, 'shop-detail.html')


def contact(request):
    return render(request, 'contact.html')


def error(request):
    return render(request, '404.html')


def testimonial(request):
    return render(request, 'testimonial.html')
