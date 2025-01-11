import streamlit as st
from collections import Counter
import pandas as pd




class SlovakWordGenerator:
    def __init__(self):
        # Built-in dictionary of common Slovak words
        self.dictionary = {
            # Basic words and conjunctions
            'a', 'aby', 'ak', 'ako', 'alebo', 'ale', 'ani', 'až', 'že', 'keď', 'však',
            
            # Common verbs (more forms)
            'byť', 'mať', 'ísť', 'prísť', 'odísť', 'robiť', 'vidieť', 'počuť', 'hovoriť',
            'písať', 'čítať', 'spať', 'jesť', 'piť', 'variť', 'učiť', 'pracovať', 'hrať',
            'plakať', 'smiať', 'bežať', 'skákať', 'sedieť', 'stáť', 'ležať', 'cestovať',
            'nakupovať', 'predávať', 'platiť', 'študovať', 'rozumieť', 'myslieť', 'vedieť',
            'chcieť', 'môcť', 'musieť', 'začať', 'skončiť', 'pokračovať',
            
            # House and furniture
            'dom', 'byt', 'izba', 'kuchyňa', 'kúpeľňa', 'záchod', 'spálňa', 'obývačka',
            'stôl', 'stolička', 'skriňa', 'posteľ', 'police', 'zrkadlo', 'umývadlo',
            'vaňa', 'sprcha', 'záclona', 'koberec', 'lampa', 'obraz', 'hodiny', 'dvere',
            'okno', 'stena', 'strop', 'podlaha', 'balkón', 'garáž', 'záhrada', 'plot',
            
            # Food and cooking
            'chlieb', 'maslo', 'syr', 'mlieko', 'smotana', 'jogurt', 'vajce', 'mäso',
            'kura', 'ryba', 'šunka', 'klobása', 'párky', 'polievka', 'zemiak', 'ryža',
            'cestoviny', 'šalát', 'mrkva', 'paradajka', 'uhorka', 'cibuľa', 'cesnak',
            'jablko', 'hruška', 'banán', 'pomaranč', 'citrón', 'čučoriedky', 'jahoda',
            
            # School and education
            'škola', 'trieda', 'žiak', 'študent', 'učiteľ', 'profesor', 'kniha',
            'zošit', 'pero', 'ceruzka', 'tabuľa', 'krieda', 'úloha', 'skúška',
            'známka', 'vysvedčenie', 'prestávka', 'fyzika', 'chémia', 'biológia',
            
            # Technology and modern life
            'počítač', 'telefón', 'mobil', 'tablet', 'internet', 'wifi', 'email',
            'správa', 'aplikácia', 'program', 'heslo', 'súbor', 'video', 'fotka',
            'kamera', 'televízor', 'rádio', 'nabíjačka', 'batéria', 'obrazovka',
            
            # Transportation
            'auto', 'autobus', 'vlak', 'lietadlo', 'bicykel', 'motorka', 'loď',
            'metro', 'električka', 'zastávka', 'stanica', 'letenka', 'lístok',
            'vodič', 'cestujúci', 'batožina', 'kufor', 'cesta', 'ulica', 'most',
            
            # Nature and environment
            'slnko', 'mesiac', 'hviezda', 'nebo', 'oblak', 'dážď', 'sneh', 'vietor',
            'búrka', 'strom', 'kvet', 'tráva', 'list', 'koreň', 'hora', 'les',
            'rieka', 'jazero', 'more', 'ostrov', 'pláž', 'púšť', 'vzduch', 'zem',
            
            # Animals
            'pes', 'mačka', 'kôň', 'krava', 'ovca', 'koza', 'prasa', 'sliepka',
            'kohút', 'zajac', 'myš', 'medveď', 'vlk', 'líška', 'jeleň', 'veverička',
            'vták', 'holub', 'orol', 'sova', 'had', 'žaba', 'ryba', 'motýľ', 'včela',
            
            # Sports and leisure
            'futbal', 'hokej', 'tenis', 'volejbal', 'basketbal', 'plávanie',
            'beh', 'lyžovanie', 'korčuľovanie', 'tanec', 'šport', 'hra', 'zápas',
            'tréning', 'cvičenie', 'prechádzka', 'výlet', 'dovolenka', 'prázdniny',
            
            # Health and medicine
            'zdravie', 'choroba', 'bolesť', 'liek', 'doktor', 'lekár', 'zubár',
            'nemocnica', 'sanitka', 'ordinácia', 'recept', 'teplota', 'chrípka',
            'nádcha', 'kašeľ', 'rana', 'operácia', 'vyšetrenie', 'poisťovňa'
        }

        # Add common word variations
        self.dictionary.update({
            # Verb conjugations
            'som', 'si', 'je', 'sme', 'ste', 'sú',
            'bol', 'bola', 'bolo', 'boli',
            'budem', 'budeš', 'bude', 'budeme', 'budete', 'budú',
            'mám', 'máš', 'má', 'máme', 'máte', 'majú',
            'mal', 'mala', 'malo', 'mali',
            'idem', 'ideš', 'ide', 'ideme', 'idete', 'idú',
            'šiel', 'šla', 'šlo', 'šli',
            'robím', 'robíš', 'robí', 'robíme', 'robíte', 'robia',
            'robil', 'robila', 'robilo', 'robili',
            
            # Noun cases
            'človeka', 'človeku', 'človekom', 'ľudia', 'ľudí', 'ľuďom', 'ľuďmi',
            'mesta', 'mestu', 'mestom', 'mestá', 'miest', 'mestám', 'mestami',
            'domu', 'domom', 'domy', 'domov', 'domom', 'domami',
            'ženy', 'žene', 'ženu', 'ženou', 'žien', 'ženám', 'ženami',
            'dieťa', 'dieťaťa', 'dieťaťu', 'dieťaťom', 'deti', 'detí', 'deťom', 'deťmi'
        })

    def normalize_slovak(self, text: str) -> str:
        """Convert text with diacritics to basic form"""
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
        """Calculate score based on word length and special characters"""
        base_score = len(word) * 10
        special_chars = 'áäčďéíĺľňóôŕšťúýž'
        bonus = sum(2 for c in word if c in special_chars)
        return base_score + bonus

    def can_make_word(self, available_letters: str, word: str) -> bool:
        """Check if word can be made from available letters"""
        available = Counter(self.normalize_slovak(available_letters))
        needed = Counter(self.normalize_slovak(word))
        return all(available[c] >= needed[c] for c in needed)

    def generate_words(self, letters: str) -> list:
        """Generate possible words and their scores"""
        results = []
        for word in self.dictionary:
            if self.can_make_word(letters, word):
                score = self.calculate_word_score(word)
                results.append((word, score))
        return sorted(results, key=lambda x: (-x[1], -len(x[0])))

def main():
    st.set_page_config(page_title="Generátor slovenských slov", page_icon="🇸🇰", layout="wide")
    st.title("Generátor slovenských slov")

    generator = SlovakWordGenerator()

    # Create two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        letters = st.text_input("Zadajte písmená (presne 10):", key="letters")

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
                if cols[i].button(char):
                    letters = st.session_state.letters + char
                    st.session_state.letters = letters

    with col2:
        generate_button = st.button("Generovať slová", type="primary")
        clear_button = st.button("Vyčistiť")

    if clear_button:
        st.session_state.letters = ""
        st.experimental_rerun()

    if generate_button and letters:
        normalized_len = len(generator.normalize_slovak(letters))
        if normalized_len != 10:
            st.error(f"Prosím, zadajte presne 10 písmen! (Zadali ste {normalized_len})")
        else:
            words = generator.generate_words(letters)
            
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