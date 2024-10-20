from django.contrib import admin

from store.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    list_filter = ('parent',)
    search_fields = ('^title',)
    list_select_related = ('parent',)

    def get_queryset(self, request):
        """Optimize the queryset"""
        queryset = super().get_queryset(request)
        return queryset.select_related('parent')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'get_categories')
    list_filter = ('categories',)
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)
    raw_id_fields = ('categories',)

    def get_queryset(self, request):
        """Optimize for the admin list view"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('categories')

    def get_categories(self, obj):
        return ", ".join([category.title for category in obj.categories.all()])

    get_categories.short_description = 'Categories'
