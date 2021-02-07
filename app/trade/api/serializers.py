from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from trade.models import Product, Order, Shop


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ["shop_id"]


class ProductSerializer(ModelSerializer):
    shop_id = ShopSerializer()

    class Meta:
        model = Product
        fields = ("id", "price", "stock_pcs", "shop_id", "vip")

    def get_shop_id_detail(self, obj):
        return ShopSerializer(obj.shop_id).data


class OrderSerializer(ModelSerializer):
    product_detail = serializers.SerializerMethodField("get_product_detail")

    class Meta:
        model = Order
        fields = ["id", "product_id", "product_detail", "qty", "customer_id"]
        read_only_fields = ["id", "product_detail"]

    def get_product_detail(self, obj):
        return ProductSerializer(obj.product_id).data

    def save(self, data):
        Order.objects.create_order(
            customer_id=data["customer_id"],
            product_id=data["product_id"],
            qty=data["qty"],
        )


class OrderSalesSerializer(Serializer):
    product_id = serializers.IntegerField()
    # total_sales = serializers.IntegerField()
