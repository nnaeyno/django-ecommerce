from django.urls import path
from . import views
from .category_view import CategoryView
from .views import ProductDetail, Contact, Error, Testimonial, HomeView




urlpatterns = [
    path("", HomeView.as_view(), name="main"),
    path('category/', CategoryView.as_view(), name="category"),
    path('category/<slug:slug>/', CategoryView.as_view(), name="category"),
    path('product/<slug:slug>/', ProductDetail.as_view(), name="product"),
    path('contact/', Contact.as_view(), name="contact"),
    path('error/', Error.as_view(), name="error"),
    path('testimonial/', Testimonial.as_view(), name="testimonial"),
]

"""
მთავარი გვერდი (/)
ლისტინგის გვერდი(სადაც ყველა პროდუქტია თავმოყრილი შესაბამისი ფილტრებით) (/category/<slug:slug>/)
პროდუქტის დეტალური გვერდი (/product/<slug:slug>/)
კონტაქტის გვერდი (/contact/)
"""