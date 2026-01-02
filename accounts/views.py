from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Signup successful! Please login.")
            return redirect("login")

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        #copy cart before login
        old_cart = request.session.get("cart" , {}).copy()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            #restore cart

            request.session["cart"] = old_cart
            request.session.modified = True

            print(request.session.get("cart"))

            messages.success(request, f"Welcome back, {user.username}")
            return redirect("view_cart")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")

@login_required(login_url='login')
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/orders.html', {'orders': orders})

