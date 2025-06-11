from django.contrib import admin
from .models import DashboardWidget, DashboardMetric, UserDashboardPreference, UserWidgetSettings

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type', 'refresh_rate', 'is_active']
    list_filter = ['widget_type', 'is_active']
    search_fields = ['name']
    ordering = ['name']
    list_editable = ['is_active']

@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_sales', 'total_orders', 'average_order_value', 'active_tables']
    list_filter = ['date']
    search_fields = ['date']
    ordering = ['-date']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(UserDashboardPreference)
class UserDashboardPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'layout']
    list_filter = ['layout']
    search_fields = ['user__username']

@admin.register(UserWidgetSettings)
class UserWidgetSettingsAdmin(admin.ModelAdmin):
    list_display = ['user_preference', 'widget', 'position', 'is_visible']
    list_filter = ['is_visible']
    search_fields = ['user_preference__user__username', 'widget__name']
    ordering = ['position']
    list_editable = ['position', 'is_visible']
