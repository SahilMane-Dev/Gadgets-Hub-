from django.shortcuts import render , get_object_or_404
from .models import Product

# Create your views here.
def home(request):
    top_three = Product.objects.all()[4:7]
    return render(request , "home.html" , {"top_three" : top_three})

def product_list(request):
    products = Product.objects.all() #get all products added frm admin
    return render(request , 'products/products_list.html' , {"products" : products})


def product_detail(request , id):
    product = get_object_or_404(Product , id = id)
    return render(request , "products/product_detail.html" , {"product" : product})


