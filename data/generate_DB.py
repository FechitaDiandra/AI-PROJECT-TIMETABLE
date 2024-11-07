import json

profesori = {
    "profesor_logica": {"nume": "Prof. Ionescu", "intervale_preferate": [], "restrictii": []},
    "profesor_matematica": {"nume": "Prof. Popescu", "intervale_preferate": [], "restrictii": []},
    "profesor_proiectare_algoritmi": {"nume": "Prof. Marinescu", "intervale_preferate": [], "restrictii": []},
    "profesor_po": {"nume": "Prof. Georgescu", "intervale_preferate": [], "restrictii": []},
    "profesor_sisteme_operare": {"nume": "Prof. Dumitrescu", "intervale_preferate": [], "restrictii": []},
    
    "profesor_java": {"nume": "Prof. Constantinescu", "intervale_preferate": [], "restrictii": []},
    "profesor_tehnologii_web": {"nume": "Prof. Mihailescu", "intervale_preferate": [], "restrictii": []},
    "profesor_baze_date": {"nume": "Prof. Enescu", "intervale_preferate": [], "restrictii": []},
    "profesor_algoritmi_genetici": {"nume": "Prof. Iliescu", "intervale_preferate": [], "restrictii": []},
    "profesor_antreprenoriat": {"nume": "Prof. Bratu", "intervale_preferate": [], "restrictii": []},
    "profesor_retele_calculatoare": {"nume": "Prof. Vasilescu", "intervale_preferate": [], "restrictii": []},

    "profesor_ai": {"nume": "Prof. Andreescu", "intervale_preferate": [], "restrictii": []},
    "profesor_dotnet": {"nume": "Prof. Cazacu", "intervale_preferate": [], "restrictii": []},
    "profesor_machine_learning": {"nume": "Prof. Golescu", "intervale_preferate": [], "restrictii": []},
    "profesor_a3d": {"nume": "Prof. Barbu", "intervale_preferate": [], "restrictii": []},
    "profesor_python": {"nume": "Prof. Ciobanu", "intervale_preferate": [], "restrictii": []},
    "profesor_securitate_info": {"nume": "Prof. Dumitriu", "intervale_preferate": [], "restrictii": []},
}

activitati = [
    # Anul 1
    {"tip": "curs", "materie": "Logica", "profesor": "profesor_logica", "an": 1},
    {"tip": "laborator", "materie": "Logica", "profesor": "profesor_logica", "an": 1},
    {"tip": "curs", "materie": "Matematica", "profesor": "profesor_matematica", "an": 1},
    {"tip": "laborator", "materie": "Matematica", "profesor": "profesor_matematica", "an": 1},
    {"tip": "curs", "materie": "Proiectarea Algoritmilor", "profesor": "profesor_proiectare_algoritmi", "an": 1},
    {"tip": "laborator", "materie": "Proiectarea Algoritmilor", "profesor": "profesor_proiectare_algoritmi", "an": 1},
    {"tip": "curs", "materie": "Proiectare Orientată pe Obiect", "profesor": "profesor_po", "an": 1},
    {"tip": "laborator", "materie": "Proiectare Orientată pe Obiect", "profesor": "profesor_po", "an": 1},
    {"tip": "curs", "materie": "Sisteme de Operare", "profesor": "profesor_sisteme_operare", "an": 1},
    {"tip": "laborator", "materie": "Sisteme de Operare", "profesor": "profesor_sisteme_operare", "an": 1},

    # Anul 2
    {"tip": "curs", "materie": "Java", "profesor": "profesor_java", "an": 2},
    {"tip": "laborator", "materie": "Java", "profesor": "profesor_java", "an": 2},
    {"tip": "curs", "materie": "Tehnologii Web", "profesor": "profesor_tehnologii_web", "an": 2},
    {"tip": "laborator", "materie": "Tehnologii Web", "profesor": "profesor_tehnologii_web", "an": 2},
    {"tip": "curs", "materie": "Baze de Date", "profesor": "profesor_baze_date", "an": 2},
    {"tip": "laborator", "materie": "Baze de Date", "profesor": "profesor_baze_date", "an": 2},
    {"tip": "curs", "materie": "Algoritmi Genetici", "profesor": "profesor_algoritmi_genetici", "an": 2},
    {"tip": "laborator", "materie": "Algoritmi Genetici", "profesor": "profesor_algoritmi_genetici", "an": 2},
    {"tip": "curs", "materie": "Antreprenoriat", "profesor": "profesor_antreprenoriat", "an": 2},
    {"tip": "laborator", "materie": "Antreprenoriat", "profesor": "profesor_antreprenoriat", "an": 2},
    {"tip": "curs", "materie": "Rețele de Calculatoare", "profesor": "profesor_retele_calculatoare", "an": 2},
    {"tip": "laborator", "materie": "Rețele de Calculatoare", "profesor": "profesor_retele_calculatoare", "an": 2},

    # Anul 3
    {"tip": "curs", "materie": "Inteligență Artificială", "profesor": "profesor_ai", "an": 3},
    {"tip": "laborator", "materie": "Inteligență Artificială", "profesor": "profesor_ai", "an": 3},
    {"tip": "curs", "materie": "DotNet", "profesor": "profesor_dotnet", "an": 3},
    {"tip": "laborator", "materie": "DotNet", "profesor": "profesor_dotnet", "an": 3},
    {"tip": "curs", "materie": "Machine Learning", "profesor": "profesor_machine_learning", "an": 3},
    {"tip": "laborator", "materie": "Machine Learning", "profesor": "profesor_machine_learning", "an": 3},
    {"tip": "curs", "materie": "A3D", "profesor": "profesor_a3d", "an": 3},
    {"tip": "laborator", "materie": "A3D", "profesor": "profesor_a3d", "an": 3},
    {"tip": "curs", "materie": "Python", "profesor": "profesor_python", "an": 3},
    {"tip": "laborator", "materie": "Python", "profesor": "profesor_python", "an": 3},
    {"tip": "curs", "materie": "Securitatea Informației", "profesor": "profesor_securitate_info", "an": 3},
    {"tip": "laborator", "materie": "Securitatea Informației", "profesor": "profesor_securitate_info", "an": 3},
]

