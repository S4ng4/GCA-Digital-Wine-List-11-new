#!/usr/bin/env python3
"""
Script per estrarre tutti i produttori unici dal file wines.json
e creare un file di testo con la lista
"""

import json
from collections import Counter

def main():
    # Leggi il file wines.json
    try:
        with open('data/wines.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Errore: file data/wines.json non trovato")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Errore nel parsing del JSON: {e}")
        return

    # Estrai tutti i produttori (escludendo UNKNOWN PRODUCER e valori vuoti)
    producers = []
    for wine in data.get('wines', []):
        producer = wine.get('wine_producer', '').strip()
        if producer and producer != 'UNKNOWN PRODUCER' and producer:
            producers.append(producer)

    # Conta i vini per produttore
    producer_counts = Counter(producers)

    # Crea lista unica e ordinata alfabeticamente (case-insensitive)
    unique_producers = sorted(set(producers), key=lambda x: x.lower())

    # Scrivi il file di testo
    output_file = 'produttori_lista.txt'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("LISTA PRODUTTORI - GRAN CAFFÈ L'AQUILA\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Totale produttori unici: {len(unique_producers)}\n")
            f.write(f"Totale vini: {sum(producer_counts.values())}\n\n")
            f.write("-" * 60 + "\n\n")
            
            # Scrivi ogni produttore con il numero di vini
            f.write("Lista con conteggio vini:\n")
            f.write("-" * 60 + "\n\n")
            for producer in unique_producers:
                count = producer_counts[producer]
                f.write(f"{producer} ({count} vino{'i' if count > 1 else ''})\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("Lista semplice (solo nomi):\n")
            f.write("=" * 60 + "\n\n")
            for producer in unique_producers:
                f.write(f"{producer}\n")
        
        print(f"✅ File creato: {output_file}")
        print(f"📊 Totale produttori unici: {len(unique_producers)}")
        print(f"🍷 Totale vini: {sum(producer_counts.values())}")
        
    except IOError as e:
        print(f"❌ Errore nella scrittura del file: {e}")

if __name__ == '__main__':
    main()
