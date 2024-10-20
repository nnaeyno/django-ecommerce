from django.urls import path
from . import views

app_name = 'order_app'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]

""""
კალათის გვერდი(/order/cart/)
შეკვეთის განთავსების გვერდი - checkout (/order/checkout/)
"""