from django.shortcuts import render, redirect
from products.models import Product
from orders.models import Order , OrderItem
from django.contrib.auth.decorators import login_required

# ---------------------------
# VIEW CART
# ---------------------------

def view_cart(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0

    for product_id_str, qty in cart.items():
        product_id = int(product_id_str)
        product = Product.objects.get(id=product_id)

        items.append({
            "product": product,
            "quantity": qty,
            "subtotal": product.price * qty,
        })

        total += product.price * qty

    return render(request, "cart/cart.html", {
        "items": items,
        "total": total
    })


# ---------------------------
# ADD TO CART
# ---------------------------

def add_to_cart(request, id):
    cart = request.session.get("cart", {})

    # always store product_id as STRING
    pid = str(id)

    cart[pid] = cart.get(pid, 0) + 1
    request.session["cart"] = cart

    return redirect("view_cart")


# ---------------------------
# INCREASE QTY
# ---------------------------
def increase_cart(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)

    cart[pid] = cart.get(pid, 0) + 1
    request.session["cart"] = cart

    return redirect("view_cart")


# ---------------------------
# DECREASE QTY
# ---------------------------
def decrease_cart(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)

    if cart.get(pid, 0) > 1:
        cart[pid] -= 1
    else:
        cart.pop(pid, None)

    request.session["cart"] = cart
    return redirect("view_cart")


# ---------------------------
# REMOVE ITEM
# ---------------------------
def remove_cart(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)

    cart.pop(pid, None)
    request.session["cart"] = cart

    return redirect("view_cart")


from django.shortcuts import render, redirect
from products.models import Product

@login_required(login_url="login")
def checkout(request):
    cart = request.session.get("cart", {})

    items = []
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=int(pid))

        items.append({
            "product" : product,
            "quantity": qty,
            "subtotal": float(product.price * qty)
        })

        total += product.price * qty

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        name = first_name + " " + last_name

        # create a order
        order = Order.objects.create(
            user = request.user,
            customer_name = name,
            email = email,
            phone = phone,
            address = address,
            city = city,
            total_amount = total

        )

        for item in items:
            OrderItem.objects.create(
                order = order,
                product = item["product"],
                quantity = item["quantity"],
                price = item['product'].price
            )

        request.session["cart"] = {}


        request.session["last_order_id"] = order.id

        return redirect("order_success")

    return render(request, "cart/checkout.html", {
        "items": items,
        "total": total
    })

@login_required
def order_success(request):
    order_id = request.session.get("last_order_id")

    if not order_id:
        return redirect("view_cart")  # if someone opens success page without order

    order = Order.objects.get(id = order_id)
    return render(request, "cart/order_success.html", {
        "order": order
    })
