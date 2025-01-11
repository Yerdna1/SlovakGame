import streamlit as st
from collections import Counter
import pandas as pd

class SlovakWordGenerator:
    def __init__(self, allowed_diacritics=None):
        self.dictionary = set()
        self.allowed_diacritics = allowed_diacritics or set()
        # Extended map to include uppercase letters
        self.slovak_map = {
            'á': 'a', 'ä': 'a', 'č': 'c', 'ď': 'd', 
            'é': 'e', 'í': 'i', 'ĺ': 'l', 'ľ': 'l',
            'ň': 'n', 'ó': 'o', 'ô': 'o', 'ŕ': 'r',
            'š': 's', 'ť': 't', 'ú': 'u', 'ý': 'y',
            'ž': 'z',
            'Á': 'a', 'Ä': 'a', 'Č': 'c', 'Ď': 'd',
            'É': 'e', 'Í': 'i', 'Ĺ': 'l', 'Ľ': 'l',
            'Ň': 'n', 'Ó': 'o', 'Ô': 'o', 'Ŕ': 'r',
            'Š': 's', 'Ť': 't', 'Ú': 'u', 'Ý': 'y',
            'Ž': 'z'
        }
        self.all_diacritics = set('áäčďéíĺľňóôŕšťúýžÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ')
        self.load_dictionary('sk_SK.dic')

    def load_dictionary(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                word = line.split('/')[0]
                # Store words in lowercase to avoid case issues
                self.dictionary.add(word.lower())

    def normalize_slovak(self, text: str) -> str:
        # Convert to lowercase first
        text = text.lower()
        result = []
        for c in text:
            if c in self.allowed_diacritics:
                result.append(c)
            else:
                result.append(self.slovak_map.get(c, c))
        return ''.join(result)

    def has_unauthorized_diacritics(self, word: str) -> bool:
        # Check both lowercase and uppercase diacritics
        return any(c in (self.all_diacritics - set(self.allowed_diacritics)) for c in word)

    def calculate_word_score(self, word: str) -> int:
        base_score = len(word) * 10
        # Only count allowed diacritics for bonus
        bonus = sum(2 for c in word if c in self.allowed_diacritics)
        return base_score + bonus

    def can_make_word(self, available_letters: str, word: str) -> bool:
        available = Counter(self.normalize_slovak(available_letters))
        needed = Counter(self.normalize_slovak(word))
        return all(available[c] >= needed[c] for c in needed)

    def generate_words(self, letters: str) -> list:
        results = []
        for word in self.dictionary:
            # Skip words with unauthorized diacritics
            if self.has_unauthorized_diacritics(word):
                continue
                
            if self.can_make_word(letters, word):
                score = self.calculate_word_score(word)
                results.append((word, score))
        return sorted(results, key=lambda x: (-x[1], -len(x[0])))

def main():
    st.set_page_config(page_title="Generátor slovenských slov", page_icon="🇸🇰", layout="wide")
    st.title("Generátor slovenských slov")

    # Initialize session states
    if 'letters' not in st.session_state:
        st.session_state['letters'] = ""
    if 'allowed_diacritics' not in st.session_state:
        st.session_state['allowed_diacritics'] = set()

    # Create three columns for better layout
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        letters = st.text_input(
            "Zadajte písmená (presne 10):",
            value=st.session_state.letters,
            key="text_input"
        )

        # Group special characters by type
        diacritic_groups = {
            "Dlhé samohlásky": ['á', 'é', 'í', 'ó', 'ú', 'ý'],
            "Mäkké spoluhlásky": ['č', 'ď', 'ľ', 'ň', 'š', 'ť', 'ž'],
            "Ostatné": ['ä', 'ĺ', 'ô', 'ŕ']
        }

        # Create tabs for different diacritic groups
        tabs = st.tabs(list(diacritic_groups.keys()))
        
        for tab, (group_name, chars) in zip(tabs, diacritic_groups.items()):
            with tab:
                st.write(f"Vybrané {group_name.lower()}:")
                cols = st.columns(len(chars))
                for i, char in enumerate(chars):
                    checkbox = cols[i].checkbox(
                        char,
                        value=char in st.session_state.allowed_diacritics,
                        key=f"check_{char}"
                    )
                    if checkbox and char not in st.session_state.allowed_diacritics:
                        st.session_state.allowed_diacritics.add(char)
                    elif not checkbox and char in st.session_state.allowed_diacritics:
                        st.session_state.allowed_diacritics.remove(char)

    with col2:
        st.write("Vybrané diakritické znaky:")
        if st.session_state.allowed_diacritics:
            st.code(" ".join(sorted(st.session_state.allowed_diacritics)))
        else:
            st.write("Žiadne")

        if st.button("Vyčistiť diakritiku", key="clear_diacritics"):
            st.session_state.allowed_diacritics = set()
            st.rerun()

    with col3:
        generate_button = st.button("Generovať slová", type="primary")
        if st.button("Vyčistiť text", key="clear"):
            st.session_state.letters = ""
            st.rerun()

    # Update letters in session state
    if letters != st.session_state.letters:
        st.session_state.letters = letters

    if generate_button and st.session_state.letters:
        # Create generator with current allowed diacritics
        generator = SlovakWordGenerator(st.session_state.allowed_diacritics)
        
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