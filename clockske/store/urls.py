from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('shop', views.shop, name='shop'),
    path('product/<int:product_id>', views.product, name='product'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('login', views.user_login, name='login'),
    path('signup', views.user_signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('update_item', views.UpdateItem, name='update_item'),
    path('process_order', views.processOrder, name='process_order'),
]
