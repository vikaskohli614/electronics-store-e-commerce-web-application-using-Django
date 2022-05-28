from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
from .utils import *
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,logout,login

# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order=data['order']
    items=data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    print(context)

    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )
    else:
        customer, order = guestOrder(request,data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    return JsonResponse("Payment complete..", safe=False)

def profile(request):
    return render(request,'profile.html')

def product_view(request,id):
    product = Product.objects.filter(id=id)
    print(product)
    return render(request,'products_view.html',{'product':product[0]})

def signup(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username=form.cleaned_data.get('username')

            Customer.objects.create(
                user = user,
                name= user.username,
                email=user.email
           )
            messages.success(request,f'Hii {username},your account is created successfully, login now')
            return redirect('login')
    else:
        form= CustomUserCreationForm()
    context={'form':form}
    return render(request,'signup.html',context)

def loginpage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
            messages.success(request,"successfully logged-in")
            return redirect("store")
        else:
            # No backend authenticated the credentials
            return render(request,'login')

    return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect('store')