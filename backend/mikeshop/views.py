from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import *
from django.views.generic import CreateView


# Import all Models 
from .models import *

# Rest framework Methods
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status

# Django Website Views
def homePage(request):
    return render(request, 'index.html')

def all_products(request):
    context = {
        'products': Product.objects.all(),
    }

    return render(request, 'products.html', context)

def individual_product(request, prodid):

    product = Product.objects.get(id=prodid)
    context = {
        'product':product,
    }

    return render(request, 'product_detail.html', context)

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

# Login View

class UserLoginView(LoginView):
    template_name='login.html'

def logout_user(request):
    logout(request)
    return redirect("/")
