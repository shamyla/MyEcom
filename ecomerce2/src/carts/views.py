from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Variation
from carts.models import Cart, CartItem
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView

from django.views.generic.edit import FormMixin
from orders.forms import GuestCheckoutForm
from orders.models import UserCheckout

class ItemCountView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if cart_id == None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()

            request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "carts/view.html"

    def get_object(self, *args, **kwargs):
        #*************************single object mixin ......copying the get data stuff from the get function
        # replace request to self.request
        # session expiry
        self.request.session.set_expiry(0)# when web browser is closed
        #create session
        cart_id = self.request.session.get("cart_id")

        if cart_id == None:
            cart = Cart() # create new cart
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id

        cart = Cart.objects.get(id=cart_id)

        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart



    def get(self, request, *args, **kwargs):
        cart = self.get_object()

        # # session expiry

        item_id = request.GET.get("item")

        delete_item = request.GET.get("delete", False)

        print item_id
        if item_id:

            item_instance = get_object_or_404(Variation, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty)<1:
                    delete_item=True

            except:

                raise Http404

            #cart = Cart.objects.all().first()...as we are creating a new cart above
            cart_item , created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            flash_message = ""
            item_added = False
            if created:

                item_added = True
                flash_message = "successfully added to cart"

            if delete_item:
                flash_message = "successfully removed from cart"
                cart_item.delete()
            else:
                if not created:
                    flash_message = "Cart updated successfully"
                cart_item.quantity = qty
                cart_item.save()
                print cart_item

            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))

        if request.is_ajax():
            try:
                total = cart_item.total
            except:
                total = None
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None
            try:
                total = cart_item.cart.items.count()
            except:
                total = None
            try:
                cart_total = cart_item.cart.total
            except:
                cart_total = None
            try:
                tax_total = cart_item.cart.tax_total
            except:
                tax_total = None

            data = {
                "item_added": item_added,
                "deleted": delete_item,
                "line_total": total,
                "subtotal": subtotal,
                "tax_total": tax_total,
                "cart_total": cart_total,
                "flash_message" : flash_message,
                "total": total

                }
            return JsonResponse(data)

        context = {
            "object": self.get_object()
            }
        template = self.template_name
        return render(request, template, context)


class CheckoutView(FormMixin, DetailView):
    model = Cart
    template_name = "carts/checkout_view.html"
    form_class = GuestCheckoutForm

    def get_object(self, *args, **kwargs):
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
           return redirect("cart")
        cart = Cart.objects.get(id=cart_id)
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)

        user_can_continue = False
        user_check_id = self.request.session.get("user_checkout_id")

        if not self.request.user.is_authenticated() or user_check_id == None:
            context["user_login"] = AuthenticationForm() #instance of the form
            context["next_url"] = self.request.build_absolute_uri()

        elif self.request.user.is_authenticated() or user_check_id != None:
            user_can_continue = True
        else:
            pass
        if self.request.user.is_authenticated():
            user_checkout, created = UserCheckout.objects.get_or_create(email = self.request.user.email)
            user_checkout.user = self.request.user
            print user_checkout
            user_checkout.save()
            self.request.session["user_checkout_id"] = user_checkout.id

        context["user_can_continue"] = user_can_continue
        context["form"] = self.get_form()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_checkout, created = UserCheckout.objects.get_or_create(email=email)
            self.request.session["user_checkout_id"] = user_checkout.id
            return self.form_valid(form)

        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout")
















