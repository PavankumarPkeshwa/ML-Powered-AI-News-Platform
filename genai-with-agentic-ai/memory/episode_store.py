"""
Simple episodic memory store using SQLite for agent actions and outcomes.
"""
import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agent_memory.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            task_type TEXT,
            payload TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()


def log_episode(entry: dict):
    try:
        init_db()
        conn = _get_conn()
        c = conn.cursor()
        c.execute(
            "INSERT INTO episodes (timestamp, task_type, payload, result) VALUES (?, ?, ?, ?)",
            (datetime.utcnow().isoformat(), entry.get("task"), json.dumps(entry), json.dumps(entry.get("result") if entry.get("result") is not None else {"ok": True}))
        )
        conn.commit()
        conn.close()
    except Exception:
        # best-effort logging
        pass


if __name__ == "__main__":
    init_db()
    print("Agent memory DB initialized at", DB_PATH)
