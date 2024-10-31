# Generated by Django 5.1.1 on 2024-10-31 11:44

import django.db.models.deletion
import mptt.fields
import uuid
import versatileimagefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProductTags",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Product Tag",
                "verbose_name_plural": "Product Tags",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("title", models.CharField(max_length=100)),
                ("category_id", models.AutoField(primary_key=True, serialize=False)),
                ("slug", models.SlugField(unique=True)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="store.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("name", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("product_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "product_image",
                    versatileimagefield.fields.VersatileImageField(
                        upload_to="store/product_images/", verbose_name="Image"
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("is_available", models.BooleanField(default=True)),
                ("slug", models.SlugField(default=uuid.uuid1, unique=True)),
                ("categories", models.ManyToManyField(to="store.category")),
                ("tag", models.ManyToManyField(to="store.producttags")),
            ],
        ),
    ]
