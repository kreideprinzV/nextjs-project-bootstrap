from django.contrib import admin
from .models import Order, OrderItem, Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'capacity', 'is_occupied']
    list_filter = ['is_occupied']
    search_fields = ['number']
    ordering = ['number']
    list_editable = ['is_occupied']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ['menu_item']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'table', 'server', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at', 'server']
    search_fields = ['order_number', 'customer_name', 'notes']
    ordering = ['-created_at']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ['COMPLETED', 'CANCELLED']:
            return self.readonly_fields + ['status']
        return self.readonly_fields

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'menu_item__name']
    ordering = ['-order__created_at']
    readonly_fields = ['subtotal']

    def subtotal(self, obj):
        return obj.quantity * obj.unit_price
    subtotal.short_description = 'Subtotal'
