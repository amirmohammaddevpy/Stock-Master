from django.shortcuts import render ,redirect
from django.db import transaction
from .forms import Transactions , CategoryForm ,SaleProduct
from django.contrib import messages
from .models import Product ,SelesProduct
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum

# Create your views here.
@login_required(login_url="accounts:login")
def product_entry(request):
    form_category = CategoryForm()
    if request.method == "POST":
        form = Transactions(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.owner = request.user
            user.save()
            messages.success(request,"Succesfully add product")
            return redirect("product:product_entry")
        else:
            messages.error(request,"for is't valid")
    else:
        form = Transactions()
    return render(request,"product/transactions.html",{'form':form,'form_category':form_category})

@login_required(login_url="accounts:login")
def sale_product(request):
    product = Product.objects.filter(owner=request.user,is_active=True)

    if request.method == "POST":
        form = SaleProduct(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity']
            
            with transaction.atomic():
                product = Product.objects.select_for_update().get(
                    pk = form.cleaned_data['product'].pk , owner=request.user    
                )
                if product.quantity < qty:
                    messages.error(request,"The entered quantity exceeds the available stock!")
                    return redirect("product:sale_product")
                sale = form.save(commit=False)
                sale.owner = request.user
                sale.quntity = qty
                sale.total_price = qty * product.sell_price
                sale.save()
                product.quantity -= qty
                product.save()
                messages.success(request,"Sale completed successfully")
                return redirect("product:sale_product")
        messages.error(request,"Form is not valid")
    else:
        form = SaleProduct()
    return render(request,"product/create_sale.html",{'form':form,'products':product})

@login_required(login_url="accounts:login")
@require_POST
def category_create(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request,'successfully added category')
        return JsonResponse({'status':'add'})
    else:
        return JsonResponse({'status':'error'})

@login_required(login_url="accounts:login")
def product_price(request,pk):
    product = Product.objects.get(id=pk)
    return JsonResponse({'unit_price':product.sell_price})

def sales_history(request):
    search = request.GET.get('search','').strip()
    product = SelesProduct.objects.select_related('product').all()
    if search:
        product = product.filter(product__name__icontains=search)
    
    total_price = SelesProduct.objects.filter(product__name=search).aggregate(total=Sum("total_price"))['total'] or 0
    total_transactions = SelesProduct.objects.filter(product__name=search).count()
    
    return render(request,"product/sales_history.html",{'product':product,'search':search,"total_sales":total_price,"total_transactions":total_transactions})

def products(request):
    product = Product.objects.filter(owner=request.user)
    return render(request,"product/product.html",{'products':product})