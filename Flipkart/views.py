
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Product, Category,Cart,CartItem
from django.contrib.auth import  login,logout,authenticate
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import datetime
 

#product category and product
def home(request):
    category_id = request.GET.get('category')
    if category_id:
        data = Product.objects.filter(category_id=category_id)
    else:
        data = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "home.html", {"products": data, "categories": categories})

def index(request):
    now=datetime.datetime.now()
    name="bholujaat"
    return render(request, 'index.html',{'td':now,'name':name})

  
#signup login logout view
def signup(request):
    user = None  # Initialize user variable to None to avoid errors
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and log them in
            login(request,user)  # Log the user in only if form is valid
            return redirect('home')  # Redirect to the home page after successful signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    form = AuthenticationForm(request)  # Initialize form
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Get POST data
        if form.is_valid():
            email = form.cleaned_data.get('username')  # `username` is the email here
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)  # Authenticate the user
            if user is not None:
                login(request, user)  # Log the user in only if valid credentials
                 
                return redirect("home")  # Redirect to the home page
            else:
                form.add_error(None, "Invalid credentials")  # Add error if authentication fails
    return render(request, 'login.html', {'form': form})  

def user_logout(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # session_key generate करें अगर अभी तक नहीं है
        cart, created = Cart.objects.get_or_create(session_id=session_key)
    return cart
 
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product
    cart = get_cart(request)  # Get or create the cart

    # Get or create CartItem (if product already in cart, increase quantity)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # If the CartItem already exists, just increase the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')  # Redirect to cart detail page after adding product

# View for cart details
@login_required
def cart_detail(request):
    cart = get_cart(request)

    # Handle quantity change (increase or decrease)
    if request.method == "POST":
        action = request.POST.get('action')
        if action.startswith("increase_"):
            item_id = action.split("_")[1]
            item = CartItem.objects.get(id=item_id)
            item.quantity += 1
            item.save()
        elif action.startswith("decrease_"):
            item_id = action.split("_")[1]
            item = CartItem.objects.get(id=item_id)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()

        # Redirect to the same cart detail page after update
        return redirect('cart_detail')

    return render(request, 'cart_detail.html', {'cart': cart})

# Remove product from cart
@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product
    cart = get_cart(request)  # Get the cart

    # Remove the CartItem
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()

    return redirect('cart_detail')  # Redirect to the cart detail page after removing item

# # Checkout view
def checkout(request):
    return render(request, 'checkout.html',{})
 
# views.py
def search(request):
    query = request.GET.get('q')  # Search query ko get karte hain

    if query:
        # Agar query di gayi hai, to products ko search karte hain
        results = Product.objects.filter(name__icontains=query)  # 'name' ko apne model ki field se replace karen
    else:
        results = Product.objects.none()  # Agar query nahi hai, to koi results nahi dikhayein

    return render(request, 'search.html', {'results': results})
