from langdetect import detect
from collections import Counter
import string
import os

def citeste_text(fisier):
    print(f"Se încearcă citirea fișierului: {fisier}")
    if not os.path.exists(fisier):
        raise FileNotFoundError(f"Fișierul {fisier} nu există.")
    with open(fisier, 'r', encoding='utf-8') as f:
        return f.read()

def identifica_limba(text):
    print(f"Detectez limba pentru text: {text[:100]}...")
    return detect(text)

def analiza_stilometrica(text):
    text_fara_punctuatie = text.translate(str.maketrans('', '', string.punctuation))
    cuvinte = text_fara_punctuatie.split()
    caractere = len(text)
    lungime_cuvinte = len(cuvinte)
    frecventa_cuvinte = Counter(cuvinte)
    print(f"Analiza stilometrică: {caractere} caractere, {lungime_cuvinte} cuvinte.")
    return caractere, lungime_cuvinte, frecventa_cuvinte

def main():
    print("Alegeți opțiunea:")
    print("1. Citire text din fișier")
    print("2. Introducere text de la tastatură")
    optiune = input("Introduceți opțiunea (1 sau 2): ")

    if optiune == '1':
        fisier = input("Introduceți calea către fișierul text: ")
        try:
            text = citeste_text(fisier)
            print(f"Text citit cu succes: {text[:100]}...")
        except FileNotFoundError as e:
            print(f"Eroare: {e}")
            return
    elif optiune == '2':
        print("Introduceți textul pentru analiză:")
        text = input("> ")
    else:
        print("Opțiune invalidă. Vă rugăm să alegeți 1 sau 2.")
        return

    # Identificăm limba textului
    limba = identifica_limba(text)
    print(f"Limba detectată: {limba}")

    # Analizăm textul
    caractere, cuvinte, frecventa = analiza_stilometrica(text)
    print(f"Lungime text: {caractere} caractere, {cuvinte} cuvinte.")
    print("Frecvența cuvintelor:")
    for cuvant, frecventa_cuv in frecventa.most_common(10):  # Primele 10 cuvinte frecvente
        print(f"{cuvant}: {frecventa_cuv}")

if __name__ == "__main__":
    print("Script pornit")
    main()
    print("Script terminat")
1