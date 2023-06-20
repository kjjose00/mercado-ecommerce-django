from django.contrib import admin
from .models import CustomUser,Products,Cart,Shipping,Order,Cartcopy

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Shipping)


class AdminCartCopy(admin.ModelAdmin):
    list_display=['id','user','product','qty','transaction_id']

admin.site.register(Cartcopy,AdminCartCopy)

class AdminOrder(admin.ModelAdmin):
    list_display=['id','user','amount','status','transaction_id','shipping_address']

admin.site.register(Order,AdminOrder)

