from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import InventoryItem, Supplier, InventoryTransaction

class InventoryItemListView(LoginRequiredMixin, ListView):
    model = InventoryItem
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'inventory_items'
    paginate_by = 10
    ordering = ['name']

class InventoryItemDetailView(LoginRequiredMixin, DetailView):
    model = InventoryItem
    template_name = 'inventory/inventory_detail.html'
    context_object_name = 'inventory_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = self.object.transactions.all()[:10]
        return context

class InventoryItemCreateView(LoginRequiredMixin, CreateView):
    model = InventoryItem
    template_name = 'inventory/inventory_form.html'
    fields = ['name', 'description', 'unit', 'quantity', 'reorder_level', 'supplier', 'cost_per_unit']
    success_url = reverse_lazy('inventory:inventory-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Inventory item "{form.instance.name}" created successfully.')
        return response

class InventoryItemUpdateView(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    template_name = 'inventory/inventory_form.html'
    fields = ['name', 'description', 'unit', 'quantity', 'reorder_level', 'supplier', 'cost_per_unit']
    success_url = reverse_lazy('inventory:inventory-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Inventory item "{form.instance.name}" updated successfully.')
        return response

class InventoryItemDeleteView(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/inventory_confirm_delete.html'
    success_url = reverse_lazy('inventory:inventory-list')

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        messages.success(request, f'Inventory item "{item.name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)

class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'
    context_object_name = 'suppliers'
    ordering = ['name']

class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'inventory/supplier_detail.html'
    context_object_name = 'supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_items'] = self.object.inventory_items.all()
        return context

class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    template_name = 'inventory/supplier_form.html'
    fields = ['name', 'contact_person', 'email', 'phone', 'address']
    success_url = reverse_lazy('inventory:supplier-list')

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    template_name = 'inventory/supplier_form.html'
    fields = ['name', 'contact_person', 'email', 'phone', 'address']
    success_url = reverse_lazy('inventory:supplier-list')

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'inventory/supplier_confirm_delete.html'
    success_url = reverse_lazy('inventory:supplier-list')

class TransactionListView(LoginRequiredMixin, ListView):
    model = InventoryTransaction
    template_name = 'inventory/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    ordering = ['-date']

class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = InventoryTransaction
    template_name = 'inventory/transaction_detail.html'
    context_object_name = 'transaction'

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = InventoryTransaction
    template_name = 'inventory/transaction_form.html'
    fields = ['item', 'transaction_type', 'quantity', 'unit_price', 'notes']
    success_url = reverse_lazy('inventory:transaction-list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Transaction recorded successfully.')
            return response
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

class LowStockItemsView(LoginRequiredMixin, ListView):
    template_name = 'inventory/low_stock_items.html'
    context_object_name = 'low_stock_items'

    def get_queryset(self):
        return InventoryItem.objects.filter(
            quantity__lte=models.F('reorder_level')
        ).order_by('name')

class ReorderReportView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/reorder_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items_to_reorder'] = InventoryItem.objects.filter(
            quantity__lte=models.F('reorder_level')
        ).select_related('supplier')
        return context

class StockAdjustmentView(LoginRequiredMixin, CreateView):
    model = InventoryTransaction
    template_name = 'inventory/stock_adjustment.html'
    fields = ['item', 'quantity', 'notes']
    success_url = reverse_lazy('inventory:inventory-list')

    def form_valid(self, form):
        form.instance.transaction_type = 'ADJ'
        form.instance.unit_price = form.instance.item.cost_per_unit
        return super().form_valid(form)

class ExportInventoryView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/export_inventory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_items'] = InventoryItem.objects.all().order_by('name')
        return context
