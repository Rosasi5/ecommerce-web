from django.shortcuts import render
from .models import Product, Customer, Order, OrderItem
from django.http import JsonResponse
import json

# Create your views here.


def store(request):
    products = Product.objects.all()
    # context dictionary for passing in data dynamically
    context = {
        'products': products,
        'user': request.user,
        }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:  # check if the current user is authenticated
        try:
            # gets the customer object associated with the current logged-in user assuming there is a one-to-one relationship
            customer = request.user.customer
            # attempts to get an existing order object for the customer which is not complete and if no such order exists, it creates a new one
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            # retrieve all orderitems associated with an order
            items = order.orderitem_set.all()
            # orderitem_set - allows access to related 'orderItem' objects
        except Customer.DoesNotExist:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            print("Customer does not exist for the authenticated user.")
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        print("User is not authenticated")

    context = {
        'items': items,
        'order': order
    }

    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:  # check if the current user is authenticated
        try:
            # gets the customer object associated with the current logged-in user assuming there is a one-to-one relationship
            customer = request.user.customer
            # attempts to get an existing order object for the customer which is not complete and if no such order exists, it creates a new one
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            # retrieve all orderitems associated with an order
            items = order.orderitem_set.all()
            # orderitem_set - allows access to related 'orderItem' objects
        except Customer.DoesNotExist:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            print("Customer does not exist for the authenticated user.")
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        print("User is not authenticated")

    context = {
        'items': items,
        'order': order
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('productId:', productId)
    print('Action:', action)

     
    return JsonResponse('item was added', safe=False)
