from langdetect import detect
from collections import Counter
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string
import os
import random
from sklearn.feature_extraction.text import TfidfVectorizer

# Download NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Citirea unui fișier text
def citeste_text(fisier):
    print(f"Se încearcă citirea fișierului: {fisier}")
    if not os.path.exists(fisier):
        raise FileNotFoundError(f"Fișierul {fisier} nu există.")
    with open(fisier, 'r', encoding='utf-8') as f:
        return f.read()

# Detectarea limbii utilizând langdetect
def identifica_limba(text):
    if len(text) < 20:  # Text prea scurt
        print("Text prea scurt pentru detectare precisă. Repet textul.")
        text += " " + text
    elif len(text) > 1000:  # Text prea lung
        print("Text prea lung. Se utilizează doar un extras pentru detectare.")
        text = text[:1000]

    detected_language = detect(text)
    print(f"Detected language: {detected_language}")

    # Fallback la română dacă limba detectată nu este relevantă
    if detected_language not in ['ro', 'en', 'fr', 'de']:  # Lista limbilor acceptate
        print(f"Limba detectată ({detected_language}) nu este validă. Fallback la 'ro'.")
        return 'ro'

    return detected_language

# Obține lista de stopwords pentru o limbă specifică
def get_stopwords_for_language(limba):
    try:
        stop_words = set(stopwords.words(limba))
        if limba == 'ro':  # Exemple suplimentare pentru română
            stop_words.update(["printr", "că", "nu", "este", "și", "în", "la", "de", "cu", "pe"])
        return list(stop_words)
    except OSError:
        print(f"Stopwords pentru limba {limba} nu sunt disponibile. Se utilizează limba engleză ca fallback.")
        return list(stopwords.words('english'))

# Analiză stilometrică
def analiza_stilometrica(text):
    cuvinte = word_tokenize(text)
    caractere = len(text)
    lungime_cuvinte = len(cuvinte)
    frecventa_cuvinte = Counter(cuvinte)
    print(f"Analiza stilometrică: {caractere} caractere, {lungime_cuvinte} cuvinte.")
    return caractere, lungime_cuvinte, frecventa_cuvinte

# Generarea versiunilor alternative ale textului
def genereaza_alternative_text(text, limba):
    stop_words = get_stopwords_for_language(limba)
    cuvinte = word_tokenize(text)
    num_to_replace = max(1, int(len(cuvinte) * 0.2))
    cuvinte_inlocuibile = [cuvant for cuvant in cuvinte if cuvant.lower() not in stop_words and cuvant not in string.punctuation]

    print(f"Cuvinte eligibile pentru înlocuire: {cuvinte_inlocuibile}")

    if not cuvinte_inlocuibile:
        return text

    cuvinte_de_inlocuit = random.sample(cuvinte_inlocuibile, min(num_to_replace, len(cuvinte_inlocuibile)))
    text_inlocuit = cuvinte.copy()

    for i, cuvant in enumerate(cuvinte):
        if cuvant in cuvinte_de_inlocuit:
            alternative = get_alternative_cuvinte(cuvant)
            print(f"Alternative pentru '{cuvant}': {alternative}")
            if alternative:
                text_inlocuit[i] = random.choice(alternative)

    return ' '.join(text_inlocuit)

# Obținerea sinonimelor, hipernimelor sau antonimelor negării
def get_alternative_cuvinte(cuvant):
    alternative = set()
    for synset in wordnet.synsets(cuvant):
        for lemma in synset.lemmas():
            alternative.add(lemma.name())
            if lemma.antonyms():
                alternative.add(f"not {lemma.antonyms()[0].name()}")
        for hypernym in synset.hypernyms():
            for lemma in hypernym.lemmas():
                alternative.add(lemma.name())
    return list(alternative - {cuvant})

# Extragerea cuvintelor cheie folosind TF-IDF
def extrage_cuvinte_cheie_tfidf(text, limba):
    stop_words = list(get_stopwords_for_language(limba))
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=5)
    tfidf_matrix = vectorizer.fit_transform([text])
    scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0])
    cuvinte_cheie = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    return [cuvant for cuvant, _ in cuvinte_cheie]

# Generarea propozițiilor pentru fiecare cuvânt cheie
def genereaza_propozitii_cuvinte_cheie(text, cuvinte_cheie):
    propozitii = sent_tokenize(text)
    rezumat = {}
    for cuvant_cheie in cuvinte_cheie:
        for propozitie in propozitii:
            if cuvant_cheie.lower() in propozitie.lower():
                rezumat[cuvant_cheie] = propozitie
                break
    return rezumat

# Main
def main():
    print("Language detection system ready!")
    print("Enter 'quit' to exit")

    while True:
        print("\nChoose an option:")
        print("1. Enter text manually")
        print("2. Read text from a file")
        print("Type 'quit' to exit.")

        option = input("> ")

        if option.lower() == 'quit':
            print("Goodbye!")
            break

        if option == "1":
            print("\nEnter text to detect language:")
            user_input = input("> ")
        elif option == "2":
            print("\nEnter the file path:")
            file_path = input("> ")
            try:
                user_input = citeste_text(file_path)
                print(f"Text read from file:\n{user_input[:100]}...")
            except FileNotFoundError as e:
                print(f"Error: {e}")
                continue
        else:
            print("Invalid option. Please choose 1 or 2.")
            continue

        if not user_input.strip():
            print("Please enter some text or provide a valid file.")
            continue

        try:
            detected_language = identifica_limba(user_input)
            print(f"Detected language: {detected_language}")
        except Exception as e:
            print(f"Error detecting language: {e}")
            continue

        try:
            caractere, cuvinte, frecventa = analiza_stilometrica(user_input)
            print(f"Lungime text: {caractere} caractere, {cuvinte} cuvinte.")
            print("Frecvența cuvintelor:")
            for cuvant, frecventa_cuv in frecventa.most_common(10):
                print(f"{cuvant}: {frecventa_cuv}")
        except Exception as e:
            print(f"Error in stylometric analysis: {e}")
            continue

        try:
            alt_text = genereaza_alternative_text(user_input, detected_language.lower())
            print("\nAlternative text with replacements:")
            print(alt_text)
        except Exception as e:
            print(f"Error generating alternative text: {e}")
            continue

        try:
            keywords = extrage_cuvinte_cheie_tfidf(user_input, detected_language.lower())
            print(f"\nKeywords extracted: {', '.join(keywords)}")
            keyword_sentences = genereaza_propozitii_cuvinte_cheie(user_input, keywords)
            print("\nKeywords and their context:")
            for keyword, sentence in keyword_sentences.items():
                print(f"\nKeyword: {keyword}")
                print(f"Context: {sentence}")
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            continue

if __name__ == "__main__":
    main()
