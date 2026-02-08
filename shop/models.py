from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
#===================product Table============================
class Product(models.Model) :
    product_id = models.AutoField(primary_key=True)
    product_name= models.CharField(max_length=200)
    product_price= models.DecimalField(max_digits=10 ,decimal_places=2)
    productcategory = [
        ('Pizza' ,'Pizza'),
        ('Burger' ,'Burger'),
        ('Drink' ,'Drink'),
        ('Khmer-Food' ,'Khmer-Food'),
    ]
    category = models.CharField(max_length=200 ,choices=productcategory)
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(max_length=900)
    def reduce_stock(self, qty):
        if qty <= 0:
            raise ValueError('Quantity must be greater than 0')

        if qty > self.stock:
            raise ValueError('Not enough stock')

        self.stock -= qty
        self.save()
    def __str__(self):
        return self.product_name
#======================checkout Table====================================================
class CheckOut(models.Model) :
    customer = models.CharField(max_length=100)
    tel = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    def __str__(self) :
        return self.customer
#===============================================================================================
class OrderManager(models.Manager):
    def today(self):
        return self.filter(order_datetime__date=timezone.now().date())
    
    def this_month(self):
        return self.filter(order_datetime__month=timezone.now().month)

    def this_year(self):
        return self.filter(order_datetime__year=timezone.now().year)

    def this_week(self):
        return self.filter(order_datetime__week=timezone.now().isocalendar()[1])
#=============================orderTable===================================================
class Order(models.Model) :
     user = models.ForeignKey(User , on_delete=models.CASCADE, null=True , blank=True)
     order_datetime = models.DateTimeField(auto_now_add=True)
     objects = OrderManager()
     def __str__(self) :
        return f"Order #{self.id}"
#=========================order Item table===================================================
class OrderItem(models.Model) :
    order = models.ForeignKey(Order , on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product , on_delete= models.CASCADE)   
    order_qty = models.IntegerField(default=1)
    order_price = models.DecimalField(max_digits=10 ,decimal_places=2)
    def save(self, *args, **kwargs):
     if self.pk is None:  # create only
        self.product.reduce_stock(self.order_qty)
     super().save(*args, **kwargs)

    def __str__(self) :
      return f"{self.product.product_name} x {self.order_qty}"
    
#===================================================Update Decount APP========================  
class Decount(models.Model)  :
    text = models.CharField(max_length=200)
    image = models.URLField(max_length=900)
    def __str__(self):
        return self.text
    




