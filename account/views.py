from django.shortcuts import render ,redirect
from .forms import RegisterUser ,LoginUser
from django.contrib.auth import login ,logout ,authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta ,datetime
from django.contrib.auth.models import User
import secrets



# Create your views here.

def login_user(request):
    subject = "ورود موفق به حساب کاربری | StockMaster"
    
    if request.method == "POST":
        form = LoginUser(request.POST)
        if form.is_valid():
            user = authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                message = f"""
                کاربر گرامی {user.username}،
                ورود شما به سامانه StockMaster با موفقیت انجام شد.

                جزئیات ورود:
                نام کاربری: {user.username}
                ایمیل: {user.email}

                اگر این ورود توسط شما انجام نشده است، لطفاً در اسرع وقت رمز عبور حساب خود را تغییر دهید.

                با احترام
                تیم StockMaster
                مدیریت هوشمند فروش و انبارداری"""
                
                login(request,user)
                get_user = User.objects.get(username=user.username)
                send_mail(subject,message,settings.EMAIL_HOST_USER,[get_user.email])
                return redirect("home:home")
            else:
                messages.error(request,"user not found")
    else:
        form = LoginUser()
    return render(request,'account/login.html',{'form':form})

def register_user(request):
    code = secrets.randbelow(900000) + 100000
    request.session['code'] = code
    subject = "StockMaster"
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            
            if password != password_confirm:
                messages.error(request,"Password is not match")
                return render(request,"account/register.html",{"form": form})
            else:
                user.set_password(password_confirm)
                user.save()
                request.session['user_id'] = user.id
                address = user.email
                try:
                    send_mail(subject,f"code verify {code}" , settings.EMAIL_HOST_USER, [address])
                    request.session['time_send_code'] = (timezone.now() + timedelta(minutes=2)).isoformat()
                except Exception:
                    user.delete()
                    request.session.pop("user_id", None)
                    request.session.pop("code", None)
                    messages.error(request,"Email could not be sent. Please try again.")
                    return render(request,"account/register.html",{"form": form})
                
                return redirect("accounts:verify_code")
        else:
            print(form.errors)
            messages.error(request,"form isn't valid")
    else:
        form = RegisterUser()
    return render(request,"account/register.html",{'form':form})

def verify_code(request):
    get_code = request.session.get("code")
    get_time = request.session.get("time_send_code")
    get_user_id = request.session.get("user_id")

    
    try:
        user = User.objects.get(id=get_user_id)
    except:
        messages.error(request,"user is not found")
    
    if request.method == "POST":
        code = request.POST.get("verify_code")
        get_time = datetime.fromisoformat(get_time)
        if timezone.now() > get_time:
            messages.error(request, "Verification code expired.")
            return redirect("accounts:register")
        if str(code) == str(get_code):
            user.is_active = True
            user.save()
            login(request,user)            
            request.session.pop("code", None)
            request.session.pop("code_expire", None)
            request.session.pop("user_id", None)
            return redirect("home:home")
    return render(request,"account/verify_code.html")

def logout_user(request):
    logout(request)
    return redirect("home:home")