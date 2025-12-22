#!/usr/bin/env python3
"""
Script per aggiornare gca_wine_link.json con i link trovati
"""

import json
import re
import requests
from urllib.parse import quote

def verify_image_url(url):
    """Verifica se un URL di immagine è valido"""
    if not url:
        return False
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.head(url, timeout=5, allow_redirects=True, headers=headers)
        content_type = response.headers.get('Content-Type', '')
        is_image = response.status_code == 200 and (
            'image' in content_type.lower() or 
            url.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))
        )
        return is_image
    except:
        return False

def find_wine_in_json(data, wine_name):
    """Trova il vino nel JSON e restituisce la sua posizione"""
    # Cerca in White
    if 'White' in data:
        for i, item in enumerate(data['White']):
            for key, value in item.items():
                if key.startswith('http'):
                    continue
                if isinstance(value, str) and value.strip() == wine_name.strip():
                    return ('White', i, item)
    
    # Cerca in Red
    if 'Red' in data:
        for i, item in enumerate(data['Red']):
            wine_name_in_item = None
            image_url_key = None
            
            for key, value in item.items():
                if key == 'Link Image':
                    image_url_key = key
                elif key == 'null':
                    if value and isinstance(value, str) and not value.startswith('http'):
                        wine_name_in_item = value
            
            if wine_name_in_item and wine_name_in_item.strip() == wine_name.strip():
                return ('Red', i, item, image_url_key)
    
    return None

def update_wine_image_in_json(data, wine_name, new_image_url):
    """Aggiorna l'URL dell'immagine per un vino nel JSON"""
    wine_location = find_wine_in_json(data, wine_name)
    
    if not wine_location:
        return False
    
    if len(wine_location) == 3:
        category, index, item = wine_location
        # Trova la chiave URL placeholder e aggiorna il valore
        for key in item.keys():
            if key.startswith('http'):
                item[key] = new_image_url
                data[category][index] = item
                return True
    elif len(wine_location) == 4:
        category, index, item, image_key = wine_location
        if image_key:
            item[image_key] = new_image_url
            data[category][index] = item
            return True
        else:
            # Cerca una chiave URL
            for key in item.keys():
                if key.startswith('http'):
                    item[key] = new_image_url
                    data[category][index] = item
                    return True
    
    return False

# Mapping dei vini con i link trovati
wine_links = {
    "AMARONE, LA BASTIA": "https://www.wineconnection.com.sg/products/ca-de-rocchi-la-bastia-amarone-della-valpolicella-veneto-italy",
    "INZOILIO BIANCO, COLOSI": "https://www.bottleshop.com/products/14249261/colosi-salina-bianco-2024",
    "VILLA ANTINORI BIANCO, VILLA ANTINORI": "https://www.antinori.it/en/vino/villa-antinori-bianco-en/",
    "TREBBIANO, CATALDI MADONNA": "https://cataldimadonna.com/product/trebbiano-d-abruzzo/",
    "PASSERINA, IL CONTE": "https://www.vinello.co.uk/ceppo-marche-passerina-igp-il-conte-villa-prandone",
    "PISA VERMENTINO COLOMBANA": "https://www.villasofiawine.com/product/colombana-igt-terre-di-pisa-hills/",
    "VERNACCIA TERRE TUFI, TERUZZI": "https://www.palmbay.com/wines/teruzzi/teruzzi-terre-di-tufi-toscana-bianco-igt/",
    "VINO NOBILE, POLIZIANO": "https://www.wine.com/product/poliziano-vino-nobile-di-montepulciano-2021/2028495",
    "BAROLO, TERREDDAVINO": "https://www.saq.com/en/15192279",
    "BRUNELLO , SANT'ANTIMO": "https://www.wine.com/product/molino-di-santantimo-brunello-di-montalcino-2016/973625",
    "MONTEPULCIANO, EMIDIO PEPE": "https://www.emidiopepe.com/en/",
    "SANGIOVESE, SANTA CRISTINA": "http://www.santacristina.wine/en/product/vermentino-bottle/",
    "FRANCIACORTA ANNAMARIA CLEMENTI, CA' DEL BOSCO": "https://www.cadelbosco.com/en/wine-categories/franciacorta-wines/annamaria-clementi/",
    "AMARONE, TOMASSI": "https://shop.allamarone.com/wine/amarone-docg-classico-tommasi/",
    "AMARONE, SPERI": "https://www.speri.com/en/wines/amarone/",
    "AMARONE, BUGLIONI": "https://buglioni.it/en/shop/amarone-riserva-testedure/",
    "AMARONE, ALLEGRINI": "https://allegrini.it/en/wines/amarone-della-valpolicella-classico-allegrini/",
    "AMARONE, BERTANI": "https://www.bertani.net/wines/tradition/amarone-della-valpolicella-classico/",
    "VALPOLICELLA SUPERIORE, DAL FORNO": "https://bottleofitaly.com/en-us/products/amarone-della-valpolicella-docg-dal-forno-romano",
    "AMARONE, DAL FORNO*": "https://bottleofitaly.com/en-us/products/amarone-della-valpolicella-docg-dal-forno-romano"
}

