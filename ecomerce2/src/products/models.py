
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save


# Model manager to handle the products
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def get_related(self, instance):
        products_one = self.get_queryset().filter(categories__in=instance.categories.all() )
        products_two = self.get_queryset().filter(default=instance.default)
        qs = (products_one |products_two).exclude(id=instance.id).distinct()
        return qs
        return self.get_queryset()







# Create your models here.
class products(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    #Image = models.ImageField(upload_to='/Products/')
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey('Category', related_name='default_category', null=True, blank= True)#To shoe default category to user

    #calling the function of prodcut manager
    objects = ProductManager()


    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('/products/%s'% self.pk)

    # def get_absolute_url(self):
    #     return reverse('product_detail',kwargs={"pk": self.pk})

# variation

class Variation(models.Model):

    products = models.ForeignKey(products)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(default="-1", null=True, blank=True)# -1 means unlimited

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.products.get_absolute_url()

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" %(reverse("cart", self.id))




# post_save

def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    print sender
    products = instance
    variations = products.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.products = products
        new_var.title = "Default"
        new_var.price = products.price
        new_var.save()


post_save.connect(product_post_saved_receiver,sender=products)


# product image

class ProductImage(models.Model):
    products = models.ForeignKey(products)
    Image = models.ImageField(upload_to='products/')

    def __unicode__(self):
        return self.products.title




class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.title


def image_upload_to_featured(instance, filename):
    title = models.instance.products.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s,%s" %(slug, instance.id, file_extension)
    return "products/%s/featured/%s" %(slug, new_filename)

class productfeatured(models.Model):
    products = models.ForeignKey(products)
    image = models.ImageField(upload_to=image_upload_to_featured)
    title = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=220, null=True, blank=True)
    text_right = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    show_price = models.BooleanField(default=False)

    def __unicode__(self):
        return self.products.title



