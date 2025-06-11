from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard overview
    path('', views.ReportsDashboardView.as_view(), name='reports-dashboard'),
    
    # Daily Reports
    path('daily/', views.DailyReportListView.as_view(), name='daily-report-list'),
    path('daily/create/', views.DailyReportCreateView.as_view(), name='daily-report-create'),
    path('daily/<int:pk>/', views.DailyReportDetailView.as_view(), name='daily-report-detail'),
    path('daily/<int:pk>/update/', views.DailyReportUpdateView.as_view(), name='daily-report-update'),
    path('daily/generate/', views.GenerateDailyReportView.as_view(), name='generate-daily-report'),
    
    # Monthly Reports
    path('monthly/', views.MonthlyReportListView.as_view(), name='monthly-report-list'),
    path('monthly/create/', views.MonthlyReportCreateView.as_view(), name='monthly-report-create'),
    path('monthly/<int:pk>/', views.MonthlyReportDetailView.as_view(), name='monthly-report-detail'),
    path('monthly/<int:pk>/update/', views.MonthlyReportUpdateView.as_view(), name='monthly-report-update'),
    path('monthly/generate/', views.GenerateMonthlyReportView.as_view(), name='generate-monthly-report'),
    
    # Sales Analytics
    path('sales/', views.SalesAnalyticsView.as_view(), name='sales-analytics'),
    path('sales/by-category/', views.SalesByCategoryView.as_view(), name='sales-by-category'),
    path('sales/by-item/', views.SalesByItemView.as_view(), name='sales-by-item'),
    path('sales/by-hour/', views.SalesByHourView.as_view(), name='sales-by-hour'),
    path('sales/trends/', views.SalesTrendsView.as_view(), name='sales-trends'),
]
