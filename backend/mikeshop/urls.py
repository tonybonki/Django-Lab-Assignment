from django.urls import path
from . import views

urlpatterns = [
   path('api/items/', views.index, name='item-list'),
   path('', views.homePage, name='homepage'),
   path('products/', views.all_products, name="products"),
   path('product_detail/<int:prodid>/', views.individual_product, name="individual_product"),

] 