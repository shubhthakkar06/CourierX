"""
migrate_otp.py — Add mobile OTP support to the database.
Run once: python database/migrate_otp.py
"""

import mysql.connector, os, sys

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
env = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

print(f"Connecting to {env.get('DB_HOST')} …")
try:
    con = mysql.connector.connect(
        host=env['DB_HOST'], port=int(env.get('DB_PORT', 4000)),
        user=env['DB_USER'], password=env['DB_PASSWORD'],
        ssl_disabled=False,
    )
except Exception as e:
    print(f"❌ Connection failed: {e}"); sys.exit(1)

cur = con.cursor()
cur.execute("USE Project")

migrations = [
    ("Add mobile to user",
     "ALTER TABLE user ADD COLUMN mobile VARCHAR(15)"),

    ("Drop recoverycode from user",
     "ALTER TABLE user DROP COLUMN recoverycode"),

    ("Add last_notified_step to orders",
     "ALTER TABLE orders ADD COLUMN last_notified_step INT DEFAULT -1"),

    ("Create otp_store table",
     """CREATE TABLE IF NOT EXISTS otp_store (
         mobile     VARCHAR(15) NOT NULL PRIMARY KEY,
         otp_code   VARCHAR(6)  NOT NULL,
         created_at BIGINT      NOT NULL
     )"""),
]

for label, sql in migrations:
    try:
        cur.execute(sql)
        con.commit()
        print(f"  ✅ {label}")
    except Exception as e:
        msg = str(e)
        if 'Duplicate column' in msg or 'already exists' in msg or "Can't DROP" in msg or "Unknown column" in msg:
            print(f"  ⏭️  {label} — already applied")
        else:
            print(f"  ⚠️  {label} — {msg}")

cur.close(); con.close()
print("\n🎉 Migration complete!")
