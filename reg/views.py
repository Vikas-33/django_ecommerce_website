from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from reg.forms import *
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
import random
from django.utils.timezone import now

def signup(request):
    if request.method == 'POST':
        # Initial Sign-Up Phase
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm')
        email = request.POST.get('email')
        is_seller = request.POST.get('is_seller', 'off') == 'on'

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Generate OTP and store it in the session
        otp = str(random.randint(100000, 999999))
        request.session['otp'] = otp

        # Send the OTP to the user's email
        send_mail(
            'Your OTP for sign-up',
            f'Your OTP is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Store relevant information in session
        request.session['username'] = username
        request.session['password'] = password
        request.session['email'] = email
        request.session['is_seller'] = is_seller

        messages.success(request, "OTP has been sent to your email. Please verify.")
        return redirect('verify_otp')

    return render(request, 'signup.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        # Check the OTP stored in session
        if 'otp' in request.session and request.session['otp'] == entered_otp:
            # Create the user after OTP verification
            username = request.session.get('username')
            password = request.session.get('password')
            email = request.session.get('email')
            is_seller = request.session.get('is_seller')

            user = User.objects.create_user(username=username, password=password, email=email)
            user.profile.is_seller = is_seller  # Ensure you have this field in your Profile model
            user.save()

            # Clear the session data
            del request.session['otp']
            del request.session['username']
            del request.session['password']
            del request.session['email']
            del request.session['is_seller']

            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Adjust according to your flow
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')  # Redirect back to OTP verification page

    return render(request, 'verify_otp.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            user.profile.last_login_time = now()  # Update last login time in Profile model
            user.profile.save()
            auth_login(request, user)
            if user.profile.is_seller:
                return redirect('seller_dashboard')
            else:
                return redirect('login2')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
            
    return render(request, 'login.html')

@login_required
def login2(request):
    if request.user.is_authenticated:
        username = request.user.username
        products = Product.objects.all()
        categories = Category.objects.all()
    return render(request, 'ind.html', { 'categories': categories, 'products': products, 'username': username})

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories,'products': products})



def home(request):
    return redirect('index')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            form = ContactForm()  
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def log_out(request):
    logout(request)
    return redirect('index')

def add_product(request):
    if not request.user.profile.is_seller:
        return redirect('index')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False) 
            product.seller = request.user  # product to this seller
            product.save()  
            messages.success(request, "Product added successfully")
            return redirect('seller_dashboard')
        else:
            messages.error(request, "Product is not added, try again")
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

def product_desc(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = None

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    context = {
        'product': product,
        'cart_item': cart_item,
    }

    return render(request, 'product_desc.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if request.method == 'POST':
        quantity_requested = int(request.POST.get('quantity', 1))
        
        if quantity_requested > product.available_quantity:
            messages.error(request, f"Only {product.available_quantity} units of {product.name} are available.")
            cart_item.quantity = product.available_quantity
        else:
            cart_item.quantity = quantity_requested
        
        cart_item.save()
        return JsonResponse({'quantity': cart_item.quantity})

    return redirect('view_cart')

@login_required
def view_cart(request):
    DELIVERY_CHARGE = 5.00  
    DISCOUNT_RATE = 0.05   
    platform_fee = 2

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.info(request, "Your cart is empty.")
        return render(request, 'cart.html', {'cart_empty': True})

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('quantity'))
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        product = cart_item.product

        # quantity cheack
        if new_quantity > product.available_quantity:
            messages.error(request, f"Only {product.available_quantity} units of {product.name} are available.")
            cart_item.quantity = product.available_quantity
        else:
            cart_item.quantity = new_quantity
        
        cart_item.save()

        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            messages.info(request, "Your cart is now empty.")
            return JsonResponse({'cart_empty': True})

        total_cost = sum(item.quantity * item.product.price for item in cart_items)
        discount = total_cost * DISCOUNT_RATE
        grand_total = total_cost - discount + platform_fee +DELIVERY_CHARGE

        return JsonResponse({
            'quantity': cart_item.quantity,
            'total': cart_item.get_total_price(),
            'subtotal': total_cost,
            'delivery_charge': DELIVERY_CHARGE,
            'discount': discount,
            'grand_total': grand_total,
            'platform_fee':platform_fee,
            'cart_empty': False,
        })

    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.info(request, "Your cart is empty.")
        return render(request, 'cart.html', {'cart_empty': True})

    total_cost = sum(item.quantity * item.product.price for item in cart_items)
    discount = total_cost * DISCOUNT_RATE
    grand_total = total_cost - discount  + DELIVERY_CHARGE

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'delivery_charge': DELIVERY_CHARGE,
        'discount': discount,
        'platform_fee':platform_fee,
        'grand_total': grand_total,
        
        'cart_empty': False,
    }
    
    return render(request, 'cart.html', context)

    


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

