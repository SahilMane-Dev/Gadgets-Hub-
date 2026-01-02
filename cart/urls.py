from django.urls import path
from . views import add_to_cart , view_cart
from . import views

urlpatterns =[
    path("add/<int:id>/" , add_to_cart , name="add_to_cart"),
    path("" , view_cart , name="view_cart"),
    path("increase/<int:product_id>/", views.increase_cart, name="increase_cart"),
    path("decrease/<int:product_id>/", views.decrease_cart, name="decrease_cart"),
    path("remove/<int:product_id>/", views.remove_cart, name="remove_cart"),


    path("checkout/" , views.checkout , name= "checkout"),
    path("order_success/" ,views.order_success , name = "order_success")
 


]