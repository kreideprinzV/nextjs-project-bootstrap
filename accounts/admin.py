from django.contrib import admin
from .models import UserProfile, UserActivity, LoginHistory, UserNotificationSetting

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme_preference', 'language_preference', 'receive_notifications']
    search_fields = ['user__username', 'user__email']
    list_filter = ['theme_preference', 'language_preference', 'receive_notifications']

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'content_type', 'timestamp']
    search_fields = ['user__username', 'action', 'content_type']
    list_filter = ['action', 'content_type', 'timestamp']
    readonly_fields = ['timestamp']

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'login_datetime', 'ip_address', 'user_agent']
    search_fields = ['user__username', 'ip_address']
    list_filter = ['login_datetime', 'success']
    readonly_fields = ['login_datetime']

@admin.register(UserNotificationSetting)
class UserNotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'email_enabled', 'push_enabled']
    search_fields = ['user__username', 'notification_type']
    list_filter = ['notification_type', 'email_enabled', 'push_enabled']
