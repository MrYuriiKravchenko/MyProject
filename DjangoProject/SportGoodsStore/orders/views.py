from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem


class OrderCreateView(FormView):
    template_name = 'orders/order/create.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('order_created')

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
        cart.clear()
        return render(self.request, 'orders/order/create.html', {'order': order})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context