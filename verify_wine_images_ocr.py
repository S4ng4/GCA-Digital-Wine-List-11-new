#!/usr/bin/env python3
"""
Script per verificare che le immagini dei vini corrispondano ai vini nel JSON
utilizzando OCR per estrarre il testo dalle immagini e confrontarlo con i dati del vino.
"""

import json
import requests
import re
import time
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher
import easyocr
from PIL import Image
import io

# Inizializza EasyOCR reader (supporta italiano e inglese)
print("Inizializzazione EasyOCR...")
init_start = time.time()
reader = easyocr.Reader(['en', 'it'], gpu=False)
init_time = time.time() - init_start
print(f"✅ EasyOCR inizializzato in {init_time:.1f} secondi\n")

def download_image(url: str, timeout: int = 10) -> Optional[Image.Image]:
    """Scarica un'immagine da un URL e la restituisce come PIL Image"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=timeout, headers=headers, stream=True)
        response.raise_for_status()
        
        # Verifica che sia un'immagine
        content_type = response.headers.get('Content-Type', '')
        if 'image' not in content_type.lower():
            return None
        
        # Carica l'immagine
        image = Image.open(io.BytesIO(response.content))
        return image
    except Exception as e:
        print(f"   ⚠️  Errore download: {str(e)}")
        return None

def extract_text_with_ocr(image: Image.Image) -> str:
    """Estrae testo da un'immagine usando OCR"""
    try:
        # Converti PIL Image a numpy array per EasyOCR
        import numpy as np
        img_array = np.array(image)
        
        # Esegui OCR
        results = reader.readtext(img_array)
        
        # Combina tutto il testo estratto
        extracted_text = ' '.join([result[1] for result in results])
        return extracted_text.upper()
    except Exception as e:
        print(f"   ⚠️  Errore OCR: {str(e)}")
        return ""

def normalize_text(text: str) -> str:
    """Normalizza il testo per il confronto (rimuove caratteri speciali, spazi extra, etc.)"""
    if not text:
        return ""
    # Converti in maiuscolo
    text = text.upper()
    # Rimuovi caratteri speciali comuni
    text = re.sub(r'[^\w\s]', ' ', text)
    # Rimuovi spazi multipli
    text = re.sub(r'\s+', ' ', text)
    # Rimuovi spazi iniziali/finali
    return text.strip()

def extract_keywords(text: str) -> List[str]:
    """Estrae parole chiave significative dal testo (rimuove parole comuni)"""
    # Parole comuni da ignorare
    stop_words = {'THE', 'A', 'AN', 'AND', 'OR', 'BUT', 'IN', 'ON', 'AT', 'TO', 'FOR', 
                  'OF', 'WITH', 'BY', 'FROM', 'AS', 'IS', 'WAS', 'ARE', 'WERE', 'BE',
                  'BEEN', 'BEING', 'HAVE', 'HAS', 'HAD', 'DO', 'DOES', 'DID', 'WILL',
                  'WOULD', 'SHOULD', 'COULD', 'MAY', 'MIGHT', 'MUST', 'CAN', 'THIS',
                  'THAT', 'THESE', 'THOSE', 'I', 'YOU', 'HE', 'SHE', 'IT', 'WE', 'THEY',
                  'DOC', 'IGT', 'DOP', 'IGP', 'VINO', 'WINE', 'VIN', 'VINI', 'VINE',
                  'BOTTLE', 'BOTTIGLIA', 'ML', 'CL', 'L', '750', '500', '375'}
    
    words = normalize_text(text).split()
    keywords = [w for w in words if len(w) > 2 and w not in stop_words]
    return keywords

def similarity_score(text1: str, text2: str) -> float:
    """Calcola un punteggio di similarità tra due testi (0-1)"""
    if not text1 or not text2:
        return 0.0
    
    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)
    
    if not norm1 or not norm2:
        return 0.0
    
    # Calcola similarità usando SequenceMatcher
    similarity = SequenceMatcher(None, norm1, norm2).ratio()
    
    # Bonus se una stringa contiene l'altra
    if norm1 in norm2 or norm2 in norm1:
        similarity = max(similarity, 0.8)
    
    return similarity

def check_keywords_match(keywords1: List[str], keywords2: List[str], threshold: int = 2) -> bool:
    """Verifica se ci sono abbastanza parole chiave in comune"""
    if not keywords1 or not keywords2:
        return False
    
    common = set(keywords1) & set(keywords2)
    return len(common) >= threshold

