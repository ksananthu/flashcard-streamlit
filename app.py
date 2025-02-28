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
    
    load_css()
    
    init_db()

    st.title("📖 Flashcard App")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    # 👉 Only show filter when on the home page
    if st.session_state.page == "home":
        st.subheader("📅 Filter Words by Date")
        date_filter = st.selectbox(
            "Select timeframe:",
            ["All", "1 Day", "2 Days", "7 Days", "14 Days", "30 Days"]
        )

        # Map selected time frame to days
        days_mapping = {
            "1 Day": 1,
            "2 Days": 2,
            "7 Days": 7,
            "14 Days": 14,
            "30 Days": 30,
            "All": None
        }
        
        selected_days = days_mapping[date_filter]

        # Set a random word from the selected time frame
        if "word" not in st.session_state or st.session_state.get("selected_days") != selected_days:
            st.session_state.word = get_random_word(selected_days)
            st.session_state.selected_days = selected_days  # Store selected days in session

        st.markdown(
            f"""
            <div class="word-card">
                <h2>{st.session_state.word}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        word_count = get_word_count(selected_days)
        if st.button(f"🔄 Refresh Words ({word_count})", key="count_refresh"):
            st.session_state.word = get_random_word(selected_days)
            st.rerun()

        if st.button("📖 View Meaning", key="view_meaning"):
            st.session_state.page = "meaning"
            st.rerun()

        uploaded_file = st.file_uploader("📤 Import JSON", type=["json"], key="import_json")
        if uploaded_file:
            import_json(uploaded_file)
            st.success("Data Imported Successfully!")
            st.rerun()

        # 📥 **Download JSON** button
        download_json()

    # 👉 Handle page navigation
    elif st.session_state.page == "meaning":
        show_meaning_page()
    elif st.session_state.page == "edit":
        show_edit_page()

if __name__ == "__main__":
    main()
