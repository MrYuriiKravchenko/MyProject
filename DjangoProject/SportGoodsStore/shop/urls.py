from django.urls import path

from . import views
from .views import ProductListView, ProductDetailView, SearchResultsListView, AboutPageView

app_name = 'shop'

urlpatterns = [
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('', ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('about/', AboutPageView.as_view(), name='about'),
]
