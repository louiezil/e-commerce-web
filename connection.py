import sqlite3
from flask import g
from config import Config


def get_conn():
    if "conn" not in g:
        g.conn = sqlite3.connect(Config.DATABASE)
        g.conn.execute("PRAGMA foreign_keys= ON")
    return g.conn


def close_conn(exception=None):
    db_close = g.pop("conn", None)
    if db_close is not None:
        db_close.close()
        
