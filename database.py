# database.py
import sqlite3

DB_NAME = 'toko.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Akses hasil query seperti dictionary
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            nama   TEXT NOT NULL,
            harga  REAL NOT NULL,
            stok   INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print('Database berhasil diinisialisasi.')
