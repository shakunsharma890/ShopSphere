from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name = 'home'),
    path('cart/',cart,name = 'cart'),
    path('add_to_cart/<int:pk>/',add_to_cart,name = 'add_to_cart'),
    path('remove/<int:pk>/',remove,name = 'remove'),
    path('plus/<int:pk>/',plus,name = 'plus'),
    path('minus/<int:pk>/',minus,name = 'minus'),
    path('support/',support, name='support'),
    path('know_us/',know_us, name='know_us'),
    path('buy_now/<int:pk>/',buy_now, name='buy_now'),
    path('checkout/',checkout, name='checkout'),
    path('place_order/',place_order, name='place_order'),
    path('order_success/',order_success, name='order_success'),
    path('product_detail/<int:pk>/',product_detail, name='product_detail'),
]