from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Employee, Schedule, Attendance, Leave
from django.contrib.auth.models import User
from django.utils import timezone

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'staff/employee_list.html'
    context_object_name = 'employees'
    ordering = ['user__last_name', 'user__first_name']

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'staff/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedules'] = self.object.schedules.filter(
            date__gte=timezone.now().date()
        ).order_by('date', 'start_time')[:5]
        context['recent_attendance'] = self.object.attendance.order_by('-created_at')[:5]
        context['leaves'] = self.object.leaves.order_by('-start_date')[:5]
        return context

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = 'staff/employee_form.html'
    fields = ['position', 'phone', 'address', 'emergency_contact', 'emergency_phone', 
              'date_hired', 'hourly_rate']
    success_url = reverse_lazy('staff:staff-list')

    def form_valid(self, form):
        # Create User account first
        user = User.objects.create_user(
            username=self.request.POST['username'],
            password=self.request.POST['password'],
            first_name=self.request.POST['first_name'],
            last_name=self.request.POST['last_name'],
            email=self.request.POST['email']
        )
        form.instance.user = user
        return super().form_valid(form)

class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'staff/employee_form.html'
    fields = ['position', 'phone', 'address', 'emergency_contact', 'emergency_phone', 
              'hourly_rate', 'is_active']

    def get_success_url(self):
        return reverse_lazy('staff:staff-detail', kwargs={'pk': self.object.pk})

class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'staff/employee_confirm_delete.html'
    success_url = reverse_lazy('staff:staff-list')

class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'staff/schedule_list.html'
    context_object_name = 'schedules'
    ordering = ['date', 'start_time']

    def get_queryset(self):
        return Schedule.objects.filter(
            date__gte=timezone.now().date()
        ).select_related('employee__user')

class ScheduleDetailView(LoginRequiredMixin, DetailView):
    model = Schedule
    template_name = 'staff/schedule_detail.html'
    context_object_name = 'schedule'

class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    template_name = 'staff/schedule_form.html'
    fields = ['employee', 'date', 'shift', 'start_time', 'end_time', 'notes']
    success_url = reverse_lazy('staff:schedule-list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    template_name = 'staff/schedule_form.html'
    fields = ['employee', 'date', 'shift', 'start_time', 'end_time', 'notes']
    success_url = reverse_lazy('staff:schedule-list')

class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule
    template_name = 'staff/schedule_confirm_delete.html'
    success_url = reverse_lazy('staff:schedule-list')

class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'staff/attendance_list.html'
    context_object_name = 'attendance_records'
    ordering = ['-schedule__date']

class AttendanceDetailView(LoginRequiredMixin, DetailView):
    model = Attendance
    template_name = 'staff/attendance_detail.html'
    context_object_name = 'attendance'

class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    template_name = 'staff/attendance_form.html'
    fields = ['employee', 'schedule', 'status', 'notes']
    success_url = reverse_lazy('staff:attendance-list')

class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Attendance
    template_name = 'staff/attendance_form.html'
    fields = ['status', 'notes']
    success_url = reverse_lazy('staff:attendance-list')

class LeaveListView(LoginRequiredMixin, ListView):
    model = Leave
    template_name = 'staff/leave_list.html'
    context_object_name = 'leaves'
    ordering = ['-start_date']

class LeaveDetailView(LoginRequiredMixin, DetailView):
    model = Leave
    template_name = 'staff/leave_detail.html'
    context_object_name = 'leave'

class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = Leave
    template_name = 'staff/leave_form.html'
    fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
    success_url = reverse_lazy('staff:leave-list')

class LeaveUpdateView(LoginRequiredMixin, UpdateView):
    model = Leave
    template_name = 'staff/leave_form.html'
    fields = ['leave_type', 'start_date', 'end_date', 'reason', 'status']
    success_url = reverse_lazy('staff:leave-list')

class LeaveApproveView(LoginRequiredMixin, UpdateView):
    model = Leave
    template_name = 'staff/leave_approve.html'
    fields = ['status']
    success_url = reverse_lazy('staff:leave-list')

    def form_valid(self, form):
        form.instance.approved_by = self.request.user
        messages.success(self.request, 'Leave request has been approved.')
        return super().form_valid(form)

class LeaveRejectView(LoginRequiredMixin, UpdateView):
    model = Leave
    template_name = 'staff/leave_reject.html'
    fields = ['status']
    success_url = reverse_lazy('staff:leave-list')

    def form_valid(self, form):
        form.instance.approved_by = self.request.user
        messages.success(self.request, 'Leave request has been rejected.')
        return super().form_valid(form)
