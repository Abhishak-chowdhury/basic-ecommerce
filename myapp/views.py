from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from myapp.models import Category,Products,Cart,CartItem,Address,Order,OrderItem
from django.contrib import messages
from django.db.models import Sum,Count 
from django.contrib.auth import authenticate,login,logout
import string
import random
import razorpay
from django.conf import settings
# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        if password !=confirmpassword:
            messages.warning(request, "sucessfully is not registered")
            return render(request,'sign-up.html')
        else:
            N = 5
            res = ''.join(random.choices(string.ascii_letters, k=N))
            user=first_name+"_"+res
            user_obj=User(first_name=first_name,last_name=last_name,email=email,username=user)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "sucessfully registered")
            return redirect('login')
    return render(request,'sign-up.html')

def loginform(request):
    if request.method == 'POST':
        user=None
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            obj=User.objects.get(email=email)
            username=obj.username
        
            user=authenticate(request,email=email,password=password,username=username)
            print(user)
        except Exception as e:
            print(e)
        if user is not None:
            login(request,user)
            messages.success(request,f'{email} is sucessfully login ')
            return redirect('home')
        else:
            messages.warning(request,'login details are incorrect')
            return redirect('login')
    return render(request,'login.html')

def logoutform(request):
    logout(request)
    messages.success(request,'thankyou for spending some time')
    return redirect('login')

def home(request):
    cat_obj=Category.objects.all()
    latest_productone=Products.objects.all().order_by('-id')[0:3]
    latest_product2=Products.objects.all().order_by('id')[0:3]
    contex={
        'category_objs':cat_obj,
        'latest_productone':latest_productone,
        'latest_product2': latest_product2
    }
    return render(request,'index.html',contex)

def shop(request):
    cat_obj=Category.objects.all()
    latest_productone=Products.objects.all().order_by('-id')[0:3]
    latest_product2=Products.objects.all().order_by('id')[0:3]
    product_objects=Products.objects.all()
    contex={
        'category_objs':cat_obj,
        'latest_productone':latest_productone,
        'latest_product2': latest_product2,
        'product_objects':product_objects,
    }
    return render(request,'shop-grid.html',contex)

def category_wise_product(request,data):
    category_obj=Category.objects.get(category_name=data)
    cat_obj=Category.objects.all()
    latest_productone=Products.objects.all().order_by('-id')[0:3]
    latest_product2=Products.objects.all().order_by('id')[0:3]
    product_objects=Products.objects.all()
    contex={
        'category_objs':cat_obj,
        'latest_productone':latest_productone,
        'latest_product2': latest_product2,
        'product_objects':product_objects,
        'cat_per_obj': category_obj,
    }
    return render(request,'caregory_wise_products.html',contex)
def productdetails(request,slug):
    product=Products.objects.get(product_slug=slug)
    related_product=Products.objects.exclude(product_slug=slug)
    contex={
        'product':product,
        'related_product':related_product
    }
    return render(request,'shop-details.html',contex)

def add_to_cart(request,id):
    user_obj, _=Cart.objects.get_or_create(user=request.user)
    
    product=Products.objects.get(id=id)
    cart_item, item_created=CartItem.objects.get_or_create(cart=user_obj,product=product)
    
    if not item_created:
        cart_item.quantity+=1
        cart_item.save()
    print(cart_item)
    
    return redirect('cart')

def cart(request):
    contex=None
    try:
        cart=Cart.objects.get(user=request.user)
        cart_item=CartItem.objects.filter(cart=cart)
        # total_price=CartItem.objects.filter(cart=cart).aggregate(Sum('product__product_price'))['product__product_price__sum']
        total_price=0
        # per_price=cart_item.product.product_price*cart_item.quantity
        for i in cart_item:
            total_price=total_price+i.product.product_price
            
            total_price=total_price*i.quantity
        print(total_price)
        contex={
            'cart_item':cart_item,
            'total':total_price,
            
        }
    except Exception as e:
        print(e)
    
    
    return render(request,'shoping-cart.html',contex)

def Addressfun(request):
    if request.method == 'POST':
        user=request.user
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        country=request.POST.get('country')
        streetaddress=request.POST.get('streetaddress')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip=request.POST.get('zip')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        Address.objects.create(user=user,first_name=firstname,last_name=lastname,country=country,
                            address_name=streetaddress,city=city,state=state,zip=zip,phone=phone,email=email)
        return redirect('alladdress')
    return render(request,'address.html')

def Alladdress(request):
    address_objs=Address.objects.all()
    contex={
        'address_objs':address_objs
    }
    return render(request,'alladdress.html',contex)

def deleteaddress(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        address_item=Address.objects.get(id=id)
        if address_item:
            address_item.delete()
    return redirect('alladdress')
def delete_cart(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        cart_item=CartItem.objects.get(id=id)
        if cart_item:
            cart_item.delete()

    return redirect('cart')

def checkout(request):
    contex=None
    try:
        address_obj=Address.objects.filter(user=request.user)
        total_obj=Cart.objects.get(user=request.user)
        cart_items=CartItem.objects.filter(cart=total_obj)
        total_price=0
            # per_price=cart_item.product.product_price*cart_item.quantity
        for i in cart_items:
            total_price=total_price+i.product.product_price
                
            total_price=total_price*i.quantity
        client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
        data = { "amount": total_price*100, "currency": "INR", "receipt": "order_rcptid_11","payment_capture": 1}
        payment = client.order.create(data=data)
        print(payment)
        contex={
            'address_obj':address_obj,
            'total_obj':total_obj,
            'cart_items':cart_items,
            'payment':payment
        }
    except Exception as e:
        print(e)
    return render(request,'checkout.html',contex)

def success(request):
        
        p_id=request.GET.get('payment_id')
        address=request.GET.get('a_id')
        address_bj=Address.objects.get(id=address)
        cart=Cart.objects.get(user=request.user)
        cart_items=CartItem.objects.filter(cart=cart)
        total_price=0
            # per_price=cart_item.product.product_price*cart_item.quantity
        for i in cart_items:
            total_price=total_price+i.product.product_price
                
            total_price=total_price*i.quantity
        ord=Order.objects.create(user=request.user,total_price=total_price,address=address_bj,is_paid=True,payment_id=p_id) 
        
        
        for cart_item in cart_items:
             
            OrderItem.objects.create(order=ord,products=cart_item.product,quantity=cart_item.quantity)
           
                
        cart_items.delete()        
        cart.delete()
        
    
        return render(request,'sucess.html')

def orderhistoty(request):
    order_obj=Order.objects.filter(user=request.user)
    # order_item_objs=[]
    # for i in order_obj:
    #     ord=OrderItem.objects.filter(order=i)
    #     ord=list(ord)
    #     order_item_objs += ord
    order_item_objs=OrderItem.objects.filter(order__in=order_obj)
    contex={
        'order_item_objs':order_item_objs
    }
    return render(request,'orderhistory.html',contex)