from django.contrib import admin

# Register your models here.
from .models import Order , OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):

    list_display = ("id" , "customer_name" , "total_amount" , "status", "created_at" )
    list_filter = ("status" , "created_at")
    list_editable= ("status",)
    inlines = [OrderItemInline]

admin.site.register(Order , OrderAdmin)
admin.site.register(OrderItem)