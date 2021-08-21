from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductCategoryCreateForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data()
        context['title'] = 'админка | пользователи'
        # context.update({'title': 'админка | пользователи'})  # можно и так
        return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')


class UserCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_create.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'пользователи | создать'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopUserEditForm  # ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = 'пользователи | редактировать'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    context_object_name = 'user_to_delete'
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesListView, self).get_context_data()
        context['title'] = 'админка | категории'
        return context


class CategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryCreateForm
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data()
        context['title'] = 'категории | создать'
        return context


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'категории | редактировать'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    context_object_name = 'category_to_delete'
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_staff:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk')).order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))

        context['title'] = 'админка | продукт'
        context['category'] = category
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_create.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data()
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))

        context['title'] = 'продукты | создание'
        context['category'] = category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['title'] = 'продукты | подробнее'
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        category = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))

        context['title'] = 'продукты | редактирование'
        context['category'] = category
        return context


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product_to_delete'
    template_name = 'adminapp/product_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        self.success_url = reverse('admin_staff:products', args=[self.get_object().category.pk])

        return HttpResponseRedirect(self.get_success_url())


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_deleted_update_product_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_deleted:
            instance.product_set.update(is_deleted=True)
        else:
            instance.product_set.update(is_deleted=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
