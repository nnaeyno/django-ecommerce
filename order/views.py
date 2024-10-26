from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from order.models import Cart, Entry
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from store.models import Product

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse


# Create your views here.
def cart(request):
    return render(request, 'cart.html')


def checkout(request):
    return render(request, 'checkout.html')


class AddToCartView(LoginRequiredMixin, View):
    """
    Class-based view to add a product to cart with quantity validation
    """

    def get_error_url(self):
        return self.request.META.get('HTTP_REFERER', reverse('error'))

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse('category'))

    def get(self, request, *args, **kwargs):
        return redirect('category')

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, product_id=product_id)

        # Check if product is in stock
        if product.quantity <= 0:
            messages.error(request, f'Sorry, "{product.name}" is out of stock.')
            return redirect(self.get_error_url())

        # Get or create cart for user
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get or create cart entry
        entry, created = Entry.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0}
        )

        # Validate available quantity
        if product.quantity < (entry.quantity + 1):
            messages.error(
                request,
                f'Sorry, only {product.quantity} items of "{product.name}" available.'
            )
            return redirect(self.get_error_url())

        # Update entry quantity
        entry.quantity += 1
        entry.save()

        # Update cart totals
        cart.count = Entry.objects.filter(cart=cart).count()
        cart.total = sum(
            entry.product.price * entry.quantity
            for entry in Entry.objects.filter(cart=cart)
        )
        cart.save()

        messages.success(request, f'Added "{product.name}" to your cart.')
        return redirect(self.get_success_url())
