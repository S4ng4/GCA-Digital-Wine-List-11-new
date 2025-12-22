/**
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
            .replace(/\s+/g, ' ')
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
        'ACQUESI': {
            name: 'Acquesi',
            notes: 'Information available in wineries database',
        },
        'AGRICOLA PUNICA': {
            name: 'AGRICOLA PUNICA',
            region: 'Sardinia',
            location: 'Sulcis',
            year: '2002',
            grapes: 'Carignano, Cabernet Sauvignon, Merlot, Syrah',
            mainWines: 'Barrua, Montessu, Samas.',
            founder: 'Tachis + Tenuta San Guido + Cantina Santadi',
        },
        'ALBINO ROCCA OVELO': {
            name: 'ALBINO ROCCA OVELO',
            region: 'Piedmont',
            location: 'Barbaresco',
            ownership: 'Rocca family',
            mainWines: 'Barbaresco from historic vineyards like Vigneto Brich Ronchi and Vigneto Loreto.',
            style: 'Traditional yet modern.',
        },
        'ALTESINO': {
            name: 'ALTESINO',
            region: 'Tuscany',
            location: 'Montalcino',
            history: 'Historic estate of Brunello di Montalcino, known for the innovative introduction of barrique in the area.',
            mainWines: 'Brunello di Montalcino "Montosoli" (reference cru).',
        },
        'ANARKOS': {
            name: 'Anarkos',
            notes: 'Information available in wineries database',
        },
        'ANIMA UMBRA': {
            name: 'Anima Umbra',
            notes: 'Information available in wineries database',
        },
        'ANTINORI': {
            name: 'ANTINORI',
            region: 'Tuscany',
            location: 'Florence',
            year: '1385',
            history: 'One of the oldest and most celebrated wine families in Italy, based in Florence since 1385. Constant innovators, they created icons like Tignanello and Solaia, and own estates throughout Italy.',
            philosophy: 'Innovation while respecting tradition.',
        },
        'ARCENO': {
            name: 'ARCENO',
            region: 'Tuscany',
            location: 'Chianti Classico (between Castellina and Radda)',
            year: '1994',
            ownership: 'American Kunz family',
            mainWines: 'Chianti Classico, Supertuscan wines.',
        },
        'ARGIANO': {
            name: 'ARGIANO',
            region: 'Tuscany',
            location: 'Montalcino',
            year: '1580',
            history: 'Historic Montalcino estate, famous for its Brunello. In 2013 it was acquired by a Brazilian group, maintaining high-quality standards.',
            mainWines: 'Brunello di Montalcino.',
        },
        'AVIGNONESI': {
            name: 'AVIGNONESI',
            region: 'Tuscany',
            location: 'Valdichiana',
            history: 'Important winery historically linked to Vino Nobile di Montepulciano. Since 2009 it has been owned by a Belgian couple and converted to organic farming.',
            mainWines: 'Vino Nobile di Montepulciano.',
            certification: 'Organic',
        },
        'AZIENDA AGRICOLA POSSA': {
            name: 'AZIENDA AGRICOLA POSSA',
            aliases: ['AGR. POSSA'],
            region: 'Liguria',
            location: 'Riomaggiore (Cinque Terre)',
            products: 'Sciacchetrà, white & red local wines, distillates.',
        },
        'BANFI': {
            name: 'BANFI',
            region: 'Tuscany',
            location: 'Montalcino',
            year: '1978',
            history: 'One of the largest and most innovative estates in Montalcino (Brunello). A pioneer in research on Sangiovese clones.',
            ownership: 'American Mariani brothers',
            mainWines: 'Brunello di Montalcino.',
        },
        'BINDI SERGARDI': {
            name: 'BINDI SERGARDI',
            region: 'Tuscany (Chianti Classico)',
            year: '1349',
            history: '23 generations.',
            grapes: 'Sangiovese',
        },
        'BIONDI-SANTI': {
            name: 'BIONDI-SANTI',
            region: 'Tuscany',
            location: 'Montalcino',
            history: 'The family that "invented" Brunello di Montalcino in the late 1800s. The "Biondi Santi Tenuta Il Greppo" is a global icon, a symbol of longevity and elegance.',
            mainWines: 'Brunello di Montalcino.',
        },
        'BRANCAIA': {
            name: 'BRANCAIA',
            region: 'Tuscany',
            location: 'Chianti Classico',
            ownership: 'Swiss Widmer family',
            mainWines: 'Chianti Classico, supertuscan "Brancaia Il Blu."',
        },
        'BRUNO': {
            name: 'BRUNO',
            region: 'Piedmont',
            location: 'Barolo (La Morra area)',
            mainWines: 'Barolo from crus like "Rocche dell\'Annunziata" and "Sarmassa."',
            style: 'Elegant and traditional.',
        },
        'BUCEFALO': {
            name: 'Bucefalo',
            notes: 'Information available in wineries database',
        },
        'CASTELFEDER': {
            name: 'Castelfeder',
            notes: 'Information available in wineries database',
        },
        'CASTELLO DI NEIVE': {
            name: 'CASTELLO DI NEIVE',
            region: 'Piedmont',
            location: 'Neive (Langhe)',
            history: 'Historic estate in the eponymous comune in the Langhe.',
            mainWines: 'Barbaresco, Barbera, Moscato d\'Asti from vineyards situated in the best positions of the town.',
        },
        'CERETTO': {
            name: 'CERETTO',
            region: 'Piedmont',
            location: 'Langhe',
            year: '1937',
            history: 'Historic Langhe family. Innovators in marketing and quality, they have mapped and valorized Barolo and Barbaresco crus (like "Brunate," "Bricco Rocche").',
            mainWines: 'Barolo, Barbaresco.',
            founder: 'Riccardo Ceretto',
        },
        'CIACCI': {
            name: 'CIACCI',
            region: 'Tuscany',
            location: 'Montalcino',
            ownership: 'Ciacci family',
            mainWines: 'Brunello di Montalcino, particularly from the famous "Pianrosso" cru.',
            style: 'Powerful and elegant.',
        },
        'CIAVOLICH': {
            name: 'Ciavolich',
            notes: 'Information available in wineries database',
        },
        'CITRA': {
            name: 'Citra',
            notes: 'Information available in wineries database',
        },
        'COCCHI': {
            name: 'COCCHI',
            region: 'Piedmont',
            location: 'Asti',
            year: '1891',
            history: 'Historic house.',
            mainWines: 'Vermouths, Asti, metodo classico "Villadoria."',
            founder: 'Giulio Cocchi',
        },
        'COL D'ORCIA': {
            name: 'COL D\'ORCIA',
            region: 'Tuscany',
            location: 'Montalcino',
            history: 'Ancient Montalcino estate. One of the largest properties in the DOCG.',
            ownership: 'Cinzano family (since 1973)',
            mainWines: 'Brunello di Montalcino (traditional and long-aging style).',
        },
        'COLLOSORBO': {
            name: 'Collosorbo',
            notes: 'Information available in wineries database',
        },
        'CONTADI CASTALDI': {
            name: 'Contadi Castaldi',
            notes: 'Information available in wineries database',
        },
        'CONTRATTO': {
            name: 'CONTRATTO',
            region: 'Piedmont',
            location: 'Canelli (AT)',
            year: '1867',
            history: 'One of the oldest metodo classico sparkling wine houses in Italy.',
            mainWines: 'Millesimati, Vermouth.',
        },
        'DIEVOLE': {
            name: 'DIEVOLE',
            region: 'Tuscany',
            location: 'Chianti Classico (between Castelnuovo Berardenga and Siena)',
            philosophy: 'Approach that combines tradition and technological innovation.',
            mainWines: 'Chianti Classico.',
        },
        'ERCOLE': {
            name: 'Ercole',
            notes: 'Information available in wineries database',
        },
        'ERMES PAVESE': {
            name: 'ERMES PAVESE',
            region: 'Valle d’Aosta',
            location: 'Morgex‑La Salle',
            grapes: 'Prié Blanc (pre‑phylloxera)',
            mainWines: 'Blanc de Morgex et de La Salle, metodo classico, passiti.',
            altitude: 'Up to 1200m',
        },
        'FANTINI/FARNESE': {
            name: 'Fantini/Farnese',
            notes: 'Information available in wineries database',
        },
        'FATTOI': {
            name: 'Fattoi',
            notes: 'Information available in wineries database',
        },
        'FATTORIA DE VAIRA': {
            name: 'FATTORIA DE VAIRA',
            region: 'Molise',
            location: 'Near Campobasso',
            philosophy: 'Biodynamic; native yeasts; minimal sulfur; manual harvest.',
            hectares: '500 total (40 vineyards)',
            grapes: 'Falanghina, Trebbiano, Montepulciano, Sangiovese, Merlot',
            mainWines: 'Vincenzo Bianco',
        },
        'FATTORIA DI MAGLIANO': {
            name: 'FATTORIA DI MAGLIANO',
            region: 'Tuscany (Maremma)',
            year: '1996',
            mainWines: 'Heba, Brissaia, Poggio Bestiale, Pagliatura, Illario.',
            certification: 'Organic',
        },
        'FEUDI BIZANTINI TENUTA ULISSE': {
            name: 'FEUDI BIZANTINI',
            aliases: ['TENUTA ULISSE'],
            region: 'Abruzzo',
            grapes: 'Pecorino (Passofino), Trebbiano, Montepulciano',
            notes: 'Pecorino grape recovered from near extinction.',
        },
        'FEUDI DEL PISCIOTTO': {
            name: 'FEUDI DEL PISCIOTTO',
            region: 'Sicily',
            location: 'Cerasuolo di Vittoria DOCG',
            history: 'Ancient 1700s palmento preserved; modern winery built nearby.',
            philosophy: 'Gravity-flow vinification without pumps; manual harvest; lower emissions; energy efficiency.',
            hectares: '44',
            mainWines: '“Grandi Stilisti” line (includes L’Eterno, Pinot Nero 100%), “Baglio del Sole” line.',
            notes: 'High quality driven by altitude and sea breezes.',
            production: 'Capacity 1.5M bottles; actual 400k bottles (16 labels).',
        },
        'FONTANAFREDDA': {
            name: 'FONTANAFREDDA',
            region: 'Piedmont',
            location: 'Langhe',
            year: '1878',
            history: 'Historic Langhe estate, founded by the will of the first King of Italy, Vittorio Emanuele II, and his mistress Rosa Vercellana. One of the most important producers of Barolo, Barbaresco, and sparkling wines.',
            mainWines: 'Barolo, Barbaresco, sparkling wines.',
        },
        'FOSSACOLLE': {
            name: 'FOSSACOLLE',
            region: 'Tuscany',
            location: 'Montalcino',
            philosophy: 'Traditional style, aged in large oak casks.',
            mainWines: 'Brunello di Montalcino.',
        },
        'GAJA': {
            name: 'GAJA',
            region: 'Piedmont',
            location: 'Barbaresco',
            history: 'The winery of Angelo Gaja, an absolute innovator and global ambassador of Italian wine. He revolutionized Barbaresco and Barolo by introducing modern methods.',
            ownership: 'Angelo Gaja (today led by his daughters Gaia, Rossana, and Lucia)',
            mainWines: 'Barbaresco icons like "Sori San Lorenzo," "Sori Tildìn," "Sperss."',
        },
        'GUADO AL TASSO ANTINORI': {
            name: 'GUADO AL TASSO',
            aliases: ['ANTINORI'],
            region: 'Tuscany',
            location: 'Bolgheri DOC',
            ownership: 'Antinori',
            mainWines: 'Supertuscan "Guado al Tasso" (Cabernet, Merlot, Syrah), Vermentino.',
        },
        'IL POGGIONE': {
            name: 'IL POGGIONE',
            region: 'Tuscany',
            location: 'Montalcino',
            year: 'Late 1800s',
            history: 'One of the first producers of Brunello.',
            ownership: 'Franceschi family',
            mainWines: 'Brunello di Montalcino.',
            style: 'Traditional and long-lived.',
        },
        'IPPOLITO 1845': {
            name: 'IPPOLITO 1845',
            region: 'Calabria',
            location: 'Cirò Marina',
            year: '1845',
            hectares: '100',
            grapes: 'Gaglioppo, Greco Bianco, Pecorello',
            notes: 'Oldest winery in Calabria.',
        },
        'JERMANN': {
            name: 'Jermann',
            notes: 'Information available in wineries database',
        },
        'LA GIOIOSA': {
            name: 'La Gioiosa',
            notes: 'Information available in wineries database',
        },
        'LAMOLE DI LAMOLE': {
            name: 'Lamole di Lamole',
            notes: 'Information available in wineries database',
        },
        'LE COLTURE': {
            name: 'Le Colture',
            notes: 'Information available in wineries database',
        },
        'MABIS': {
            name: 'Mabis',
            notes: 'Information available in wineries database',
        },
        'MANFREDI': {
            name: 'Manfredi',
            notes: 'Information available in wineries database',
        },
        'MARCHESI DI BAROLO': {
            name: 'MARCHESI DI BAROLO',
            region: 'Piedmont',
            location: 'Barolo',
            year: '1800s',
            history: 'One of the historic and most representative Barolo wineries. Marchesa Giulia Colbert Falletti entrusted Paolo Francesco Staglieno here with the first production of "Barolo" wine as we know it today. A guardian of tradition.',
            mainWines: 'Barolo.',
        },
        'MASCIARELLI': {
            name: 'Masciarelli',
            notes: 'Information available in wineries database',
        },
        'MAZZEI': {
            name: 'MAZZEI',
            region: 'Tuscany',
            location: 'Chianti Classico (Fonterutoli)',
            year: '1435',
            history: 'Tuscan family owning Fonterutoli in Chianti Classico since 1435.',
            mainWines: 'Chianti Classico, supertuscan "Siepi."',
        },
        'MEDICI ERMETE': {
            name: 'Medici Ermete',
            notes: 'Information available in wineries database',
        },
        'MEZZACORONA': {
            name: 'Mezzacorona',
            notes: 'Information available in wineries database',
        },
        'MORISFARMS': {
            name: 'MORISFARMS',
            region: 'Tuscany',
            location: 'Maremma (near Massa Marittima)',
            philosophy: 'Modern approach.',
            mainWines: 'Morellino di Scansano, Vermentino.',
        },
        'NINO NEGRI': {
            name: 'Nino Negri',
            notes: 'Information available in wineries database',
        },
        'NIVOLE': {
            name: 'NIVOLE',
            region: 'Piedmont',
            location: 'Asti',
            mainWines: 'Moscato d\'Asti.',
            style: 'Light, aromatic, and sweet.',
        },
        'ODOARDI': {
            name: 'Odoardi',
            notes: 'Information available in wineries database',
        },
        'PALADIN': {
            name: 'Paladin',
            notes: 'Information available in wineries database',
        },
        'PAOLO LEO': {
            name: 'Paolo Leo',
            notes: 'Information available in wineries database',
        },
        'PAOLO SCAVINO': {
            name: 'PAOLO SCAVINO',
            region: 'Piedmont',
            location: 'Barolo',
            year: '1921',
            ownership: 'Enrico Scavino and his daughters',
            mainWines: 'Barolo from single crus (Bric del Fiasc, Cannubi, Rocche dell\'Annunziata).',
            style: 'Great elegance and purity.',
            founder: 'Paolo Scavino',
        },
        'PASSO SARDO': {
            name: 'Passo Sardo',
            notes: 'Information available in wineries database',
        },
        'PELISSERO': {
            name: 'Pelissero',
            notes: 'Information available in wineries database',
        },
        'PIAN DELLE VIGNE ANTINORI': {
            name: 'PIAN DELLE VIGNE',
            aliases: ['ANTINORI'],
            region: 'Tuscany',
            location: 'Montalcino',
            ownership: 'Antinori',
            mainWines: 'Brunello di Montalcino (elegant and accessible style), named after the eponymous locality.',
        },
        'PICCINI': {
            name: 'Piccini',
            notes: 'Information available in wineries database',
        },
        'PIO CESARE': {
            name: 'PIO CESARE',
            region: 'Piedmont',
            location: 'Alba',
            year: '1881',
            history: 'Historic Alba winery. One of the first to bottle and market wines from the Langhe under its own name.',
            mainWines: 'Barolo, Barbaresco, Barbera.',
        },
        'POLIZIANO': {
            name: 'POLIZIANO',
            region: 'Tuscany',
            location: 'Montepulciano',
            year: '1961',
            mainWines: 'Vino Nobile di Montepulciano (particularly the "Asinone" selection), supertuscan "Le Stanze."',
            founder: 'Dino Carletti',
        },
        'PRIMA PAVÉ': {
            name: 'PRIMA PAVÉ',
            region: 'Northern Italy',
            grapes: 'Pinot Grigio, Sauvignon Blanc, Gewürztraminer, Montepulciano, Chardonnay',
            products: 'Alcohol‑free sparkling and still drinks from dealcoholized wine.',
            abv: '0.0%',
        },
        'PRODUTTORI DEL BARBARESCO': {
            name: 'PRODUTTORI DEL BARBARESCO',
            region: 'Piedmont',
            location: 'Barbaresco',
            year: '1958',
            grapes: 'Nebbiolo',
            mainWines: 'Barbaresco DOCG + Riservas (great vintages).',
        },
        'PRUNOTTO': {
            name: 'PRUNOTTO',
            region: 'Piedmont',
            location: 'Langhe',
            year: '1904',
            history: 'Historic Langhe winery.',
            ownership: 'Acquired by Antinori in 1989',
            mainWines: 'Barolo from crus (Bussia, Cannubi), Barbaresco.',
            style: 'Great tradition and balance.',
        },
        'PUIATTI': {
            name: 'Puiatti',
            notes: 'Information available in wineries database',
        },
        'QUERCIAVALLE LOSI': {
            name: 'QUERCIAVALLE',
            aliases: ['LOSI'],
            region: 'Tuscany (Chianti Classico)',
            history: 'Family cultivating grapes since 1870; estate acquired 1954.',
            grapes: 'Sangiovese',
        },
        'R. MASCARELLO': {
            name: 'R. MASCARELLO',
            region: 'Piedmont',
            location: 'Barolo',
            history: 'Historic Barolo winery, symbol of purist tradition.',
            philosophy: 'Produces blended Barolo from different crus (like the "Barolo" blend) according to traditional methods: fermentation with pied de cuve, long macerations, large casks.',
            mainWines: 'Barolo.',
        },
        'RATTI': {
            name: 'RATTI',
            region: 'Piedmont',
            location: 'Langhe',
            year: '1865',
            history: 'One of the most respected wineries in Piedmont. The son, Renato Ratti, was a pioneer in the zoning of Barolo crus in the 60s-70s.',
            mainWines: 'Barolo, Barbaresco, Barbera.',
            founder: 'Giovanni Battista Ratti',
        },
        'ROMITORO': {
            name: 'ROMITORO',
            region: 'Tuscany',
            location: 'Montalcino',
            ownership: 'Artist Sandro Chia',
            philosophy: 'Approach respectful of tradition.',
            mainWines: 'Brunello di Montalcino, Rosso di Montalcino.',
        },
        'RUFFINO': {
            name: 'RUFFINO',
            region: 'Tuscany',
            location: 'Pontassieve (FI)',
            year: '1877',
            history: 'One of the most well-known Tuscan wineries worldwide.',
            ownership: 'Folonari family',
            mainWines: 'Chianti "Ducale" and a vast range of products.',
        },
        'SAN FELICE': {
            name: 'SAN FELICE',
            region: 'Tuscany',
            location: 'Chianti Classico (comune of Castelnuovo Berardenga)',
            mainWines: 'Chianti Classico "Il Grigio," supertuscan "Vigorello."',
        },
        'SAN MARZANO': {
            name: 'San Marzano',
            notes: 'Information available in wineries database',
        },
        'SAN PATRIGNANO': {
            name: 'San Patrignano',
            notes: 'Information available in wineries database',
        },
        'SANTA TRESA': {
            name: 'SANTA TRESA',
            region: 'Sicily',
            location: 'Vittoria',
            year: '1697',
            hectares: '50',
            notes: 'Historic estate near River Dirillo; symbol is a medieval golden sun.',
        },
        'SAROTTO': {
            name: 'Sarotto',
            notes: 'Information available in wineries database',
        },
        'SCARBOLO': {
            name: 'SCARBOLO',
            region: 'Friuli Venezia Giulia',
            location: 'Lauzacco',
            year: '1982',
            grapes: 'Friulano, Refosco, Merlot, Sauvignon.',
            specialization: 'Pinot Grigio (four styles including Ramato)',
        },
        'SICILIANA': {
            name: 'Siciliana',
            notes: 'Information available in wineries database',
        },
        'SPORTOLETTI': {
            name: 'SPORTOLETTI',
            region: 'Umbria',
            location: 'Spello / Assisi',
            history: 'Estate switched to bottling in 1979.',
            grapes: 'Sangiovese, Merlot, Cabernet Sauvignon, Grechetto, Chardonnay',
            mainWines: 'Assisi Rosso, Assisi Grechetto, Villa Fidelia.',
        },
        'TAMELLINI': {
            name: 'TAMELLINI',
            region: 'Veneto (Soave)',
            year: '1998',
            history: 'Family of four generations of viticulturists.',
            grapes: 'Garganega',
            mainWines: 'Soave DOC, Le Bine de Costiola, Spumante Metodo Classico Extra Brut.',
        },
        'TENUTA MARMORELLE.': {
            name: 'Tenuta Marmorelle.',
            notes: 'Information available in wineries database',
        },
        'TENUTA PRINCIPE ALBERICO': {
            name: 'TENUTA PRINCIPE ALBERICO',
            aliases: ['T. PRINCIPE ALBERICO'],
            region: 'Lazio',
            location: 'Appia Antica (Rome)',
            history: 'Founded 1946 by Prince Alberico Boncompagni Ludovisi; today owned by the Antinori family (descendants).',
            grapes: 'Cabernet Sauvignon, Merlot, Sémillon',
            mainWines: 'Alberico Rosso, Alberico Bianco, Appia Antica 400.',
        },
        'TENUTA SAN FRANCESCO': {
            name: 'TENUTA SAN FRANCESCO',
            aliases: ['T. SAN FRANCESCO'],
            region: 'Campania',
            location: 'Tramonti, Amalfi Coast',
            year: '2004',
            grapes: 'Tintore (300‑year‑old pre‑phylloxera vines), Aglianico, Piedirosso, Falanghina, Pepella, Ginestra',
            mainWines: 'È Iss (Tintore), 4 Spine, Per Eva, Tramonti Rosso/Bianco.',
        },
        'TENUTA SANT’ANTONIO': {
            name: 'Tenuta Sant’Antonio',
            notes: 'Information available in wineries database',
        },
        'TENUTA VITANZA': {
            name: 'TENUTA VITANZA',
            aliases: ['T. VITANZA'],
            region: 'Tuscany',
            location: 'Montalcino',
            history: 'Project began 1994; founders Rosalba Vitanza and Guido Andretta. First Brunello (1995) received 93 points from Wine Spectator. Gravity-flow winery built in 2002.',
            grapes: 'Sangiovese',
            mainWines: 'Brunello di Montalcino (various labels), Rosso di Montalcino, Chianti Colli Senesi, “Quadrimendo” Super Tuscan.',
        },
        'TENUTE DI GIULIO': {
            name: 'TENUTE DI GIULIO',
            region: 'Molise',
            location: 'Campomarino (CB)',
            history: 'Estate purchased 1960; first winery built 1977; modern expansion in the 1990s by Enrico and Pasquale.',
            hectares: '100 (80 vineyards)',
            grapes: 'Montepulciano, Trebbiano, Aglianico, Falanghina',
            mainWines: 'Volto Marino Rosso, Tintilia del Molise',
            notes: 'Advanced technological approach.',
        },
        'TERLANO/TERLAN': {
            name: 'Terlano/Terlan',
            notes: 'Information available in wineries database',
        },
        'TERRE DI MARIO': {
            name: 'Terre di Mario',
            notes: 'Information available in wineries database',
        },
        'THE FOLLOWING WINERIES APPEARED IN THE FILE BUT WITHOUT DESCRIPTIONS:
ABBAZIA DI NOVACELLA': {
            name: 'The following wineries appeared in the file but without descriptions:
Abbazia di Novacella',
            notes: 'Information available in wineries database',
        },
        'THE WANTED WINES ORION WINES': {
            name: 'THE WANTED WINES',
            aliases: ['ORION WINES'],
            region: 'Italy (production), Trentino (headquarters)',
            location: 'Lavis, Trento',
            philosophy: 'American strength meets Italian elegance; bold, soft, fruit‑forward style.',
            mainWines: 'The Chard, The Zin Old Vines, The Zin Rosé, The Cab, The Ranger.',
        },
        'THOMAIN': {
            name: 'THOMAIN',
            region: 'Valle d\'Aosta',
            location: 'Arvier',
            history: 'Winery active since 1920; three generations.',
            grapes: 'Enfer d’Arvier DOC area (2 hectares).',
            notes: 'Visits by appointment.',
        },
        'TIGNANELLO ANTINORI': {
            name: 'TIGNANELLO',
            aliases: ['ANTINORI'],
            region: 'Tuscany',
            history: 'The Supertuscan that in 1971 (in its first vintages as "Chianti Classico Riserva vigneto Tignanello") changed the history of Italian wine. The first modern Tuscan wine with a Bordeaux blend (Sangiovese/Cabernet) and the first Chianti not to use white grapes. A world icon.',
            ownership: 'Antinori',
            mainWines: 'Tignanello.',
        },
        'TONNINO WINERY': {
            name: 'TONNINO WINERY',
            region: 'Sicily',
            history: 'Began with Paolo (grandfather) producing must in the 1950s; family later started bottling.',
            philosophy: 'Manual harvest, natural approach.',
            notes: 'Located between sea and mountains.',
        },
        'TORNATORE': {
            name: 'Tornatore',
            notes: 'Information available in wineries database',
        },
        'TORRE MORA': {
            name: 'Torre Mora',
            notes: 'Information available in wineries database',
        },
        'TUA RITA': {
            name: 'Tua Rita',
            notes: 'Information available in wineries database',
        },
        'UMANI RONCHI': {
            name: 'Umani Ronchi',
            notes: 'Information available in wineries database',
        },
        'VACCA BARBARESCO': {
            name: 'VACCA',
            aliases: ['BARBARESCO'],
            region: 'Piedmont',
            location: 'Barbaresco',
            history: 'Active since 1958; three generations.',
            grapes: 'Nebbiolo, Barbera, Arneis',
            notes: 'Member of the Produttori del Barbaresco cooperative.',
        },
        'VAL DI SUGA': {
            name: 'VAL DI SUGA',
            region: 'Tuscany',
            location: 'Montalcino',
            ownership: 'Angelini group',
            philosophy: 'Produces Brunello di Montalcino from three different areas of the comune (north, south-east, south), expressing the different souls of the territory.',
            mainWines: 'Brunello di Montalcino.',
        },
        'VIGNETI DEL SALENTO': {
            name: 'Vigneti del Salento',
            notes: 'Information available in wineries database',
        },
        'VIGNETI DEL VULTURE': {
            name: 'Vigneti del Vulture',
            notes: 'Information available in wineries database',
        },
        'VIGNETI VUMBACA': {
            name: 'VIGNETI VUMBACA',
            region: 'Calabria',
            location: 'Cirò',
            year: '1984',
            philosophy: 'Organic farming',
            grapes: 'Gaglioppo, Greco Bianco',
            notes: 'Recognized by major Italian guides.',
        },
        'VILLA CALCINAIA': {
            name: 'VILLA CALCINAIA',
            region: 'Tuscany',
            location: 'Greve in Chianti',
            year: '1524',
            history: 'Historic estate.',
            ownership: 'Capponi family (since 1524)',
            mainWines: 'Chianti Classico.',
            style: 'Great elegance and tradition.',
        },
        'VINCHIO VAGLIO': {
            name: 'Vinchio Vaglio',
            notes: 'Information available in wineries database',
        },
        'VINEKA': {
            name: 'VINEKA',
            region: 'Puglia',
            location: 'Valle d’Itria',
            philosophy: 'Preservation of regional heritage; focus on native grapes; sustainability.',
            lines: 'ZITO (premium), VINEKA (environment-focused).',
        },
        'VINI VENTURINI AZIENDA AGRICOLA VENTURINI MASSIMINO': {
            name: 'VINI VENTURINI',
            aliases: ['AZIENDA AGRICOLA VENTURINI MASSIMINO'],
            region: 'Veneto',
            location: 'Valpolicella (San Floriano)',
            year: '1963',
            history: 'Three generations working the vineyards.',
            mainWines: 'Valpolicella.',
        },
        'VITE COLTE': {
            name: 'VITE COLTE',
            region: 'Piedmont',
            location: 'Barolo',
            philosophy: 'Payment per hectare to reward quality.',
            structure: 'Cooperative (180 growers, 300 hectares)',
        },
        'VOGA': {
            name: 'Voga',
            notes: 'Information available in wineries database',
        },
        'ZORZETTIG': {
            name: 'Zorzettig',
            notes: 'Information available in wineries database',
        },
    }
};

// Make WineriesDB available globally
if (typeof window !== 'undefined') {
    window.WineriesDB = WineriesDB;
}

// Export for Node.js if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WineriesDB;
}
