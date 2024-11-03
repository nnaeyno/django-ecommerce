from django.urls import path
from . import views, error_views
from .category_view import CategoryView
from .views import ProductDetail, Contact, Testimonial, HomeView

handler404 = 'store.error_views.error_404'
handler500 = 'store.error_views.error_500'

app_name = 'store'


urlpatterns = [
    path("", HomeView.as_view(), name="main"),
    path('category/', CategoryView.as_view(), name="category"),
    path('category/<slug:slug>/', CategoryView.as_view(), name="category"),
    path('product/<slug:slug>/', ProductDetail.as_view(), name="product"),
    path('contact/', Contact.as_view(), name="contact"),
    path('error/', error_views.error_404, name="error"),
    path('testimonial/', Testimonial.as_view(), name="testimonial"),
]

"""
მთავარი გვერდი (/)
ლისტინგის გვერდი(სადაც ყველა პროდუქტია თავმოყრილი შესაბამისი ფილტრებით) (/category/<slug:slug>/)
პროდუქტის დეტალური გვერდი (/product/<slug:slug>/)
კონტაქტის გვერდი (/contact/)
"""