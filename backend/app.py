"""
app.py — CourierX Flask REST API
Serves both the JSON API and the static frontend files.

Run:
    source venv/bin/activate
    python main.py

Then open: http://localhost:5000
"""

from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import random
import time
import os
from datetime import date
from backend.db import get_db, query_db
from backend.sms import send_otp, verify_otp

# ── App Setup ──────────────────────────────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.secret_key = 'courierx_secret_xK9mP_2024'
CORS(app, supports_credentials=True)

# ── DB Helpers imported from backend.db ────────────────────────────────────────
# get_db()    → returns a new MySQL connection
# query_db()  → executes SQL and returns results


def authed():
    uid = session.get('userid')
    if not uid:
        return None
    return uid


# ── Frontend Serving ───────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_frontend(path):
    target = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(target):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')


# ── OTP Routes ─────────────────────────────────────────────────────────────────
@app.route('/api/otp/send', methods=['POST'])
def otp_send():
    """
    Send OTP. Two modes:
      - Sign-up:        body = { mobile: "9876543210" }
      - Profile action: body = {}  → reads mobile from logged-in user's profile
    """
    d      = request.json or {}
    mobile = d.get('mobile', '').strip()

    if not mobile:
        # Profile mode — fetch from session user
        uid = authed()
        if not uid:
            return jsonify(error='Not authenticated'), 401
        user = query_db('SELECT mobile FROM user WHERE userid=%s', (uid,), fetchone=True)
        if not user or not user.get('mobile'):
            return jsonify(error='No mobile number on your account. Please contact support.'), 400
        mobile = user['mobile']

    # Basic validation
    clean = mobile.replace('+91', '').replace(' ', '')
    if len(clean) != 10 or not clean.isdigit():
        return jsonify(error='Enter a valid 10-digit Indian mobile number'), 400

    ok, msg = send_otp(clean)
    if ok:
        return jsonify(message=f'OTP sent to +91{clean[-4:].zfill(10)[-4:].rjust(10,"*")}'), 200
    return jsonify(error=msg), 500


@app.route('/api/otp/verify', methods=['POST'])
def otp_verify_standalone():
    """Quick verify endpoint for frontend pre-validation (sign-up step 2 check)."""
    d      = request.json or {}
    mobile = d.get('mobile', '').replace('+91', '').replace(' ', '').strip()
    code   = str(d.get('code', '')).strip()
    valid, msg = verify_otp(mobile, code)
    if valid:
        # Re-insert a fresh verified token so signup can consume it
        import time as _t
        query_db(
            'REPLACE INTO otp_store(mobile,otp_code,created_at) VALUES(%s,%s,%s)',
            (mobile, code, int(_t.time())), commit=True
        )
        return jsonify(verified=True), 200
    return jsonify(verified=False, error=msg), 400


# ── Auth Routes ────────────────────────────────────────────────────────────────
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data     = request.json or {}
    uid      = (data.get('userid')   or '').lower().strip()
    username = (data.get('username') or '').strip().lower()
    password = (data.get('password') or '').strip()
    mobile   = (data.get('mobile')   or '').replace('+91', '').replace(' ', '').strip()
    otp_code = str(data.get('otp_code', '')).strip()
    dob      = (data.get('dob')      or '').strip()

    # Validations
    if len(username) < 8 or len(username) > 30:
        return jsonify(error='Username must be 8–30 characters'), 400
    if not username.isalpha():
        return jsonify(error='Username must contain only letters'), 400
    if len(uid) < 8 or len(uid) > 30:
        return jsonify(error='Email must be 8–30 characters'), 400
    if '@' not in uid or not uid.endswith('.com'):
        return jsonify(error='Email must be like user@gmail.com'), 400
    if len(password) < 8 or len(password) > 20:
        return jsonify(error='Password must be 8–20 characters'), 400
    if password.islower() or password.isupper():
        return jsonify(error='Password needs at least one uppercase letter'), 400
    if '@' not in password:
        return jsonify(error='Password must contain the @ symbol'), 400
    if ' ' in password:
        return jsonify(error='Password must not have spaces'), 400
    if len(mobile) != 10 or not mobile.isdigit():
        return jsonify(error='Enter a valid 10-digit mobile number'), 400
    if not dob:
        return jsonify(error='Date of birth is required'), 400

    # Verify OTP
    valid, msg = verify_otp(mobile, otp_code)
    if not valid:
        return jsonify(error=f'OTP error: {msg}'), 400

    # Uniqueness checks
    if query_db('SELECT userid FROM user WHERE userid=%s', (uid,), fetchone=True):
        return jsonify(error='Email already registered'), 409
    if query_db('SELECT mobile FROM user WHERE mobile=%s', (mobile,), fetchone=True):
        return jsonify(error='Mobile number already registered'), 409

    query_db(
        'INSERT INTO user(userid,username,password,DOB,mobile) VALUES(%s,%s,%s,%s,%s)',
        (uid, username, password, dob, mobile), commit=True
    )
    session['userid']   = uid
    session['username'] = username
    return jsonify(message='Account created', userid=uid, username=username), 201


