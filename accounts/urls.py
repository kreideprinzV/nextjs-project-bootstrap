from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Password management
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='password-change-done'
    ), name='password-change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password-change-done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password-reset-confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password-reset-complete'),
    
    # Profile management
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/theme/', views.UpdateThemeView.as_view(), name='update-theme'),
    path('profile/language/', views.UpdateLanguageView.as_view(), name='update-language'),
    
    # Notification settings
    path('notifications/', views.NotificationSettingsView.as_view(), name='notification-settings'),
    path('notifications/update/', views.UpdateNotificationSettingsView.as_view(), name='update-notifications'),
    path('notifications/test/', views.TestNotificationView.as_view(), name='test-notification'),
    
    # Activity history
    path('activity/', views.UserActivityView.as_view(), name='user-activity'),
    path('activity/<int:pk>/', views.ActivityDetailView.as_view(), name='activity-detail'),
    path('login-history/', views.LoginHistoryView.as_view(), name='login-history'),
    
    # API endpoints for AJAX requests
    path('api/check-username/', views.CheckUsernameView.as_view(), name='check-username'),
    path('api/check-email/', views.CheckEmailView.as_view(), name='check-email'),
    path('api/update-notification/', views.UpdateNotificationSettingView.as_view(), name='update-notification'),
]
