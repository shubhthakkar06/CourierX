"""
setup_cloud.py — Create the Project database and all tables on TiDB Cloud.
Run once: python database/setup_cloud.py
"""

import mysql.connector
import os
import sys

# Load credentials from .env manually (avoids find_dotenv issues)
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
env = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

print(f"Connecting to {env.get('DB_HOST')}:{env.get('DB_PORT')} as {env.get('DB_USER')} …")

try:
    con = mysql.connector.connect(
        host     = env['DB_HOST'],
        port     = int(env.get('DB_PORT', 4000)),
        user     = env['DB_USER'],
        password = env['DB_PASSWORD'],
        ssl_disabled = False,
    )
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

cur = con.cursor()

statements = [
    ("Create database",  "CREATE DATABASE IF NOT EXISTS Project"),
    ("Use database",     "USE Project"),
    ("Table: user",      """CREATE TABLE IF NOT EXISTS user (
        userid       VARCHAR(31)  NOT NULL PRIMARY KEY,
        username     VARCHAR(30)  NOT NULL,
        password     VARCHAR(50)  NOT NULL,
        DOB          DATE,
        recoverycode INT UNIQUE
    )"""),
    ("Table: addresses", """CREATE TABLE IF NOT EXISTS addresses (
        userid          VARCHAR(31),
        pincode         CHAR(6),
        reciever_name   VARCHAR(30),
        reciever_city   VARCHAR(25),
        reciever_street VARCHAR(25),
        reciever_house  VARCHAR(25),
        reciever_no     CHAR(10)
    )"""),
    ("Table: orders",    """CREATE TABLE IF NOT EXISTS orders (
        orderID    INT         NOT NULL PRIMARY KEY,
        address    VARCHAR(150),
        weight     DECIMAL(5,2),
        price      VARCHAR(10),
        order_date VARCHAR(20),
        userid     VARCHAR(31)
    )"""),
    ("Table: delivery",  """CREATE TABLE IF NOT EXISTS delivery (
        orderid     INT,
        delivery_no BIGINT
    )"""),
    ("Table: feedback",  """CREATE TABLE IF NOT EXISTS feedback (
        review  VARCHAR(20),
        orderid INT
    )"""),
    ("Table: wtscale",   """CREATE TABLE IF NOT EXISTS wtscale (
        min_weight INT,
        max_weight INT,
        price      INT
    )"""),
    ("Table: wpd",       "CREATE TABLE IF NOT EXISTS wpd (attemps INT DEFAULT 1)"),
    ("Seed wpd",         "INSERT INTO wpd VALUES (1)"),
    ("Seed wtscale",     """INSERT INTO wtscale VALUES
        (2,4,500),(4,6,1000),(6,8,1500),(8,10,2000),(10,12,2500),
        (12,14,3000),(14,16,3500),(16,18,4000),(18,20,4500),(20,22,5000),
        (22,24,5500),(24,26,6000),(26,28,6500),(28,30,7000)
    """),
]

for label, sql in statements:
    try:
        cur.execute(sql)
        con.commit()
        print(f"  ✅ {label}")
    except Exception as e:
        print(f"  ⚠️  {label} — {e}")

cur.close()
con.close()
print("\n🎉 TiDB Cloud database is ready! Run: python main.py")
