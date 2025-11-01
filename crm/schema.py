import re
import graphene
from graphene_django.types import DjangoObjectType
from crm.models import Customer, Order, Product
from django.core.exceptions import ValidationError

class CustomerType(DjangoObjectType):
  class Meta:
    model = Customer
    fields = "__all__"

class OrderType(DjangoObjectType):
  class Meta:
    model = Order
    fields = "__all__"

class ProductType(DjangoObjectType):
  class Meta:
    model = Product
    fields = "__all__"

class CreateCustomer(graphene.Mutation):
  class Arguments:
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)

  customer = graphene.Field(CustomerType)
  success = graphene.Boolean()
  message = graphene.String()

  def mutate(self, info, name, email, phone=None):
    if Customer.objects.filter(email=email).exists():
      raise ValidationError("A customer with the same email exits already")
    
    if phone:
      correct_number_pattern= r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$'
      if not re.match(correct_number_pattern, phone):
        raise ValidationError("Invalid phone format. Use +1234567890 or 123-456-7890")
      
    customer = Customer(name=name, email=email, phone=phone)
    customer.save()

    return CreateCustomer(
      customer=customer,
      success=True,
      message="Customer created successfully!"
    )

class CreateProduct(graphene.Mutation):
  class Arguments:
    name = graphene.String(required=True)
    price= graphene.Float(required=True)
    stock= graphene.Int(required=False, default_value=0)

  product = graphene.Field(ProductType)
  success = graphene.Boolean()
  message = graphene.String()
  def mutate(self, info, name, price, stock=0):
    if price < 0:
      raise ValidationError("Price must be a positive number")
    
    if not isinstance(stock, int) or stock < 0:
      raise ValidationError("Stock can not be less than 0 and should be an integer")
    
    if Product.objects.filter(name__iexact=name).exists():
      raise ValidationError("This product already exist")
    
    
    product = Product(name=name, price=price, stock=stock)
    product.save()

    return CreateProduct(
      product=product,
      success=True,
      message="Product created successfully"
    )

class CreateOrder(graphene.Mutation):
  class Arguments:
    customer_id = graphene.UUID(required=True)
    product_id = graphene.List(graphene.UUID, required=True)
  
  order = graphene.Field(OrderType)
  success = graphene.Boolean()
  message = graphene.String()

  def mutate(self, info, customer_id, product_id):
    try:
      customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
      raise ValidationError("Customer not found")
    
    products = Product.objects.filter(id__in=product_id)
    found_ids = set(products.values_list('id', flat=True))
    missing = [str(pid) for pid in product_id if pid not in found_ids]
    if missing:
      raise ValidationError(f"Products not found: {', '.join(missing)}")
    
    order = Order.objects.create(customer_id=customer)
    order.product_ids.set(products)
    order.save()
    return CreateOrder(
      order=order,
      success=True,
      message="Order(s) created successfully"
    )

#Special class
class UpdateLowStockProducts(graphene.Mutation):
  class Arguments:
    pass

  updated_product = graphene.List(ProductType)
  success = graphene.Boolean()
  message = graphene.String()
  
  def mutate(self, info):

    low_stock_product = Product.objects.filter(stock__lt=10)

    if not low_stock_product:
      return UpdateLowStockProducts(
        updated_product=[],
        success=False,
        message="No low stock product found"
      )

    for product in low_stock_product:
      product.stock += 10
      product.save()
    
    return UpdateLowStockProducts(
      updated_product=low_stock_product,
      success=True,
      message="Low product updated successfully"
    )
    

    

class Query(graphene.ObjectType):
  all_customers = graphene.List(CustomerType)
  all_product = graphene.List(ProductType)
  all_order = graphene.List(OrderType)

  customer = graphene.Field(CustomerType, id=graphene.UUID(required=True))
  product = graphene.Field(ProductType, id=graphene.UUID(required=True))
  order = graphene.Field(OrderType, id=graphene.UUID(required=True))

  def resolve_all_customers(root, info):
    return Customer.objects.all()
  
  def resolve_all_product(root, info):
    return Product.objects.all()
  
  def resolve_all_order(root, info):
    return Order.objects.all()
  
  def resolve_customer(root, info, id):
    return Customer.objects.get(id=id)
  
  def resolve_product(root, info, id):
    return Product.objects.get(id=id)
  
  def resolve_order(root, info, id):
    return Order.objects.get(id=id)
  

class Mutation(graphene.ObjectType):
  create_customer = CreateCustomer.Field()
  #bulk_create_customers = BulkCreateCustomers.Field()
  create_product = CreateProduct.Field()
  create_order = CreateOrder.Field()
  update_low_stock_product = UpdateLowStockProducts.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
