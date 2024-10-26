from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView, TemplateView

from store.models import Category, Product, ProductTags


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        pass


def category(request, slug=None):
    sort_by = request.GET.get('sort')
    if slug:
        selected_category = get_object_or_404(Category, slug=slug)
        subcategories = selected_category.get_children()
        products = Product.objects.filter(categories=selected_category)
    else:
        selected_category = None
        subcategories = Category.objects.filter(parent__isnull=True)
        products = Product.objects.all()

    if sort_by == 'date_newest':
        products = products.order_by('-created_at')
    context = search(request, products, selected_category, subcategories, sort_by)
    context = filter_tags(request, products, context)
    context = price_filtering(request, context.get('products', products), context)
    products = context.get('products', products)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['products'] = page_obj
    return render(request, 'shop.html', context)


def price_filtering(request, products, context):
    selected_price = request.GET.get('price', 0)
    if selected_price:
        products = products.filter(price__lte=selected_price)
        selected_price = int(selected_price) if selected_price else 0
        context['selected_price'] = selected_price
        context['products'] = products
    return context


def filter_tags(request, products, context):
    selected_tag_id = request.GET.get('tag')
    selected_tag_id = int(selected_tag_id) if selected_tag_id else None
    if selected_tag_id:
        product_tags = ProductTags.objects.all()
        products = products.filter(tag__id=selected_tag_id)
        context['products'] = products
        context['tags'] = product_tags
        context['selected_tag_id'] = selected_tag_id

    return context


def search(request, products, selected_category, subcategories, sort_by):
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query)  # | Q(description__icontains=query)
        )

    context = {
        'category': selected_category,
        'subcategories': subcategories,
        'products': products,
        'query': query,
        'selected_sort': sort_by,
    }
    return context


# thw shop detail page will be static as requirements didn't specify that we had to do this dynamically now
class ProductDetail(DetailView):
    model = Product
    template_name = 'shop-detail.html'

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Contact(FormView):
    template_name: str = "contact.html"
    success_url = "..."

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Contact, self).get_context_data(**kwargs)
        return context


class Error(TemplateView):
    template_name = '404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Testimonial(TemplateView):
    template_name = 'testimonial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
