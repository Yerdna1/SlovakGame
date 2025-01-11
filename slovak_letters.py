import streamlit as st
from collections import Counter
import pandas as pd

class SlovakWordGenerator:
    def __init__(self, allowed_diacritics=None):
        self.dictionary = set()
        self.allowed_diacritics = allowed_diacritics or set()
        self.slovak_map = {
            'á': 'a', 'ä': 'a', 'č': 'c', 'ď': 'd', 
            'é': 'e', 'í': 'i', 'ĺ': 'l', 'ľ': 'l',
            'ň': 'n', 'ó': 'o', 'ô': 'o', 'ŕ': 'r',
            'š': 's', 'ť': 't', 'ú': 'u', 'ý': 'y',
            'ž': 'z'
        }
        self.load_dictionary('sk_SK.dic')

    def load_dictionary(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                word = line.split('/')[0]
                # Store original word to preserve diacritics
                self.dictionary.add(word)

    def normalize_slovak(self, text: str) -> str:
        text = text.lower()
        result = []
        for c in text:
            if c in self.allowed_diacritics:
                result.append(c)
            else:
                result.append(self.slovak_map.get(c, c))
        return ''.join(result)

    def can_make_word(self, available_letters: str, word: str) -> bool:
        available = Counter(available_letters.lower())
        needed = Counter(word.lower())
        return all(available[c] >= needed[c] for c in needed)

    def calculate_word_score(self, word: str) -> int:
        base_score = len(word) * 10
        bonus = sum(2 for c in word if c in self.allowed_diacritics)
        return base_score + bonus

    def generate_words(self, letters: str) -> list:
        results = []
        for word in self.dictionary:
            # Only include words that can be made with given letters
            if self.can_make_word(letters, word):
                # Check if word only uses allowed diacritics
                has_valid_diacritics = all(
                    c in self.allowed_diacritics or c not in self.slovak_map 
                    for c in word
                )
                if has_valid_diacritics:
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
    if 'word_length' not in st.session_state:
        st.session_state['word_length'] = 10

    # Create tabs for main content and settings
    main_tab, settings_tab, slovak_records_tab = st.tabs(["Generátor", "Nastavenia", "Slovenské rekordy"])

    with settings_tab:
        st.header("Nastavenia")
        selected_length = st.radio(
            "Dĺžka slov:",
            [5, 10, 15],
            index=1,
            horizontal=True,
            help="Vyberte požadovanú dĺžku slov na generovanie"
        )
        if selected_length != st.session_state.word_length:
            st.session_state.word_length = selected_length
            st.session_state.letters = ""
            st.rerun()

    with slovak_records_tab:
        st.header("Najdlhšie slovenské slová")
        st.info("Top 10 najdlhších slov v slovenčine")
        
        longest_slovak_words = [
            ("najneobhospodarovávateľnejšieho", 28, "naj-ne-ob-hos-po-dar-o-vá-va-teľ-nej-šie-ho"),
            ("najnepravdepodobnejšieho", 23, "naj-ne-prav-de-po-dob-nej-šie-ho"),
            ("najnespochybniteľnejšie", 23, "naj-ne-spo-chyb-ni-teľ-nej-šie"),
            ("najcharakteristickejšie", 22, "naj-cha-rak-te-ris-tic-kej-šie"),
            ("najneprekonateľnejšieho", 22, "naj-ne-pre-ko-na-teľ-nej-šie-ho"),
            ("najnepravdepodobnejšie", 22, "naj-ne-prav-de-po-dob-nej-šie"),
            ("najnepochopiteľnejšieho", 22, "naj-ne-po-cho-pi-teľ-nej-šie-ho"),
            ("najsofistikovanejšieho", 21, "naj-so-fis-ti-ko-va-nej-šie-ho"),
            ("najnepoužiteľnejšieho", 21, "naj-ne-po-u-ži-teľ-nej-šie-ho"),
            ("najidentifikovateľnejší", 21, "naj-i-den-ti-fi-ko-va-teľ-nej-ší")
        ]
        
        for i, (word, length, syllables) in enumerate(longest_slovak_words, 1):
            st.write(f"{i}. **{word}** (dĺžka: {length})")
            st.caption(f"Po slabikách: {syllables}")

    with main_tab:
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            letters = st.text_input(
                f"Zadajte písmená (presne {st.session_state.word_length}):",
                value=st.session_state.letters,
                key="text_input"
            )

            diacritic_groups = {
                "Dlhé samohlásky": ['á', 'é', 'í', 'ó', 'ú', 'ý'],
                "Mäkké spoluhlásky": ['č', 'ď', 'ľ', 'ň', 'š', 'ť', 'ž'],
                "Ostatné": ['ä', 'ĺ', 'ô', 'ŕ']
            }

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

        if letters != st.session_state.letters:
            st.session_state.letters = letters

        if generate_button and st.session_state.letters:
            generator = SlovakWordGenerator(st.session_state.allowed_diacritics)
            
            normalized_len = len(generator.normalize_slovak(st.session_state.letters))
            if normalized_len != st.session_state.word_length:
                st.error(f"Prosím, zadajte presne {st.session_state.word_length} písmen! (Zadali ste {normalized_len})")
            else:
                words = generator.generate_words(st.session_state.letters)
                
                if not words:
                    st.warning("Neboli nájdené žiadne slová.")
                else:
                    total_words = len(words)
                    st.success(f"Nájdených {total_words} slov")

                    col1, col2 = st.columns(2)
                    
                    with col1:
                        with st.expander("Top 10 podľa skóre", expanded=True):
                            top_score = sorted(words, key=lambda x: (-x[1], -len(x[0])))[:10]
                            for i, (word, score) in enumerate(top_score, 1):
                                st.write(f"{i}. **{word}** (skóre: {score}, dĺžka: {len(word)})")
                        
                        with st.expander("Top 10 najdlhších slov", expanded=True):
                            top_longest = sorted(words, key=lambda x: (len(x[0]), x[1]), reverse=True)[:10]
                            for i, (word, score) in enumerate(top_longest, 1):
                                st.write(f"{i}. **{word}** (dĺžka: {len(word)}, skóre: {score})")

                    with col2:
                        with st.expander("Top 10 s najviac diakritickými znamienkami", expanded=True):
                            def count_diacritics(word):
                                return sum(1 for c in word if c in 'áäčďéíĺľňóôŕšťúýž')
                            
                            top_diacritics = sorted(words, 
                                                key=lambda x: (count_diacritics(x[0]), len(x[0]), x[1]), 
                                                reverse=True)[:10]
                            for i, (word, score) in enumerate(top_diacritics, 1):
                                diacritic_count = count_diacritics(word)
                                st.write(f"{i}. **{word}** (diakritika: {diacritic_count}, skóre: {score})")
                        
                        with st.expander("Slová podľa dĺžky", expanded=True):
                            length_groups = {}
                            for word, score in words:
                                length = len(word)
                                if length not in length_groups:
                                    length_groups[length] = []
                                length_groups[length].append((word, score))
                            
                            for length in sorted(length_groups.keys(), reverse=True):
                                group = length_groups[length]
                                group.sort(key=lambda x: x[1], reverse=True)
                                st.write(f"**{length} písmen** ({len(group)} slov):")
                                for word, score in group[:5]:
                                    st.write(f"- {word} (skóre: {score})")
                                if len(group) > 5:
                                    st.write(f"- *...a ďalších {len(group) - 5} slov*")

                    # Create DataFrame for display
                    data = []
                    for word, score in sorted(words, key=lambda x: (-len(x[0]), -x[1])):
                        data.append({
                            "Dĺžka": len(word),
                            "Slovo": word,  # Using original word with diacritics
                            "Skóre": score,
                            "Diakritika": sum(1 for c in word if c in 'áäčďéíĺľňóôŕšťúýž')
                        })

                    df = pd.DataFrame(data)
                    st.dataframe(
                        df,
                        column_config={
                            "Dĺžka": st.column_config.NumberColumn(help="Počet písmen v slove"),
                            "Slovo": st.column_config.TextColumn(help="Nájdené slovo", width="large"),
                            "Skóre": st.column_config.NumberColumn(help="Skóre slova"),
                            "Diakritika": st.column_config.NumberColumn(help="Počet diakritických znamienok")
                        },
                        hide_index=True
                    )

if __name__ == "__main__":
    main()