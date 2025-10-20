from django.db import models
import uuid
# Create your models here.
class Customer(models.Model):
  """Customer class"""
  id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4)
  name = models.CharField(max_length=100)
  email = models.EmailField(unique=True, null=False)
  phone = models.CharField(null=True, blank=True, max_length=20)
  address = models.CharField(null=True, blank=True, max_length=100)
  def __str__(self):
    return self.name

class Product(models.Model):
  """Poduct class that defines the product schema"""
  id = models.UUIDField(null=False, primary_key=True, default=uuid.uuid4)
  name = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.IntegerField(blank=True, null=True, default=0)
  def __str__(self):
    return self.name

class Order(models.Model):
  id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4)
  customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name="orders")
  product_ids = models.ManyToManyField('Product', related_name="orders")
  order_date = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return f"Order #{self.id} by {self.customer}"
