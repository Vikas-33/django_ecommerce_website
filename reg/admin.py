from django.contrib import admin
from reg.models import *
from django.contrib.auth.admin import UserAdmin 
 

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_seller', 'last_login_time', 'time_since_last_login')
    readonly_fields = ('time_since_last_login',)  # Make it visible in the detail page

    def time_since_last_login(self, obj):
        return obj.time_since_last_login()  # Calls method from model

    time_since_last_login.short_description = "Time Since Last Login"

    # Organizing the fields in the detailed view
    fieldsets = (
        ("User Information", {"fields": ("user", "is_seller")}),
        ("Login Details", {"fields": ("last_login_time", "time_since_last_login")}),
    )

admin.site.register(Profile, ProfileAdmin)
    
