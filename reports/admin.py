from django.contrib import admin
from .models import DailyReport, MonthlyReport, SalesAnalytics

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_sales', 'total_orders', 'average_order_value', 'generated_by']
    list_filter = ['date']
    search_fields = ['date', 'generated_by__username']
    ordering = ['-date']
    readonly_fields = ['generated_by', 'created_at', 'updated_at']

@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'total_sales', 'total_orders', 'average_daily_sales', 'generated_by']
    list_filter = ['year', 'month']
    search_fields = ['year', 'month', 'generated_by__username']
    ordering = ['-year', '-month']
    readonly_fields = ['generated_by', 'created_at', 'updated_at']

@admin.register(SalesAnalytics)
class SalesAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'hour', 'total_sales', 'order_count', 'average_order_value']
    list_filter = ['date']
    search_fields = ['date']
    ordering = ['-date', 'hour']
    readonly_fields = ['date', 'hour', 'created_at', 'updated_at']
