from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .forms import CustomUserChangeForm
from .forms import CustomUserCreationForm


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def profile_view(request):
    user = request.user
    cart = Cart(request)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserChangeForm(instance=user)

    # Получаем информацию о скидке и сумме с учетом скидки
    discount = cart.get_discount()
    total_with_discount = cart.get_total_price_after_discount()

    context = {
        'form': form,
        'cart': cart,
        'discount': discount,
        'total_with_discount': total_with_discount,
    }
    return render(request, 'users/profile.html', context)
