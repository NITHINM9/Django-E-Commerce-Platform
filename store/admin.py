from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress

class ProductAdmin(admin.ModelAdmin):
    # Define the fields to display in the admin list view
    list_display = (
        'name', 
        'price', 
        'quantity_in_stock', 
        'is_active', 
        'date_added', 
        'date_updated'
    )
    
    # Define which fields are searchable in the admin interface
    search_fields = ('name', 'category', 'brand')
    
    # Add filters for the admin interface
    list_filter = ('is_active', 'category', 'brand')
    
    # Add prepopulated fields for URL slugs if applicable (add a slug field in the model if needed)
    # prepopulated_fields = {'slug': ('name',)}

# Register models with the custom admin
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
