from django.urls import path
from myapp.views import(
    home,
    register,
    loginform,
    logoutform,
    shop,
    category_wise_product,
    productdetails,
    add_to_cart,
    cart,
    delete_cart,
    Addressfun,
    Alladdress,
    deleteaddress,
    checkout,
    success,
    orderhistoty
)
urlpatterns = [
    path('',home,name='home'),
    path('register',register,name='register'),
    path('login',loginform,name='login'),
    path('logout',logoutform,name='logout'),
    path('shopping',shop,name='shopping'),
    path('shopping/<slug:data>',category_wise_product,name='category_wise_product'),
    path('productdetails/<slug:slug>',productdetails,name='product_details'),
    path('productdetails/cart/<int:id>',add_to_cart,name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('cart/delete',delete_cart,name='delete_cart'),
    path('address',Addressfun,name='address'),
    path('alladdress',Alladdress,name='alladdress'),
    path('deleteaddress',deleteaddress,name='deleteaddress'),
    path('checkout',checkout,name='checkout'),
    path('success/',success,name='success'),
    path('order-history',orderhistoty,name='orderhistoty')
]
