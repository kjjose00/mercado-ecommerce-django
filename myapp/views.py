# views.py

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm




from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from verify_email.email_handler import send_verification_email
from django.http import HttpResponseRedirect,JsonResponse
from .models import Products,Cart,Shipping,Order,Cartcopy
from django.http import HttpResponse

from django.template.response import TemplateResponse


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			# form.save()
			inactive_user = send_verification_email(request, form)
			print("form saved")
			
			messages.success(request, f'Your account has been created ! You are now able to log in')
			return redirect('login')
		else:
			messages.error(request,"invalid data")
	else:
		form = UserRegisterForm()
	return render(request, 'myapp/register.html', {'form': form, 'title':'register here'})

################ login forms###################################################
def Login(request):
	if request.method == 'POST':

		# AuthenticationForm_can_also_be_used__

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!')
			return redirect('home')
		else:
			messages.info(request, f'account done not exit plz sign in')
	form = AuthenticationForm()
	return render(request, 'myapp/login.html', {'form':form, 'title':'log in'})
def log_out(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect('login')
	else:
		return redirect('home')
		
	
	



# Create your views here.
def home(request):
    return render(request,"myapp/home.html",{})

def organic_fruits(request):
    p=Products.objects.filter(product_type__contains='Organic Fruits')
    cart=Cart.objects.filter(user=request.user.id)
    for obj in p:
	    obj.difference = obj.product_price - obj.product_discount

    return render(request,"myapp/organic_fruits.html",{"p":p,"cart":cart})


def organic_vegetables(request):
    p=Products.objects.filter(product_type__contains='Organic Vegetables')
    cart=Cart.objects.filter(user=request.user.id)
    for obj in p:
	    obj.difference = obj.product_price - obj.product_discount
    return render(request,"myapp/organic_vegetables.html",{'p':p,"cart":cart})

def fresh_fruits(request):
    p=Products.objects.filter(product_type__contains='Fresh Fruits')
    cart=Cart.objects.filter(user=request.user.id)
    for obj in p:
	    obj.difference = obj.product_price - obj.product_discount
    return render(request,"myapp/fresh_fruits.html",{'p':p,'cart':cart})

def fresh_vegetables(request):
    p=Products.objects.filter(product_type__contains='Fresh Vegetables')
    cart=Cart.objects.filter(user=request.user.id)
    for obj in p:
	    if obj.product_discount !="":
		    obj.difference = obj.product_price - obj.product_discount
    return render(request,"myapp/fresh_vegetables.html",{'p':p,'cart':cart})

def cart(request):
	if request.user.is_authenticated:
		cart=Cart.objects.filter(user=request.user)
		print(cart.count())
		if cart.count()!=0:
			subtotal=0
			for c in cart:
				if c.product.product_discount !="":
					c.difference = (c.product.product_price*c.quantity) - (c.quantity*c.product.product_discount)
					subtotal=subtotal+c.difference
			total=subtotal+50
			return render(request,"myapp/cart.html",{"cart":cart,"total":total,"subtotal":subtotal,"cart_count":cart.count()})
		else:
			return render(request,"myapp/empty_cart.html",{})


		
	else:
		return redirect('login')

def add_cart(request,product_id):
	if request.user.is_authenticated:
		p=Products.objects.get(id=product_id)

		cart=Cart(product=p,quantity=1,user=request.user)
		cart.save()
		

		
		
		return JsonResponse({"msg":"added to cart successfully"})
	else:
		return redirect('login')
	
def increase_cart_qty(request,cart_id):
	if request.user.is_authenticated:
		cart=Cart.objects.get(pk=cart_id)
		if cart.quantity<cart.product.product_qty:
			cart.quantity=cart.quantity+1
			print(cart.quantity)
			cart.save()
			if cart.product.product_discount!="":
				cart.difference=(cart.quantity*cart.product.product_price)-(cart.quantity*cart.product.product_discount)
			cart1=Cart.objects.filter(user=request.user)
			subtotal=0
			for c in cart1:
				if c.product.product_discount!="":
					c.difference1=(c.product.product_price*c.quantity)-(c.product.product_discount*c.quantity)
					subtotal=subtotal+c.difference1
			total=subtotal+50
			
		return JsonResponse({'msg':"increased quantity","cart_quantity":cart.quantity,"cart_diff":cart.difference,"subtotal":subtotal,"total":total})
	else:
		return redirect('login')
	

def decrease_cart_qty(request,cart_id):
	if request.user.is_authenticated:
		cart=Cart.objects.get(pk=cart_id)

		if cart.quantity>1:
			cart.quantity=cart.quantity-1
			cart.save()
			if cart.product.product_discount!="":
				cart.difference=(cart.quantity*cart.product.product_price)-(cart.quantity*cart.product.product_discount)
			cart1=Cart.objects.filter(user=request.user)
			subtotal=0
			for c in cart1:
				if c.product.product_discount!="":
					c.difference1=(c.product.product_price*c.quantity)-(c.product.product_discount*c.quantity)
					subtotal=subtotal+c.difference1
			total=subtotal+50
			
			return JsonResponse({'msg':"decreased quantity","cart_quantity":cart.quantity,"cart_diff":cart.difference,"subtotal":subtotal,"total":total},status=200)
		else:
			return JsonResponse({"msg":"at least 2 kg should be there in cart to decrease it"},status=500)
	else:
		return redirect('login')
	
def delete_cart_item(request,cart_id):
	if request.user.is_authenticated:
		Cart.objects.get(pk=cart_id).delete()
		
		cart1=Cart.objects.filter(user=request.user)
		cart1.count()
		subtotal=0
		for obj in cart1:
			if obj.product.product_discount !="":
				obj.product.difference1 =(obj.quantity*obj.product.product_price) - (obj.product.product_discount*obj.quantity)
				subtotal=subtotal+obj.product.difference1
		total=subtotal+50
		return JsonResponse({'msg':"decreased quantity","subtotal":subtotal,"total":total,'cart_count':cart1.count()})
	else:
		return redirect('login')

def add_shipping_address(request):
	if request.user.is_authenticated:
		if request.method=="POST":
			address=request.POST['address']
			zip=request.POST['zip']
			phone=request.POST['phone']
			try:
				s=Shipping.objects.get(user=request.user)
				s.shipping_address=address
				s.zip=zip
				s.phone=phone
				s.save()
			except:
				s1=Shipping(user=request.user,shipping_address=address,zip=zip,phone=phone)
				s1.save()
			messages.success(request,"shipping address added successfully")
			return redirect('payment_process')
		else:
			s=Shipping.objects.filter(user=request.user)

			return render(request,"myapp/add_shipping_address.html",{"s":s})
	else:
		return redirect('login')

def payment(request):
	if request.user.is_authenticated:
		ordr=Order.objects.filter(user=request.user)
		ordr_count=ordr.count()
		client_id=settings.CLIENT_ID
		cart=Cart.objects.filter(user=request.user)
		if cart:
			cart.count()
			subtotal=0
			for obj in cart:
				if obj.product.product_discount!="":
					obj.product.difference=(obj.quantity*obj.product.product_price) - (obj.product.product_discount*obj.quantity)
					subtotal=subtotal+obj.product.difference
			total=subtotal+50
			if request.method=="POST":
				transactions_id=request.POST['transaction_id']
				print(transactions_id)
				ship=Shipping.objects.get(user=request.user)
				order=Order(user=request.user,amount=total,transaction_id=transactions_id,shipping_address=(ship.shipping_address+str(ship.zip)+str(ship.phone)))
				order.save()
				
				for obj in cart:
					p=Products.objects.get(id=obj.product.id)
					print(p.id,"product instance")

					cart_copy=Cartcopy(user=request.user,product=p,qty=obj.quantity,transaction_id=transactions_id)
					cart_copy.save()

				for c in cart:
					p=Products.objects.get(id=c.product.id)
					p.product_qty=p.product_qty-c.quantity
					p.save()
				cart.delete()

				return redirect('payment_done')

			return render(request,"myapp/payment.html",{"cart":cart,"total":total,"client_id":client_id})
		else:
			return redirect('cart')

	else:
		return redirect('login')


def payment_done(request):
	if request.user.is_authenticated:
		o=Order.objects.filter(user=request.user)
		print(type(o))
		if o:
			return render(request,"myapp/paymentdone.html",{})	
		else:
			return redirect('payment_process')		
		
	else:
		return redirect('login')
		

def dashboard(request):
	if request.user.is_authenticated:
		ordr=Order.objects.exclude(user=request.user,status__contains="Delivered")
		cartcopy=[]
		subtotal_copy=[]
		total=[]
		for c in ordr:
			cart_copy=Cartcopy.objects.filter(transaction_id=c.transaction_id)
			cartcopy.append(cart_copy)
			subtotal=0
			for i in cart_copy:
				i.difference=(i.product.product_price*i.qty)-(i.product.product_discount*i.qty)
				
				subtotal=subtotal+i.difference
			total.append(subtotal+50)
			# subtotal_copy.append(subtotal+50)
			
		
				
			



		return render(request,"myapp/dashboard.html",{"cartcopy":cartcopy,"subtotal_copy":subtotal_copy,"total":total,"ordr":ordr})	
			

			
	else:
		return redirect('login')
	


	





		







				
