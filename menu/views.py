from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MenuItem, Category

class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'menu/menu_list.html'
    context_object_name = 'menu_items'
    paginate_by = 12
    ordering = ['category', 'name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class MenuItemDetailView(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = 'menu/menu_detail.html'
    context_object_name = 'menu_item'

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = 'menu/menu_form.html'
    fields = ['name', 'category', 'description', 'price', 'image_url', 'is_available']
    success_url = reverse_lazy('menu:menu-list')

class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    template_name = 'menu/menu_form.html'
    fields = ['name', 'category', 'description', 'price', 'image_url', 'is_available']
    success_url = reverse_lazy('menu:menu-list')

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'menu/menu_confirm_delete.html'
    success_url = reverse_lazy('menu:menu-list')

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'menu/category_list.html'
    context_object_name = 'categories'
    ordering = ['name']

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'menu/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = self.object.menu_items.all()
        return context

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'menu/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('menu:category-list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'menu/category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('menu:category-list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'menu/category_confirm_delete.html'
    success_url = reverse_lazy('menu:category-list')
