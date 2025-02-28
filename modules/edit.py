import streamlit as st
from utils.database import get_word_details, update_word_details
import json


def show_edit_page():
    word = st.session_state.get("word", "No word selected")

    word_data = get_word_details(word)

    if not word_data:
        st.error("Word details not found!")
        return

    # Unpacking the tuple (since get_word_details returns a tuple)
    meanings, synonyms, antonyms, note = word_data
    

    # Convert string lists to actual lists using eval() (ensure stored format is correct)
    
    # meanings = "\n ".join(eval(meanings))
    # synonyms = ", ".join(eval(synonyms))
    # antonyms = ", ".join(eval(antonyms))
    
    meanings = "\n".join(json.loads(meanings)) if meanings else ""
    synonyms = ", ".join(json.loads(synonyms)) if synonyms else ""
    antonyms = ", ".join(json.loads(antonyms)) if antonyms else ""

    # box_height = len(meanings.split("\n")) * 100
    # print(box_height, meanings)
    
    # Editable fields
    new_meanings = st.text_area("Meanings (Newline separated)", meanings, height=box_height)
    new_synonyms = st.text_area("Synonyms (Comma separated)", synonyms)
    new_antonyms = st.text_area("Antonyms (Comma separated)", antonyms)
    new_note = st.text_area("Note", note)

    # Save button
    if st.button("💾 Save"):
        # Convert back to list format before saving
        # updated_meanings = str(new_meanings.split("\n"))
        # updated_synonyms = str(new_synonyms.split(","))
        # updated_antonyms = str(new_antonyms.split(","))
        
        updated_meanings = json.dumps(new_meanings.split("\n"), ensure_ascii=False)
        updated_synonyms = json.dumps([s.strip() for s in new_synonyms.split(",") if s.strip()], ensure_ascii=False)
        updated_antonyms = json.dumps([a.strip() for a in new_antonyms.split(",") if a.strip()], ensure_ascii=False)


        update_word_details(word, updated_meanings, updated_synonyms, updated_antonyms, new_note)
        st.success("Word details updated successfully!")
        # st.session_state.page = "home"
        st.rerun()

    # Navigation button
    if st.button("🔙 Back"):
        st.session_state.page = "meaning"
        st.rerun()
