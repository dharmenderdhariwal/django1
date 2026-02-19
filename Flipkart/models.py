from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


 
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)  
    description = models.TextField()  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    category=models.ForeignKey(Category, on_delete=models.CASCADE)  
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  
    date = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return self.name
    

 

class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

    # Cart Model
class Cart(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL , on_delete=models.CASCADE, blank=True, null=True) # Cart is for a specific user
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255, unique=True, blank=True, null=True)  # गेस्ट उपयोगकर्ताओं के लिए
    updated_at = models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return f"Cart of {self.user.username if self.user else self.session_id}"

    
    
        # Total price of the cart (recalculate whenever needed)
    def update_total_price(self):
        self.total_price = sum([item.total_price() for item in self.cartitem_set.all()])
        self.save()


    def add_product(self, product, quantity):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        self.update_total_price()  # Update total price after adding a product

    def remove_product(self, product):
        CartItem.objects.filter(cart=self, product=product).delete()
        self.update_total_price()  # Update total price after removing a product

    
    
    # CartItem Model (Product with quantity in Cart)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cartitem_set", on_delete=models.CASCADE)  # Link to the Cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the Product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart

    # Calculate total price for this CartItem (product price * quantity)
    def total_price(self):
        return self.product.price * self.quantity

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the cart item
        self.cart.update_total_price()  # Update total price when a cart item is saved
    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"


 