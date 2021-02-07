from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_text

from trade.models import Product, Shop, Order

class OrderTest(TestCase):
    def setUp(self):
        s = Shop.objects.create(shop_id="um")
        p1 = Product.objects.create(price=666,stock_pcs=10,shop_id=s,vip=True)
        p2 = Product.objects.create(price=666,stock_pcs=10,shop_id=s,vip=True)
        p3 = Product.objects.create(price=666,stock_pcs=10,shop_id=s,vip=True)
        p1.save()
        p2.save()
        p3.save()

    def create_order(self,qty, product_id):
        query_product = Product.objects.get(id=product_id)
        query = Order.objects.create_order(product_id=query_product,qty=qty,customer_id=1) 
        query.save()

    def test_order_post_vip_denied(self):
        response = self.client.post(
            reverse("orders"),
            {
                "product_id": 1,
                "qty": 1,
                "customer_id": 1,
                "vip": "no"
            }, content_type='application/json'
        )

        self.assertJSONEqual(force_text(response.content), {'message': '權限不足'})

    def test_order_post_stock_denied(self):
        response = self.client.post(
            reverse("orders"),
            {
                "product_id": 1,
                "qty": 11,
                "customer_id": 1,
                "vip": "yes"
            }, content_type='application/json'
        )
        self.assertJSONEqual(force_text(response.content), {'message': '貨源不足'})

    def test_order_post_success(self):
        response = self.client.post(
            reverse("orders"),
            {
                "product_id": 1,
                "qty": 1,
                "customer_id": 1,
                "vip": "yes"
            }, content_type='application/json'
        )
        self.assertJSONEqual(force_text(response.content), {'message': 'success'})

    def test_order_delete_prodcut_arived(self):
        self.create_order(qty=10,product_id=1)

        response = self.client.delete(
            reverse("orders"),
            {
                "order_id": 1
            }, content_type='application/json'
        )
        self.assertJSONEqual(force_text(response.content), {'message': '商品到貨'})

    def test_order_delete_success(self):
        self.create_order(qty=1,product_id=1)

        response = self.client.delete(
            reverse("orders"),
            {
                "order_id": 1
            }, content_type='application/json'
        )
        self.assertJSONEqual(force_text(response.content), {'message': 'success'})

    def test_top_sales_get(self):
        self.create_order(qty=3,product_id=1)
        self.create_order(qty=2,product_id=2)
        self.create_order(qty=1,product_id=3)

        response = self.client.get(
            reverse("topsales"),
        )
        self.assertJSONEqual(force_text(response.content),[{'product_id': 1}, {'product_id': 2}, {'product_id': 3}])
