from django.contrib import admin
from .models import Product, ProductImage, Contact, UserData, Address   #,purchases,purchasesItems # Make sure to import all your models

# Inline to add multiple images to a product
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # Allows adding one extra image field by default

# Registers the Product model with the new inline
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category', 'stock')
    search_fields = ('name', 'description')

# Register your other models here
admin.site.register(Contact)
admin.site.register(UserData)
admin.site.register(Address)
# admin.site.register(purchases)
# admin.site.register(purchasesItems)
