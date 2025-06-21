import streamlit as st
from utils.database import get_word_details  # Ensure correct import



def parse_meaning_and_examples(text):
    parts = text.split("=>")

    meaning = parts[0].strip()
    examples = []

    for i in range(1, len(parts)):
        example = parts[i].strip()

        if '.' in example:
            sentence, rest = example.split('.', 1)
            sentence = sentence.strip() + '.'
            parts[i] = rest.strip()
        else:
            sentence = example.strip()

        if sentence:
            examples.append(sentence)

    return meaning, examples



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
    
    # Display note
    st.subheader("📝 Note")
    st.markdown(f'<p class="note-text">{note if note else "No additional notes"}</p>', unsafe_allow_html=True)
    
    # Display meanings
    # st.subheader("📖 Meanings")
    # for meaning in eval(meanings):  # Convert string to list
    #     st.markdown(f'<p class="meaning-text"> {meaning}</p>', unsafe_allow_html=True)
    
    # Display meanings with example bullets
    st.subheader("📖 Meanings")

    for raw in eval(meanings):  # meanings is a list of raw strings
        meaning, examples = parse_meaning_and_examples(raw)

        # Show the main definition
        st.markdown(f'<p class="meaning-text">{meaning}</p>', unsafe_allow_html=True)

        # Show the examples as bullets in italics
        for ex in examples:
            st.markdown(f'<ul style="margin-top: -10px;"><li><i>{ex}</i></li></ul>', unsafe_allow_html=True)

    # Display synonyms with increased font size
    st.subheader("🔄 Synonyms")
    st.markdown(f'<p class="synonym-text">{", ".join(eval(synonyms))}</p>', unsafe_allow_html=True)

    # Display antonyms with increased font size
    st.subheader("🚫 Antonyms")
    st.markdown(f'<p class="antonym-text">{", ".join(eval(antonyms))}</p>', unsafe_allow_html=True)


    # Navigation buttons

    if st.button("✏️ Edit"):
        st.session_state.page = "edit"
        st.rerun()
        
    if st.button("🔙 Back"):
        st.session_state.page = "home"
        st.rerun()



