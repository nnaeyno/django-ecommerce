from order.models import Cart
from store.models import Category, ProductTags


def parent_categories(request):
    parents = Category.objects.filter(parent__isnull=True)
    return {'parent_categories': parents}


def product_tags(request):
    tags = ProductTags.objects.all()
    return {'product_tags': tags}



