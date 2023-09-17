from django.contrib import admin
from myapp.models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=['category_name']
admin.site.register(Category,CategoryAdmin)
class ProductsAdmin(admin.ModelAdmin):
    list_display=['category','product_name','product_title','product_slug','product_desc','product_price','product_img']
admin.site.register(Products,ProductsAdmin)




admin.site.register(Quantity)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
