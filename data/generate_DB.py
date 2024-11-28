import json

profesori = [
    {"nume": "Ionescu", "materie": "Logica"},
    {"nume": "Popescu", "materie": "Matematica"},
    {"nume": "Marinescu", "materie": "Proiectarea_Algoritmilor"},
    {"nume": "Georgescu", "materie": "Proiectare_Orientata_pe_Obiect"},
    {"nume": "Dumitrescu", "materie": "Sisteme_de_Operare"},
    
    {"nume": "Constantinescu", "materie": "Java"},
    {"nume": "Mihailescu", "materie": "Tehnologii_Web"},
    {"nume": "Enescu", "materie": "Baze_de_Date"},
    {"nume": "Iliescu", "materie": "Algoritmi_Genetici"},
    {"nume": "Bratu", "materie": "Antreprenoriat"},
    {"nume": "Vasilescu", "materie": "Retele_de_Calculatoare"},

    {"nume": "Andreescu", "materie": "Inteligenta_Artificiala"},
    {"nume": "Cazacu", "materie": "DotNet"},
    {"nume": "Golescu", "materie": "Machine_Learning"},
    {"nume": "Barbu", "materie": "A3D"},
    {"nume": "Ciobanu", "materie": "Python"},
    {"nume": "Dumitriu", "materie": "Securitatea_Informatiei"},
]

activitati = [
    {"tip": "curs", "materie": "Logica", "profesor": "Ionescu", "an": 1},
    {"tip": "laborator", "materie": "Logica", "profesor": "Ionescu", "an": 1},
    {"tip": "curs", "materie": "Matematica", "profesor": "Popescu", "an": 1},
    {"tip": "laborator", "materie": "Matematica", "profesor": "Popescu", "an": 1},
    {"tip": "curs", "materie": "Proiectarea_Algoritmilor", "profesor": "Marinescu", "an": 1},
    {"tip": "laborator", "materie": "Proiectarea_Algoritmilor", "profesor": "Marinescu", "an": 1},
    {"tip": "curs", "materie": "Proiectare_Orientata_pe_Obiect", "profesor": "Georgescu", "an": 1},
    {"tip": "laborator", "materie": "Proiectare_Orientata_pe_Obiect", "profesor": "Georgescu", "an": 1},
    {"tip": "curs", "materie": "Sisteme_de_Operare", "profesor": "Dumitrescu", "an": 1},
    {"tip": "laborator", "materie": "Sisteme_de_Operare", "profesor": "Dumitrescu", "an": 1},

    {"tip": "curs", "materie": "Java", "profesor": "Constantinescu", "an": 2},
    {"tip": "laborator", "materie": "Java", "profesor": "Constantinescu", "an": 2},
    {"tip": "curs", "materie": "Tehnologii_Web", "profesor": "Mihailescu", "an": 2},
    {"tip": "laborator", "materie": "Tehnologii_Web", "profesor": "Mihailescu", "an": 2},
    {"tip": "curs", "materie": "Baze_de_Date", "profesor": "Enescu", "an": 2},
    {"tip": "laborator", "materie": "Baze_de_Date", "profesor": "Enescu", "an": 2},
    {"tip": "curs", "materie": "Algoritmi_Genetici", "profesor": "Iliescu", "an": 2},
    {"tip": "laborator", "materie": "Algoritmi_Genetici", "profesor": "Iliescu", "an": 2},
    {"tip": "curs", "materie": "Antreprenoriat", "profesor": "Bratu", "an": 2},
    {"tip": "laborator", "materie": "Antreprenoriat", "profesor": "Bratu", "an": 2},
    {"tip": "curs", "materie": "Retele_de_Calculatoare", "profesor": "Vasilescu", "an": 2},
    {"tip": "laborator", "materie": "Retele_de_Calculatoare", "profesor": "Vasilescu", "an": 2},

    {"tip": "curs", "materie": "Inteligenta_Artificiala", "profesor": "Andreescu", "an": 3},
    {"tip": "laborator", "materie": "Inteligenta_Artificiala", "profesor": "Andreescu", "an": 3},
    {"tip": "curs", "materie": "DotNet", "profesor": "Cazacu", "an": 3},
    {"tip": "laborator", "materie": "DotNet", "profesor": "Cazacu", "an": 3},
    {"tip": "curs", "materie": "Machine_Learning", "profesor": "Golescu", "an": 3},
    {"tip": "laborator", "materie": "Machine_Learning", "profesor": "Golescu", "an": 3},
    {"tip": "curs", "materie": "A3D", "profesor": "Barbu", "an": 3},
    {"tip": "laborator", "materie": "A3D", "profesor": "Barbu", "an": 3},
    {"tip": "curs", "materie": "Python", "profesor": "Ciobanu", "an": 3},
    {"tip": "laborator", "materie": "Python", "profesor": "Ciobanu", "an": 3},
    {"tip": "curs", "materie": "Securitatea_Informatiei", "profesor": "Dumitriu", "an": 3},
    {"tip": "laborator", "materie": "Securitatea_Informatiei", "profesor": "Dumitriu", "an": 3},
]

grupe = {
    "1A1": {"an": 1, "semian": "A", "numar_grupa": 1},
    "1B1": {"an": 1, "semian": "B", "numar_grupa": 1},
    "1E1": {"an": 1, "semian": "E", "numar_grupa": 1},
    "2A1": {"an": 2, "semian": "A", "numar_grupa": 1},
    "2B1": {"an": 2, "semian": "B", "numar_grupa": 1},
    "2E1": {"an": 2, "semian": "E", "numar_grupa": 1},
    "3A1": {"an": 3, "semian": "A", "numar_grupa": 1},
    "3B1": {"an": 3, "semian": "B", "numar_grupa": 1},
    "3E1": {"an": 3, "semian": "E", "numar_grupa": 1},
}

sali = {
    "C2": {"capacitate": 3,},
    "C102": {"capacitate": 3},
}

for i in range(301, 306):
    sali[f"C{i}"] = {"capacitate": 1}

def save_to_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

save_to_json("data/profesori", profesori)
save_to_json("data/activitati", activitati)
save_to_json("data/sali", sali)
save_to_json("data/grupe", grupe)