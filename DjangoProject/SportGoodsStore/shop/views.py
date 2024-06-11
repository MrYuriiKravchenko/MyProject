from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category
from cart.forms import CartAddProductForm
from .forms import ProductFilterForm
from django.core.paginator import Paginator
from .recommender import Recommender


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        sort_by = self.request.GET.get('sort_by')
        queryset = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        if sort_by == 'asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'desc':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['categories'] = Category.objects.all()
        if category_slug:
            context['category'] = get_object_or_404(Category, slug=category_slug)
        else:
            context['category'] = None

        context['filter_form'] = ProductFilterForm(self.request.GET)

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_object(self):
        id = self.kwargs.get('id')
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product, id=id, slug=slug, available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['cart_product_form'] = CartAddProductForm()

        r = Recommender()
        recommended_products = r.suggest_products_for([product], 4)
        context['recommended_products'] = recommended_products
        return context


class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'shop/product/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query) | Q(price__icontains=query)
        )