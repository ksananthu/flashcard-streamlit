import sqlite3
import json
import streamlit as st

DB_PATH = "data/flashcards.db"
EXPORT_FILE = "data/flashcards_export.json"



def import_json(uploaded_file):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    data = json.load(uploaded_file)
    
    for item in data:
        cursor.execute(
            "INSERT OR IGNORE INTO flashcards (word, meanings, synonyms, antonyms, note) VALUES (?, ?, ?, ?, ?)",
            (item["word"], json.dumps(item["meanings"]), json.dumps(item["synonyms"]), json.dumps(item["antonyms"]), item.get("note", ""))
        )
    
    conn.commit()
    conn.close()

def export_json():
    """Export flashcards from the database to a JSON file."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT word, meanings, synonyms, antonyms, note FROM flashcards")
    rows = cursor.fetchall()
    
    data = []
    
    for row in rows:
        word, meanings, synonyms, antonyms, note = row

        # Ensure proper JSON parsing
        meanings = json.loads(meanings) if meanings else []
        synonyms = json.loads(synonyms) if synonyms else []
        antonyms = json.loads(antonyms) if antonyms else []
        note = note if note else ""

        data.append({
            "word": word,
            "meanings": meanings,
            "synonyms": synonyms,
            "antonyms": antonyms,
            "note": note
        })

    conn.close()
    
    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    # Save JSON to a file
    with open(EXPORT_FILE, "w", encoding="utf-8") as f:
        f.write(json_data)

    # st.success("📥 JSON Exported Successfully!")

    return EXPORT_FILE  # Return the JSON data for downloading


def download_json():
    """Provide a button to download the exported JSON file."""
    json_data = export_json()

    st.download_button(
        label="📥 Download Flashcards JSON",
        data=json_data,
        file_name="flashcards.json",
        mime="application/json",
    )
