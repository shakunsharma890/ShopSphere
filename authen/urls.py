from django.urls import path
from .views import *
urlpatterns = [
    path('',login_,name = 'login_'),
    path('register/',register,name = 'register'),
    path('profile/',profile,name = 'profile'),
    path('logout/', logout_, name='logout'),
    path('update-profile/', update_profile, name='update_profile'),
    path('change-password/',change_password, name='change_password'),
    path('my_orders/', my_orders, name='my_orders'),
    path('forgot_password/', forgot_password, name='forgot_password'),
]