@app.route('/api/auth/signin', methods=['POST'])
def signin():
    data     = request.json or {}
    uid      = (data.get('userid')   or '').lower().strip()
    password = (data.get('password') or '').strip()

    user = query_db('SELECT * FROM user WHERE userid=%s', (uid,), fetchone=True)
    if not user:
        return jsonify(error='Email not found'), 404

    wpd      = query_db('SELECT attemps FROM wpd', fetchone=True)
    attempts = wpd['attemps'] if wpd else 1

    if user['password'] != password:
        if attempts >= 3:
            query_db('UPDATE wpd SET attemps=1', commit=True)
            return jsonify(error='Too many failed attempts. Please reset your password.', locked=True), 403
        query_db('UPDATE wpd SET attemps=%s', (attempts + 1,), commit=True)
        return jsonify(error=f'Incorrect password — {3 - attempts} attempt(s) left'), 401

    query_db('UPDATE wpd SET attemps=1', commit=True)
    session['userid']   = uid
    session['username'] = user['username']
    return jsonify(message='Signed in', userid=uid, username=user['username']), 200


@app.route('/api/auth/signout', methods=['POST'])
def signout():
    session.clear()
    return jsonify(message='Signed out'), 200


@app.route('/api/auth/me', methods=['GET'])
def me():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    return jsonify(userid=uid, username=session.get('username')), 200


# ── Profile Routes ─────────────────────────────────────────────────────────────
@app.route('/api/profile', methods=['GET'])
def get_profile():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    user = query_db('SELECT userid,username,DOB,mobile FROM user WHERE userid=%s', (uid,), fetchone=True)
    if not user:
        return jsonify(error='User not found'), 404
    return jsonify(user), 200


def _get_mobile(uid):
    """Return the user's registered mobile number."""
    u = query_db('SELECT mobile FROM user WHERE userid=%s', (uid,), fetchone=True)
    return (u or {}).get('mobile')


def _verify_user_otp(uid, code):
    """Verify OTP against the logged-in user's registered mobile."""
    mobile = _get_mobile(uid)
    if not mobile:
        return False, 'No mobile number on account'
    return verify_otp(mobile, code)


@app.route('/api/profile/password', methods=['PUT'])
def update_password():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    data     = request.json or {}
    otp_code = str(data.get('otp_code', '')).strip()
    new_pass = (data.get('new_password') or '').strip()

    valid, msg = _verify_user_otp(uid, otp_code)
    if not valid:
        return jsonify(error=f'OTP error: {msg}'), 403
    if len(new_pass) < 8 or len(new_pass) > 20 or '@' not in new_pass or ' ' in new_pass:
        return jsonify(error='Password must be 8-20 chars, contain @, no spaces'), 400
    if new_pass.islower() or new_pass.isupper():
        return jsonify(error='Password needs at least one uppercase letter'), 400

    query_db('UPDATE user SET password=%s WHERE userid=%s', (new_pass, uid), commit=True)
    return jsonify(message='Password updated'), 200


@app.route('/api/profile/username', methods=['PUT'])
def update_username():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    data     = request.json or {}
    otp_code = str(data.get('otp_code', '')).strip()
    new_name = (data.get('username') or '').strip().lower()

    valid, msg = _verify_user_otp(uid, otp_code)
    if not valid:
        return jsonify(error=f'OTP error: {msg}'), 403
    if len(new_name) < 8 or len(new_name) > 30 or not new_name.isalpha():
        return jsonify(error='Username must be 8-30 letters only'), 400

    query_db('UPDATE user SET username=%s WHERE userid=%s', (new_name, uid), commit=True)
    session['username'] = new_name
    return jsonify(message='Username updated', username=new_name), 200


@app.route('/api/profile/dob', methods=['PUT'])
def update_dob():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    data     = request.json or {}
    otp_code = str(data.get('otp_code', '')).strip()
    new_dob  = (data.get('dob') or '').strip()

    valid, msg = _verify_user_otp(uid, otp_code)
    if not valid:
        return jsonify(error=f'OTP error: {msg}'), 403
    if not new_dob:
        return jsonify(error='Date of birth required'), 400

    query_db('UPDATE user SET DOB=%s WHERE userid=%s', (new_dob, uid), commit=True)
    return jsonify(message='Date of birth updated'), 200


