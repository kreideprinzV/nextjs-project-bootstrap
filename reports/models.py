from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from orders.models import Order
from inventory.models import InventoryTransaction
from staff.models import Employee
from django.utils import timezone
from decimal import Decimal

class DailyReport(models.Model):
    date = models.DateField(unique=True)
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
    total_tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    inventory_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    labor_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    net_profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_daily_reports'
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Daily Report - {self.date}"

    def generate_report(self):
        # Get all completed orders for the day
        orders = Order.objects.filter(
            created_at__date=self.date,
            status='COMPLETED'
        )
        
        # Calculate sales metrics
        self.total_orders = orders.count()
        self.total_sales = orders.aggregate(
            total=models.Sum('total', default=0)
        )['total']
        self.total_tax = orders.aggregate(
            tax=models.Sum('tax', default=0)
        )['tax']
        
        if self.total_orders > 0:
            self.average_order_value = self.total_sales / self.total_orders
        
        # Calculate inventory costs
        inventory_transactions = InventoryTransaction.objects.filter(
            date__date=self.date
        )
        self.inventory_cost = inventory_transactions.aggregate(
            cost=models.Sum(
                models.F('quantity') * models.F('unit_price'),
                default=0
            )
        )['cost']
        
        # Calculate labor costs
        from staff.models import Attendance
        attendances = Attendance.objects.filter(
            schedule__date=self.date,
            status='PRESENT'
        )
        
        labor_cost = Decimal('0')
        for attendance in attendances:
            if attendance.check_in and attendance.check_out:
                hours = (attendance.check_out - attendance.check_in).total_seconds() / 3600
                labor_cost += Decimal(str(hours)) * attendance.employee.hourly_rate
        
        self.labor_cost = labor_cost
        
        # Calculate net profit
        self.net_profit = self.total_sales - self.total_tax - self.inventory_cost - self.labor_cost
        
        self.save()

class MonthlyReport(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    total_sales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    total_orders = models.IntegerField(default=0)
    average_daily_sales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    total_tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    inventory_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    labor_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    net_profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_monthly_reports'
    )

    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['year', 'month']

    def __str__(self):
        return f"Monthly Report - {self.month}/{self.year}"

    def generate_report(self):
        # Get all daily reports for the month
        daily_reports = DailyReport.objects.filter(
            date__year=self.year,
            date__month=self.month
        )
        
        # Aggregate metrics from daily reports
        aggregates = daily_reports.aggregate(
            total_sales=models.Sum('total_sales', default=0),
            total_orders=models.Sum('total_orders', default=0),
            total_tax=models.Sum('total_tax', default=0),
            inventory_cost=models.Sum('inventory_cost', default=0),
            labor_cost=models.Sum('labor_cost', default=0),
            net_profit=models.Sum('net_profit', default=0)
        )
        
        self.total_sales = aggregates['total_sales']
        self.total_orders = aggregates['total_orders']
        self.total_tax = aggregates['total_tax']
        self.inventory_cost = aggregates['inventory_cost']
        self.labor_cost = aggregates['labor_cost']
        self.net_profit = aggregates['net_profit']
        
        # Calculate average daily sales
        days_in_month = daily_reports.count()
        if days_in_month > 0:
            self.average_daily_sales = self.total_sales / days_in_month
        
        self.save()

class SalesAnalytics(models.Model):
    """Model to store pre-calculated analytics data for quick dashboard access"""
    date = models.DateField()
    hour = models.IntegerField()
    total_sales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    order_count = models.IntegerField(default=0)
    average_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'hour']
        unique_together = ['date', 'hour']

    def __str__(self):
        return f"Sales Analytics - {self.date} Hour {self.hour}"

    @classmethod
    def update_analytics(cls, date, hour):
        """Update or create analytics for a specific hour"""
        orders = Order.objects.filter(
            created_at__date=date,
            created_at__hour=hour,
            status='COMPLETED'
        )
        
        total_sales = orders.aggregate(
            total=models.Sum('total', default=0)
        )['total']
        order_count = orders.count()
        
        analytics, _ = cls.objects.update_or_create(
            date=date,
            hour=hour,
            defaults={
                'total_sales': total_sales,
                'order_count': order_count,
                'average_order_value': total_sales / order_count if order_count > 0 else 0
            }
        )
        return analytics
