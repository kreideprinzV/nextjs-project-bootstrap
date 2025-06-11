from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Inventory Item URLs
    path('', views.InventoryItemListView.as_view(), name='inventory-list'),
    path('create/', views.InventoryItemCreateView.as_view(), name='inventory-create'),
    path('<int:pk>/', views.InventoryItemDetailView.as_view(), name='inventory-detail'),
    path('<int:pk>/update/', views.InventoryItemUpdateView.as_view(), name='inventory-update'),
    path('<int:pk>/delete/', views.InventoryItemDeleteView.as_view(), name='inventory-delete'),
    
    # Supplier URLs
    path('suppliers/', views.SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier-create'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier-detail'),
    path('suppliers/<int:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier-update'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier-delete'),
    
    # Transaction URLs
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/create/', views.TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    
    # Additional functionality
    path('low-stock/', views.LowStockItemsView.as_view(), name='low-stock'),
    path('reorder-report/', views.ReorderReportView.as_view(), name='reorder-report'),
    path('stock-adjustment/', views.StockAdjustmentView.as_view(), name='stock-adjustment'),
    path('export-inventory/', views.ExportInventoryView.as_view(), name='export-inventory'),
]
