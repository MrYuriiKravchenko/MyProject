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
        if not cart:
            return redirect('cart:cart_detail')

        try:
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            order_created.delay(order.id)
        except Exception as e:
            return render(self.request, 'orders/order/create.html', {'form': form, 'error': str(e)})

        return render(self.request, 'orders/order/created.html', {'order': order})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context
