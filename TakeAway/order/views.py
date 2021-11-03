from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {'cartItems': cartItems}

    return render(request, 'order/index.html', context)


def about(request):
    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'cartItems': cartItems}
    

    return render(request, 'order/about.html', context)

def menu(request):
    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']


    food = Food.objects.all()
    context = {'food': food, 'cartItems': cartItems}
    return render(request, 'order/menu.html', context)

def cart(request):
    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'order/cart.html', context)

def review(request):
    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
 

    context = {'cartItems': cartItems}
    return render(request, 'order/review.html', context)

def order(request):
    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'order/order.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)
 
    client = request.user.client
    product = Food.objects.get(id=productId)
    order, created = Order.objects.get_or_create(client=client, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        client = request.user.client
        order, created = Order.objects.get_or_create(client=client, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            DeliveryAddress.objects.create(
                client=client,
                order=order,
                address=data['shipping']['address'],
                zipcode=data['shipping']['zipcode'],
                message=data['shipping']['message'],
                number=data['shipping']['number'],
                email=data['shipping']['email'],
                county=data['shipping']['county'],
            )

    else:
        print('User is not logged in...')
    return JsonResponse('Payment complete', safe=False)
