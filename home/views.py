from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Sum ,F
from decimal import Decimal
from product.models import Product ,Category , SelesProduct
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.
@login_required(login_url="accounts:login")
def home(request):
    product_count = Product.objects.filter(owner=request.user)
    total_sales = SelesProduct.objects.filter(owner=request.user).aggregate(total=Sum('total_price'))['total'] or Decimal('0')
    qty = Product.objects.filter(owner=request.user,quantity__lt = 10)
    sales = list(SelesProduct.objects.values('created_at').annotate(total=Sum("total_price")).order_by('created_at'))
    recent_products = Product.objects.filter(owner=request.user)
    
    return render(request,"home/home.html",{'total_products':product_count.count(),"total_sales":total_sales,'qty':qty,'sales_chart':sales,'recent_products':recent_products})

def reports(request):
    total_products = Product.objects.filter(owner=request.user)
    total_categories = Category.objects.all().count()
    total_stock_value = Product.objects.aggregate(total=Sum(F("sell_price") * F('quantity')))['total'] or 0 
    total_sales = SelesProduct.objects.aggregate(total = Sum(F('total_price')))['total'] or 0
    out_of_stock_count = Product.objects.filter(owner=request.user,quantity=0)
    low_stock_count = Product.objects.filter(owner=request.user,quantity__lt=5)
    available_products_count = Product.objects.filter(owner=request.user,quantity__gt=0)
    sales_report = SelesProduct.objects.filter(owner=request.user,)
    
    
    context = {
        'total_products':total_products.count(),
        'out_of_stock_count':out_of_stock_count.count(),
        'low_stock_count':low_stock_count.count(),
        'available_products_count':available_products_count.count(),
        'total_categories':total_categories,
        'total_stock_value':total_stock_value,
        'total_sales':total_sales,
        'low_stock_products':low_stock_count,
        'sales_report':sales_report
    }
    return render(request,'home/reports.html',context)

@require_POST
def send_email(request):
    subject = "هشدار کمبود موجودی محصول | StockMaster"
    product = Product.objects.filter(owner=request.user)
    get_user = User.objects.get(username=request.user)
    for quantity in product:
        message = f"""
            مدیر محترم،

            سیستم StockMaster به شما اطلاع می‌دهد که موجودی محصول زیر به حد هشدار رسیده است.

            نام محصول: {quantity.name}
            کد محصول: {quantity.code_product}
            موجودی فعلی: {quantity.quantity}
حداقل موجودی مجاز: 10

            لطفاً در اسرع وقت نسبت به تأمین مجدد این محصول اقدام کنید تا از بروز اختلال در روند فروش جلوگیری شود.

            با احترام
            تیم StockMaster
            مدیریت هوشمند فروش و انبارداری  """
        if quantity.quantity <= 5 or 0:
            send_mail(subject,message,settings.EMAIL_HOST_USER,[get_user.email])
    return JsonResponse({'status':"success"})