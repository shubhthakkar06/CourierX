"""
sms.py — Fast2SMS Integration
Handles OTP generation/verification and order status SMS.

Fast2SMS API Key: get from https://www.fast2sms.com → Developer → API
Add to .env:  FAST2SMS_API_KEY=your_key_here
"""

import os
import random
import time
import requests
from backend.db import query_db
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

FAST2SMS_KEY = os.getenv('FAST2SMS_API_KEY', '')
F2S_URL      = 'https://www.fast2sms.com/dev/bulkV2'

# ── Helpers ────────────────────────────────────────────────────────────────────
def _clean(mobile: str) -> str:
    """Strip country code and spaces → 10-digit number."""
    return mobile.replace('+91', '').replace(' ', '').strip()


def _enabled() -> bool:
    if not FAST2SMS_KEY:
        print('[SMS] FAST2SMS_API_KEY not set — SMS disabled')
        return False
    return True


# ── OTP (stored in DB for persistence across restarts) ────────────────────────
def _gen_otp() -> str:
    return str(random.randint(100000, 999999))


def send_otp(mobile: str) -> tuple[bool, str]:
    """
    Generate a 6-digit OTP, persist it to otp_store table, and send via Fast2SMS.
    Returns (success: bool, message: str).
    """
    number = _clean(mobile)
    otp    = _gen_otp()
    ts     = int(time.time())

    # Upsert into DB (replace any existing OTP for this number)
    query_db(
        'REPLACE INTO otp_store(mobile, otp_code, created_at) VALUES(%s, %s, %s)',
        (number, otp, ts), commit=True
    )

    if not _enabled():
        # Dev mode — print OTP to console so developer can test without SMS
        print(f'[SMS-DEV] OTP for {number}: {otp}')
        return True, 'OTP printed to console (SMS key not set)'

    try:
        r = requests.post(
            F2S_URL,
            json={'route': 'otp', 'variables_values': otp, 'numbers': number, 'flash': 0},
            headers={'authorization': FAST2SMS_KEY, 'Content-Type': 'application/json'},
            timeout=10
        )
        data = r.json()
        if data.get('return'):
            return True, 'OTP sent successfully'
        err = data.get('message', ['SMS send failed'])[0] if isinstance(data.get('message'), list) else str(data.get('message', 'Failed'))
        return False, err
    except Exception as e:
        return False, f'SMS error: {str(e)}'


def verify_otp(mobile: str, code: str) -> tuple[bool, str]:
    """
    Verify OTP against DB store. OTPs expire after 10 minutes.
    Returns (valid: bool, message: str).
    """
    number = _clean(mobile)
    row    = query_db('SELECT otp_code, created_at FROM otp_store WHERE mobile=%s', (number,), fetchone=True)

    if not row:
        return False, 'No OTP found — please request a new one'

    if int(time.time()) - row['created_at'] > 600:   # 10 min expiry
        query_db('DELETE FROM otp_store WHERE mobile=%s', (number,), commit=True)
        return False, 'OTP has expired — please request a new one'

    if row['otp_code'] != str(code).strip():
        return False, 'Incorrect OTP'

    # Valid — consume it
    query_db('DELETE FROM otp_store WHERE mobile=%s', (number,), commit=True)
    return True, 'OTP verified'


# ── Order Status SMS ───────────────────────────────────────────────────────────
# ── Stage → short numeric code sent via OTP route ─────────────────────────────
# DLT (TRAI) registration is required for custom-text SMS in India.
# Until DLT is registered, we send the delivery stage NUMBER via the OTP route
# so the user at least gets a real SMS. Message reads:
#   "Your OTP for Fast2SMS is <stage_step>. This OTP is valid for 10 minutes."
# Stage map: 0=Processing 1=Packaging 2=ReadyToShip 3=Shipped 4=OutForDelivery 5=Delivered
_STAGE_NUM = {
    'Processing': '10', 'Packaging': '20', 'Ready to Ship': '30',
    'Shipped': '40', 'Out for Delivery': '50', 'Delivered': '60',
}

# Full messages for console log (shown when DLT SMS is available or in dev)
_STAGE_MSG = {
    'Processing':       'CourierX: Order #{id} received & is being processed.',
    'Packaging':        'CourierX: Order #{id} is being packaged.',
    'Ready to Ship':    'CourierX: Order #{id} is ready to ship!',
    'Shipped':          'CourierX: Order #{id} has been shipped!',
    'Out for Delivery': 'CourierX: Order #{id} is OUT FOR DELIVERY today!',
    'Delivered':        'CourierX: Order #{id} DELIVERED! Thank you for using CourierX.',
}


def send_order_sms(mobile: str, order_id: int, stage: str) -> bool:
    """
    Send an order status SMS via Fast2SMS.
    Uses OTP route (no DLT needed) — sends stage number so user knows something changed.
    Upgrade to DLT route for full custom messages in production.
    """
    number  = _clean(mobile)
    log_msg = _STAGE_MSG.get(stage, f'Order #{order_id}: {stage}').replace('{id}', str(order_id))

    if not _enabled():
        print(f'[SMS-DEV] Order SMS to {number}: {log_msg}')
        return True

    # Use OTP route (no DLT) — stage code as the variable
    stage_code = _STAGE_NUM.get(stage, '99')
    try:
        r = requests.post(
            F2S_URL,
            json={'route': 'otp', 'variables_values': stage_code, 'numbers': number, 'flash': 0},
            headers={'authorization': FAST2SMS_KEY, 'Content-Type': 'application/json'},
            timeout=10
        )
        data = r.json()
        success = bool(data.get('return'))
        if success:
            print(f'[SMS] Order notification sent → {number} | Stage: {stage}')
        else:
            print(f'[SMS] Order SMS failed: {data}')
        return success
    except Exception as e:
        print(f'[SMS] Order SMS error: {e}')
        return False
