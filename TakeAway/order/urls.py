from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('menu/', views.menu, name="menu"),
    path('cart/', views.cart, name="cart"),
    path('review/', views.review, name="review"),
    path('order/', views.order, name="order"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order")
]