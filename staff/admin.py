from django.contrib import admin
from .models import Employee, Schedule, Attendance, Leave

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'phone', 'date_hired', 'is_active']
    list_filter = ['position', 'is_active', 'date_hired']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    ordering = ['user__last_name', 'user__first_name']
    list_editable = ['is_active']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'shift', 'start_time', 'end_time']
    list_filter = ['date', 'shift']
    search_fields = ['employee__user__username', 'employee__user__first_name', 'employee__user__last_name']
    ordering = ['-date', 'start_time']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'schedule', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['employee__user__username', 'employee__user__first_name', 'employee__user__last_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'status']
    list_filter = ['leave_type', 'status', 'start_date']
    search_fields = ['employee__user__username', 'employee__user__first_name', 'employee__user__last_name']
    ordering = ['-start_date']
    list_editable = ['status']
