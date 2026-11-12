from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250,unique=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name="products")
    quantity = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    buy_price = models.DecimalField(validators=[MinValueValidator(0)])
    sell_price = models.DecimalField(validators=[MinValueValidator(0)])
    code_product = models.CharField(max_length=250,unique=True)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class SelesProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="sales")
    owner = models.ForeignKey(User,on_delete=models.CASCADE,)
    quantity = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(validators=[MinValueValidator(0)])
    total_price = models.DecimalField(validators=[MinValueValidator(0)])
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.product} - {self.total_price} '