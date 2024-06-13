from django.urls import path

from .views import SignupPageView, profile_view

app_name = 'users'

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('profile/', profile_view, name='profile'),
]