def extract_image_from_page(url):
    """Cerca di estrarre URL di immagine da una pagina web"""
    # Pattern comuni per URL di immagini su vari siti
    # Per ora restituiamo None, l'utente dovrà inserire manualmente gli URL delle immagini
    return None

def main():
    print("=" * 80)
    print("AGGIORNAMENTO JSON CON LINK TROVATI")
    print("=" * 80)
    print()
    
    # Carica il file JSON principale
    try:
        with open('data/gca_wine_link.json', 'r', encoding='utf-8') as f:
            gca_data = json.load(f)
    except FileNotFoundError:
        print("❌ File gca_wine_link.json non trovato!")
        return
    
    # Crea backup
    backup_file = 'data/gca_wine_link.json.backup'
    try:
        with open('data/gca_wine_link.json', 'r', encoding='utf-8') as f:
            backup_data = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(backup_data)
        print(f"💾 Backup creato: {backup_file}\n")
    except:
        pass
    
    print(f"Trovati {len(wine_links)} vini con link\n")
    print("-" * 80)
    
    updated_count = 0
    not_found_count = 0
    needs_image_url = []
    
    for wine_name, page_url in wine_links.items():
        print(f"\n📝 {wine_name}")
        print(f"   Link pagina: {page_url}")
        
        # Verifica se il vino esiste nel JSON
        wine_location = find_wine_in_json(gca_data, wine_name)
        if not wine_location:
            print(f"   ⚠️  Vino non trovato nel JSON")
            not_found_count += 1
            continue
        
        # Per ora, non possiamo estrarre automaticamente l'URL dell'immagine
        # Dobbiamo cercare l'immagine sulla pagina o usare pattern noti
        print(f"   💡 Link pagina salvato, ma serve l'URL diretto dell'immagine")
        print(f"   📋 Visita il link e copia l'URL dell'immagine del vino")
        
        needs_image_url.append({
            'wine_name': wine_name,
            'page_url': page_url,
            'image_url': None
        })
    
    # Salva i link trovati per riferimento
    with open('data/found_wine_links.json', 'w', encoding='utf-8') as f:
        json.dump(needs_image_url, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("RIEPILOGO")
    print("=" * 80)
    print(f"Vini processati: {len(wine_links)}")
    print(f"Vini trovati nel JSON: {len(wine_links) - not_found_count}")
    print(f"Vini non trovati: {not_found_count}")
    print(f"\n📋 Link salvati in: data/found_wine_links.json")
    print(f"\n💡 PROSSIMI PASSI:")
    print(f"   1. Visita ogni link in data/found_wine_links.json")
    print(f"   2. Trova l'immagine del vino sulla pagina")
    print(f"   3. Copia l'URL diretto dell'immagine (clic destro → 'Copia indirizzo immagine')")
    print(f"   4. Aggiorna il campo 'image_url' in data/found_wine_links.json")
    print(f"   5. Esegui: python3 apply_found_images.py")

if __name__ == '__main__':
    main()

