from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Order(models.Model):
   STATUS_CHOICES = (

    ('Pending', 'Pending'),

    ('Shipped', 'Shipped'),

    ('Delivered', 'Delivered'),

    ('Cancelled', 'Cancelled')

)

   status = models.CharField(

    max_length=20,

    choices=STATUS_CHOICES,

    default='Pending'
)
   full_name = models.CharField(max_length=200)

   phone = models.CharField(max_length=20)

   address = models.TextField()

   city = models.CharField(max_length=100)

   pincode = models.CharField(max_length=20)

   user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

   total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

   created_at = models.DateTimeField(
        auto_now_add=True
    )

def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.product.name
    
class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.product.name
    
class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.username
    
class Coupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount = models.IntegerField()

    active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return self.code