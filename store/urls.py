from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('update_item/', views.UpdateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('order_complete/', views.orderComplete, name='order_complete'),
    path('all-orders/', views.allOrders, name='all-orders'),
    path('update_shipping_status/',
         views.update_shipping_status,
         name='update_shipping_status'),
    path('product_upload/', views.product_upload, name='product_upload'),
    path('product/edit/<int:product_id>/',
         views.edit_product,
         name='edit_product'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('search/', views.search, name='search'),
]
