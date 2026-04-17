"""
scheduler.py — Background order-status SMS notifications.
Uses APScheduler to run every 6 hours and notify users via Fast2SMS.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
import logging

log = logging.getLogger(__name__)

STAGES = ['Processing', 'Packaging', 'Ready to Ship', 'Shipped', 'Out for Delivery', 'Delivered']


def check_and_notify():
    """Check every active order and SMS user when their delivery stage advances."""
    from backend.db import query_db, get_db
    from backend.sms import send_order_sms

    try:
        orders = query_db("""
            SELECT o.orderID, o.order_date, o.last_notified_step, u.mobile
            FROM orders o
            JOIN user u ON o.userid = u.userid
            WHERE o.userid != 'Deleted Account'
              AND u.mobile IS NOT NULL
              AND (o.last_notified_step IS NULL OR o.last_notified_step < 5)
        """)
    except Exception as e:
        log.warning(f'[Scheduler] DB error: {e}')
        return

    notified = 0
    for o in orders:
        try:
            ds    = o['order_date']                          # DD/MM/YYYY
            start = date(int(ds[6:10]), int(ds[3:5]), int(ds[0:2]))
            diff  = (date.today() - start).days
            step  = min(diff, 5)
            last  = o['last_notified_step'] if o['last_notified_step'] is not None else -1

            if step > last:
                log.info(f'[Scheduler] Notifying Order #{o["orderID"]} (Stage: {STAGES[step]})')
                ok = send_order_sms(o['mobile'], o['orderID'], STAGES[step])
                if ok:
                    query_db(
                        'UPDATE orders SET last_notified_step=%s WHERE orderID=%s',
                        (step, o['orderID']), commit=True
                    )
                    notified += 1
                else:
                    log.warning(f'[Scheduler] SMS failed for Order #{o["orderID"]}')
            else:
                log.debug(f'[Scheduler] Order #{o["orderID"]} still at step {step} (last notified: {last})')
        except Exception as e:
            log.warning(f'[Scheduler] Order {o.get("orderID")} error: {e}')

    if notified:
        log.info(f'[Scheduler] Sent {notified} order-status SMS(es)')


def start_scheduler():
    """Start the background scheduler. Call this once when Flask app starts."""
    scheduler = BackgroundScheduler(timezone='Asia/Kolkata')
    scheduler.add_job(
        check_and_notify,
        trigger='interval',
        seconds=5,
        id='order_notify',
        replace_existing=True,
        max_instances=1,
    )
    scheduler.start()
    log.info('[Scheduler] Background order-status job started (polling every 5s)')
    return scheduler
