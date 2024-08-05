from .models import Product, Customer, Order, OrderItem
import json


def cookieCart(request):
    try:
            # get cookies to use to update cartitems
            cart = json.loads(request.COOKIES['cart'])
    except:
            cart = {}
            print('Cart:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product' : {
                    'id' : product.id,
                    'name' : product.name,
                    'price' : product.price,
                    'imageURL' : product.imageURL,
                },
                'quantity' : cart[i]['quantity'],
                'get_total' : total
            }
            items.append(item)

            if (product.digital == False): #if the product is not a digital one
                    order['shipping'] = True
        except:
            pass
    return {'cartItems' : cartItems, 'order' : order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:  # check if the current user is authenticated
        try:
            # gets the customer object associated with the current logged-in user assuming there is a one-to-one relationship
            customer = request.user.customer
            # attempts to get an existing order object for the customer which is not complete and if no such order exists, it creates a new one
            # retrieve all orderitems associated with an order
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            # orderitem_set - allows access to related 'orderItem' objects
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except Customer.DoesNotExist:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
            print("Customer does not exist for the authenticated user.")
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
     
    print('User is not logged in...')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderitem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order