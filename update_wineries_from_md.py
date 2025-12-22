#!/usr/bin/env python3
"""
Script per estrarre informazioni sulle cantine dal file markdown
e aggiornare il database delle cantine in wineries.js
"""

import re
import json

def normalize_name(name):
    """Normalizza il nome della cantina per il matching"""
    if not name:
        return ''
    return name.upper().strip().replace('*', '').replace('(', '').replace(')', '').strip()

def parse_markdown_file(md_file):
    """Parse il file markdown e estrae le informazioni sulle cantine"""
    wineries = {}
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Estrai anche le cantine senza dettagli dalla sezione "Additional Wineries"
    additional_section = re.search(r'Additional Wineries.*?\n\n(.*?)(?:\n\n|$)', content, re.DOTALL)
    if additional_section:
        additional_text = additional_section.group(1)
        # Estrai nomi di cantine (separati da virgole)
        additional_wineries = re.findall(r'([A-Za-z][^,]+(?:/[A-Za-z][^,]+)?)', additional_text)
        for winery_name in additional_wineries:
            winery_name = winery_name.strip()
            if winery_name and len(winery_name) > 2:
                normalized_key = normalize_name(winery_name)
                if normalized_key not in wineries:
                    wineries[normalized_key] = {
                        'name': winery_name,
                        'aliases': [],
                        'notes': 'Information available in wineries database'
                    }
    
    # Dividi per sezioni (## NOME CANTINA)
    sections = re.split(r'^##\s+(.+)$', content, flags=re.MULTILINE)
    
    # Le sezioni sono: [testo_precedente, nome1, contenuto1, nome2, contenuto2, ...]
    for i in range(1, len(sections), 2):
        if i + 1 >= len(sections):
            break
            
        winery_name = sections[i].strip()
        winery_content = sections[i + 1].strip()
        
        # Salta sezioni che non sono cantine (come "Additional Wineries")
        if 'Additional Wineries' in winery_name or 'Structured Archive' in winery_name:
            continue
        
        # Estrai informazioni strutturate
        winery_info = {
            'name': winery_name,
            'aliases': []
        }
        
        # Estrai campi dal contenuto
        lines = winery_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('---'):
                continue
            
            # Pattern per campi chiave:valore
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == 'region':
                    winery_info['region'] = value
                elif key == 'location':
                    winery_info['location'] = value
                elif key == 'year' or key == 'year of foundation':
                    winery_info['year'] = value
                elif key == 'history' or key == 'history and origins':
                    winery_info['history'] = value
                elif key == 'family' or key == 'family / ownership' or key == 'ownership':
                    winery_info['ownership'] = value
                elif key == 'philosophy' or key == 'production philosophy':
                    winery_info['philosophy'] = value
                elif key == 'hectares' or key == 'hectares / grapes':
                    # Potrebbe contenere informazioni su ettari o uve
                    if 'grapes' in key.lower() or any(g in value.lower() for g in ['gaglioppo', 'sangiovese', 'nebbiolo', 'pinot', 'chardonnay']):
                        winery_info['grapes'] = value
                    else:
                        winery_info['hectares'] = value
                elif key == 'grapes':
                    winery_info['grapes'] = value
                elif key == 'main wines' or key == 'wines':
                    winery_info['mainWines'] = value
                elif key == 'notes' or key == 'additional notes':
                    winery_info['notes'] = value
                elif key == 'certification':
                    winery_info['certification'] = value
                elif key == 'style':
                    winery_info['style'] = value
                elif key == 'specialization':
                    winery_info['specialization'] = value
                elif key == 'altitude':
                    winery_info['altitude'] = value
                elif key == 'products':
                    winery_info['products'] = value
                elif key == 'structure':
                    winery_info['structure'] = value
                elif key == 'founder' or key == 'founders':
                    winery_info['founder'] = value
                elif key == 'production':
                    winery_info['production'] = value
                elif key == 'lines':
                    winery_info['lines'] = value
                elif key == 'abv':
                    winery_info['abv'] = value
        
        # Gestisci alias (es. "THE WANTED WINES (Orion Wines)")
        if '(' in winery_name and ')' in winery_name:
            main_name = winery_name.split('(')[0].strip()
            alias = winery_name.split('(')[1].split(')')[0].strip()
            if 'aliases' not in winery_info:
                winery_info['aliases'] = []
            winery_info['aliases'].append(normalize_name(alias))
            winery_info['name'] = main_name
        
        # Aggiungi alias comuni basati sul nome
        # Es: "TENUTA" -> "T.", "AZIENDA AGRICOLA" -> "AGR."
        name_upper = winery_info['name'].upper()
        if 'TENUTA' in name_upper:
            short = name_upper.replace('TENUTA', 'T.').strip()
            if short != name_upper:
                if 'aliases' not in winery_info:
                    winery_info['aliases'] = []
                winery_info['aliases'].append(short)
        
        if 'AZIENDA AGRICOLA' in name_upper:
            short = name_upper.replace('AZIENDA AGRICOLA', 'AGR.').strip()
            if short != name_upper:
                if 'aliases' not in winery_info:
                    winery_info['aliases'] = []
                winery_info['aliases'].append(short)
        
        # Rimuovi duplicati dagli alias
        if 'aliases' in winery_info:
            winery_info['aliases'] = list(set(winery_info['aliases']))
        
        # Normalizza il nome per la chiave
        normalized_key = normalize_name(winery_name)
        wineries[normalized_key] = winery_info
    
    return wineries

