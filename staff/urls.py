from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    # Employee URLs
    path('', views.EmployeeListView.as_view(), name='staff-list'),
    path('create/', views.EmployeeCreateView.as_view(), name='staff-create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='staff-detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='staff-update'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='staff-delete'),
    
    # Schedule URLs
    path('schedules/', views.ScheduleListView.as_view(), name='schedule-list'),
    path('schedules/create/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/<int:pk>/', views.ScheduleDetailView.as_view(), name='schedule-detail'),
    path('schedules/<int:pk>/update/', views.ScheduleUpdateView.as_view(), name='schedule-update'),
    path('schedules/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
    
    # Attendance URLs
    path('attendance/', views.AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/create/', views.AttendanceCreateView.as_view(), name='attendance-create'),
    path('attendance/<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
    path('attendance/<int:pk>/update/', views.AttendanceUpdateView.as_view(), name='attendance-update'),
    
    # Leave URLs
    path('leaves/', views.LeaveListView.as_view(), name='leave-list'),
    path('leaves/create/', views.LeaveCreateView.as_view(), name='leave-create'),
    path('leaves/<int:pk>/', views.LeaveDetailView.as_view(), name='leave-detail'),
    path('leaves/<int:pk>/update/', views.LeaveUpdateView.as_view(), name='leave-update'),
    path('leaves/<int:pk>/approve/', views.LeaveApproveView.as_view(), name='leave-approve'),
    path('leaves/<int:pk>/reject/', views.LeaveRejectView.as_view(), name='leave-reject'),
]
