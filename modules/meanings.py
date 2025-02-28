import streamlit as st
from utils.database import get_word_details  # Ensure correct import

def show_meaning_page():
    word = st.session_state.get("word", "No word selected")

    word_data = get_word_details(word)

    if not word_data:
        st.error("Word details not found!")
        return

    # Unpacking the tuple (since get_word_details returns a tuple)
    meanings, synonyms, antonyms, note = word_data

    # Display the word as the title
    st.title(f"📚 {word}")

    # Display meanings
    st.subheader("📖 Meanings")
    for meaning in eval(meanings):  # Convert string to list
        st.markdown(f"- {meaning}")

    # Display synonyms
    st.subheader("🔄 Synonyms")
    st.markdown(", ".join(eval(synonyms)))

    # Display antonyms
    st.subheader("🚫 Antonyms")
    st.markdown(", ".join(eval(antonyms)))

    # Display note
    st.subheader("📝 Note")
    st.text(note if note else "No additional notes")

    # Navigation buttons
    if st.button("🔙 Back"):
        st.session_state.page = "home"
        st.rerun()

    if st.button("✏️ Edit"):
        st.session_state.page = "edit"
        st.rerun()



