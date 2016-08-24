from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    FormView,
)
import requests
from .forms import AddProductForm

# Create your views here.


class IndexListView(ListView):
    # form_class = SearchProduct
    context_object_name = 'products'
    template_name = 'index.html'
    paginate_by = 6

    def get_queryset(self):
        all_products = requests.get(
            'http://127.0.0.1:8000/api/products/?format=json'
        ).json()
        # form = self.form_class(self.request.GET)
        # form.is_valid()
        # if self.request.GET:
        #     if self.request.GET['name'] and self.request.GET['ordering']:
        #         q = Products.objects.filter(
        #             name__icontains=form.cleaned_data['name']).order_by(
        #             form.cleaned_data['ordering'])
        #     elif self.request.GET['ordering']:
        #         q = Products.objects.all().order_by(
        #             form.cleaned_data['ordering'])
        #     else:
        #         q = Products.objects.filter(
        #             name__icontains=form.cleaned_data['name'])
        #     return q
        return all_products

    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        # if self.request.GET.get('name'):
        #     context['search_name'] = self.request.GET.get('name')
        # if self.request.GET.get('ordering'):
        #     context['search_ordering'] = self.request.GET.get('ordering')
        context['categories'] = requests.get(
            'http://127.0.0.1:8000/api/categories/?format=json'
        ).json()
        return context


class ProductsListView(ListView):
    context_object_name = 'products'
    template_name = 'products.html'
    paginate_by = 6

    def get_queryset(self):
        # self.category = get_object_or_404(Categories, id=self.args[0])
        products = requests.get(
            'http://127.0.0.1:8000/api/products/?format=json'
        ).json()
        my_products = []
        for product in products:
            if product['category'] == int(self.args[0]):
                my_products.append(product)
        return my_products

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['categories'] = requests.get(
            'http://127.0.0.1:8000/api/categories/?format=json'
        ).json()
        return context


class DeleteProductView(View):

    def get(self, request, *args, **kwargs):
        product = requests.get('http://127.0.0.1:8000/api/products/%s/' %
                               (int(kwargs['pk']))).json()
        requests.delete('http://127.0.0.1:8000/api/products/%s/' %
                             (int(kwargs['pk'])))
        return redirect(to='/%s/' % product['category'])


class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        product = requests.get('http://127.0.0.1:8000/api/products/%s/' %
                               (int(kwargs['pk']))).json()
        categories = requests.get(
            'http://127.0.0.1:8000/api/categories/?format=json'
        ).json()
        context = {
            'product': product,
            'categories': categories,
        }
        return render(request, 'product.html', context)


class AddProductView(FormView):
    form_class = AddProductForm
    template_name = 'add_product.html'

    def get_context_data(self, **kwargs):
        context = super(AddProductView, self).get_context_data(**kwargs)
        context['categories'] = requests.get(
            'http://127.0.0.1:8000/api/categories/?format=json'
        ).json()
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        hi = requests.post(
            'http://localhost:8000/api/products/',
            {
                "name": request.POST.get('name', False),
                "description": request.POST.get('description', False),
                "category": request.POST.get('category', False),
                "image": request.POST.get('image', False),
                "size": request.POST.get('size', False),
                "colour": request.POST.get('colour', False),
                "price": request.POST.get('price', False),
                "quantity": request.POST.get('quantity', False),
            }
        ).json()
        print(hi)
        return HttpResponseRedirect('/')


# class LoginUser(FormView):
#     form_class = AuthenticationForm
#     template_name = 'login.html'
#     success_url = '/'
#
#     def form_valid(self, form):
#         self.user = form.get_user()
#         login(self.request, self.user)
#         return super(LoginUser, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(LoginUser, self).get_context_data(**kwargs)
#         context['categories'] = Categories.objects.all()
#         return context


class CartView(TemplateView):
    template_name = 'cart.html'

    def post(self, request, *args, **kwargs):
        my_lists = request.session.get('cart', False)
        for product in my_lists:
            if int(request.POST.get('product_id', False)) == int(product['id']):
                this_product = requests.get(
                    'http://127.0.0.1:8000/api/products/%s/' %
                    (int(request.POST.get('product_id', False)))
                ).json()
                request.session['total_cart'] -= product['price']
                price = this_product['price'] * int(
                    request.POST.get('new_quantity', False))
                product['price'] = price
                if product['quantity_in_cart'] < product['quantity']:
                    product['quantity_in_cart'] = int(request.POST.get(
                        'new_quantity', False))
                request.session['total_cart'] += product['price']
        request.session['cart'] = my_lists
        return HttpResponseRedirect('/cart/')

    def get(self, request, *args, **kwargs):
        if not request.session.get('cart', False):
            request.session['cart'] = list()
            request.session['total_cart'] = 0
        if request.GET.get('product', False):
            my_lists = request.session.get('cart', False)
            product = requests.get(
                'http://127.0.0.1:8000/api/products/%s/' %
                (int(request.GET.get('product', False)))
            ).json()
            product['quantity_in_cart'] = 1
            my_lists.append(product)
            request.session['cart'] = my_lists
            request.session['total_cart'] += product['price']
            return HttpResponseRedirect('/cart/')
        if request.GET.get('delete', False):
            my_lists = request.session.get('cart', False)
            for prod in my_lists:
                if prod['id'] == int(request.GET.get('delete', False)):
                    request.session['total_cart'] -= prod['price']
                    my_lists.remove(prod)
                    request.session['cart'] = my_lists
            return HttpResponseRedirect('/cart/')
        return super(CartView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['categories'] = requests.get(
            'http://127.0.0.1:8000/api/categories/?format=json'
        ).json()
        return context


class MakeOrderView(TemplateView):
    template_name = "make_order.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            u = requests.get(
                'http://localhost:8000/api/users/%s/?format=json' % (request.user.id)
            ).json()
            # u = MyUsers.objects.get(user_id=request.user.id)
            self.user_id = u['id']
        else:
            self.user_id = None
        return super(MakeOrderView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MakeOrderView, self).get_context_data(**kwargs)
        context['categories'] = requests.get(
            'http://127.0.0.1:8000/api/categories/?format=json'
        ).json()
        if self.user_id:
            context['user_all_info'] = requests.get(
                'http://localhost:8000/api/users/%s/?format=json' % (self.user_id)
            ).json()
        return context
