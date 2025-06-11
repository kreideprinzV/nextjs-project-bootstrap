from django.views.generic import CreateView, UpdateView, DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import UserProfile, LoginHistory, UserNotificationSetting, UserActivity

class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        # Set password properly
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Account created successfully. Please log in.')
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_activities'] = self.request.user.activities.all()[:5]
        context['recent_logins'] = self.request.user.login_history.all()[:5]
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'accounts/profile_edit.html'
    fields = ['theme_preference', 'language_preference', 'receive_notifications']
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

class UpdateThemeView(LoginRequiredMixin, View):
    def post(self, request):
        theme = request.POST.get('theme')
        if theme in ['LIGHT', 'DARK']:
            request.user.profile.theme_preference = theme
            request.user.profile.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid theme'})

class UpdateLanguageView(LoginRequiredMixin, View):
    def post(self, request):
        language = request.POST.get('language')
        if language in ['en', 'es', 'fr']:
            request.user.profile.language_preference = language
            request.user.profile.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid language'})

class NotificationSettingsView(LoginRequiredMixin, ListView):
    model = UserNotificationSetting
    template_name = 'accounts/notification_settings.html'
    context_object_name = 'notification_settings'

    def get_queryset(self):
        return self.request.user.notification_settings.all()

class UpdateNotificationSettingsView(LoginRequiredMixin, View):
    def post(self, request):
        notification_type = request.POST.get('notification_type')
        email_enabled = request.POST.get('email_enabled') == 'true'
        push_enabled = request.POST.get('push_enabled') == 'true'

        setting = request.user.notification_settings.filter(
            notification_type=notification_type
        ).first()

        if setting:
            setting.email_enabled = email_enabled
            setting.push_enabled = push_enabled
            setting.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid notification type'})

class TestNotificationView(LoginRequiredMixin, View):
    def post(self, request):
        notification_type = request.POST.get('notification_type')
        setting = request.user.notification_settings.filter(
            notification_type=notification_type
        ).first()

        if setting:
            # Send test notification logic would go here
            messages.success(request, f'Test notification sent for {notification_type}')
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid notification type'})

class UserActivityView(LoginRequiredMixin, ListView):
    model = UserActivity
    template_name = 'accounts/user_activity.html'
    context_object_name = 'activities'
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.activities.all()

class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = UserActivity
    template_name = 'accounts/activity_detail.html'
    context_object_name = 'activity'

    def get_queryset(self):
        return self.request.user.activities.all()

class LoginHistoryView(LoginRequiredMixin, ListView):
    model = LoginHistory
    template_name = 'accounts/login_history.html'
    context_object_name = 'login_history'
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.login_history.all()

class CheckUsernameView(View):
    def get(self, request):
        username = request.GET.get('username', '')
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})

class CheckEmailView(View):
    def get(self, request):
        email = request.GET.get('email', '')
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})

class UpdateNotificationSettingView(LoginRequiredMixin, View):
    def post(self, request):
        setting_id = request.POST.get('setting_id')
        enabled = request.POST.get('enabled') == 'true'
        
        try:
            setting = UserNotificationSetting.objects.get(
                id=setting_id,
                user=request.user
            )
            setting.email_enabled = enabled
            setting.save()
            return JsonResponse({'status': 'success'})
        except UserNotificationSetting.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Notification setting not found'
            })
