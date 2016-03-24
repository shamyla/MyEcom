from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


from django.contrib import admin

from carts.views import CartView, CheckoutView, ItemCountView
from orders.views import AddressSelectFormView

urlpatterns = [
    # Examples:

    url(r'^$', 'newsletter.views.home', name='home'),

    url(r'^contact/$', 'newsletter.views.contact', name='contact'),
    url(r'^about/$', 'ecomerce2.views.about', name='about'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),


    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='address'),

    url(r'^products/', include('products.urls')),
    #url(r'^carts/', include('carts.urls')),


]#nai h oraha muj se kaam its deadly slow...u need to restart systemok. waisay ap ne CartView ko quotes main present kiyaa thaa
#muje b samaj naai aaya...aur????????????????

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)