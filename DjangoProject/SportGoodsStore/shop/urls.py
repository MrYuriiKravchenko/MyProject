from django.urls import path
from .views import ProductListView, ProductDetailView, SearchResultsListView

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
]