def verify_wine_image(wine: Dict, image_url: str) -> Dict:
    """
    Verifica che l'immagine corrisponda al vino.
    Restituisce un dizionario con i risultati della verifica.
    """
    wine_number = wine.get('wine_number', 'N/A')
    wine_name = wine.get('wine_name', '')
    wine_producer = wine.get('wine_producer', '')
    
    result = {
        'wine_number': wine_number,
        'wine_name': wine_name,
        'wine_producer': wine_producer,
        'image_url': image_url,
        'image_downloaded': False,
        'ocr_successful': False,
        'extracted_text': '',
        'producer_match': False,
        'wine_name_match': False,
        'overall_match': False,
        'producer_similarity': 0.0,
        'wine_name_similarity': 0.0,
        'error': None
    }
    
    # 1. Scarica l'immagine
    print(f"   📥 Download immagine...")
    image = download_image(image_url)
    if not image:
        result['error'] = 'Impossibile scaricare immagine'
        return result
    
    result['image_downloaded'] = True
    
    # 2. Esegui OCR
    print(f"   🔍 Esecuzione OCR...")
    extracted_text = extract_text_with_ocr(image)
    if not extracted_text:
        result['error'] = 'OCR non ha estratto testo'
        return result
    
    result['ocr_successful'] = True
    result['extracted_text'] = extracted_text[:200]  # Limita per il report
    
    # 3. Normalizza i testi per il confronto
    normalized_producer = normalize_text(wine_producer)
    normalized_wine_name = normalize_text(wine_name)
    normalized_extracted = normalize_text(extracted_text)
    
    # 4. Estrai parole chiave
    producer_keywords = extract_keywords(normalized_producer)
    wine_name_keywords = extract_keywords(normalized_wine_name)
    extracted_keywords = extract_keywords(normalized_extracted)
    
    # 5. Verifica match del produttore
    producer_similarity = similarity_score(normalized_producer, normalized_extracted)
    producer_keyword_match = check_keywords_match(producer_keywords, extracted_keywords, threshold=1)
    
    result['producer_similarity'] = producer_similarity
    result['producer_match'] = producer_similarity >= 0.6 or producer_keyword_match
    
    # 6. Verifica match del nome vino
    wine_name_similarity = similarity_score(normalized_wine_name, normalized_extracted)
    wine_name_keyword_match = check_keywords_match(wine_name_keywords, extracted_keywords, threshold=1)
    
    result['wine_name_similarity'] = wine_name_similarity
    result['wine_name_match'] = wine_name_similarity >= 0.6 or wine_name_keyword_match
    
    # 7. Match complessivo: entrambi devono corrispondere
    result['overall_match'] = result['producer_match'] and result['wine_name_match']
    
    return result

def estimate_time(num_wines: int, sample_time: float = None) -> Dict:
    """Stima il tempo necessario per processare tutti i vini"""
    if sample_time:
        # Stima basata su campione reale
        time_per_wine = sample_time
    else:
        # Stima conservativa basata su tempi tipici
        # Download: 2s, OCR: 4s, processing: 1s = ~7s per vino
        time_per_wine = 7.0
    
    total_seconds = init_time + (num_wines * time_per_wine)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    
    return {
        'total_seconds': total_seconds,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'time_per_wine': time_per_wine
    }

