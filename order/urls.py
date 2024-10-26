from django.urls import path
from . import views
from .views import AddToCartView, CartView, CheckoutView, RemoveFromCartView

app_name = 'order_app'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<str:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/',
         RemoveFromCartView.as_view(),
         name='remove-from-cart'),
]

""""
კალათის გვერდი(/order/cart/)
შეკვეთის განთავსების გვერდი - checkout (/order/checkout/)
"""