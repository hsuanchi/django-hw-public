from datetime import date
from django.db import connection

import csv


def daily_report():
    """
    每日零點根據訂單記錄算出各個館別的
    1. 總銷售金額
    2. 總銷售數量
    3. 總訂單數量
    """

    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT  
        s.shop_id AS shop_name,
        COUNT("order".id) AS total_order_count,
        SUM("order".qty) AS total_qty_sum,
        SUM("order".qty*p.price) AS total_order_sale
    FROM "order"
        LEFT JOIN "product" p ON "order".product_id_id=p.id
        LEFT JOIN "trade_shop" s ON p.shop_id_id=s.id 
    GROUP BY
        shop_name
    """
    )

    querys = cursor.fetchall()

    today = date.today()
    date_str = today.strftime("%Y-%m-%d")

    with open("document/" + date_str + "_result.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["館別", "總訂單數量", "總銷售數量", "總銷售金額"])
        for query in querys:
            writer.writerow(query)
