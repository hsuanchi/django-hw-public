from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum

from rest_framework import generics, views, status, response

from trade.models import Product, Order
from trade.api.serializers import (
    ProductSerializer,
    OrderSerializer,
    OrderSalesSerializer,
)
from trade.api.decorator import check_stock_and_vip


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderList(views.APIView):
    def get(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return response.Response(serializer.data)

    @check_stock_and_vip
    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            serializer.save(data)
            return JsonResponse({"message": "success"})
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_stock_and_vip
    def delete(self, request, format=None):
        data = request.data
        Order.objects.delete_order(data["order_id"])
        return JsonResponse({"message": "success"})


class OrderTopSalesDetail(views.APIView):
    def get(self, request):
        queryset = (
            Order.objects.values("product_id")
            .annotate(total_sales=Sum("qty"))
            .order_by("-total_sales")
        )
        serializer = OrderSalesSerializer(queryset[:3], many=True)
        return response.Response(serializer.data)
