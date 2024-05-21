from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('shop', views.shop, name='shop'),
    path('product', views.product, name='product'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
]
