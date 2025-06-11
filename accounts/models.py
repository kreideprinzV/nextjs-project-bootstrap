from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    THEME_CHOICES = [
        ('LIGHT', 'Light Theme'),
        ('DARK', 'Dark Theme'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    theme_preference = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='LIGHT'
    )
    language_preference = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    receive_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile - {self.user.username}"

class LoginHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_history'
    )
    login_datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=True)

    class Meta:
        ordering = ['-login_datetime']
        verbose_name_plural = 'Login Histories'

    def __str__(self):
        status = 'Success' if self.success else 'Failed'
        return f"{self.user.username} - {status} - {self.login_datetime}"

class UserNotificationSetting(models.Model):
    NOTIFICATION_TYPES = [
        ('ORDER_STATUS', 'Order Status Updates'),
        ('INVENTORY_ALERTS', 'Inventory Alerts'),
        ('STAFF_UPDATES', 'Staff Updates'),
        ('REPORTS', 'Report Generation'),
        ('SYSTEM', 'System Notifications'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_settings'
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'notification_type']

    def __str__(self):
        return f"{self.user.username} - {self.get_notification_type_display()}"

class UserActivity(models.Model):
    ACTION_TYPES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('VIEW', 'View'),
        ('EXPORT', 'Export'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    action = models.CharField(max_length=10, choices=ACTION_TYPES)
    content_type = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.content_type}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)
        
        # Create default notification settings for the user
        for notification_type, _ in UserNotificationSetting.NOTIFICATION_TYPES:
            UserNotificationSetting.objects.create(
                user=instance,
                notification_type=notification_type
            )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    instance.profile.save()
