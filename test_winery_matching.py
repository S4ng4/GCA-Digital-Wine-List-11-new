#!/usr/bin/env python3
"""
Script per testare il matching tra i produttori nei vini e le cantine nel database
"""

import json
import re

def normalize_name(name):
    """Normalizza il nome per il matching (come in wineries.js)"""
    if not name:
        return ''
    return name.upper().strip().replace('*', '').replace('(', '').replace(')', '').strip()

def load_wineries_from_js(js_file):
    """Carica le cantine dal file JavaScript"""
    wineries = {}
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Estrai le cantine dal formato JavaScript
    # Pattern: 'NOME': { ... }
    pattern = r"'([^']+)':\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}"
    matches = re.finditer(pattern, content)
    
    for match in matches:
        key = match.group(1)
        winery_content = match.group(2)
        
        winery = {}
        # Estrai i campi
        for field in ['name', 'region', 'location', 'year', 'history', 'philosophy', 
                     'hectares', 'grapes', 'mainWines', 'notes', 'aliases']:
            field_pattern = rf"{field}:\s*'([^']*)'"
            field_match = re.search(field_pattern, winery_content)
            if field_match:
                winery[field] = field_match.group(1)
        
        # Gestisci aliases (array)
        aliases_pattern = r"aliases:\s*\[([^\]]+)\]"
        aliases_match = re.search(aliases_pattern, winery_content)
        if aliases_match:
            aliases_str = aliases_match.group(1)
            aliases = [a.strip().strip("'\"") for a in aliases_str.split(',')]
            winery['aliases'] = aliases
        
        wineries[normalize_name(key)] = winery
    
    return wineries

def find_winery_match(producer_name, wineries):
    """Trova un match per il produttore nelle cantine"""
    normalized = normalize_name(producer_name)
    
    # Direct match
    if normalized in wineries:
        return normalized, wineries[normalized]
    
    # Partial matching
    for key, winery in wineries.items():
        # Check if producer name contains winery name or vice versa
        if normalized in key or key in normalized:
            return key, winery
        
        # Check aliases
        if winery.get('aliases'):
            for alias in winery['aliases']:
                alias_norm = normalize_name(alias)
                if normalized in alias_norm or alias_norm in normalized:
                    return key, winery
        
        # Word-based matching
        producer_words = [w for w in normalized.split() if len(w) > 2]
        key_words = [w for w in key.split() if len(w) > 2]
        
        if producer_words and key_words:
            matching = [pw for pw in producer_words if any(kw in pw or pw in kw for kw in key_words)]
            if matching and len(matching) >= min(len(producer_words), 2):
                return key, winery
    
    return None, None

def main():
    # Carica vini
    print("📖 Caricando vini...")
    with open('data/wines.json', 'r', encoding='utf-8') as f:
        wines_data = json.load(f)
    
    wines = wines_data.get('wines', [])
    print(f"✅ Caricati {len(wines)} vini")
    
    # Carica cantine
    print("\n📖 Caricando cantine...")
    wineries = load_wineries_from_js('js/wineries.js')
    print(f"✅ Caricate {len(wineries)} cantine")
    
    # Test matching
    print("\n🔍 Testando matching...")
    matches = {}
    no_matches = []
    
    producers = {}
    for wine in wines:
        producer = wine.get('wine_producer', '').strip()
        if producer:
            normalized = normalize_name(producer)
            if normalized not in producers:
                producers[normalized] = producer
    
    print(f"\n📊 Produttori unici nei vini: {len(producers)}")
    
    for normalized_prod, original_prod in producers.items():
        key, winery = find_winery_match(original_prod, wineries)
        if key:
            if key not in matches:
                matches[key] = {'winery': winery, 'producers': []}
            matches[key]['producers'].append(original_prod)
        else:
            no_matches.append(original_prod)
    
    print(f"\n✅ Match trovati: {len(matches)}")
    print(f"❌ Nessun match: {len(no_matches)}")
    
    # Mostra alcuni esempi di match
    print("\n📋 Esempi di match trovati:")
    for i, (key, data) in enumerate(list(matches.items())[:10]):
        print(f"  {i+1}. {key}")
        print(f"     → Produttori: {', '.join(data['producers'][:3])}")
        if len(data['producers']) > 3:
            print(f"     ... e altri {len(data['producers']) - 3}")
    
    # Mostra alcuni esempi senza match
    print("\n📋 Esempi di produttori senza match:")
    for i, prod in enumerate(no_matches[:10]):
        print(f"  {i+1}. {prod}")
    
    # Statistiche
    total_wines_with_match = sum(len(data['producers']) for data in matches.values())
    print(f"\n📊 Statistiche:")
    print(f"   - Vini con cantina matchata: {total_wines_with_match}")
    print(f"   - Percentuale: {total_wines_with_match / len(producers) * 100:.1f}%")

if __name__ == '__main__':
    main()

