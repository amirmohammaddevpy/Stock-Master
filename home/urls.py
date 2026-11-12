from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path("",views.home,name="home"),
    path('reports/',views.reports,name="reports"),
    path('daily/stock/check',views.send_email,name="daily_stock_check")
]
