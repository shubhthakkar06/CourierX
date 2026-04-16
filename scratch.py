import os
import sys
from datetime import date
sys.path.insert(0, os.path.abspath('.'))
from backend.db import query_db

try:
    orders = query_db("""
        SELECT o.orderID, o.order_date, o.last_notified_step, u.mobile
        FROM orders o
        JOIN user u ON o.userid = u.userid
        WHERE o.userid != 'Deleted Account'
        AND u.mobile IS NOT NULL
        AND (o.last_notified_step IS NULL OR o.last_notified_step < 5)
    """)
    print(f"DEBUG: Found {len(orders)} active orders needing attention.")
    for o in orders:
        ds    = o['order_date']
        start = date(int(ds[6:10]), int(ds[3:5]), int(ds[0:2]))
        diff  = (date.today() - start).days
        step  = min(diff, 5)
        last  = o['last_notified_step'] if o['last_notified_step'] is not None else -1
        print(f"DEBUG: Order {o['orderID']} | date: {o['order_date']} | diff: {diff} | step: {step} | last: {last} | send? {step > last}")
except Exception as e:
    print(f"ERROR: {e}")