@app.route('/api/profile', methods=['DELETE'])
def delete_account():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    data     = request.json or {}
    otp_code = str(data.get('otp_code', '')).strip()

    valid, msg = _verify_user_otp(uid, otp_code)
    if not valid:
        return jsonify(error=f'OTP error: {msg}'), 403

    query_db('DELETE FROM addresses WHERE userid=%s',          (uid,), commit=True)
    query_db("UPDATE orders SET userid='Deleted Account' WHERE userid=%s", (uid,), commit=True)
    query_db('DELETE FROM user WHERE userid=%s',               (uid,), commit=True)
    session.clear()
    return jsonify(message='Account deleted'), 200


# ── Address Routes ─────────────────────────────────────────────────────────────
@app.route('/api/addresses', methods=['GET'])
def get_addresses():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    rows = query_db('SELECT * FROM addresses WHERE userid=%s', (uid,))
    return jsonify(rows), 200


@app.route('/api/addresses', methods=['POST'])
def add_address():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    d       = request.json or {}
    pincode = str(d.get('pincode', ''))
    name    = str(d.get('name',    ''))
    city    = str(d.get('city',    ''))
    street  = str(d.get('street',  ''))
    house   = str(d.get('house',   ''))
    mobile  = str(d.get('mobile',  ''))

    if len(pincode) != 6 or not pincode.isdigit():
        return jsonify(error='Pincode must be exactly 6 digits'), 400
    if not name or len(name) > 30:
        return jsonify(error='Receiver name required (max 30 chars)'), 400
    if len(mobile) != 10 or not mobile.isdigit():
        return jsonify(error='Mobile number must be exactly 10 digits'), 400

    query_db(
        'INSERT INTO addresses(userid,pincode,reciever_name,reciever_city,reciever_street,reciever_house,reciever_no) VALUES(%s,%s,%s,%s,%s,%s,%s)',
        (uid, pincode, name, city, street, house, mobile), commit=True
    )
    return jsonify(message='Address added successfully'), 201


# ── Order Helpers ──────────────────────────────────────────────────────────────
def gen_order_id():
    while True:
        oid = random.randint(10000000, 99999999)
        if not query_db('SELECT orderid FROM orders WHERE orderid=%s', (oid,), fetchone=True):
            return oid


def calc_price(weight):
    w = float(weight)
    exact = {3:500,5:1000,7:1500,9:2000,11:2500,13:3000,15:3500,
             17:4000,19:4500,21:5000,23:5500,25:6000,27:6500,29:7000,30:7000}
    for k, v in exact.items():
        if w == k:
            return str(v)
    rows = query_db('SELECT * FROM wtscale')
    for r in rows:
        if int(r['min_weight']) < w < int(r['max_weight']):
            return str(r['price'])
    return None


# ── Order Routes ───────────────────────────────────────────────────────────────
@app.route('/api/orders', methods=['GET'])
def get_orders():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    rows = query_db('SELECT * FROM orders WHERE userid=%s', (uid,))
    return jsonify(rows), 200


@app.route('/api/orders', methods=['POST'])
def place_order():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    d           = request.json or {}
    weight      = d.get('weight')
    address_str = d.get('address', '')

    if not weight:
        return jsonify(error='Weight is required'), 400
    try:
        weight = float(weight)
    except ValueError:
        return jsonify(error='Weight must be a number'), 400
    if weight < 3 or weight > 30:
        return jsonify(error='Weight must be between 3 and 30 kg'), 400

    price = calc_price(weight)
    if not price:
        return jsonify(error='Could not calculate price'), 500

    t       = time.ctime().split()
    mon_map = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
               'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    month      = mon_map.get(t[1], '01')
    order_date = f"{t[2].zfill(2)}/{month}/{t[4]}"
    oid        = gen_order_id()

    query_db(
        'INSERT INTO orders(orderID,address,weight,price,order_date,userid,last_notified_step) VALUES(%s,%s,%s,%s,%s,%s,%s)',
        (oid, address_str, weight, price, order_date, uid, -1), commit=True
    )

    # Immediately send "Processing" SMS
    user = query_db('SELECT mobile FROM user WHERE userid=%s', (uid,), fetchone=True)
    if user and user.get('mobile'):
        from backend.sms import send_order_sms
        if send_order_sms(user['mobile'], oid, 'Processing'):
            query_db('UPDATE orders SET last_notified_step=0 WHERE orderID=%s', (oid,), commit=True)

    return jsonify(orderid=oid, price=price, order_date=order_date, message='Order placed successfully'), 201


