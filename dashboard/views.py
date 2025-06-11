from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import DashboardWidget, UserDashboardPreference, DashboardMetric
from orders.models import Order
from inventory.models import InventoryItem
from staff.models import Employee
from django.utils import timezone
from datetime import timedelta

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Get or create user dashboard preferences
        preference, _ = UserDashboardPreference.objects.get_or_create(
            user=self.request.user
        )
        
        # Get user's widgets
        context['widgets'] = preference.widgets.filter(is_active=True)
        
        # Get latest metrics
        try:
            metrics = DashboardMetric.objects.latest()
            context['metrics'] = metrics
        except DashboardMetric.DoesNotExist:
            context['metrics'] = None
        
        # Get recent orders
        context['recent_orders'] = Order.objects.filter(
            created_at__date=today
        ).order_by('-created_at')[:5]
        
        # Get low stock items
        context['low_stock_items'] = InventoryItem.objects.filter(
            quantity__lte=models.F('reorder_level')
        )[:5]
        
        # Get active staff
        context['active_staff'] = Employee.objects.filter(
            is_active=True
        )[:5]
        
        return context

class WidgetListView(LoginRequiredMixin, ListView):
    model = DashboardWidget
    template_name = 'dashboard/widget_list.html'
    context_object_name = 'widgets'

class WidgetCreateView(LoginRequiredMixin, CreateView):
    model = DashboardWidget
    template_name = 'dashboard/widget_form.html'
    fields = ['name', 'widget_type', 'refresh_rate']
    success_url = reverse_lazy('dashboard:widget-list')

class WidgetUpdateView(LoginRequiredMixin, UpdateView):
    model = DashboardWidget
    template_name = 'dashboard/widget_form.html'
    fields = ['name', 'widget_type', 'refresh_rate', 'is_active']
    success_url = reverse_lazy('dashboard:widget-list')

class WidgetDeleteView(LoginRequiredMixin, DeleteView):
    model = DashboardWidget
    template_name = 'dashboard/widget_confirm_delete.html'
    success_url = reverse_lazy('dashboard:widget-list')

class UserPreferencesView(LoginRequiredMixin, UpdateView):
    model = UserDashboardPreference
    template_name = 'dashboard/user_preferences.html'
    fields = ['layout']
    success_url = reverse_lazy('dashboard:dashboard-home')

    def get_object(self, queryset=None):
        return UserDashboardPreference.objects.get_or_create(
            user=self.request.user
        )[0]

# Views for handling AJAX requests
from django.http import JsonResponse
from django.views import View

class WidgetDataView(LoginRequiredMixin, View):
    def get(self, request, widget_id):
        try:
            widget = DashboardWidget.objects.get(id=widget_id)
            # Get widget-specific data based on widget type
            data = self.get_widget_data(widget)
            return JsonResponse({'success': True, 'data': data})
        except DashboardWidget.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Widget not found'})

    def get_widget_data(self, widget):
        if widget.widget_type == 'SALES_SUMMARY':
            return self.get_sales_summary()
        elif widget.widget_type == 'TOP_ITEMS':
            return self.get_top_items()
        elif widget.widget_type == 'INVENTORY_ALERTS':
            return self.get_inventory_alerts()
        elif widget.widget_type == 'STAFF_SCHEDULE':
            return self.get_staff_schedule()
        elif widget.widget_type == 'RECENT_ORDERS':
            return self.get_recent_orders()
        elif widget.widget_type == 'DAILY_REVENUE':
            return self.get_daily_revenue()
        return {}

    def get_sales_summary(self):
        today = timezone.now().date()
        orders = Order.objects.filter(created_at__date=today)
        return {
            'total_sales': orders.aggregate(total=models.Sum('total'))['total'] or 0,
            'order_count': orders.count(),
            'average_order': orders.aggregate(avg=models.Avg('total'))['avg'] or 0
        }

    def get_top_items(self):
        # Implementation for top selling items
        pass

    def get_inventory_alerts(self):
        # Implementation for inventory alerts
        pass

    def get_staff_schedule(self):
        # Implementation for staff schedule
        pass

    def get_recent_orders(self):
        # Implementation for recent orders
        pass

    def get_daily_revenue(self):
        # Implementation for daily revenue chart
        pass

class UpdateWidgetPositionView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            widget_id = request.POST.get('widget_id')
            position = request.POST.get('position')
            preference = request.user.dashboard_preference
            widget_setting = preference.userwidgetsettings_set.get(
                widget_id=widget_id
            )
            widget_setting.position = position
            widget_setting.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class ToggleWidgetVisibilityView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            widget_id = request.POST.get('widget_id')
            preference = request.user.dashboard_preference
            widget_setting = preference.userwidgetsettings_set.get(
                widget_id=widget_id
            )
            widget_setting.is_visible = not widget_setting.is_visible
            widget_setting.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
