from django.urls import path
from . import views
from .views import OrderCreateView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
]