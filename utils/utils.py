import sqlite3
import json
import streamlit as st
from datetime import datetime

DB_PATH = "data/flashcards.db"
EXPORT_FILE = "data/flashcards_export.json"



def import_json(uploaded_file):
    """Import JSON data into the database and set date_added if missing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    data = json.load(uploaded_file)
    
    for item in data:
        cursor.execute(
            '''INSERT OR IGNORE INTO flashcards 
               (word, meanings, synonyms, antonyms, note, date_added) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (
                item["word"],
                json.dumps(item["meanings"]),
                json.dumps(item["synonyms"]),
                json.dumps(item["antonyms"]),
                item.get("note", ""),
                item.get("date_added", datetime.now().isoformat())  # Use existing date or set now
            )
        )
    
    conn.commit()
    conn.close()



def export_json():
    """Export flashcards from the database to a JSON file, including date_added."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT word, meanings, synonyms, antonyms, note, date_added FROM flashcards")
    rows = cursor.fetchall()
    
    data = []
    
    for row in rows:
        word, meanings, synonyms, antonyms, note, date_added = row

        meanings_list = json.loads(meanings) if meanings else []
        synonyms_list = json.loads(synonyms) if synonyms else []
        antonyms_list = json.loads(antonyms) if antonyms else []
        note = note if note else ""

        data.append({
            "word": word,
            "meanings": meanings_list,
            "synonyms": synonyms_list,
            "antonyms": antonyms_list,
            "note": note,
            "date_added": date_added  # Include date in JSON
        })

    conn.close()
    
    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    return json_data  # Return the JSON data for downloading


def download_json():
    """Provide a button to download the exported JSON file."""
    json_data = export_json()

    st.download_button(
        label="📥 Download Flashcards JSON",
        data=json_data,
        file_name="flashcards-backup.json",
        mime="application/json",
    )
