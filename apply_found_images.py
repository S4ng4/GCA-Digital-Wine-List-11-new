#!/usr/bin/env python3
"""
Script per applicare gli URL delle immagini trovati al file JSON
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

def main():
    print("=" * 80)
    print("APPLICA IMMAGINI TROVATE AL JSON")
    print("=" * 80)
    print()
    
    # Carica il file con i link trovati
    try:
        with open('data/found_wine_links.json', 'r', encoding='utf-8') as f:
            found_links = json.load(f)
    except FileNotFoundError:
        print("❌ File found_wine_links.json non trovato!")
        print("   Esegui prima: python3 update_wines_with_found_links.py")
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
    
    print(f"Trovati {len(found_links)} vini con link\n")
    print("-" * 80)
    
    updated_count = 0
    verified_count = 0
    not_found_count = 0
    missing_image_url = 0
    
    for wine_data in found_links:
        wine_name = wine_data.get('wine_name', '')
        image_url = wine_data.get('image_url')
        page_url = wine_data.get('page_url', '')
        
        print(f"\n📝 {wine_name}")
        
        if not image_url:
            print(f"   ⚠️  URL immagine mancante")
            print(f"   💡 Visita: {page_url}")
            print(f"   📋 Copia l'URL dell'immagine e aggiorna found_wine_links.json")
            missing_image_url += 1
            continue
        
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
    print(f"Totale vini: {len(found_links)}")
    print(f"✅ Vini aggiornati: {updated_count}")
    print(f"✅ URL verificati: {verified_count}")
    print(f"⚠️  URL immagine mancanti: {missing_image_url}")
    print(f"❌ Vini non trovati: {not_found_count}")

if __name__ == '__main__':
    main()

