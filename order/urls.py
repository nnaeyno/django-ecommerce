from django.urls import path
from . import views

app_name = 'order_app'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]

""""
კალათის გვერდი(/order/cart/)
შეკვეთის განთავსების გვერდი - checkout (/order/checkout/)
"""