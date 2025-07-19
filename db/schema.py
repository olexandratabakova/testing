import sqlite3
def get_connection():
    return sqlite3.connect("my_database.db")
def init_db():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP
)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    chunk_index INTEGER,
    text TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chunk_id INTEGER NOT NULL,
    object_1 TEXT,
    object_2 TEXT,
    relation_type TEXT,
    polarity TEXT,
    keywords TEXT,
    FOREIGN KEY (chunk_id) REFERENCES chunks(id) ON DELETE CASCADE
)""")

def insert_document(file_path):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO documents (filename) VALUES (?)', (file_path,))
    conn.commit()
    document_id = cursor.lastrowid
    conn.close()
    return document_id

def insert_chunk(document_id, chunk_id, text):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO chunks (document_id, chunk_id, text) VALUES (?, ?, ?)', (document_id, chunk_id, text))
    conn.commit()
    chunk_id = cursor.lastrowid
    conn.close()
    return chunk_id

def insert_relation(chunk_id, obj1, obj2, relation_type, polarity, keywords):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO relations (chunk_id, object_1, object_2, relation_type, polarity, keywords) VALUES (?, ?, ?, ?, ?, ?)",
        (chunk_id, obj1, obj2, relation_type, polarity, keywords)
    )
    conn.commit()
    conn.close()