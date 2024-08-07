from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender


class CartAddView(FormView):
    form_class = CartAddProductForm
    success_url = reverse_lazy('cart:cart_detail')

    def form_valid(self, form):
        cart = Cart(self.request)
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect('shop:product_list')


class CartRemoveView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetailView(TemplateView):
    template_name = 'cart/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'override': True})
        context['cart'] = cart
        context['coupon_apply_form'] = CouponApplyForm()

        r = Recommender()
        cart_products = [item['product'] for item in cart]
        if cart_products:
            recommended_products = r.suggest_products_for(
                cart_products,
                max_results=4
            )
        else:
            recommended_products = []

        context['recommended_products'] = recommended_products
        return context
