# db.py
import sqlite3
from sqlite3 import Error

DB_PATH = "my.db"

def list_tables():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    con.close()
    return tables

def list_columns(table_name: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"PRAGMA table_info({table_name});")
    cols = [c[1] for c in cur.fetchall()]
    con.close()
    return cols

def create_table(table_name: str, columns: list[tuple[str,str]]):
    # columns: [("id","INTEGER"), ("name","TEXT")]
    cols_sql = ", ".join([f"{name} {typ}" for name, typ in columns])
    q = f"CREATE TABLE {table_name} ({cols_sql});"
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(q)
    con.commit()
    con.close()

def insert_row(table: str, values: dict):
    # values: {"id":1, "name":"Ali"}
    cols = ", ".join(values.keys())
    placeholders = ", ".join(["?"] * len(values))
    q = f"INSERT INTO {table} ({cols}) VALUES ({placeholders});"
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(q, list(values.values()))
    con.commit()
    con.close()

def select_all(table: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table};")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    con.close()
    return cols, rows
