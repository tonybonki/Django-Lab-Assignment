from django.http import HttpResponse
from django.shortcuts import render

# Rest framework Methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# decorator from the Django REST framework
@api_view(['GET'])

def index(request):
    # Your logic to fetch data and serialize it goes here
    items = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
    return Response(items, status=status.HTTP_200_OK)