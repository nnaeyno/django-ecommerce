from store.models import Category, Product


def parent_categories(request):
    parents = Category.objects.filter(parent__isnull=True)
    return {'parent_categories': parents}


def product_tags(request):
    tags = Product.objects.all()
    return {'product_tags': tags}
