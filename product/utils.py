from django.db.models import Q
from . import models
def get_products_filter(key,value):

    # Generating Filter Objects

    if key == "category":
        
        kwargs = {"{0}__exact".format(key): models.Category.objects.get(name= value.strip()).id}
        return Q(**kwargs)
    elif key == "brand":
        kwargs = {"{0}__exact".format(key): models.Brands.objects.get(name= value.strip()).id}
        return Q(**kwargs)
    elif key == "created_at":
        kwargs = {"{0}__exact".format(key): value}
        return Q(**kwargs)
    elif key == "min_price":
        kwargs = {"{0}__lte".format(key): value}
        return Q(**kwargs)
    elif key == "min_price":
        kwargs = {"{0}__gte".format(key): value}
        return Q(**kwargs)
    elif key == "min_quantity":
        kwargs = {"{0}__lte".format(key): value}
        return Q(**kwargs)
    elif key == "max_quantity":
        kwargs = {"{0}__gte".format(key): value}
        return Q(**kwargs)
    elif key == "rating":
        kwargs = {"{0}__gte".format(key): value}
        return Q(**kwargs)

    

