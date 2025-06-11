from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Order, Table, OrderItem

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    ordering = ['-created_at']

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['table', 'customer_name', 'notes']
    success_url = reverse_lazy('orders:order-list')

    def form_valid(self, form):
        form.instance.server = self.request.user.employee_profile
        return super().form_valid(form)

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['table', 'customer_name', 'status', 'notes']
    
    def get_success_url(self):
        return reverse_lazy('orders:order-detail', kwargs={'pk': self.object.pk})

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders:order-list')

class TableListView(LoginRequiredMixin, ListView):
    model = Table
    template_name = 'orders/table_list.html'
    context_object_name = 'tables'

class TableDetailView(LoginRequiredMixin, DetailView):
    model = Table
    template_name = 'orders/table_detail.html'
    context_object_name = 'table'

class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    template_name = 'orders/table_form.html'
    fields = ['number', 'capacity']
    success_url = reverse_lazy('orders:table-list')

class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = Table
    template_name = 'orders/table_form.html'
    fields = ['number', 'capacity', 'is_occupied']
    success_url = reverse_lazy('orders:table-list')

class TableDeleteView(LoginRequiredMixin, DeleteView):
    model = Table
    template_name = 'orders/table_confirm_delete.html'
    success_url = reverse_lazy('orders:table-list')

# Order Status Management Views
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

class OrderStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, status):
        order = get_object_or_404(Order, pk=pk)
        order.status = status
        order.save()
        messages.success(request, f'Order #{order.order_number} status updated to {status}')
        return redirect('orders:order-detail', pk=pk)

class MarkOrderPreparingView(OrderStatusUpdateView):
    def post(self, request, pk):
        return super().post(request, pk, 'PREPARING')

class MarkOrderReadyView(OrderStatusUpdateView):
    def post(self, request, pk):
        return super().post(request, pk, 'READY')

class MarkOrderServedView(OrderStatusUpdateView):
    def post(self, request, pk):
        return super().post(request, pk, 'SERVED')

class MarkOrderCompletedView(OrderStatusUpdateView):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.mark_completed()
        messages.success(request, f'Order #{order.order_number} has been completed')
        return redirect('orders:order-detail', pk=pk)

class MarkOrderCancelledView(OrderStatusUpdateView):
    def post(self, request, pk):
        return super().post(request, pk, 'CANCELLED')
