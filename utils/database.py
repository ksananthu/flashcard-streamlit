import sqlite3
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "flashcards.db")

def init_db():
    """Ensure database exists and initialize the flashcards table."""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)  # Create the 'data' directory if missing

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS flashcards (
                      word TEXT PRIMARY KEY,
                      meanings TEXT,
                      synonyms TEXT,
                      antonyms TEXT,
                      note TEXT DEFAULT '',
                      date_added TEXT DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_random_word(days=None):
    """Retrieve a random word from the database within the given timeframe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if days:
        cursor.execute('''SELECT word FROM flashcards 
                          WHERE date_added >= datetime('now', ?) 
                          ORDER BY RANDOM() LIMIT 1''', 
                       (f"-{days} days",))
    else:
        cursor.execute("SELECT word FROM flashcards ORDER BY RANDOM() LIMIT 1")

    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else "No words available"

def get_word_count(days=None):
    """Get the count of words in the database within the given timeframe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if days:
        cursor.execute('''SELECT COUNT(*) FROM flashcards 
                          WHERE date_added >= datetime('now', ?)''', 
                       (f"-{days} days",))
    else:
        cursor.execute("SELECT COUNT(*) FROM flashcards")

    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_word_details(word):
    """Retrieve meanings, synonyms, antonyms, and notes for a given word."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT meanings, synonyms, antonyms, note FROM flashcards WHERE word=?", (word,))
    result = cursor.fetchone()
    conn.close()
    return result if result else ("No meaning available", "", "", "")

def update_word_details(word, meanings, synonyms, antonyms, note):
    """Update a word's details in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''UPDATE flashcards SET meanings=?, synonyms=?, antonyms=?, note=? WHERE word=?''',
                   (meanings, synonyms, antonyms, note, word))
    conn.commit()
    conn.close()
