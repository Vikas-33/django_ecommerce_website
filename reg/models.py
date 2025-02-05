from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, F
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings



class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    desc = models.TextField()
    price = models.FloatField(default=0.0)
    available_quantity = models.PositiveIntegerField(default=0)  # Renamed for clarity
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    print(seller)
    def __str__(self):
        return self.name
    
    
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)
    last_login_time=models.DateTimeField(default= now , blank=True, null=True)

    def time_since_last_login(self):
        if self.last_login_time is None:  # If user never logged in
            return "Didn't log in yet"
        diff = now() - self.last_login_time  # Get time difference
            
        seconds = diff.total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        
        # Send email if login is older than 5 minutes
        # if minutes > 5:
        #     self.send_inactivity_email(minutes)

        # hours = int(minutes // 60)
        # minutes = minutes % 60

        return f"{hours}h {minutes}m ago" if hours or minutes else "Just now"

    # def send_inactivity_email(self, minutes):
    #     subject = "You haven't logged in for a while"
    #     message = f"Dear {self.user.username},\n\nYou have not logged in for {minutes} minutes. Please log in to keep your account active."
    #     recipient_list = [self.user.email]

    #     # Send email (you should have email settings configured in your settings.py)
    #     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

    time_since_last_login.short_description = "Time Since Last Login"

    
    

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"













# {% block homebtn %}
# <div class="sidebar" id="sidebar">
#     <a href="{% url 'index' %}">HOME</a>
#     <a href="{% url 'about' %}">ABOUT US</a>
#     <a href="{% url 'contact' %}">CONTACT</a>
    # <a href="{% url 'contact' %}">CONTACT</a>

# </div>


# {% endblock homebtn %}


# <nav class="navbar navbar-expand-lg navbar-dark  " id="navbar">
#             <div class="container-fluid">
#                 <button class="btn btn-outline-light me-3" id="sidebarToggle">☰</button>
#                 <a class="navbar-brand" href="{% url 'index' %}">STORE</a>
#                 <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
#                     <span class="navbar-toggler-icon"></span>
#                 </button>
#                 <div class="collapse navbar-collapse" id="navbarSupportedContent">
#                     {% block ln %}
#                     <button class="btn btn-outline-danger ms-auto" onclick="location.href='{% url 'login' %}'">LOGIN</button>
#                     <button class="btn btn-outline-danger ms-2" onclick="location.href='{% url 'signup' %}'">SIGNUP</button>
#                     {% endblock ln %}
#                 </div>
#             </div>

#         </nav>




























































#def reduce_quantity(self, amount):
#         """Reduce the quantity of the product."""
#         if self.available_quantity >= amount:
#             self.available_quantity -= amount
#             self.save()
#             return True
#         return False

#     def increase_quantity(self, amount):
#         """Increase the quantity of the product."""
#         self.available_quantity += amount
#         self.save()