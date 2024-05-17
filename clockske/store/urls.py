from django.urls import path

from . import views

urlpatterns = [
    path('', views.hello, name='hello'),
    path('store', views.store, name='store'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
]
