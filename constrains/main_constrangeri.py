from input_constrangeri_fisier import citeste_constrangeri, citeste_fisier_json, clasifica_constrangeri, aplica_constrangeri


fisier_constrangeri = '/Users/diandrafechita/AI-PROJECT-TIMETABLE/constrains/constrangeri.json'
constrangeri = citeste_fisier_json(fisier_constrangeri)
hard, soft = clasifica_constrangeri(constrangeri)

zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri"]
intervale = ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]

for zi in zile:
    print(f"\n=== Verificări pentru ziua {zi} ===")
    for interval in intervale:
        profesor = "Prof. Popescu"
        sala = "Sala X"
        disponibil, mesaje = aplica_constrangeri(hard, soft, zi, interval, profesor, sala)

        if disponibil:
            print(f"[DISPONIBIL] Interval {interval} este disponibil pentru {profesor} în sala {sala} pe {zi}.")
            if mesaje:
                print("  Avertismente:")
                for mesaj in mesaje:
                    print(f"    - {mesaj}")
        else:
            print(f"[INDISPONIBIL] Interval {interval} NU este disponibil pentru {profesor} în sala {sala} pe {zi}:")
            for mesaj in mesaje:
                print(f"  - {mesaj}")

    print(f"=== Sfârșit verificări pentru {zi} ===")
