from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart
from user.models import User


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_cart(sender, instance, **kwargs):
    try:
        instance.cart.save()
    except Cart.DoesNotExist:
        Cart.objects.create(user=instance)
