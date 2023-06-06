from django.db import models
# from core.models import TimeStampedModel
from django.dispatch import receiver
from django.db.models.signals import post_save
from user.models import User
from product.models import  Products



# Create your models here.
class Cart(models.Model):

    user = models.OneToOneField(
        User, related_name="user_cart", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Products, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("cart", "product"),)

