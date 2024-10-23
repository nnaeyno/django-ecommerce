from store.models import Category


def parent_categories(request):
    parents = Category.objects.filter(parent__isnull=True)
    return {'parent_categories': parents}