def generate_wineries_js(wineries):
    """Genera il codice JavaScript per il database delle cantine"""
    
    js_code = '''/**
 * Wineries Database
 * Contains structured information about wineries extracted from wineries_12-11.md
 * Used to dynamically populate producer descriptions in wine detail pages
 * 
 * Auto-generated from wineries_12-11.md
 */

const WineriesDB = {
    // Helper function to normalize winery names for matching
    normalizeName(name) {
        if (!name) return '';
        return name
            .toUpperCase()
            .trim()
            .replace(/[*]/g, '')
            .replace(/\\s+/g, ' ')
            .replace(/[()]/g, '');
    },

    // Helper function to find winery by producer name (fuzzy matching)
    findWinery(producerName) {
        if (!producerName) return null;
        
        const normalized = this.normalizeName(producerName);
        
        // Direct match
        if (this.wineries[normalized]) {
            return this.wineries[normalized];
        }
        
        // Try partial matching
        for (const [key, winery] of Object.entries(this.wineries)) {
            if (normalized.includes(key) || key.includes(normalized)) {
                return winery;
            }
            
            // Check aliases
            if (winery.aliases) {
                for (const alias of winery.aliases) {
                    if (normalized.includes(alias) || alias.includes(normalized)) {
                        return winery;
                    }
                }
            }
        }
        
        return null;
    },

    getDescription(winery) {
        if (!winery) return null;
        
        const parts = [];
        
        if (winery.history) {
            parts.push(winery.history);
        }
        
        if (winery.region && winery.location) {
            parts.push(`Located in ${winery.location}, ${winery.region}.`);
        } else if (winery.region) {
            parts.push(`Located in ${winery.region}.`);
        } else if (winery.location) {
            parts.push(`Located in ${winery.location}.`);
        }
        
        if (winery.year) {
            parts.push(`Founded in ${winery.year}.`);
        }
        
        if (winery.philosophy) {
            parts.push(winery.philosophy);
        }
        
        if (winery.ownership) {
            parts.push(`Ownership: ${winery.ownership}.`);
        }
        
        if (winery.grapes) {
            parts.push(`Main grapes: ${winery.grapes}.`);
        }
        
        if (winery.mainWines) {
            parts.push(`Main wines: ${winery.mainWines}.`);
        }
        
        if (winery.notes) {
            parts.push(winery.notes);
        }
        
        return parts.join(' ');
    },

    // Wineries database
    wineries: {
'''
    
    # Aggiungi le cantine
    for key, winery in sorted(wineries.items()):
        js_code += f"        '{key}': {{\n"
        name_escaped = winery['name'].replace("'", "\\'")
        js_code += f"            name: '{name_escaped}',\n"
        
        if winery.get('aliases'):
            aliases_str = ', '.join([f"'{a}'" for a in winery['aliases']])
            js_code += f"            aliases: [{aliases_str}],\n"
        
        for field in ['region', 'location', 'year', 'history', 'ownership', 'philosophy', 
                     'hectares', 'grapes', 'mainWines', 'notes', 'certification', 'style',
                     'specialization', 'altitude', 'products', 'structure', 'founder', 
                     'production', 'lines', 'abv']:
            if field in winery:
                value = str(winery[field]).replace("'", "\\'").replace('\n', ' ')
                js_code += f"            {field}: '{value}',\n"
        
        js_code += "        },\n"
    
    js_code += '''    }
};

// Make WineriesDB available globally
if (typeof window !== 'undefined') {
    window.WineriesDB = WineriesDB;
}

// Export for Node.js if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WineriesDB;
}
'''
    
    return js_code

def main():
    md_file = 'wineries_12-11.md'
    js_file = 'js/wineries.js'
    
    print(f"📖 Leggendo {md_file}...")
    wineries = parse_markdown_file(md_file)
    print(f"✅ Trovate {len(wineries)} cantine")
    
    print(f"📝 Generando {js_file}...")
    js_code = generate_wineries_js(wineries)
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print(f"✅ File {js_file} aggiornato con successo!")
    print(f"\n📊 Statistiche:")
    print(f"   - Cantine totali: {len(wineries)}")
    
    # Conta quante hanno informazioni complete
    complete = sum(1 for w in wineries.values() if w.get('history') or w.get('philosophy'))
    print(f"   - Cantine con informazioni dettagliate: {complete}")

if __name__ == '__main__':
    main()

