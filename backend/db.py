"""
db.py — Database Connection
Reads config from environment variables (.env file) so you can swap
between local MySQL and any cloud MySQL provider without touching code.

Supported providers (just change .env):
  - Local MySQL (default)
  - TiDB Cloud (recommended free cloud option)
  - Aiven for MySQL
  - PlanetScale / Railway / any MySQL-compatible cloud
"""

import os
import mysql.connector
from dotenv import load_dotenv

# Load .env from project root (one level up from backend/)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ── Connection config from environment ────────────────────────────────────────
DB_HOST     = os.getenv('DB_HOST',     'localhost')
DB_PORT     = int(os.getenv('DB_PORT', '3306'))
DB_USER     = os.getenv('DB_USER',     'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '20052006')
DB_NAME     = os.getenv('DB_NAME',     'Project')

# Set DB_SSL=true for TiDB Cloud, Aiven, PlanetScale etc.
DB_SSL      = os.getenv('DB_SSL', 'false').lower() == 'true'

# ── Connection factory ─────────────────────────────────────────────────────────
def get_db():
    """Return a new MySQL connection using the configured credentials."""
    kwargs = dict(
        host     = DB_HOST,
        port     = DB_PORT,
        user     = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME,
    )
    if DB_SSL:
        # Cloud providers require SSL; mysql-connector handles it automatically
        # when ssl_disabled=False (the default). Force it explicitly here.
        kwargs['ssl_disabled'] = False
    return mysql.connector.connect(**kwargs)


def query_db(sql, params=(), fetchone=False, commit=False):
    """Execute a query and optionally return results or commit."""
    con = get_db()
    cur = con.cursor(dictionary=True)
    cur.execute(sql, params)
    if commit:
        con.commit()
        con.close()
        return None
    result = cur.fetchone() if fetchone else cur.fetchall()
    con.close()
    return result
