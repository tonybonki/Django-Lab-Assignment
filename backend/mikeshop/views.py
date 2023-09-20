from django.http import HttpResponse
from django.shortcuts import render

# Import all Models 
from .models import *

# Rest framework Methods
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status


# decorator from the Django REST framework


def index(request):
    # Your logic to fetch data and serialize it goes here
    # Retrieve the products and categories querysets

    products = Product.objects.all()
    products_list = [
        {
         "id": product.id,
         "name": product.name,
         'price': product.price,
         'description': product.description,
         'image_url': product.product_image.url,
         }
         
        for product in products
        
    ]

    data = {
        "products": products_list,

    }
 
    # Return the combined data as a JSON response
    return JsonResponse(data, status=status.HTTP_200_OK)