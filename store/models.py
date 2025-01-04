from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now 

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)  
    def __str__(self):
        return self.name if self.name else self.user.username  


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    description = models.TextField(default="No description available")
    category = models.CharField(max_length=100, default='Uncategorized')
    brand = models.CharField(max_length=100, default='Unknown')
    quantity_in_stock = models.PositiveIntegerField(default=0)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)  
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        return self.image.url if self.image else ''  

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        return any(item.product.digital is False for item in self.orderitem_set.all())

    @property
    def get_cart_total(self):
        return sum(item.get_total for item in self.orderitem_set.all())

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)  
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity if self.product else 0  


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=20, null=False)  
    date_added = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100, null=False, default='INDIA')

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.zipcode}, {self.country}"


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=now)
    logout_time = models.DateTimeField(null=True, blank=True)
    username = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username} - Login: {self.login_time} - Logout: {self.logout_time}"
