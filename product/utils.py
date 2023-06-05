from django.db.models import Q
from .models import Category
def get_products_filter(key,value):

    # Generating Filter Objects

    if key == "category":
        
        kwargs = {"{0}__exact".format(key): Category.objects.get(name= value.strip()).id}
        return Q(**kwargs)