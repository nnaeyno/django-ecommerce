from django.contrib import admin
from order.models import Cart, Entry

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'count', 'total', 'updated', 'timestamp')
    list_filter = ('user', 'count', 'total', 'updated', 'timestamp')
    search_fields = ('user', 'count', 'total', 'updated', 'timestamp')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity')
    list_filter = ('product', 'cart', 'quantity')
    search_fields = ('product', 'cart', 'quantity')
