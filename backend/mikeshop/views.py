from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import *
from .models import *

# Reusable function to get basket quantity
def get_basket_quantity(user):
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    return basket.total_quantity if basket else 0

# Django Website Views
def homePage(request):
    user = request.user
    basket_quantity = get_basket_quantity(user)
    context = {
        'user': user,
        'basket_quantity': basket_quantity
    }
    return render(request, 'base.html', context)

def all_products(request):
    user = request.user
    basket_quantity = get_basket_quantity(user)
    products = Product.objects.all()
    context = {
        'products': products,
        'user': user,
        'basket_quantity': basket_quantity
    }
    return render(request, 'products.html', context)

def individual_product(request, prodid):
    user = request.user
    product = Product.objects.get(id=prodid)
    basket_quantity = get_basket_quantity(user)
    context = {
        'product': product,
        'user': user,
        'basket_quantity': basket_quantity
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
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if not basket:
        basket = Basket.objects.create(user_id=user)
    product = Product.objects.get(id=prodid)
    sbi, created = BasketItem.objects.get_or_create(basket_id=basket, product_id=product)
    if not created:
        sbi.item_quantity += 1
        sbi.save()
    return redirect("/products")

@login_required
def show_basket(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    basket_quantity = get_basket_quantity(user)
    
    if not basket:
        return render(request, 'basket.html', {'empty': True, 'basket_quantity': basket_quantity})

    sbi = BasketItem.objects.filter(basket_id=basket)
    
    if sbi.exists():
        return render(request, 'basket.html', {'basket': basket, 'sbi': sbi, 'basket_quantity': basket_quantity})
    else:
        return render(request, 'basket.html', {'empty': True, 'basket_quantity': basket_quantity})

# Remove item from basket
@login_required
def remove_item(request, sbi_id):
    if request.method == 'POST':
        try:
            basket_item = BasketItem.objects.get(id=sbi_id)
            
            if basket_item.item_quantity > 1:
                basket_item.item_quantity -= 1
                basket_item.save()
            else:
                basket_item.delete()

        except BasketItem.DoesNotExist:
            pass

    return redirect('/basket')

# Order View
@login_required
def order(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    
    if not basket:
        return redirect("/")
    
    sbi = BasketItem.objects.filter(basket_id=basket)
    
    if not sbi.exists():
        return redirect("/")
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = user
            order.basket_id = basket
            total = sum(item.item_price() for item in sbi)
            order.total_price = Decimal(total)
            order.save()
            basket.is_active = False
            basket.save()
            return render(request, 'ordercomplete.html', {'order': order, 'basket': basket, 'sbi': sbi})
    
    else:
        form = OrderForm()
    
    return render(request, 'orderform.html', {'form': form, 'basket': basket, 'sbi': sbi})

# Previous Orders View
@login_required
def previous_orders(request):
    user = request.user
    orders = Order.objects.filter(user_id=user)
    return render(request, 'previous_orders.html', {'orders': orders})
