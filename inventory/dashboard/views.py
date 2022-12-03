from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product,Order
from .forms import ProductForm,OrderForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
   orders = Order.objects.all()
   products = Product.objects.all()
   order_count = orders.count()
   product_count = products.count()
   workers_count = User.objects.all().count

   if request.method == 'POST':
      form = OrderForm(request.POST)
      if form.is_valid():
         instance = form.save(commit=False)
         instance.staff = request.user
         instance.save()
         return redirect('dashboard-index')
   else:
      form = OrderForm()
   context = {
      'orders': orders,
      'form': form,
      'products': products,
      'order_count': order_count,
      'product_count': product_count,
      'workers_count': workers_count
   }

   return render(request, 'dashboard/index.html',context)

@login_required
def staff(request):
   workers = User.objects.all()
   workers_count = workers.count()
   order_count = Order.objects.all().count()
   product_count = Product.objects.all().count()
   context = {
      'workers': workers,
      'workers_count': workers_count,
      'order_count': order_count,
      'product_count': product_count 
   }
   return render(request, 'dashboard/staff.html', context)
@login_required
def staff_detail(request, pk):
   workers = User.objects.get(id=pk)
   context = {
      'workers' : workers
   }
   return render(request, 'dashboard/staff_details.html',context)

@login_required
def product(request):
   items = Product.objects.all()
   product_count = items.count()
   workers_count = User.objects.all().count()
   order_count = Order.objects.all().count()
   #items = Product.objects.raw('SELECT * FROM dashboard_product')
   if request.method == 'POST':
      form = ProductForm(request.POST)
      if form.is_valid():
         form.save()
         product_name = form.cleaned_data.get('name')
         messages.success(request,f'{product_name} has been added')
         return redirect('dashboard-products')

   else:
      form = ProductForm()


   context = {
      'items': items,
      'form': form,
      'workers_count': workers_count,
      'order_count': order_count,
      'product_count': product_count
   }
   return render(request, 'dashboard/products.html', context)

@login_required
def product_delete(request, pk):
   item = Product.objects.get(id=pk)
   if request.method == 'POST':
      item.delete()
      return redirect('dashboard-products')
   return render(request, 'dashboard/product_delete.html')

@login_required
def product_update(request, pk):
   item = Product.objects.get(id=pk)
   if request.method == 'POST':
      form = ProductForm(request.POST, instance=item)
      if form.is_valid():
         form.save()
         return redirect('dashboard-products')
   else:
      form = ProductForm(instance=item)
      context = {
         'form': form,
      }
   return render(request, 'dashboard/product_update.html', context)

@login_required
def order(request):
   orders = Order.objects.all()
   order_count = orders.count()
   workers_count = User.objects.all().count()
   product_count = Product.objects.all().count()

   context = {
      'orders': orders,
      'workers_count': workers_count,
      'order_count': order_count,
      'product_count': product_count 
   }

   return render(request, 'dashboard/orders.html',context)
