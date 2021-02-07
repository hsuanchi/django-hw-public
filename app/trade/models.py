from django.db import models
from django.shortcuts import get_object_or_404


class OrderManager(models.Manager):
    def create_order(self, customer_id, product_id, qty):
        queryset = self.model(customer_id=customer_id, product_id=product_id, qty=qty)
        queryset.save()
        product_id.stock_pcs -= int(qty)
        product_id.save()
        return queryset

    def delete_order(self, order_id):
        queryset = get_object_or_404(Order, id=order_id)
        product = queryset.product_id
        product.stock_pcs += int(queryset.qty)
        product.save()
        queryset.delete()


class Shop(models.Model):
    shop_id = models.CharField(max_length=50)

    def __str__(self):
        return str(self.shop_id)


class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock_pcs = models.IntegerField(default=0)
    shop_id = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    vip = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "product"


class Order(models.Model):
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    customer_id = models.IntegerField(default=1)

    objects = OrderManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "order"
