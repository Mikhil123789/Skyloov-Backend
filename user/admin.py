from django.contrib import admin
# from mptt.admin import MPTTModelAdmin
from .models import (
    User
)

admin.site.register(User)
