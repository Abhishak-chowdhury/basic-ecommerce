from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid
import string
import random
Quan=(
    ('kg','kg'),
    ('piece','piece'),
    ('liter','liter'),
    ('gm','gm')
)
# Create your models here.
class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    class Meta:
        abstract=True

class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    def __str__(self):
        return self.category_name
    

class Products(BaseModel):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products_category')
    product_name=models.CharField(max_length=100)
    product_title=models.CharField(max_length=100)
    product_slug=models.SlugField(unique=True,verbose_name='auto_slug_generated',blank=True)
    product_desc=models.CharField(max_length=200)
    product_price=models.IntegerField(default=0)
    product_qy=models.IntegerField(default=1)
    product_img=models.ImageField(upload_to='products')
    def save(self, *args, **kwargs):
        if not self.product_slug:
            self.product_slug = slugify(self.product_title)
            k=Products.objects.filter(product_slug=self.product_slug).exists()
            if k:
                N = 5
                res = ''.join(random.choices(string.ascii_letters, k=N))
                self.product_slug=self.product_slug+"_"+res
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name

class Quantity(BaseModel):
    product=models.OneToOneField(Products,on_delete=models.CASCADE,related_name='product_quantity')
    product_type=models.CharField(choices=Quan,max_length=100)

class Cart(BaseModel):
    user=models.OneToOneField(User,on_delete=models.SET_NULL,related_name='cart_name',null=True)
    payment_id=models.CharField(max_length=100)
    is_paid=models.BooleanField(default=False)
    def total_cart(self):
        cart=Cart.objects.get(user=self.user)
        cart_item=CartItem.objects.filter(cart=cart)
        total_price=0
        for i in cart_item:
            total_price=total_price+i.product.product_price
            total_price=total_price*i.quantity
        return total_price
    
class CartItem(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item_name')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product')
    quantity=models.IntegerField(default=1)
    
    
class Address(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_address')
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    address_name=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip=models.PositiveIntegerField(default=0)
    phone=models.PositiveIntegerField(default=0)
    email=models.EmailField(max_length=100)

class Order(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart_order',null=True)
    total_price=models.IntegerField(default=0)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,related_name='address_order',null=True)
    is_paid=models.BooleanField(default=False)
    order_date=models.DateField(auto_now_add=True)
    payment_id=models.CharField(max_length=100)

class OrderItem(BaseModel):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    products=models.ForeignKey(Products,models.CASCADE,related_name='products_name')
    quantity=models.IntegerField(default=1)
    

