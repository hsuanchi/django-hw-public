from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from trade.models import Product, Order


def check_stock_and_vip(fn):
    def decorator(self, request, *args, **kw):

        if request.method == "POST":
            qty = int(request.data["qty"])
            product_id = request.data["product_id"]
            vip_only = request.data["vip"]
            quertset = get_object_or_404(Product, id=product_id)

            # 權限不足
            if quertset.vip and vip_only == "no":
                return JsonResponse({"message": "權限不足"})

            # 庫存不足
            if qty > quertset.stock_pcs:
                return JsonResponse({"message": "貨源不足"})

            return fn(self, request, *args, **kw)

        if request.method == "DELETE":
            order_id = request.data["order_id"]
            queryset = get_object_or_404(Order, id=order_id)

            # 庫存等於零
            if queryset.product_id.stock_pcs == 0:
                fn(self, request, *args, **kw)
                return JsonResponse({"message": "商品到貨"})
            return fn(self, request, *args, **kw)

    return decorator
