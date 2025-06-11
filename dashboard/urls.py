from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', views.DashboardView.as_view(), name='dashboard-home'),
    
    # Widget management
    path('widgets/', views.WidgetListView.as_view(), name='widget-list'),
    path('widgets/create/', views.WidgetCreateView.as_view(), name='widget-create'),
    path('widgets/<int:pk>/update/', views.WidgetUpdateView.as_view(), name='widget-update'),
    path('widgets/<int:pk>/delete/', views.WidgetDeleteView.as_view(), name='widget-delete'),
    
    # User preferences
    path('preferences/', views.UserPreferencesView.as_view(), name='user-preferences'),
    
    # API endpoints for AJAX requests
    path('api/widget-data/<int:widget_id>/', views.WidgetDataView.as_view(), name='widget-data'),
    path('api/update-widget-position/', views.UpdateWidgetPositionView.as_view(), name='update-widget-position'),
    path('api/toggle-widget-visibility/', views.ToggleWidgetVisibilityView.as_view(), name='toggle-widget-visibility'),
]
