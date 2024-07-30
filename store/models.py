from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self): # defines the string representation of a customer instance
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    # image attribute error when there is no image for a product
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) # SET_NULL ensures that if a customer gets deleted the order record is not deleted
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False) # a new order is initially marked as incomplete
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False #if nothing is done shipping is always going to be false
        orderitems = self.orderitem_set.all()# retrieves all related orderitems objects for this order
        for i in orderitems:# loop through each orderitem
            if i.product.digital == False:
                shipping = True
        return shipping


    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()# retrieves all related orderitem objects for this order
        total = sum([item.quantity for item in orderitems])# sums up the quantity of each orderItem in the order
        return total
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()# retrieves all related orderItem objects in that order
        total = sum([item.get_total for item in orderitems])# sums up the total cost of each orderItem, get_total is a method that calculates the total cost of one orderItem
        return total #rreturns the calculated total cost
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True) # if the product is deleted the order item record is not deleted
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
