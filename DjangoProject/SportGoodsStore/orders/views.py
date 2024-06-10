from .tasks import order_created
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


class OrderCreateView(FormView):
    template_name = 'orders/order/create.html'
    form_class = OrderCreateForm

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save()
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        # Очистить корзину
        cart.clear()
        # запустить асинхронное задание
        order_created.delay(order.id)
        return render(self.request, 'orders/order/created.html', {'order': order})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context
