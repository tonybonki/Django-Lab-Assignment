from django.urls import path
from . import views
from .forms import *
urlpatterns = [
   path('', views.homePage, name='homepage'),
   path('register/', views.UserSignupView.as_view(), name="register"),
   path('products/', views.all_products, name="products"),
   path('product_detail/<int:prodid>/', views.individual_product, name="individual_product"),
   path('login/',views.login_view.as_view(), name='login'),
   path('logout/', views.logout_user, name="logout"),
   path('basket/', views.show_basket, name="show_basket"),
   path('remove_item/<int:sbi>/', views.remove_item, name='remove_item'),
   path('addbasket/<int:prodid>', views.add_to_basket, name="add_basket"),
] 