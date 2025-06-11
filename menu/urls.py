from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.MenuItemListView.as_view(), name='menu-list'),
    path('create/', views.MenuItemCreateView.as_view(), name='menu-create'),
    path('<int:pk>/', views.MenuItemDetailView.as_view(), name='menu-detail'),
    path('<int:pk>/update/', views.MenuItemUpdateView.as_view(), name='menu-update'),
    path('<int:pk>/delete/', views.MenuItemDeleteView.as_view(), name='menu-delete'),
    
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
]