def seller_dashboard(request):
    if not request.user.profile.is_seller:
        return redirect('index')
#all products
    products = Product.objects.filter(seller=request.user)

    total_products = products.count()

    
    total_revenue = sum(
        item.get_total_price() for item in CartItem.objects.filter(product__seller=request.user)
    )

    context = {
        'total_products': total_products,
        'total_revenue': total_revenue,
        'products': products,  
    }

    return render(request, 'seller_dashboard.html', context)

def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Ensure the user is the seller of the product
    if product.seller == request.user:
        product.delete()
        messages.success(request, "Product removed successfully.")
    else:
        messages.error(request, "You do not have permission to remove this product.")
    
    return redirect('seller_dashboard')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Replace 'contact' with your contact page URL name
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


@login_required
def user_profile(request):
    if request.user.is_authenticated:
        time_diffrence = now()-request.user.last_login
        Minutes_since_last_login = time_diffrence.total_seconds()//60
    else:
        hours_since_last_login=None
    return render (request ,'user_profile.html',{'Minutes_since_last_login':Minutes_since_last_login})


def edit_profile(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('about')  # Replace 'contact' with your contact page URL name
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
def change_password(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('about')  # Replace 'contact' with your contact page URL name
    else:
        form = ContactForm()



# @login_required
# def user_profile(request):
#     # Get the current logged-in user
#     user = request.user
    
#     # Retrieve the user's order history
#     order_history = Product.objects.filter(user=user).order_by('-date_ordered')
    
#     # Pass the user and order history to the template
#     context = {
#         'user': user,
#         'order_history': order_history,
#     }
    
#     return render(request, 'user_profile.html', context)







































































# compare available quantity
#         if new_quantity > product.available_quantity:
#             messages.error(request, f"Only {product.available_quantity} units of {product.name} are available.")
#             cart_item.quantity = product.available_quantity
#         else:
# #             cart_item.quantity = new_quantity




# cart = get_object_or_404(Cart, user=request.user)

#     if request.method == 'POST':
#         item_id = request.POST.get('item_id')
#         new_quantity = int(request.POST.get('quantity'))
        
#         cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
#         product = cart_item.product

                
        
        
#         return JsonResponse({
#             'quantity': cart_item.quantity,
#             'total': cart_item.get_total_price(),
#         })

#     cart_items = CartItem.objects.filter(cart=cart)

    
#     DELIVERY_CHARGE = 5.00 
#     PLATFORM_FEE = 2.00    
#     DISCOUNT_RATE = 0.5   

#     # totals
#     total_cost = sum(item.quantity * item.product.price for item in cart_items)
#     discount = total_cost * DISCOUNT_RATE
#     grand_total = total_cost - discount + DELIVERY_CHARGE + PLATFORM_FEE

#     context = {
#         'cart': cart,
#         'cart_items': cart_items,
#         'total_cost': total_cost,
#         'delivery_charge': DELIVERY_CHARGE,
#         'platform_fee': PLATFORM_FEE,
#         'discount': discount,
#         'grand_total': grand_total,
#     }
    
#     return render(request, 'cart.html', context)
