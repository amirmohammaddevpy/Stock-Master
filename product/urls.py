from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("",views.product_entry,name="product_entry"),
    path("category/create/",views.category_create,name="category_create"),
    path("sale/product",views.sale_product,name="sale_product"),
    path('<int:pk>/price/',views.product_price ,name="product_price"),
    path('sale/history',views.sales_history,name="sales_history"),
    path('products/',views.products,name="products")
]
