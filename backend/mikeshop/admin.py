from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Product)

# ...the rest of the models 