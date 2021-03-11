from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView

from .models import *
import json


def get_or_create_customer(request):
    customer_id = request.session.get("customer_id")
    if customer_id is not None:
        customer = Customer.objects.filter(pk=customer_id).first()
    else:
        customer = Customer()
        customer.save()
        request.session['customer_id'] = customer.id

    return customer


class PostDetailView(DetailView):
    model = Products
    template_name = "view_info.html"
    context_object_name = "product"


def intro(request):
    customer = get_or_create_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    basketItems = order.get_total_items

    context = {'basketItems': basketItems}
    return render(request, 'intro.html', context)



def store(request):
    customer = get_or_create_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    basketItems = order.get_total_items

    products = Products.objects.all()
    product_count = request.GET.get('count', 10)
    p = Paginator(products, product_count)
    page_number = request.GET.get('page', 1)

    context = {'products': p.page(page_number), 'basketItems': basketItems}
    return render(request, 'store.html', context)

def view_info(request):
    customer = get_or_create_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    basketItems = order.get_total_items

    author = Author.objects.all()
    products = Products.objects.all()

    context = {'products': products, 'basketItems': basketItems}
    return render(request, 'view_info.html', context)

def basket(request):
    customer = get_or_create_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    basketItems = order.get_total_items

    context = {'items': items, 'order': order, 'basketItems': basketItems}
    return render(request, 'basket.html', context)


def checkout(request):
    customer = get_or_create_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    basketItems = order.get_total_items

    context = {'items': items, 'order': order, 'basketItems': basketItems}
    return render(request, 'checkout.html', context)




def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = get_or_create_customer(request)
    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)



