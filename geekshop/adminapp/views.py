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
# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка | пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)


class UserCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_create.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'пользователи | создать'
        return context

# def user_create(request):
#     title = 'пользователи | создать'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': title,
#         'user_form': user_form
#     }
#
#     return render(request, 'adminapp/user_create.html', context)


class UserUpdateView(UpdateView):
    model = ShopUser
    form_class = ShopUserEditForm  # ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = 'пользователи | редактировать'
        return context

# def user_update(request, pk):
#     title = 'пользователи | редактировать'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': title,
#         'user_form': edit_form
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


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


# def user_delete(request, pk):
#     title = 'пользователи | удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         user.is_deleted = True
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     context = {
#         'title': title,
#         'user_to_delete': user
#     }
#
#     return render(request, 'adminapp/user_delete.html', context)

class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesListView, self).get_context_data()
        context['title'] = 'админка | категории'
        return context

# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка | категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     context = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', context)


class CategoryCreateView(CreateView):
    model = ProductCategory
    form_class = ProductCategoryCreateForm
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data()
        context['title'] = 'категории | создать'
        return context
# def category_create(request):
#     title = 'категории | создать'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryCreateForm(request.POST, request.FILES)
#
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#     else:
#         category_form = ProductCategoryCreateForm()
#
#     context = {
#         'title': title,
#         'category_form': category_form
#     }
#
#     return render(request, 'adminapp/category_create.html', context)


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data()
        context['title'] = 'категории | редактировать'
        return context
# def category_update(request, pk):
#     title = 'категории | редактировать'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#
#     context = {
#         'title': title,
#         'category_form': edit_form
#     }
#
#     return render(request, 'adminapp/category_update.html', context)


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
# def category_delete(request, pk):
#     title = 'категории | удаление'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category.is_deleted = True
#         category.save()
#         return HttpResponseRedirect(reverse('admin_staff:categories'))
#
#     context = {
#         'title': title,
#         'category_to_delete': category
#     }
#
#     return render(request, 'adminapp/category_delete.html', context)


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
# def products(request, pk):
#     title = 'админка | продукт'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     context = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', context)


# class ProductCreateView(CreateView):
#     model = Product
#     form_class = ProductEditForm
#     template_name = 'adminapp/product_create.html'
#     success_url = reverse_lazy('admin_staff:products')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ProductCreateView, self).get_context_data()
#         context['title'] = 'продукты | создание'
#         return context


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
# def product_create(request, pk):
#     title = 'продукты | создание'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#
#             return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
#     else:
#         product_form = ProductEditForm(initial={'category': category})
#
#     context = {
#         'title': title,
#         'update_form': product_form,
#         'category': category,
#     }
#
#     return render(request, 'adminapp/product_create.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['title'] = 'продукты | подробнее'
        return context
# def product_read(request, pk):
#     title = 'продукты | подробнее'
#
#     product = get_object_or_404(Product, pk=pk)
#
#     context = {
#         'title': title,
#         'product': product
#     }
#
#     return render(request, 'adminapp/product_read.html', context)


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
# def product_update(request, pk):
#     title = 'продукты | редактирование'
#
#     edit_product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
#
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:products', args=[edit_product.category.pk]))
#     else:
#         edit_form = ProductEditForm(instance=edit_product)
#
#     context = {
#         'title': title,
#         'update_form': edit_form,
#         'category': edit_product.category,
#         'product': edit_product,
#     }
#
#     return render(request, 'adminapp/product_update.html', context)


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
# def product_delete(request, pk):
#     title = 'продукты | редактирование'
#
#     product = get_object_or_404(Product, pk=pk)
#
#     if request.method == 'POST':
#         product.is_deleted = True
#         product.save()
#         return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))
#
#     context = {
#         'title': title,
#         'product_to_delete': product
#     }
#
#     return render(request, 'adminapp/product_delete.html', context)