@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    order = query_db('SELECT * FROM orders WHERE orderid=%s AND userid=%s', (order_id, uid), fetchone=True)
    if not order:
        return jsonify(error='Order not found'), 404

    d2date = order['order_date']
    try:
        start = date(int(d2date[6:10]), int(d2date[3:5]), int(d2date[0:2]))
        diff  = (date.today() - start).days
        if diff > 2:
            return jsonify(error='Order cannot be cancelled — it has already been shipped'), 409
    except Exception:
        pass

    user = query_db('SELECT mobile FROM user WHERE userid=%s', (uid,), fetchone=True)
    if user and user.get('mobile'):
        from backend.sms import send_order_sms
        send_order_sms(user['mobile'], order_id, 'Cancelled_User')

    query_db('DELETE FROM orders WHERE orderid=%s', (order_id,), commit=True)
    query_db('DELETE FROM delivery WHERE orderid=%s', (order_id,), commit=True)
    return jsonify(message='Order cancelled successfully'), 200


@app.route('/api/orders/<int:order_id>/track', methods=['GET'])
def track_order(order_id):
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    order = query_db('SELECT * FROM orders WHERE orderid=%s AND userid=%s', (order_id, uid), fetchone=True)
    if not order:
        return jsonify(error='Order not found'), 404

    d2date = order['order_date']
    try:
        start = date(int(d2date[6:10]), int(d2date[3:5]), int(d2date[0:2]))
        diff  = (date.today() - start).days
    except Exception:
        diff = 0

    stages = ['Processing','Packaging','Ready to Ship','Shipped','Out for Delivery','Delivered']
    step   = min(diff, 5)
    status = stages[step]

    delivery_no = None
    if diff >= 4:
        drow = query_db('SELECT delivery_no FROM delivery WHERE orderid=%s', (order_id,), fetchone=True)
        if drow:
            delivery_no = drow['delivery_no']
        else:
            delivery_no = random.randint(1000000000, 9999999999)
            query_db('INSERT INTO delivery(orderid,delivery_no) VALUES(%s,%s)', (order_id, delivery_no), commit=True)

    return jsonify(
        orderid=order_id, status=status, step=step,
        days_since_order=diff, delivery_no=delivery_no, order=order
    ), 200


# ── Feedback Route ─────────────────────────────────────────────────────────────
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    uid = authed()
    if not uid:
        return jsonify(error='Not authenticated'), 401
    d        = request.json or {}
    review   = (d.get('review') or '').lower()
    order_id = d.get('orderid')

    if review not in ('excellent', 'moderate', 'bad'):
        return jsonify(error='Review must be excellent, moderate, or bad'), 400

    query_db('INSERT INTO feedback(review,orderid) VALUES(%s,%s)', (review, order_id), commit=True)
    return jsonify(message='Thank you for your feedback!'), 201


# ── About / Stats Route ────────────────────────────────────────────────────────
@app.route('/api/about/feedback-stats', methods=['GET'])
def feedback_stats():
    rows  = query_db('SELECT review, COUNT(*) as count FROM feedback GROUP BY review')
    stats = {'excellent': 0, 'moderate': 0, 'bad': 0}
    for r in rows:
        if r['review'] in stats:
            stats[r['review']] = r['count']
    return jsonify(stats), 200


# ── Admin Routes ───────────────────────────────────────────────────────────────
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    d = request.json or {}
    if d.get('userid', '').lower() == 'admin' and d.get('password', '').lower() == 'admin':
        session['admin'] = True
        return jsonify(message='Admin logged in'), 200
    return jsonify(error='Invalid admin credentials'), 401


@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin', None)
    return jsonify(message='Admin logged out'), 200


@app.route('/api/admin/users', methods=['GET'])
def admin_users():
    if not session.get('admin'):
        return jsonify(error='Unauthorized'), 401
    rows = query_db('SELECT userid, username, DOB, mobile FROM user')
    return jsonify(rows), 200


@app.route('/api/admin/addresses', methods=['GET'])
def admin_addresses():
    if not session.get('admin'):
        return jsonify(error='Unauthorized'), 401
    rows = query_db('SELECT * FROM addresses')
    return jsonify(rows), 200


@app.route('/api/admin/orders', methods=['GET'])
def admin_orders():
    if not session.get('admin'):
        return jsonify(error='Unauthorized'), 401
    rows = query_db('SELECT * FROM orders')
    return jsonify(rows), 200


