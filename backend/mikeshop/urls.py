from django.urls import path
from . import views

urlpatterns = [
   path('api/items/', views.index, name='item-list')
] 