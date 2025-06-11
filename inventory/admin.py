from django.contrib import admin
from .models import InventoryItem, Supplier, InventoryTransaction

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone']
    search_fields = ['name', 'contact_person', 'email']
    ordering = ['name']

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'unit', 'supplier', 'reorder_level', 'cost_per_unit']
    list_filter = ['supplier']
    search_fields = ['name', 'description']
    ordering = ['name']
    list_editable = ['quantity', 'reorder_level', 'cost_per_unit']

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['item', 'transaction_type', 'quantity', 'unit_price', 'date']
    list_filter = ['transaction_type', 'date']
    search_fields = ['item__name', 'notes']
    ordering = ['-date']
    readonly_fields = ['date']
