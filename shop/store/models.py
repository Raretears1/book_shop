from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Customer(models.Model):

    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    # author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    author_name = models.CharField(max_length=300)
    description = models.TextField()
    pages_count = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('product', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Author(models.Model):
    author_d = models.CharField(max_length=20, null=True)
    author_info = models.TextField()
    author_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.product.id)

    @property
    def imageURL(self):
        try:
            url = self.author_image.url
        except:
            url = ''
        return url


class Order(models.Model):
    # устанавливаю связь между клиентом и заказами
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    # делаю логику между электронными и реальными книгами(для электронных мне не нужна инфа про доставку)
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    # делаю функцию которая обсчитывает всю суму заказа с учетом всех продуктов
    @property
    def get_basket_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    # делаю функцию которая аналогична предидущей только с кол-вом продуктов
    @property
    def get_total_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItem(models.Model):
    # устанавливаю связь между продуктом и заказами
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # Делаю фун-цию чтоб обсчитывала суму одного заказа(продукта в зависимости от кол-ва)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    post_number = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address

