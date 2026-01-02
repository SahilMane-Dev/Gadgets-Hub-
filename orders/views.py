from django.shortcuts import render , HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Order
# Create your views here.


@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(user = request.user).order_by("-created_at")


    return render(request, "orders/my_orders.html", {
        "orders": orders
    })