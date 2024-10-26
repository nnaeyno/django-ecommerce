from django.urls import path
from . import views
from .views import AddToCartView

app_name = 'order_app'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<str:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
]

""""
კალათის გვერდი(/order/cart/)
შეკვეთის განთავსების გვერდი - checkout (/order/checkout/)
"""