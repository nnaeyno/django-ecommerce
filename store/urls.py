from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path('category/', views.category, name="category"),
    path('category/<slug:slug>/', views.category, name="category"),
    path('product/<slug:slug>/', views.product, name="product"),
    path('contact/', views.contact, name="contact"),
    path('error/', views.error, name="error"),
    path('testimonial/', views.testimonial, name="testimonial"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]

"""
მთავარი გვერდი (/)
ლისტინგის გვერდი(სადაც ყველა პროდუქტია თავმოყრილი შესაბამისი ფილტრებით) (/category/<slug:slug>/)
პროდუქტის დეტალური გვერდი (/product/<slug:slug>/)
კონტაქტის გვერდი (/contact/)
"""