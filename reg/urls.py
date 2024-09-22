from django.contrib import admin #type:ignore
from django.urls import path #type:ignore
from reg import views


urlpatterns = [
    path('signup/', views.signup, name ="signup"),
    path('verify-otp/', views.verify_otp, name='verify_otp'), 
    path('', views.index, name="index"),
    path('login/', views.login, name ="login"),
    path('',views.home, name="home"),
    path('contact/',views.contact, name="contact"),
    path('about/',views.about, name="about"),
    path('about/',views.about, name="about"),
    path('login2/', views.login2, name="login2"),
    path('logout/', views.log_out, name="log_out"),
    path('add_product',views.add_product, name="add_product"),
    path('product/<int:product_id>/', views.product_desc, name='product_desc'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product_desc/<int:product_id>/', views.product_desc, name='product_desc'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('remove_product/<int:product_id>/', views.remove_product, name='remove_product'),
        
    
    



]

# .navbar {
#             background-color: black;
#             transition: background-color 0.5s ease;
#         }

#         .navbar.scrolled {
#             background-color: rgba(0, 0, 0, 0.8);
#         }

#         .navbar .btn {
#             background-color: green;
#             border: none;
#             transition: background-color 0.3s ease;
#         }

#         .navbar .btn:hover {
#             background-color: #ff416c;
#             color: #fff;
#         }

