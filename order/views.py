
from django.views.generic import TemplateView

from order.models import Cart, Entry

from store.models import Product

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart.html'
    model = Cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'
    model = Cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddToCartView(LoginRequiredMixin, View):
    """
    Class-based view to add a product to cart with quantity validation
    """
    login_url = 'users:login'
    redirect_field_name = 'next'

    def get_login_url(self):
        return f"{reverse(self.login_url)}?next={self.request.path}"

    def get_error_url(self):
        return self.request.META.get('HTTP_REFERER', reverse('store:error'))

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse('store:category'))

    def get(self, request, *args, **kwargs):
        return redirect('category')

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, product_id=product_id)

        # Check if product is in stock
        if product.quantity <= 0:
            messages.error(request, f'Sorry, "{product.name}" is out of stock.')
            return redirect(self.get_error_url())

        cart, created = Cart.objects.get_or_create(user=request.user)

        entry, created = Entry.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 0}
        )

        if product.quantity < (entry.quantity + 1):
            messages.error(
                request,
                f'Sorry, only {product.quantity} items of "{product.name}" available.'
            )
            return redirect(self.get_error_url())

        entry.quantity += 1
        entry.save()

        cart.count = Entry.objects.filter(cart=cart).count()
        cart.total = sum(
            entry.product.price * entry.quantity
            for entry in Entry.objects.filter(cart=cart)
        )
        cart.save()

        messages.success(request, f'Added "{product.name}" to your cart.')
        return redirect(self.get_success_url())


# Cart.html is still static as homework requirements didn't specify
# to change that page, this is only a backend logic that isn't attached to front
class RemoveFromCartView(LoginRequiredMixin, View):
    """
    Class-based view to remove a product from cart
    """

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse('order_app:cart'))

    def post(self, request, product_id, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        entry = get_object_or_404(Entry, cart=cart, product_id=product_id)

        product_name = entry.product.name

        # Delete the entry
        entry.delete()

        cart.count = Entry.objects.filter(cart=cart).count()
        cart.total = sum(
            entry.product.price * entry.quantity
            for entry in Entry.objects.filter(cart=cart)
        )
        cart.save()

        messages.success(request, f'Removed "{product_name}" from your cart.')
        return redirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return redirect('cart')
