from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .views import ProductListView, ProductDetailView, SearchResultsListView, AboutPageView, WishlistView, \
    RemoveFromWishlistView, AddToWishlistView

app_name = 'shop'

urlpatterns = [
    path('wishlist/add/<int:product_id>/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('', ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('about/', AboutPageView.as_view(), name='about'),
]
