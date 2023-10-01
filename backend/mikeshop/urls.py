from django.urls import path
from . import views
from .forms import *
urlpatterns = [
   path('', views.homePage, name='homepage'),
   path('register/', views.UserSignupView.as_view(), name="register"),
   path('products/', views.all_products, name="products"),
   path('product_detail/<int:prodid>/', views.individual_product, name="individual_product"),
   path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm)),
   path('logout/', views.logout_user, name="logout"),
   path('addbasket/<int:prodid>', views.add_to_basket, name="add_basket"),
] 