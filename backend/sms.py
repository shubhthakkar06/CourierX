"""
sms.py — Twilio SMS Integration
Handles OTP generation/verification and order status SMS.

Twilio Account: get from https://console.twilio.com/
Add to .env:  TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
"""

import os
import random
import time
import requests
import threading
from backend.db import query_db
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN  = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUM   = os.getenv('TWILIO_PHONE_NUMBER', '')
TWILIO_URL         = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"

# ── Helpers ────────────────────────────────────────────────────────────────────
def _clean(mobile: str) -> str:
    """Ensure standard E.164 format limit. Defaults to +91 if missing."""
    clean_num = mobile.replace(' ', '').strip()
    if not clean_num.startswith('+'):
        # If lengths match local number, prefix with +91
        if len(clean_num) == 10:
            return f"+91{clean_num}"
        return f"+{clean_num}"
    return clean_num


def _enabled() -> bool:
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUM:
        print('[SMS] Twilio credentials not set — SMS disabled')
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
        return True, 'OTP printed to console (Twilio credentials not set)'

    try:
        r = requests.post(
            TWILIO_URL,
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            data={
                'To': number,
                'From': TWILIO_PHONE_NUM,
                'Body': f'Your CourierX verification code is: {otp}. This code expires in 10 minutes.'
            },
            timeout=10
        )
        data = r.json()
        if r.status_code in (200, 201):
            return True, 'OTP sent successfully'
        err = data.get('message', 'SMS send failed')
        return False, str(err)
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
# Messages for order status updates sent to the user
_STAGE_MSG = {
    'Processing':       'CourierX: Order #{id} received & is being processed.',
    'Packaging':        'CourierX: Order #{id} is being packaged.',
    'Ready to Ship':    'CourierX: Order #{id} is ready to ship!',
    'Shipped':          'CourierX: Order #{id} has been shipped!',
    'Out for Delivery': 'CourierX: Order #{id} is OUT FOR DELIVERY today!',
    'Delivered':        'CourierX: Order #{id} DELIVERED! Thank you for using CourierX.',
    'Cancelled_User':   'CourierX: Your order #{id} has been successfully cancelled.',
    'Cancelled_Admin':  "CourierX: We're sorry for the inconvenience, but your order #{id} has been cancelled by our system administrator."
}


def _send_twilio_async(number: str, message_body: str, stage: str):
    """Background task to avoid blocking the user API route."""
    try:
        r = requests.post(
            TWILIO_URL,
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            data={
                'To': number,
                'From': TWILIO_PHONE_NUM,
                'Body': message_body
            },
            timeout=10
        )
        data = r.json()
        if r.status_code in (200, 201):
            print(f'[SMS] Success: Order SMS sent to {number} | Stage: {stage}')
        else:
            print(f'[SMS] Twilio Error: {r.status_code} | {data.get("message", data)}')
    except Exception as e:
        print(f'[SMS] Connection Error: {e}')


def send_order_sms(mobile: str, order_id: int, stage: str) -> bool:
    """
    Spawns an asynchronous background thread to send an order status SMS via Twilio.
    """
    number  = _clean(mobile)
    message_body = _STAGE_MSG.get(stage, f'CourierX Order #{order_id}: {stage}').replace('{id}', str(order_id))

    if not _enabled():
        print(f'[SMS-DEV] Order SMS to {number}: {message_body}')
        return True

    # Fire and forget asynchronously
    threading.Thread(target=_send_twilio_async, args=(number, message_body, stage)).start()
    return True
