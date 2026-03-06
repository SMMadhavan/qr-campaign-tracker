import sqlite3
from datetime import datetime

DB_NAME = "campaigns.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Table to store campaigns
    c.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            destination_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Table to store every scan
    c.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT NOT NULL,
            scanned_at TEXT NOT NULL,
            user_agent TEXT,
            ip_address TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def create_campaign(name, destination_url, short_code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO campaigns (name, destination_url, short_code, created_at)
        VALUES (?, ?, ?, ?)
    ''', (name, destination_url, short_code, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_all_campaigns():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT c.name, c.destination_url, c.short_code, c.created_at,
               COUNT(s.id) as scan_count
        FROM campaigns c
        LEFT JOIN scans s ON c.short_code = s.short_code
        GROUP BY c.short_code
        ORDER BY c.created_at DESC
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

def log_scan(short_code, user_agent, ip_address):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO scans (short_code, scanned_at, user_agent, ip_address)
        VALUES (?, ?, ?, ?)
    ''', (short_code, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_agent, ip_address))
    conn.commit()
    conn.close()

def get_campaign_by_code(short_code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM campaigns WHERE short_code = ?', (short_code,))
    row = c.fetchone()
    conn.close()
    return row

def get_scans_by_code(short_code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM scans WHERE short_code = ? ORDER BY scanned_at DESC', (short_code,))
    rows = c.fetchall()
    conn.close()
    return rows