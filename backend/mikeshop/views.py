from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
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
    user = request.user
    return render(request, 'base.html', {'user': user})

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

class login_view(LoginView):
    template_name = 'login.html'
    form_class = LoginForm




def logout_user(request):
    logout(request)
    return redirect("/")

# Basket View

@login_required
def add_to_basket(request, prodid):
    user = request.user
    # is there a shopping basket for the user 
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        # create a new one
        Basket.objects.create(user_id = user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    # get the product 
    product = Product.objects.get(id=prodid)
    sbi = BasketItem.objects.filter(basket_id=basket, product_id = product).first()
    if sbi is None:
        # there is no basket item for that product 
        # create one 
        sbi = BasketItem(basket_id=basket, product_id = product)
        sbi.save()
    else:
        # a basket item already exists 
        # just add 1 to the quantity
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return redirect("/products")