# Shops/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_shop, name='register-shop'),
    path('list/', views.shop_list, name='shop-list'),
    path('search/', views.search_shops, name='search-shops'),
    path('check-shop-name/', views.check_shop_name, name='check-shop-name'),
    path('check-lat-long/', views.check_lat_long, name='check-lat-long'),\
]
