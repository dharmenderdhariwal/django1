 

from django.contrib import admin
from django.urls import path
from .views import *

 


urlpatterns = [
        
    path('home/', home, name="home"),
    path('index/', index, name="index"),
    path('signup/', signup, name="signup"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),

    # Add to Cart URL (passing product_id)
    path('add_to_cart/<int:product_id>/', add_to_cart, name="add_to_cart"),

    # Remove from Cart URL (passing product_id)
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name="remove_from_cart"),

    # Cart Detail URL (view the cart content)
    path('cart/', cart_detail, name="cart_detail"),

    # Checkout URL
    path('checkout/', checkout, name='checkout'),
 
    # Add the login URL (if it's missing)
    path('accounts/login/', user_login, name="login"),  # Ensure login is handled

    path('search/',search,name='search'),  # New search route

   
]
