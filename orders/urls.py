from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order URLs
    path('', views.OrderListView.as_view(), name='order-list'),
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order-delete'),
    
    # Table URLs
    path('tables/', views.TableListView.as_view(), name='table-list'),
    path('tables/create/', views.TableCreateView.as_view(), name='table-create'),
    path('tables/<int:pk>/', views.TableDetailView.as_view(), name='table-detail'),
    path('tables/<int:pk>/update/', views.TableUpdateView.as_view(), name='table-update'),
    path('tables/<int:pk>/delete/', views.TableDeleteView.as_view(), name='table-delete'),
    
    # Order status management
    path('<int:pk>/mark-preparing/', views.MarkOrderPreparingView.as_view(), name='mark-preparing'),
    path('<int:pk>/mark-ready/', views.MarkOrderReadyView.as_view(), name='mark-ready'),
    path('<int:pk>/mark-served/', views.MarkOrderServedView.as_view(), name='mark-served'),
    path('<int:pk>/mark-completed/', views.MarkOrderCompletedView.as_view(), name='mark-completed'),
    path('<int:pk>/mark-cancelled/', views.MarkOrderCancelledView.as_view(), name='mark-cancelled'),
]
