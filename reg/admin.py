from django.contrib import admin
from reg.models import *

 

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject')


admin.site.register(Profile)
    
#example 