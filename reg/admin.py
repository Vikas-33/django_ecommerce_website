from reg.models import *
from django.contrib import admin

 

# Register your models here.
admin.site.register(Category)


@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available_quantity', 'seller')
    search_fields = ('name', 'category__category_name', 'seller__username')
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'created_at')

@admin.register(CartItem)
class CartItemInline(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__name')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_seller','time_since_last_login')
    search_fields = ('user__username', 'is_seller')
    

     
 
    
    
#example 