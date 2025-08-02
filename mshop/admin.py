from django.contrib import admin
from django.utils.html import format_html
from .models import Product,Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'price','discount', 'stock', 'image_tag')
    search_fields = ('name',)
    list_filter = ('price',)
    readonly_fields = ('image_preview',)

    # Show image in list view
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image'

    # Show image in detail (add/edit) form
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" height="200" style="object-fit: contain;"/>', obj.image.url)
        return "No image uploaded yet."
    image_preview.short_description = "Current Image"
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer_name','customer_phone','customer_address','order_details', 'quantity','total_price', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('customer_name', 'customer_email','customer_phone', 'product__name')