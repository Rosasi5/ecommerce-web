from django.shortcuts import render, redirect
from .models import Product, Customer, Order, OrderItem, ShippingAddress
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
from .utils import cookieCart, cartData, guestOrder


# Create your views here.

def login_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.set_level(request, messages.WARNING)
            messages.warning(request, "There was an error login in...")
            return redirect('login')
    else:
        return render(request, 'store/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('login')


def store(request):

    
    data = cookieCart(request)
    cartItems = data['cartItems']

    
    products = Product.objects.all()
    
    context = {  # context dictionary for passing in data dynamically
        'products': products,
        'user': request.user,
        'cartItems': cartItems,
        }
    return render(request, 'store/store.html', context)


def cart(request):
    
    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'store/cart.html', context)


def checkout(request):
    
    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    
    data = json.loads(request.body.decode('utf-8')) # json.loads converts the http request into a python dictionary
    productId = data['productId'] #extracts the id of the product to be updated from the data dictionary
    action = data['action']# extacts the value associated with the key action i.e add, remove whioch reps the action to be performed

    print('productId:', productId)
    print('Action:', action)
    customer = request.user.customer #gets the customer associated with the currently authenticated user
    product = Product.objects.get(id=productId) # gets Product object whose id matches the productId from the request
    order, created = Order.objects.get_or_create(customer=customer, complete=False)#retrieves the order associated with authenticated customer and product with the matching productId of the request and if it does not exist it creates a new order

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)# attempts to get an existing orderitem associated with the given order and product and if such an order item doesnt exist it creates a new one

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item was added....', safe=False)

#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt #whenever data is sent to this view, dont worry about the csrf token
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp() #generate a unique transaction id
    data = json.loads(request.body) # parse the data and access it

    if request.user.is_authenticated:
        customer = request.user.customer # get the customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False) #get the order associated with the authenticated customer or create if not found
        

        # check if shipping is true and set the data in the database
        

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

       # check if the total is the same as the cart_total
    if total == float(order.get_cart_total):
            order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['Shipping']['address'],
            city=data['Shipping']['city'],
            state=data['Shipping']['state'],
            zipcode=data['Shipping']['zipcode'],
        )

    #print('Data:', request.body)
    return JsonResponse('Payment complete....', safe=False)
    
