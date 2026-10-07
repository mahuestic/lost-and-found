import sqlite3
import os

DB_PATH = 'lost_found.db'

def init_database():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE found_items (
                id INTEGER PRIMARY KEY,
                item_name TEXT,
                description TEXT,
                photo_path TEXT,
                finder_name TEXT,
                finder_contact TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database created!")

if __name__ == '__main__':
    init_database()