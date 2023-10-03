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
    # If a Basket object exists then caldulate the basket quantity and return its value in the context
    if Basket.objects.filter(user_id=user, is_active=True):
        basket_quantity = Basket.objects.filter(user_id=user, is_active=True).first().total_quantity
    else:
    # If not the basket has 0 items 
        basket_quantity = 0
    context = {
        'user': user,
        'basket_quantity': basket_quantity
    }
    return render(request, 'base.html', context)

def all_products(request):
    user = request.user
    context = {
        'products': Product.objects.all(),
        'user': user,
        'basket_quantity': Basket.objects.filter(user_id=user, is_active=True).first().total_quantity
    }

    return render(request, 'products.html', context)

def individual_product(request, prodid):
    user = request.user
    product = Product.objects.get(id=prodid)
    context = {
        'product':product,
        'user': user,
        'basket_quantity': Basket.objects.filter(user_id=user, is_active=True).first().total_quantity
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
        sbi.item_quantity = sbi.item_quantity+1
        sbi.save()
    return redirect("/products")

# Show Basket

@login_required
def show_basket(request):
    # get the user object
    # does a shopping basket exist ? -> your basket is empty
    # load all shopping basket items
    # display on page 
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        #TODO: Show basket empty
        return render(request, 'basket.html', {'empty':True, 'basket_quantity': Basket.objects.filter(user_id=user, is_active=True).first().total_quantity})
    else:
        sbi = BasketItem.objects.filter(basket_id=basket)
        # is this list empty ? 
        if sbi.exists():
            # normal flow
            return render(request, 'basket.html', {'basket':basket, 'sbi':sbi, 'basket_quantity': Basket.objects.filter(user_id=user, is_active=True).first().total_quantity})
        else:
            return render(request, 'basket.html', {'empty':True, 'basket_quantity': Basket.objects.filter(user_id=user, is_active=True).first().total_quantity})

# Remove item from basket

@login_required
def remove_item(request, sbi):
    if request.method == 'POST':
        try:
            basket_item = BasketItem.objects.get(id=sbi)
            
            if basket_item.quantity > 1:
                basket_item.quantity -= 1
                basket_item.save()
            else:
                basket_item.delete()

        except BasketItem.DoesNotExist:
            return redirect('/basket')

    return redirect('/basket')

# Order View

@login_required
def order(request):
    # load in all data we need, user, basket, items
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return redirect("/")
    sbi = BasketItem.objects.filter(basket_id=basket)
    if not sbi.exists(): # if there are no items
        return redirect("/")
    # POST or GET
    if request.method == "POST":
        # check if valid
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = user
            order.basket_id = basket
            total = 0.0
            for item in sbi:
                total += float(item.item_price())
            order.total_price = total
            order.save()
            basket.is_active = False
            basket.save()
            return render(request, 'ordercomplete.html', {'order':order, 'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})
    else:
        # show the form
        form = OrderForm()
        return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})

#  Previous Orders View

@login_required
def previous_orders(request):
    user = request.user
    orders = Order.objects.filter(user_id=user)
    return render(request, 'previous_orders.html', {'orders':orders})