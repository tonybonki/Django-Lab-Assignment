from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    products = ['apple', 'banana', 'grapes']
    context = {'products': products,}
    return render(request, 'index.html', context)