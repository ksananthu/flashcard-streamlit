import streamlit as st
from utils.database import init_db, get_random_word, get_word_count
from utils.utils import import_json, download_json
from modules.meanings import show_meaning_page
from modules.edit import show_edit_page
from utils.database import get_all_words

def load_css():
    with open("styles/style.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Flashcard App", layout="centered")
    
    load_css()
    
    init_db()


    if "page" not in st.session_state:
        st.session_state.page = "home"

    # 👉 Only show filter when on the home page
    if st.session_state.page == "home":

        st.title("📖 Flashcard App")
        st.markdown("---")
        st.subheader("📅 Filter Words by Date")
        
        # Initialize the selected timeframe only once
        if "date_filter" not in st.session_state:
            st.session_state.date_filter = "All"
        
        # Dropdown using session state
        date_filter = st.selectbox(
            "Select timeframe:",
            ["All", "1 Day", "2 Days", "7 Days", "14 Days", "30 Days"],
            index=["All", "1 Day", "2 Days", "7 Days", "14 Days", "30 Days"].index(st.session_state.date_filter)
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
        
        # Update session state if user selected a different timeframe
        if date_filter != st.session_state.date_filter:
            st.session_state.date_filter = date_filter

        
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

        # vertical line
        st.markdown("---")
        
        uploaded_file = st.file_uploader("📤 Import JSON", type=["json"], key="import_json")
        if uploaded_file:
            import_json(uploaded_file)
            st.success("Data Imported Successfully!")
            st.rerun()

        # 📥 **Download JSON** button
        download_json()

        # vertical line
        st.markdown("---")
        
        # Search bar
        st.subheader("🔍 Search Word")

        all_words = get_all_words()
        selected_word = st.selectbox(
            "Type or choose a word:",
            options=all_words,
            index=all_words.index(st.session_state.word) if st.session_state.word in all_words else 0,
            key="search_word"
        )

        if st.button("Find", key="search_btn"):
            st.session_state.word = st.session_state.search_word
            st.session_state.page = "meaning"
            st.rerun()
        
        
        
    # 👉 Handle page navigation
    elif st.session_state.page == "meaning":
        show_meaning_page()
    elif st.session_state.page == "edit":
        show_edit_page()
        
    
      # Add to top if not already

    

if __name__ == "__main__":
    main()
