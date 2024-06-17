from django.urls import path

from .views import SignupPageView, ProfileView, PurchaseStatisticsView

app_name = 'users'

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/purchase-statistics/', PurchaseStatisticsView.as_view(), name='purchase_statistics'),
]
