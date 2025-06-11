from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from .models import DailyReport, MonthlyReport, SalesAnalytics
from orders.models import Order
from inventory.models import InventoryTransaction
from staff.models import Employee, Attendance
from datetime import datetime, timedelta

class ReportsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Get latest daily report
        context['daily_report'] = DailyReport.objects.filter(
            date=today
        ).first()
        
        # Get latest monthly report
        context['monthly_report'] = MonthlyReport.objects.filter(
            year=today.year,
            month=today.month
        ).first()
        
        return context

class DailyReportListView(LoginRequiredMixin, ListView):
    model = DailyReport
    template_name = 'reports/daily_report_list.html'
    context_object_name = 'reports'
    ordering = ['-date']
    paginate_by = 30

class DailyReportDetailView(LoginRequiredMixin, DetailView):
    model = DailyReport
    template_name = 'reports/daily_report_detail.html'
    context_object_name = 'report'

class DailyReportCreateView(LoginRequiredMixin, CreateView):
    model = DailyReport
    template_name = 'reports/daily_report_form.html'
    fields = ['date']
    success_url = reverse_lazy('reports:daily-report-list')

    def form_valid(self, form):
        form.instance.generated_by = self.request.user
        response = super().form_valid(form)
        self.object.generate_report()
        return response

class DailyReportUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyReport
    template_name = 'reports/daily_report_form.html'
    fields = ['date']
    
    def get_success_url(self):
        return reverse_lazy('reports:daily-report-detail', kwargs={'pk': self.object.pk})

class GenerateDailyReportView(LoginRequiredMixin, CreateView):
    model = DailyReport
    template_name = 'reports/generate_daily_report.html'
    fields = ['date']
    success_url = reverse_lazy('reports:daily-report-list')

    def form_valid(self, form):
        form.instance.generated_by = self.request.user
        response = super().form_valid(form)
        self.object.generate_report()
        return response

class MonthlyReportListView(LoginRequiredMixin, ListView):
    model = MonthlyReport
    template_name = 'reports/monthly_report_list.html'
    context_object_name = 'reports'
    ordering = ['-year', '-month']
    paginate_by = 12

class MonthlyReportDetailView(LoginRequiredMixin, DetailView):
    model = MonthlyReport
    template_name = 'reports/monthly_report_detail.html'
    context_object_name = 'report'

class MonthlyReportCreateView(LoginRequiredMixin, CreateView):
    model = MonthlyReport
    template_name = 'reports/monthly_report_form.html'
    fields = ['year', 'month']
    success_url = reverse_lazy('reports:monthly-report-list')

    def form_valid(self, form):
        form.instance.generated_by = self.request.user
        response = super().form_valid(form)
        self.object.generate_report()
        return response

class MonthlyReportUpdateView(LoginRequiredMixin, UpdateView):
    model = MonthlyReport
    template_name = 'reports/monthly_report_form.html'
    fields = ['year', 'month']
    
    def get_success_url(self):
        return reverse_lazy('reports:monthly-report-detail', kwargs={'pk': self.object.pk})

class GenerateMonthlyReportView(LoginRequiredMixin, CreateView):
    model = MonthlyReport
    template_name = 'reports/generate_monthly_report.html'
    fields = ['year', 'month']
    success_url = reverse_lazy('reports:monthly-report-list')

    def form_valid(self, form):
        form.instance.generated_by = self.request.user
        response = super().form_valid(form)
        self.object.generate_report()
        return response

class SalesAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/sales_analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Get today's analytics
        context['today_analytics'] = SalesAnalytics.objects.filter(
            date=today
        ).order_by('hour')
        
        # Calculate daily totals
        context['daily_totals'] = Order.objects.filter(
            created_at__date=today,
            status='COMPLETED'
        ).aggregate(
            total_sales=Sum('total'),
            order_count=Count('id'),
            average_order=Avg('total')
        )
        
        return context

class SalesByCategoryView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/sales_by_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add sales by category data
        return context

class SalesByItemView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/sales_by_item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add sales by item data
        return context

class SalesByHourView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/sales_by_hour.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add sales by hour data
        return context

class SalesTrendsView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/sales_trends.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add sales trends data
        return context