def main():
    print("=" * 80)
    print("VERIFICA IMMAGINI VINI CON OCR")
    print("=" * 80)
    print()
    
    # Controlla argomenti da linea di comando
    test_mode = '--test' in sys.argv or '-t' in sys.argv
    sample_size = 10  # Default per test mode
    
    # Carica wines.json
    try:
        with open('data/wines.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        wines = data.get('wines', [])
        print(f"✅ Caricati {len(wines)} vini dal file wines.json\n")
    except FileNotFoundError:
        print("❌ File wines.json non trovato!")
        return
    except Exception as e:
        print(f"❌ Errore nel caricamento del file: {str(e)}")
        return
    
    # Filtra vini con immagini
    wines_with_images = [w for w in wines if w.get('bottle_image_url')]
    total_wines = len(wines_with_images)
    print(f"📊 Vini con immagini: {total_wines}\n")
    
    if not wines_with_images:
        print("⚠️  Nessun vino con immagine trovato!")
        return
    
    # Stima tempo
    if not test_mode:
        estimate = estimate_time(total_wines)
        print("⏱️  STIMA TEMPO:")
        print(f"   Tempo stimato: {estimate['hours']}h {estimate['minutes']}m {estimate['seconds']}s")
        print(f"   (~{estimate['time_per_wine']:.1f} secondi per vino)")
        print()
        
        response = input("Vuoi procedere? (s/n) o usa --test per testare solo 10 vini: ").strip().lower()
        if response not in ['s', 'si', 'y', 'yes', '']:
            print("Operazione annullata.")
            return
    else:
        wines_with_images = wines_with_images[:sample_size]
        print(f"🧪 MODALITÀ TEST: processerò solo {len(wines_with_images)} vini\n")
    
    print("-" * 80)
    
    # Avvia verifica
    start_time = time.time()
    results = []
    verified_count = 0
    mismatch_count = 0
    error_count = 0
    sample_times = []
    
    for i, wine in enumerate(wines_with_images, 1):
        wine_start = time.time()
        wine_number = wine.get('wine_number', 'N/A')
        wine_name = wine.get('wine_name', '')
        wine_producer = wine.get('wine_producer', '')
        image_url = wine.get('bottle_image_url', '')
        
        print(f"\n[{i}/{len(wines_with_images)}] Vino #{wine_number}")
        print(f"   Nome: {wine_name}")
        print(f"   Produttore: {wine_producer}")
        print(f"   URL: {image_url[:60]}...")
        
        result = verify_wine_image(wine, image_url)
        results.append(result)
        
        wine_time = time.time() - wine_start
        sample_times.append(wine_time)
        
        # Calcola tempo rimanente
        if i > 0:
            avg_time = sum(sample_times) / len(sample_times)
            remaining = (len(wines_with_images) - i) * avg_time
            remaining_min = int(remaining // 60)
            remaining_sec = int(remaining % 60)
            print(f"   ⏱️  Tempo: {wine_time:.1f}s | Rimanente: ~{remaining_min}m {remaining_sec}s")
        
        if result['error']:
            print(f"   ❌ Errore: {result['error']}")
            error_count += 1
        elif result['overall_match']:
            print(f"   ✅ IMMAGINE CORRETTA")
            print(f"      Produttore: {result['producer_similarity']:.2%} | Nome: {result['wine_name_similarity']:.2%}")
            verified_count += 1
        else:
            print(f"   ⚠️  IMMAGINE NON CORRISPONDENTE")
            print(f"      Produttore: {result['producer_similarity']:.2%} | Nome: {result['wine_name_similarity']:.2%}")
            if result['extracted_text']:
                print(f"      Testo estratto: {result['extracted_text'][:100]}...")
            mismatch_count += 1
    
    total_time = time.time() - start_time
    
    # Verifica ogni vino
    results = []
    verified_count = 0
    mismatch_count = 0
    error_count = 0
    
    for i, wine in enumerate(wines_with_images, 1):
        wine_number = wine.get('wine_number', 'N/A')
        wine_name = wine.get('wine_name', '')
        wine_producer = wine.get('wine_producer', '')
        image_url = wine.get('bottle_image_url', '')
        
        print(f"\n[{i}/{len(wines_with_images)}] Vino #{wine_number}")
        print(f"   Nome: {wine_name}")
        print(f"   Produttore: {wine_producer}")
        print(f"   URL: {image_url[:60]}...")
        
        result = verify_wine_image(wine, image_url)
        results.append(result)
        
        if result['error']:
            print(f"   ❌ Errore: {result['error']}")
            error_count += 1
        elif result['overall_match']:
            print(f"   ✅ IMMAGINE CORRETTA")
            print(f"      Produttore: {result['producer_similarity']:.2%} | Nome: {result['wine_name_similarity']:.2%}")
            verified_count += 1
        else:
            print(f"   ⚠️  IMMAGINE NON CORRISPONDENTE")
            print(f"      Produttore: {result['producer_similarity']:.2%} | Nome: {result['wine_name_similarity']:.2%}")
            if result['extracted_text']:
                print(f"      Testo estratto: {result['extracted_text'][:100]}...")
            mismatch_count += 1
    
    # Genera report
    print("\n" + "=" * 80)
    print("RIEPILOGO")
    print("=" * 80)
    print(f"Totale vini verificati: {len(wines_with_images)}")
    print(f"✅ Immagini corrette: {verified_count}")
    print(f"⚠️  Immagini non corrispondenti: {mismatch_count}")
    print(f"❌ Errori: {error_count}")
    print(f"\n⏱️  Tempo totale: {int(total_time // 60)}m {int(total_time % 60)}s")
    if len(sample_times) > 0:
        avg_time = sum(sample_times) / len(sample_times)
        print(f"   Tempo medio per vino: {avg_time:.1f}s")
        if test_mode and total_wines > len(wines_with_images):
            remaining_wines = total_wines - len(wines_with_images)
            estimated_remaining = remaining_wines * avg_time
            print(f"\n📊 Stima per tutti i {total_wines} vini:")
            print(f"   Tempo totale stimato: {int((total_time + estimated_remaining) // 60)}m {int((total_time + estimated_remaining) % 60)}s")
    print()
    
    # Salva report dettagliato
    report_file = 'WINE_IMAGE_VERIFICATION_REPORT.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total': len(wines_with_images),
                'verified': verified_count,
                'mismatch': mismatch_count,
                'errors': error_count
            },
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Report dettagliato salvato in: {report_file}")
    
    # Mostra vini con problemi
    if mismatch_count > 0 or error_count > 0:
        print("\n" + "=" * 80)
        print("VINI CON PROBLEMI")
        print("=" * 80)
        
        for result in results:
            if result['error']:
                print(f"\n❌ Vino #{result['wine_number']}: {result['wine_name']} - {result['wine_producer']}")
                print(f"   Errore: {result['error']}")
            elif not result['overall_match']:
                print(f"\n⚠️  Vino #{result['wine_number']}: {result['wine_name']} - {result['wine_producer']}")
                print(f"   Produttore match: {result['producer_match']} ({result['producer_similarity']:.2%})")
                print(f"   Nome match: {result['wine_name_match']} ({result['wine_name_similarity']:.2%})")
                if result['extracted_text']:
                    print(f"   Testo estratto: {result['extracted_text'][:150]}...")

if __name__ == '__main__':
    main()

