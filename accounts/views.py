from attr import fields
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    pending = orders.filter(status = 'Pending').count()
    delivered = orders.filter(status = 'Delivered').count()

    context = {'orders':orders, 'customers':customers,  'total_customers':total_customers,
    'total_orders':total_orders, 'pending':pending, 'delivered':delivered}

    return render(request, 'accounts/dashboard.html', context)

def contact(request):
    
    return render(request, 'accounts/contact.html')

def customer(request, pk):
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'my_filter':myFilter}
    return render(request, 'accounts/customer.html', context)

def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products':products})

def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra = 5)
    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    #form = OrderForm(initial={'customer':customer})
    
    if request.method == 'POST':     
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if(formset.is_valid):
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if(form.is_valid):
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if(request.method == 'POST'):
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete_order.html', context)