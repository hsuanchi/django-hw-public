from django.urls import include, path
from rest_framework import routers
from trade.api import views

urlpatterns = [
    path("products/", views.ProductList.as_view(), name="products"),
    path("products/<int:pk>/", views.ProductDetail.as_view()),
    path("orders/", views.OrderList.as_view() ,name="orders"),
    path("orders/topsales/", views.OrderTopSalesDetail.as_view(),name="topsales"),
]
