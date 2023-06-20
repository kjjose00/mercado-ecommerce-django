
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name="home"),
    path('organic_fruits/',views.organic_fruits,name='organic_fruits'),
    path('organic_vegetables/',views.organic_vegetables,name='organic_vegetables'),
    path('fresh_fruits/',views.fresh_fruits,name='fresh_fruits'),
    path('fresh_vegetables/',views.fresh_vegetables,name='fresh_vegetables'),
    path('signup/',views.register,name='signup'),
    path('accounts/login/',views.Login,name='login'),
    path('log_out/',views.log_out,name='log_out'),
    path('cart/',views.cart,name="cart"),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('increase_cart_qty/<int:cart_id>/',views.increase_cart_qty,name='increase_cart_qty'),
    path('decrease_cart_qty/<int:cart_id>/',views.decrease_cart_qty,name='decrease_cart_qty'),
    path('delete_cart_item/<int:cart_id>/',views.delete_cart_item,name='delete_cart_item'),
    path('add_shipping_address/',views.add_shipping_address,name="add_shipping_address"),
    path('payment/',views.payment,name='payment_process'),
    path('paymentdone/',views.payment_done,name="payment_done"),
    path('dashboard/',views.dashboard,name="dashboard"),
    
]