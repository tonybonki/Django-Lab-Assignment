from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Order)
# ...the rest of the models 