@app.route('/api/admin/users/<string:uid>', methods=['PUT', 'DELETE'])
def admin_user_modify(uid):
    if not session.get('admin'):
        return jsonify(error='Unauthorized'), 401
    uid = uid.lower().strip()
    
    if request.method == 'DELETE':
        query_db('DELETE FROM addresses WHERE userid=%s', (uid,), commit=True)
        query_db("UPDATE orders SET userid='Deleted Account' WHERE userid=%s", (uid,), commit=True)
        query_db('DELETE FROM user WHERE userid=%s', (uid,), commit=True)
        return jsonify(message='User deleted successfully'), 200

    if request.method == 'PUT':
        d = request.json or {}
        n_username = d.get('username')
        n_dob      = d.get('dob')
        n_mobile   = d.get('mobile')
        
        updates = []
        params = []
        if n_username: updates.append("username=%s"); params.append(n_username)
        if n_dob:      updates.append("DOB=%s");      params.append(n_dob)
        if n_mobile:   updates.append("mobile=%s");   params.append(n_mobile)
            
        if updates:
            params.append(uid)
            q = f"UPDATE user SET {', '.join(updates)} WHERE userid=%s"
            query_db(q, tuple(params), commit=True)
        return jsonify(message='User updated successfully'), 200


@app.route('/api/admin/addresses', methods=['PUT', 'DELETE'])
def admin_addresses_modify():
    if not session.get('admin'):
        return jsonify(error='Unauthorized'), 401
    d = request.json or {}
    uid = d.get('userid')
    reciever_no = d.get('reciever_no')
    
    if not uid or not reciever_no:
        return jsonify(error='userid and reciever_no are required'), 400

    if request.method == 'DELETE':
        query_db('DELETE FROM addresses WHERE userid=%s AND reciever_no=%s', (uid, reciever_no), commit=True)
        return jsonify(message='Address deleted successfully'), 200

    if request.method == 'PUT':
        n_name  = d.get('reciever_name')
        n_city  = d.get('reciever_city')
        n_pin   = d.get('pincode')
        n_mob   = d.get('new_reciever_no')
        n_str   = d.get('reciever_street')
        n_house = d.get('reciever_house')
        
        upd = []
        par = []
        if n_name:  upd.append('reciever_name=%s');   par.append(n_name)
        if n_city:  upd.append('reciever_city=%s');   par.append(n_city)
        if n_pin:   upd.append('pincode=%s');         par.append(n_pin)
        if n_mob:   upd.append('reciever_no=%s');     par.append(n_mob)
        if n_str:   upd.append('reciever_street=%s'); par.append(n_str)
        if n_house: upd.append('reciever_house=%s');  par.append(n_house)
        
        if upd:
            par.extend([uid, reciever_no])
            q = f"UPDATE addresses SET {', '.join(upd)} WHERE userid=%s AND reciever_no=%s"
            query_db(q, tuple(par), commit=True)
        return jsonify(message='Address updated successfully'), 200


@app.route('/api/admin/orders/<int:order_id>', methods=['PUT', 'DELETE'])
def admin_orders_modify(order_id):
    if not session.get('admin'):
        return jsonify(error='Unauthorized'), 401

    if request.method == 'DELETE':
        # Send forced cancellation SMS
        user_row = query_db('''
            SELECT u.mobile 
            FROM orders o 
            JOIN user u ON o.userid = u.userid 
            WHERE o.orderid=%s
        ''', (order_id,), fetchone=True)
        if user_row and user_row.get('mobile'):
            from backend.sms import send_order_sms
            send_order_sms(user_row['mobile'], order_id, 'Cancelled_Admin')

        query_db('DELETE FROM orders WHERE orderid=%s', (order_id,), commit=True)
        query_db('DELETE FROM delivery WHERE orderid=%s', (order_id,), commit=True)
        return jsonify(message='Order deleted successfully'), 200

    if request.method == 'PUT':
        d = request.json or {}
        n_address = d.get('address')
        n_weight  = d.get('weight')
        n_price   = d.get('price')
        
        upd = []
        par = []
        if n_address: upd.append('address=%s'); par.append(n_address)
        if n_weight:  upd.append('weight=%s');  par.append(n_weight)
        if n_price:   upd.append('price=%s');   par.append(n_price)
        
        if upd:
            par.append(order_id)
            q = f"UPDATE orders SET {', '.join(upd)} WHERE orderid=%s"
            query_db(q, tuple(par), commit=True)
        return jsonify(message='Order updated successfully'), 200


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Start order-notification scheduler
    is_reloader = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    if not app.debug or is_reloader:
        from backend.scheduler import start_scheduler
        start_scheduler()

    print('\n🚀  CourierX API running at http://localhost:5000\n')
    app.run(debug=True, port=5000)
