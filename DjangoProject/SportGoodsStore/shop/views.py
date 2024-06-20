from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Category, Rating, Comment
from cart.forms import CartAddProductForm
from .forms import ProductFilterForm, RatingForm, CommentForm
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
        user = self.request.user

        context['cart_product_form'] = CartAddProductForm()
        context['rating_form'] = RatingForm()
        context['comment_form'] = CommentForm()
        context['average_rating'] = product.ratings.aggregate(Avg('score'))['score__avg']
        context['comments'] = product.comments.all()

        if user.is_authenticated:
            user_rating = product.ratings.filter(user=user).first()
            context['rating_value'] = user_rating.score if user_rating else None
        else:
            context['rating_value'] = None

        r = Recommender()
        recommended_products = r.suggest_products_for([product], 4)
        context['recommended_products'] = recommended_products
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        product = self.get_object()
        if 'rating' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating, created = Rating.objects.update_or_create(
                    product=product,
                    user=request.user,
                    defaults={'score': rating_form.cleaned_data['score']}
                )
                average_rating = product.ratings.aggregate(Avg('score'))['score__avg']
                return JsonResponse({
                    'average_rating': average_rating,
                    'user_rating': rating.score
                })
        elif 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                Comment.objects.create(
                    product=product,
                    user=request.user,
                    text=comment_form.cleaned_data['text']
                )
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error'}, status=400)


class SearchResultsListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'shop/product/search_results.html'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query) | Q(price__icontains=query)
        )


class AboutPageView(TemplateView):
    template_name = 'about.html'
