from django.db import models
from django.utils.translation import gettext_lazy as _
# from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Brands(models.Model):
    """ Product Brand"""

    name = models.CharField(
        verbose_name=_("Brand name"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(null=True, blank=True, help_text="Description of the brand")

    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
  
    class Meta:
        db_table = "sk_brands"

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    """Category of the product"""

    name = models.CharField(
        verbose_name=_("Category name"),
        max_length=255,
        unique=True,
    )
    description = models.TextField(null=True, blank=True, help_text="Description of the category")
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    # parent = TreeForeignKey(
    #     "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    # )
    class Meta:
        db_table = "sk_category"

    def __str__(self) -> str:
        return self.name
    
class Products(models.Model):
    """Master product model"""
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True, help_text="Description of the product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    rating = models.FloatField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "sk_products"

    def __str__(self) -> str:
        return self.name