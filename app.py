import streamlit as st
from utils.database import init_db, get_random_word, get_word_count
from utils.utils import import_json, download_json
from modules.meanings import show_meaning_page
from modules.edit import show_edit_page





def load_css():
    with open("styles/style.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Flashcard App", layout="centered")
    
    # load_css()
    
    init_db()

    if "word" not in st.session_state:
        st.session_state.word = get_random_word()

    if "page" not in st.session_state:
        st.session_state.page = "home"

    st.title("📖 Flashcard App")

    if st.session_state.page == "meaning":
        show_meaning_page()
    elif st.session_state.page == "edit":
        show_edit_page()
    else:
        st.markdown(f"## {st.session_state.word}", unsafe_allow_html=True)

        word_count = get_word_count()
        if st.button(f"🔄 Words: {word_count}", key="count_refresh"):
            st.session_state.word = get_random_word()
            st.rerun()

        if st.button("📖 View Meaning", key="view_meaning"):
            st.session_state.page = "meaning"
            st.rerun()

        uploaded_file = st.file_uploader("📤 Import JSON", type=["json"], key="import_json")
        if uploaded_file:
            import_json(uploaded_file)
            st.success("Data Imported Successfully!")
            st.rerun()

        # 📥 **Download JSON** button (added)
        download_json()


if __name__ == "__main__":
    main()
