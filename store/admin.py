from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "quantity", "total_price")
    readonly_fields = ("total_price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "created_at")
    list_display_links = ("id",)
    search_fields = ("user__username",)
    list_filter = ("created_at",)
    readonly_fields = ("total_price", "created_at")
    inlines = [OrderItemInline]