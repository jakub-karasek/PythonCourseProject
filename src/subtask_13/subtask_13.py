import os
import random
import copy
import xml.etree.ElementTree as ET
from pathlib import Path

# filepath: /home/students/inf/j/jk459158/ROK2/KursPython/Projekt/subtask_13/subtask_13.py

# Pomocnicza funkcja wydobywająca przestrzeń nazw z korzenia dokumentu XML
def get_namespace(root):
    if root.tag.startswith("{"):
        return root.tag.split("}")[0].strip("{")
    return ""

# Pomocnicza funkcja usuwająca przestrzeń nazw z tagu
def strip_ns(tag):
    return tag.split("}")[-1] if "}" in tag else tag

# Budowanie puli elementów (drug pools) na podstawie podanych leków.
# Dla każdego elementu <drug> (poziom drugi) tworzymy pulę elementów z głównego XML.
def build_pools(drugs):
    pools = {}
    # Przetwarzamy tylko pierwsze 100 leków, by zebrać wartości
    for drug in drugs[:100]:
        for child in drug:
            tag = strip_ns(child.tag)
            # Pominięcie identyfikatora, gdyż będzie generowany nowo
            if tag == "drugbank-id":
                continue
            pools.setdefault(tag, []).append(copy.deepcopy(child))
    return pools

# Tworzy nowy element leku, kopiując losowo wybrane elementy z puli.
def create_new_drug(new_id, pools, ns_uri, original_attribs):
    # Utworzenie elementu <drug> z przestrzenią nazw
    drug_elem = ET.Element(f"{{{ns_uri}}}drug")
    # Ustawienie losowo wybranych atrybutów (jeśli oryginalne leki posiadały atrybuty, kopiujemy je losowo)
    for attr, value in original_attribs.items():
        drug_elem.set(attr, value)
    # Dodajemy nowy <drugbank-id> z sekwencyjnym numerem
    drugbank_id = ET.SubElement(drug_elem, f"{{{ns_uri}}}drugbank-id")
    drugbank_id.text = f"DB{new_id:05d}"
    drugbank_id.set("primary", "true")
    # Dla każdej puli (pozostałe elementy) losujemy jeden egzemplarz oraz kopiujemy go (deepcopy)
    for tag, elements in pools.items():
        source_elem = random.choice(elements)
        new_elem = copy.deepcopy(source_elem)
        drug_elem.append(new_elem)
    return drug_elem

def main():
    # Ścieżki wejścia i wyjścia
    input_file = "../drugbank_partial.xml"
    output_file = "../drugbank_partial_and_generated.xml"

    # Parsowanie oryginalnego pliku XML
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Ustalenie przestrzeni nazw (np. "http://www.drugbank.ca")
    ns_uri = get_namespace(root)
    ns = {"db": ns_uri}

    # Znalezienie wszystkich elementów leków
    drugs = root.findall("db:drug", ns)
    original_drug_count = len(drugs)
    print(f"Oryginalna liczba leków: {original_drug_count}")

    # Budowanie puli z pierwszych 100 leków (dla pozostałych pól)
    if len(drugs) < 100:
        print("UWAGA: Brak 100 oryginalnych leków w pliku – pula zostanie zbudowana z dostępnych leków.")
    pools = build_pools(drugs)

    # Ustalenie najwyższego istniejącego DrugBank ID
    max_id = 0
    for drug in drugs:
        drug_id_elem = drug.find("db:drugbank-id", ns)
        if drug_id_elem is not None and drug_id_elem.text:
            try:
                num = int(drug_id_elem.text.strip().lstrip("DB"))
                if num > max_id:
                    max_id = num
            except ValueError:
                continue

    # Nowa łączna liczba leków ma wynosić 20000
    total_drugs = 200
    new_drug_count = total_drugs - original_drug_count
    print(f"Generowanie {new_drug_count} nowych leków...")

    # Utworzenie puli atrybutów - zbieramy wszystkie atrybuty z oryginalnych leków (z pierwszego leku)
    original_attribs = {}
    if drugs:
        original_attribs = drugs[0].attrib

    # Generowanie nowych leków z kolejnymi numerami DrugBank ID
    new_drugs = []
    next_id = max_id + 1
    for i in range(new_drug_count):
        new_drug = create_new_drug(next_id, pools, ns_uri, original_attribs)
        new_drugs.append(new_drug)
        next_id += 1

    # Dodanie nowych leków do drzewa XML – zachowujemy oryginalne leki
    for nd in new_drugs:
        root.append(nd)

    # Zapisz wynik do pliku wyjściowego
    ET.register_namespace('', ns_uri)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Zapisano rozszerzony plik XML (20000 leków) do: {output_file}")

if __name__ == "__main__":
    main()