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

# download resursele necesare pentru nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt_tab')
LANGUAGE_MAP = {
    'en': 'english',
    'ro': 'romanian',
    'fr': 'french',
    'de': 'german',
}
# citeste un fisier text
def citeste_text(fisier):
    print(f"se incearca citirea fisierului: {fisier}")
    if not os.path.exists(fisier):
        raise FileNotFoundError(f"fisierul {fisier} nu exista.")
    with open(fisier, 'r', encoding='utf-8') as f:
        return f.read()

def identifica_limba(text):
    if len(text) < 20:  # text prea scurt
        print("text prea scurt pentru detectare precisa. repet textul.")
        text += " " + text
    elif len(text) > 1000:  # text prea lung
        print("text prea lung. se utilizeaza doar un extras pentru detectare.")
        text = text[:1000]

    detected_language = detect(text)
    print(f"detected language: {detected_language}")

    # fallback la romana daca limba detectata nu este relevanta
    if detected_language not in ['ro', 'en', 'fr', 'de']:
        print(f"limba detectata ({detected_language}) nu este valida. fallback la 'ro'.")
        return 'ro'

    return detected_language

def get_stopwords_for_language(limba):
    try:
        mapped_language = LANGUAGE_MAP.get(limba, limba)
        if mapped_language in stopwords.fileids():
            stop_words = set(stopwords.words(mapped_language))
            if mapped_language == 'romanian':
                stop_words.update(["că", "nu", "este", "și", "în", "la", "de", "cu", "pe"])
            return list(stop_words)
        else:
            print(f"Limbă nesuportată ({limba}). Se utilizează fallback la 'english'.")
            return list(stopwords.words('english'))
    except Exception as e:
        print(f"Eroare la obținerea stopwords pentru {limba}: {e}")
        return list(stopwords.words('english'))


# analiza stilometrica
def analiza_stilometrica(text, limba='english'):
    try:
        cuvinte = word_tokenize(text.lower())
        cuvinte_fara_punctuatie = [cuvant for cuvant in cuvinte if cuvant not in string.punctuation]
        stop_words = set(stopwords.words(limba))
        cuvinte_semnificative = [cuvant for cuvant in cuvinte_fara_punctuatie if cuvant not in stop_words]
        frecventa = Counter(cuvinte_fara_punctuatie)
        caractere = len(text)
        numar_cuvinte = len(cuvinte_fara_punctuatie)
        proportie_semnificative = len(cuvinte_semnificative) / numar_cuvinte if numar_cuvinte > 0 else 0
        media_lungime_cuvinte = sum(len(cuvant) for cuvant in cuvinte_fara_punctuatie) / numar_cuvinte if numar_cuvinte > 0 else 0

        print("returning values from analiza_stilometrica...")
        return caractere, numar_cuvinte, frecventa, proportie_semnificative, media_lungime_cuvinte
    except Exception as e:
        print(f"error in analiza_stilometrica: {e}")
        return len(text), 0, Counter(), 0, 0


def genereaza_alternative_text(text, limba):
    stop_words = get_stopwords_for_language(limba)
    cuvinte = word_tokenize(text)
    

    cuvinte_inlocuibile = [
        cuvant for cuvant in cuvinte if cuvant.lower() not in stop_words and cuvant not in string.punctuation
    ]
    
    print(f"Cuvinte eligibile pentru înlocuire: {cuvinte_inlocuibile}")
    
    if not cuvinte_inlocuibile:
        return text

    num_to_replace = max(1, int(len(cuvinte_inlocuibile) * 0.8))
    cuvinte_de_inlocuit = random.sample(cuvinte_inlocuibile, num_to_replace)


    text_inlocuit = cuvinte.copy()

    for i, cuvant in enumerate(cuvinte):
        if cuvant in cuvinte_de_inlocuit:
            alternative = get_alternative_cuvinte(cuvant)
            
            
            filtered_alternatives = [alt for alt in alternative if '_' not in alt and len(alt) < 12]
            
            print(f"Alternative filtrate pentru '{cuvant}': {filtered_alternatives}")
            
            if filtered_alternatives:
                replacement = random.choice(filtered_alternatives)
                text_inlocuit[i] = replacement
                print(f"Înlocuit '{cuvant}' cu '{replacement}'")

    return ' '.join(text_inlocuit)

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

# extrage cuvinte cheie folosind tf-idf
def extrage_cuvinte_cheie_tfidf(text, limba):
    stop_words = list(get_stopwords_for_language(limba))
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=5)
    tfidf_matrix = vectorizer.fit_transform([text])
    scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0])
    cuvinte_cheie = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    return [cuvant for cuvant, _ in cuvinte_cheie]

# genereaza propozitii pentru fiecare cuvant cheie
def genereaza_propozitii_cuvinte_cheie(text, cuvinte_cheie):
    propozitii = sent_tokenize(text)
    rezumat = {}
    for cuvant_cheie in cuvinte_cheie:
        for propozitie in propozitii:
            if cuvant_cheie.lower() in propozitie.lower():
                rezumat[cuvant_cheie] = propozitie
                break
    return rezumat


def main():
    print("language detection system ready!")
    print("enter 'quit' to exit")

    while True:
        print("\nchoose an option:")
        print("1. enter text manually")
        print("2. read text from a file")
        print("type 'quit' to exit.")

        option = input("> ")

        if option.lower() == 'quit':
            print("goodbye!")
            break

        if option == "1":
            print("\nenter text to detect language:")
            user_input = input("> ")
        elif option == "2":
            print("\nenter the file path:")
            file_path = input("> ")
            try:
                user_input = citeste_text(file_path)
                print(f"text read from file:\n{user_input[:100]}...")
            except FileNotFoundError as e:
                print(f"error: {e}")
                continue
        else:
            print("invalid option. please choose 1 or 2.")
            continue

        if not user_input.strip():
            print("please enter some text or provide a valid file.")
            continue

        try:
            detected_language = identifica_limba(user_input)
            print(f"detected language: {detected_language}")
        except Exception as e:
            print(f"error detecting language: {e}")
            continue

        try:
           caractere, cuvinte, frecventa, proportie_semnificative, media_lungime_cuvinte = analiza_stilometrica(user_input)
           print(f"lungime text: {caractere} caractere, {cuvinte} cuvinte.")
           print(f"proportia cuvintelor semnificative: {proportie_semnificative:.2f}")
           print(f"media lungimii cuvintelor: {media_lungime_cuvinte:.2f}")
           print("frecventa cuvintelor:")
           for cuvant, frecventa_cuv in frecventa.most_common(10):
            print(f"{cuvant}: {frecventa_cuv}")
        except Exception as e:
          print(f"error in stylometric analysis: {e}")
          continue


        try:
            alt_text = genereaza_alternative_text(user_input, detected_language.lower())
            print("\nalternative text with replacements:")
            print(alt_text)
        except Exception as e:
            print(f"error generating alternative text: {e}")
            continue

        try:
            keywords = extrage_cuvinte_cheie_tfidf(user_input, detected_language.lower())
            print(f"\nkeywords extracted: {', '.join(keywords)}")
            keyword_sentences = genereaza_propozitii_cuvinte_cheie(user_input, keywords)
            print("\nkeywords and their context:")
            for keyword, sentence in keyword_sentences.items():
                print(f"\nkeyword: {keyword}")
                print(f"context: {sentence}")
        except Exception as e:
            print(f"error extracting keywords: {e}")
            continue

if __name__ == "__main__":
    main()
