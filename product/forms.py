from django import forms
from .models import Product ,Category,SelesProduct

class SaleProduct(forms.ModelForm):
    class Meta:
        model = SelesProduct
        fields = ('product','quantity','unit_price','total_price',)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name","description")

class Transactions(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name","category","quantity","buy_price","sell_price","code_product","description",)
        widgets = {
            'purchase_price': forms.NumberInput(attrs={
                'class': 'price-input',
                'placeholder': 'قیمت محصول را وارد کنید'
            }),
        }