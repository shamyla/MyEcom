from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


from django.shortcuts import render, get_object_or_404, redirect

from .forms import VariationInventoryFormset
from .models import products, Variation
from django.utils import timezone

#Create your views here.
# ********************************************8 VARIATION LIST VIEW ************************************888
class VariationListView(ListView):
    model = Variation
    queryset = Variation.objects.all()


    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(*args, **kwargs) #?? we are inheriting what in cotext?
        context["formset"] = VariationInventoryFormset(queryset=self.get_queryset())
        return context # ????

    def get_queryset(self, *args, **kwargs):
        products_pk= self.kwargs.get("pk")
        if products_pk:
            product = get_object_or_404(products, pk=products_pk)
            queryset = Variation.objects.filter(products=product)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormset(request.POST, request.FILES)

        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                if new_item.title:
                    products_pk = self.kwargs.get('pk')
                    product = get_object_or_404(products, pk=products_pk)
                    new_item.products = product
                    new_item.save()

            messages.success(request, "inventory updated")
            return redirect("products")

        raise Http404

#**************************************  PRODUCT  LIST VIEW  **********************************************

class ProductListView(ListView):
    model = products
    queryset = products.objects.all()



    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs) #?? we are inheriting what in cotext?
        print context
        context ["now"]= {timezone.now()}
        context['query'] = self.request.GET.get("q")#??q
        return context # ????

# search option

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains = query)
            )
        return qs


#*****************************************  DETAIL VIEW **************************************
# class base view and function base view both doing same
class ProductDetailView(DetailView):
    model = products
# template = appname/modelname_detail.html
# template = products/products_detail.html


#overriding context data
    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailView,self).get_context_data(*args, **kwargs)
        instance = self.get_object()
        context["related"] = products.objects.get_related(instance)
        return context

def product_detail_view_func(request, id):
    product_instance = products.objects.get(id=id)
    template = 'products/products_detail.html'
    context = {
        "object": product_instance
        }

    return render(request, template, context)



