from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from orders.models import Order
from inventory.models import InventoryItem
from staff.models import Employee
from menu.models import MenuItem

class DashboardWidget(models.Model):
    WIDGET_TYPES = [
        ('SALES_SUMMARY', 'Sales Summary'),
        ('TOP_ITEMS', 'Top Selling Items'),
        ('INVENTORY_ALERTS', 'Inventory Alerts'),
        ('STAFF_SCHEDULE', 'Staff Schedule'),
        ('RECENT_ORDERS', 'Recent Orders'),
        ('DAILY_REVENUE', 'Daily Revenue Chart'),
    ]

    REFRESH_RATES = [
        (300, '5 minutes'),
        (600, '10 minutes'),
        (1800, '30 minutes'),
        (3600, '1 hour'),
        (7200, '2 hours'),
    ]

    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    refresh_rate = models.IntegerField(
        choices=REFRESH_RATES,
        default=300,
        help_text='Refresh interval in seconds'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"

class UserDashboardPreference(models.Model):
    LAYOUT_CHOICES = [
        ('GRID', 'Grid Layout'),
        ('LIST', 'List Layout'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dashboard_preference'
    )
    widgets = models.ManyToManyField(
        DashboardWidget,
        through='UserWidgetSettings'
    )
    layout = models.CharField(
        max_length=10,
        choices=LAYOUT_CHOICES,
        default='GRID'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dashboard Preferences - {self.user.username}"

class UserWidgetSettings(models.Model):
    user_preference = models.ForeignKey(
        UserDashboardPreference,
        on_delete=models.CASCADE
    )
    widget = models.ForeignKey(
        DashboardWidget,
        on_delete=models.CASCADE
    )
    position = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']
        unique_together = ['user_preference', 'widget']

    def __str__(self):
        return f"{self.widget.name} - {self.user_preference.user.username}"

class DashboardMetric(models.Model):
    """Store pre-calculated metrics for quick dashboard access"""
    date = models.DateField()
    total_sales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    total_orders = models.IntegerField(default=0)
    average_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    active_tables = models.IntegerField(default=0)
    pending_orders = models.IntegerField(default=0)
    low_stock_items = models.IntegerField(default=0)
    staff_on_duty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        get_latest_by = 'date'

    def __str__(self):
        return f"Dashboard Metrics - {self.date}"

    @classmethod
    def update_metrics(cls, date):
        """Update or create metrics for a specific date"""
        # Get completed orders for the day
        completed_orders = Order.objects.filter(
            created_at__date=date,
            status='COMPLETED'
        )
        
        # Calculate sales metrics
        total_sales = completed_orders.aggregate(
            total=models.Sum('total', default=0)
        )['total']
        total_orders = completed_orders.count()
        average_order_value = total_sales / total_orders if total_orders > 0 else 0
        
        # Get current operational metrics
        active_tables = Order.objects.filter(
            created_at__date=date,
            status__in=['PENDING', 'PREPARING', 'READY']
        ).values('table').distinct().count()
        
        pending_orders = Order.objects.filter(
            created_at__date=date,
            status__in=['PENDING', 'PREPARING']
        ).count()
        
        low_stock_items = InventoryItem.objects.filter(
            quantity__lte=models.F('reorder_level')
        ).count()
        
        staff_on_duty = Employee.objects.filter(
            schedules__date=date,
            schedules__attendance__status='PRESENT'
        ).distinct().count()
        
        # Update or create metrics
        metrics, _ = cls.objects.update_or_create(
            date=date,
            defaults={
                'total_sales': total_sales,
                'total_orders': total_orders,
                'average_order_value': average_order_value,
                'active_tables': active_tables,
                'pending_orders': pending_orders,
                'low_stock_items': low_stock_items,
                'staff_on_duty': staff_on_duty
            }
        )
        return metrics