grupe = {
    # Anul 1
    "1A1": {"an": 1, "seminar": "A", "numar_grupa": 1},
    "1A2": {"an": 1, "seminar": "A", "numar_grupa": 2},
    "1A3": {"an": 1, "seminar": "A", "numar_grupa": 3},
    
    "1B1": {"an": 1, "seminar": "B", "numar_grupa": 1},
    "1B2": {"an": 1, "seminar": "B", "numar_grupa": 2},
    "1B3": {"an": 1, "seminar": "B", "numar_grupa": 3},
    
    "1E1": {"an": 1, "seminar": "E", "numar_grupa": 1},
    "1E2": {"an": 1, "seminar": "E", "numar_grupa": 2},
    "1E3": {"an": 1, "seminar": "E", "numar_grupa": 3},

    # Anul 2
    "2A1": {"an": 2, "seminar": "A", "numar_grupa": 1},
    "2A2": {"an": 2, "seminar": "A", "numar_grupa": 2},
    "2A3": {"an": 2, "seminar": "A", "numar_grupa": 3},
    
    "2B1": {"an": 2, "seminar": "B", "numar_grupa": 1},
    "2B2": {"an": 2, "seminar": "B", "numar_grupa": 2},
    "2B3": {"an": 2, "seminar": "B", "numar_grupa": 3},
    
    "2E1": {"an": 2, "seminar": "E", "numar_grupa": 1},
    "2E2": {"an": 2, "seminar": "E", "numar_grupa": 2},
    "2E3": {"an": 2, "seminar": "E", "numar_grupa": 3},

    # Anul 3
    "3A1": {"an": 3, "seminar": "A", "numar_grupa": 1},
    "3A2": {"an": 3, "seminar": "A", "numar_grupa": 2},
    "3A3": {"an": 3, "seminar": "A", "numar_grupa": 3},
    
    "3B1": {"an": 3, "seminar": "B", "numar_grupa": 1},
    "3B2": {"an": 3, "seminar": "B", "numar_grupa": 2},
    "3B3": {"an": 3, "seminar": "B", "numar_grupa": 3},
    
    "3E1": {"an": 3, "seminar": "E", "numar_grupa": 1},
    "3E2": {"an": 3, "seminar": "E", "numar_grupa": 2},
    "3E3": {"an": 3, "seminar": "E", "numar_grupa": 3},
}

sali = {
    "C1": {"capacitate": 4, "disponibilitate": {"zile": ["luni", "marti", "miercuri", "joi", "vineri"], "intervale": ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]}},
    "C2": {"capacitate": 4, "disponibilitate": {"zile": ["luni", "marti", "miercuri", "joi", "vineri"], "intervale": ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]}},
    "C102": {"capacitate": 2, "disponibilitate": {"zile": ["luni", "marti", "miercuri", "joi", "vineri"], "intervale": ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]}},
    "C202": {"capacitate": 2, "disponibilitate": {"zile": ["luni", "marti", "miercuri", "joi", "vineri"], "intervale": ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]}},
    "C123": {"capacitate": 3, "disponibilitate": {"zile": ["luni", "marti", "miercuri", "joi", "vineri"], "intervale": ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]}},
}

for i in range(301, 311):
    sali[f"C{i}"] = {
        "capacitate": 1,
        "disponibilitate": {"zile": ["luni", "marti", "miercuri", "joi", "vineri"], "intervale": ["8:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]}
    }


def save_to_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

save_to_json("profesori", profesori)
save_to_json("activitati", activitati)
save_to_json("sali", sali)
save_to_json("grupe", grupe)
