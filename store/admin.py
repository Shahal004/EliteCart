from django.contrib import admin
from .models import Product, Order, OrderItem, Review, Wishlist, Coupon

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'price',
        'category',
        'stock'
    )
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'total_price',
        'status',
        'created_at'
    )
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Coupon)