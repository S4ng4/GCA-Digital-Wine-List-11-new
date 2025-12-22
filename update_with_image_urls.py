#!/usr/bin/env python3
"""
Script per aggiornare gca_wine_link.json con URL di immagini diretti
Inserisci gli URL delle immagini nel dizionario wine_image_urls
"""

import json
import requests

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

# DIZIONARIO: Inserisci qui gli URL diretti delle immagini
# Formato: "NOME VINO": "URL_IMMAGINE"
wine_image_urls = {
    # EMIDIO PEPE - MONTEPULCIANO
    "MONTEPULCIANO, EMIDIO PEPE": "https://www.emidiopepe.com/wp-content/uploads/2021/04/cantina_emidiopepe_bottiglia1.jpg",
    
    # VERNACCIA TERRE TUFI, TERUZZI
    "VERNACCIA TERRE TUFI, TERUZZI": "https://pbi.nyc3.digitaloceanspaces.com/images/terre-di-tufi-toscana-bianco-igt-750ml-image_.height-650.png",
    
    # NEBBIOLO ROSY, PIO CESARE
    "NEBBIOLO ROSY, PIO CESARE": "https://www.mmdltd.com/wordpress-site/wp-content/uploads/2022/03/rosy-langhe-doc-314x1024-1-306x998.png",
    
    # PISA VERMENTINO COLOMBANA
    "PISA VERMENTINO COLOMBANA": "https://i0.wp.com/www.villasofiawine.com/wp-content/uploads/2023/08/colombana-bio.jpg?w=700&ssl=1",
    
    # PASSERINA, IL CONTE
    "PASSERINA, IL CONTE": "https://www.vinello.co.uk/media/image/43/a8/59/il-conte-ceppo-marche-passerina-igp-il-conte-villa-prandone_200x200.webp",
    
    # ANSONICA, CECILIA
    "ANSONICA, CECILIA": "https://www.vinicecilia.it/wp-content/uploads/2018/05/elba-ansonica-03.jpg",
}

def main():
    print("=" * 80)
    print("AGGIORNAMENTO JSON CON URL IMMAGINI")
    print("=" * 80)
    print()
    
    if not wine_image_urls:
        print("⚠️  Nessun URL immagine fornito!")
        print("   Aggiungi gli URL nel dizionario wine_image_urls nello script")
        return
    
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
    
    print(f"Trovati {len(wine_image_urls)} vini con URL immagini\n")
    print("-" * 80)
    
    updated_count = 0
    verified_count = 0
    not_found_count = 0
    
    for wine_name, image_url in wine_image_urls.items():
        print(f"\n📝 {wine_name}")
        print(f"   URL: {image_url}")
        
        # Verifica l'URL
        if verify_image_url(image_url):
            print(f"   ✅ URL verificato")
            verified_count += 1
        else:
            print(f"   ⚠️  URL non verificato (procedo comunque)")
        
        # Aggiorna il JSON
        if update_wine_image_in_json(gca_data, wine_name, image_url):
            print(f"   ✅ Aggiornato nel JSON")
            updated_count += 1
        else:
            print(f"   ❌ Vino non trovato nel JSON")
            not_found_count += 1
    
    # Salva il file JSON aggiornato
    if updated_count > 0:
        with open('data/gca_wine_link.json', 'w', encoding='utf-8') as f:
            json.dump(gca_data, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 80)
        print("✅ File gca_wine_link.json aggiornato!")
    
    print("\n" + "=" * 80)
    print("RIEPILOGO")
    print("=" * 80)
    print(f"Totale vini: {len(wine_image_urls)}")
    print(f"✅ Vini aggiornati: {updated_count}")
    print(f"✅ URL verificati: {verified_count}")
    print(f"❌ Vini non trovati: {not_found_count}")

if __name__ == '__main__':
    main()

