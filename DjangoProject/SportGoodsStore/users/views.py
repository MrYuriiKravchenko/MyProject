from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.views.generic import UpdateView
from cart.cart import Cart
from orders.models import OrderItem
from shop.models import Category
from .forms import CustomUserChangeForm, CustomUserCreationForm


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Ваш профиль успешно обновлен')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправте ошибки в форме')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        context['discount'] = cart.get_discount()
        context['total_with_discount'] = cart.get_total_price_after_discount()
        return context


class PurchaseStatisticsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        current_year = datetime.now().year
        categories = Category.objects.all()
        data = {}

        for category in categories:
            monthly_purchases = []
            for month in range(1, 13):
                count = OrderItem.objects.filter(
                    product__category=category,
                    order__created__year=current_year,
                    order__created__month=month
                ).count()
                monthly_purchases.append(count)
            data[category.name] = monthly_purchases

        return JsonResponse(data)