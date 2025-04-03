import sqlite3


def connect_db():
    """Connect to SQLite database"""
    return sqlite3.connect('database.db')


def create_table_if_not_exists():
    """Check if table exists and create if needed"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='listings';")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''CREATE TABLE listings (
            id INTEGER PRIMARY KEY,
            sent INTEGER DEFAULT 0
        )''')
        print("Table 'listings' created.")
    else:
        print("Table 'listings' already exists.")

    conn.commit()
    conn.close()


def save_listing_to_db(listing_id):
    """Save listing to database and return sent status"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT sent FROM listings WHERE id = ?", (listing_id,))
    result = cursor.fetchone()

    if result:
        print(f"Listing with ID {listing_id} already exists.")
        return result[0]
    else:
        cursor.execute("INSERT INTO listings (id, sent) VALUES (?, ?)", (listing_id, 0))
        conn.commit()
        print(f"Listing with ID {listing_id} added to database.")
        return 0


def mark_listing_as_sent(listing_id):
    """Mark listing as sent in database"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE listings SET sent = 1 WHERE id = ?", (listing_id,))
    conn.commit()
    print(f"Listing with ID {listing_id} marked as sent.")
    conn.close() 