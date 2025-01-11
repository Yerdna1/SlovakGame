import streamlit as st
from collections import Counter
import pandas as pd




class SlovakWordGenerator:
    def __init__(self):
        self.dictionary = set()
        self.load_dictionary('sk_SK.dic')  # Ensure 'sk_SK.dic' is in the project directory

    def load_dictionary(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue  # Skip comments and empty lines
                word = line.split('/')[0]  # Extract the word part
                self.dictionary.add(word)

    def normalize_slovak(self, text: str) -> str:
        slovak_map = {
            'á': 'a', 'ä': 'a', 'č': 'c', 'ď': 'd', 
            'é': 'e', 'í': 'i', 'ĺ': 'l', 'ľ': 'l',
            'ň': 'n', 'ó': 'o', 'ô': 'o', 'ŕ': 'r',
            'š': 's', 'ť': 't', 'ú': 'u', 'ý': 'y',
            'ž': 'z'
        }
        text = text.lower()
        return ''.join(slovak_map.get(c, c) for c in text)

    def calculate_word_score(self, word: str) -> int:
        base_score = len(word) * 10
        special_chars = 'áäčďéíĺľňóôŕšťúýž'
        bonus = sum(2 for c in word if c in special_chars)
        return base_score + bonus

    def can_make_word(self, available_letters: str, word: str) -> bool:
        available = Counter(self.normalize_slovak(available_letters))
        needed = Counter(self.normalize_slovak(word))
        return all(available[c] >= needed[c] for c in needed)

    def generate_words(self, letters: str) -> list:
        results = []
        for word in self.dictionary:
            if self.can_make_word(letters, word):
                score = self.calculate_word_score(word)
                results.append((word, score))
        return sorted(results, key=lambda x: (-x[1], -len(x[0])))

def main():
    st.set_page_config(page_title="Generátor slovenských slov", page_icon="🇸🇰", layout="wide")
    st.title("Generátor slovenských slov")

    # Initialize session state at the start of the app
    if 'letters' not in st.session_state:
        st.session_state['letters'] = ""

    generator = SlovakWordGenerator()

    # Create two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        # Use session state for text input
        letters = st.text_input(
            "Zadajte písmená (presne 10):",
            value=st.session_state.letters,  # Initialize with current session state
            key="text_input"
        )

        # Special characters buttons in rows
        st.write("Špeciálne znaky:")
        special_chars = [
            ['á', 'ä', 'č', 'ď', 'é'],
            ['í', 'ĺ', 'ľ', 'ň', 'ó'],
            ['ô', 'ŕ', 'š', 'ť', 'ú'],
            ['ý', 'ž']
        ]

        for row in special_chars:
            cols = st.columns(len(row))
            for i, char in enumerate(row):
                if cols[i].button(char, key=f"btn_{char}"):
                    st.session_state.letters += char  # Append the character
                    st.rerun()

    with col2:
        generate_button = st.button("Generovať slová", type="primary")
        if st.button("Vyčistiť", key="clear"):
            st.session_state.letters = ""
            st.rerun()

    # Update letters in session state when text input changes
    if letters != st.session_state.letters:
        st.session_state.letters = letters

    if generate_button and st.session_state.letters:
        normalized_len = len(generator.normalize_slovak(st.session_state.letters))
        if normalized_len != 10:
            st.error(f"Prosím, zadajte presne 10 písmen! (Zadali ste {normalized_len})")
        else:
            words = generator.generate_words(st.session_state.letters)
            
            if not words:
                st.warning("Neboli nájdené žiadne slová.")
            else:
                st.success(f"Nájdených {len(words)} slov")

                # Group words by length
                by_length = {}
                for word, score in words:
                    length = len(word)
                    if length not in by_length:
                        by_length[length] = []
                    by_length[length].append((word, score))

                # Create DataFrame for display
                data = []
                for length in sorted(by_length.keys(), reverse=True):
                    for word, score in by_length[length]:
                        data.append({
                            "Dĺžka": length,
                            "Slovo": word,
                            "Skóre": score
                        })

                df = pd.DataFrame(data)
                st.dataframe(
                    df,
                    column_config={
                        "Dĺžka": st.column_config.NumberColumn(help="Počet písmen v slove"),
                        "Slovo": st.column_config.TextColumn(help="Nájdené slovo"),
                        "Skóre": st.column_config.NumberColumn(help="Skóre slova (dĺžka + bonus za špeciálne znaky)")
                    },
                    hide_index=True
                )

if __name__ == "__main__":
    main()