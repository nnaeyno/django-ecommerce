from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from order.models import Cart, Entry
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from store.models import Product


# Create your views here.
def cart(request):
    return render(request, 'cart.html')


def checkout(request):
    return render(request, 'checkout.html')


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to cart with quantity validation
    """
    product = get_object_or_404(Product, product_id=product_id)

    if product.quantity <= 0:
        messages.error(request, f'Sorry, "{product.name}" is out of stock.')
        return redirect(request.META.get('HTTP_REFERER', reverse('shop')))

    cart, created = Cart.objects.get_or_create(user=request.user)

    entry, created = Entry.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 0}
    )

    if product.quantity < (entry.quantity + 1):
        messages.error(request, f'Sorry, only {product.quantity} items of "{product.name}" available.')
        return redirect(request.META.get('HTTP_REFERER', reverse('category')))

    entry.quantity += 1
    entry.save()

    cart.count = Entry.objects.filter(cart=cart).count()
    cart.total = sum(entry.product.price * entry.quantity
                     for entry in Entry.objects.filter(cart=cart))
    cart.save()

    messages.success(request, f'Added "{product.name}" to your cart.')
    return redirect(request.META.get('HTTP_REFERER', reverse('category')))
