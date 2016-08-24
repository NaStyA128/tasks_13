from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

# Create your models here.


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, verbose_name=_("Phone"))

    @python_2_unicode_compatible
    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    @python_2_unicode_compatible
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("Category")
    )
    image = models.ImageField(
        upload_to='photos/',
        max_length=255,
        verbose_name=_("Image")
    )
    size = models.CharField(max_length=10, verbose_name=_("Size"))
    colour = models.CharField(max_length=40, verbose_name=_("Colour"))
    price = models.FloatField(verbose_name=_("Price"))
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))

    @python_2_unicode_compatible
    def __str__(self):
        return '%s, %s, %s' % \
               (self.name, self.size, self.colour)


class Order(models.Model):
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        MyUser,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    products = models.ManyToManyField(
        Product,
        through='OrderProducts',
        verbose_name=_("Products")
    )
    total_sum = models.FloatField(verbose_name=_("Total sum"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    @python_2_unicode_compatible
    def __str__(self):
        return '%s, %s' % (self.user, self.total_sum)


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Order")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product")
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    sum = models.FloatField(verbose_name=_("Sum"))

    @python_2_unicode_compatible
    def __str__(self):
        return '%s, %s' % (self.order, self.product)


class Tree(models.Model):
    node = models.ForeignKey('self')
