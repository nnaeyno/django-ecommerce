from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib import admin


class Category(MPTTModel):
    title = models.CharField(max_length=100)
    category_id = models.AutoField(primary_key=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    categories = models.ManyToManyField(Category)
    product_id = models.AutoField(primary_key=True)
    product_image = models.ImageField(upload_to="store/product_images/")
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def overall_worth(self):
        return self.price * self.quantity
