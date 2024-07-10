from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from .models import Product, Category, Rating, Comment, Wishlist
from cart.forms import CartAddProductForm
from .forms import ProductFilterForm, RatingForm, CommentForm
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
        elif sort_by == 'rating_asc':
            queryset = queryset.annotate(average_rating=Avg('ratings__score')).order_by('average_rating')
        elif sort_by == 'rating_desc':
            queryset = queryset.annotate(average_rating=Avg('ratings__score')).order_by('-average_rating')
        else:
            queryset = queryset.order_by('-created')

        queryset = queryset.annotate(average_rating=Avg('ratings__score'))

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

        if self.request.user.is_authenticated:
            context['user_wishlist'] = self.request.user.wishlists.values_list('product_id', flat=True)
        else:
            context['user_wishlist'] = []

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
        average_rating = product.ratings.aggregate(Avg('score'))['score__avg']
        if average_rating is not None:
            context['average_rating'] = round(average_rating, 1)
        else:
            context['average_rating'] = None
        context['comments'] = product.comments.all()

        if user.is_authenticated:
            user_rating = product.ratings.filter(user=user).first()
            context['rating_value'] = user_rating.score if user_rating else None
            context['user_commented'] = product.comments.filter(user=user).exists()
        else:
            context['rating_value'] = None
            context['user_commented'] = False

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
                    'average_rating': round(average_rating, 1),
                    'user_rating': rating.score
                })
        elif 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                if Comment.objects.filter(product=product, user=request.user).exists():
                    return JsonResponse({'status': 'error', 'message': 'You have already commented on this product.'},
                                        status=400)
                Comment.objects.create(
                    product=product,
                    user=request.user,
                    text=comment_form.cleaned_data['text']
                )
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'Invalid comment data.'}, status=400)



class SearchResultsListView(ListView):
    model = Product
    template_name = 'shop/product/search_results.html'
    context_object_name = 'product_list'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query
        return context

class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = (
            "SportGoodsStore предлагает широкий выбор спортивных товаров от ведущих мировых брендов "
            "для любителей активного образа жизни. Наша цель - вдохновить клиентов на достижение "
            "спортивных целей с помощью качественных товаров и персонализированного сервиса. Мы гордимся "
            "предоставлением клиентам только лучших решений для здоровья и фитнеса, делая каждую покупку "
            "удобной и приятной.")
        context['mission'] = (
            "Миссия SportGoodsStore заключается в предоставлении клиентам доступа к высококачественным "
            "спортивным товарам и инновационным решениям, способствующим активному образу жизни и достижению "
            "спортивных целей. Мы стремимся вдохновлять и поддерживать наших клиентов, обеспечивая оптимальное "
            "соотношение цены и качества, а также надежный и персонализированный сервис на каждом этапе сотрудничества.")
        return context


class AddToWishlistView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        if Wishlist.objects.filter(user=user, product=product).exists():
            return JsonResponse({'status': 'exists'}, status=400)

        Wishlist.objects.create(user=user, product=product)
        return JsonResponse({'status': 'added'})


class RemoveFromWishlistView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        wishlist_item = Wishlist.objects.filter(user=user, product=product).select_related('product')
        if wishlist_item.exists():
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'not_found'}, status=400)


class WishlistView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'shop/wishlist.html'
    context_object_name = 'wishlist_items'
    login_url = 'account_login'

    def get_queryset(self):
        queryset = Wishlist.objects.filter(user=self.request.user).select_related('product').order_by('-created')
        for item in queryset:
            item.product.average_rating = item.product.ratings.aggregate(Avg('score'))['score__avg']
        return queryset
