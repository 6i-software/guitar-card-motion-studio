# Questions ouvertes — Guitar Card AI-Motion Studio

> **Règle :** append-only. Une question résolue garde son historique et pointe vers la décision.
> **Statuts :** `Ouvert` | `Bloquant` | `Résolu`.
> **Priorités :** `P0` (bloque une tâche), `P1` (bloque un milestone), `P2` (plus tard).

---

## Questions résolues

### #Q1 — Lecture de `aA` comme deux tokens distincts
- **Statut :** Résolu
- **Décision :** `D1` — toujours découper en tokens indépendants.
- **Date :** 2026-11-23

---

## Questions ouvertes

### #Q2 — Ambiguïté du suffixe `x<chiffre>` dans le lexer (`Punkx2`)
- **Statut :** Résolu
- **Priorité :** P0
- **Décision :** `D10` — `Punkx2` = `Punk` + multiplicateur 2, jamais `Punkx` + `2`. Le multiplicateur préfixe `2Punk` est équivalent.
- **Impact :** Lexer, parser, golden.

---

### #Q3 — Sens et rendu visuel de `¦` ou `|` sans numéro de case
- **Statut :** Ouvert
- **Priorité :** P1
- **Contexte :** spec grammar §2
- **Question :** Que représente `¦` (arpège) ou `|` (barré) sans numéro de case, et comment l'afficher/s'animer ?
- **Options :**
    1. **Motif générique / case non précisée** : rendu générique ou reprise de la dernière case connue.
    2. **Marqueur de structure / séparation** : traitement visuel distinct dans la ROI.
- **Recommandation :** option 1 pour v1 (motif générique), avec un `motif_key` stable `¦` / `|`.
- **Impact :** modèle du token, animation ROI, golden.
- **Décision :** *(à compléter)*

---

### #Q4 — Nombre collé à un motif nommé, sans `x` (`Punk2`)
- **Statut :** Résolu
- **Priorité :** P0
- **Contexte :** D10 tranche les multiplicateurs explicites : `2Punk` = `Punkx2` = `Punk` joué 2 fois. Reste le cas d'un nombre collé **sans `x`**.
- **Décision :** `D15` — `Punk2`, `Solo1`, `Solo2` sont des **noms** ; chaque occurrence est jouée **une fois**. `A Solo1 AA Solo2` = `A`, `Solo1`, `A`, `A`, `Solo2`. Une répétition exige `2Punk`, `Punkx2` ou `Punk x2`.
- **Cas limite :** `A2` (une lettre + un chiffre) est ambigu → `error` `GC-GRAM-008`, suggestion `2A` ou `Ax2`.
- **Impact :** lexer, parser, golden, zones, YouTube.

---

### #Q5 — Compteur préfixe sur un groupe (`2{AA}`)
- **Statut :** Résolu
- **Priorité :** P0
- **Décision :** `D10` — `2{AA}` est accepté syntaxiquement mais **déconseillé** (diagnostic `info`). La forme préférée est `{AA}x2`, ou `4A` pour une lettre répétée. Les accolades servent aux séquences (`{CACA 2B}x2`).
- **Impact :** parser, diagnostics, golden.

---

### #Q6 — Modificateurs répétés (`A##`, `A~~`, `A#~`)
- **Statut :** Résolu
- **Priorité :** P0
- **Décision :** `D10` + `D15` — `A#` = première variante, `A##` = deuxième variante (normalisée en `A^2`). `A#~` combine variante et modificateur rythmique. Pour plusieurs variantes, utiliser `A^1`, `A^2`, `A^3`.
- **Impact :** lexer, `motif_key`, zones.

---

### #Q7 — Une variante partage-t-elle la case du motif de base ?
- **Statut :** Résolu
- **Priorité :** P0
- **Contexte :** Sur la carte, chaque motif est dessiné dans une case. `ZoneRegion` associe une case (un rectangle) à un `motif_key`.
- **Décision :** `D12` — `a` est un **riff distinct** avec sa propre clé et sa propre zone, rattaché à la famille `A` (`motif_key="a"`, `family_key="A"`). `A#`/`A^2`/`A^3` ont également leur propre clé et leur propre zone, dans la famille `A`. Si la carte dessine `a` dans la même case que `A`, l'utilisateur peut mapper les deux clés sur le même rectangle (override manuel).
- **Justification produit :** `aaAA` doit rester distinguable de `AABB` ; `a` est une version plus légère (souvent une mesure en moins) et non une simple variation d'intensité.
- **Impact :** modèle (`family_key`), zones, animation, YouTube.

---

### #Q8 — Compteurs de groupe (`{5A BB}x2`)
- **Statut :** Bloquant
- **Priorité :** P0
- **Contexte :** `Occurrence` ne porte que `repetition_index/total` et `group_path`.
- **Question :** comment représenter à la fois les 5 pips de `5A` et les 2 pips de `x2` ?
- **Options :**
    1. **`group_path` riche** : chaque `GroupRef` porte `repetition_index/total` ; l'UI affiche le groupe le plus interne.
    2. **Champs dédiés** : `inner_repetition`, `outer_repetition`.
- **Recommandation :** option 1, avec un `GroupRef` typé.
- **Impact :** `Occurrence`, UI, chapitres YouTube.
- **Décision :** *(à compléter)*

---

### #Q9 — Conversion temps → frame
- **Statut :** Bloquant
- **Priorité :** P0
- **Contexte :** spec render : « règle d'arrondi unique et centralisée » non définie.
- **Question :** `round`, `floor` ou `ceil` ? Comment garantir durée vidéo = durée audio ?
- **Options :**
    1. **`floor` au début, `ceil` à la fin**, clamp, epsilon `1e-9`.
    2. **`round`** partout.
- **Recommandation :** option 1, testée sur des timestamps à la ms.
- **Impact :** rendu, export, sync, tests.
- **Décision :** *(à compléter)*

---

### #Q10 — Normalisation audio
- **Statut :** Bloquant
- **Priorité :** P0
- **Contexte :** spec audio : convertir en WAV/PCM à l'import, sans cible chiffrée.
- **Question :** fréquence, canaux, profondeur ?
- **Options :**
    1. **44,1 kHz, stéréo conservé, 16 bits** (référence stable, taille raisonnable).
    2. **48 kHz, mono, float32**.
- **Recommandation :** option 1 ; analyse interne en 22,05 kHz mono.
- **Impact :** import, cache, sync, export.
- **Décision :** *(à compléter)*

---

### #Q11 — Dépendances manquantes
- **Statut :** Résolu
- **Priorité :** P0
- **Décision :** `D7` + `D11` — ajouter **`pytest-cov`** (groupe dev) et **`matplotlib`** (runtime, rapports graphiques SVG/PNG, backend Agg dans un worker). Pas de `scikit-learn` (clustering via scipy/numpy) ; pas de `seaborn`, `plotnine`, `plotly`, `bokeh` ni `altair` en v1.
- **Impact :** stack, licences, build, tests.

---

### #Q12 — Détection ROI : algorithme et acceptation
- **Statut :** Ouvert
- **Priorité :** P1
- **Contexte :** spec image : « identifier la ROI globale » sans méthode ni critère.
- **Question :** quel algorithme, quel taux de réussite, quel fallback ?
- **Options :**
    1. **Baseline** : détection de zone de texte contrastée + projection ; confiance + fallback manuel.
    2. **OCR/template matching** : plus précis mais plus lourd.
- **Recommandation :** option 1 pour v1 ; l'éditeur manuel est obligatoire.
- **Impact :** M2, UI, tests.
- **Décision :** *(à compléter)*

---

### #Q13 — Zones par motif : OCR ou manuel ?
- **Statut :** Ouvert
- **Priorité :** P1
- **Contexte :** la spec demande des `ZoneRegion` par motif, sans méthode.
- **Question :** comment associer un motif à une zone ?
- **Options :**
    1. **Auto best-effort + éditeur manuel** (v1).
    2. **OCR fiable** (promesse forte, risque).
- **Recommandation :** option 1 ; ne pas promettre d'OCR.
- **Impact :** M2, UI, confiance.
- **Décision :** *(à compléter)*

---

### #Q14 — Précision de la synchro
- **Statut :** Ouvert
- **Priorité :** P1
- **Contexte :** la spec demande un score de confiance sans tolérance cible.
- **Question :** quelle tolérance sur les frontières ?
- **Options :**
    1. **±0,15 s** sur frontières à forte attaque, **±0,3 s** ailleurs.
    2. **±0,05 s** partout (irréaliste sur un mix).
- **Recommandation :** option 1, calibrée sur The Wolf.
- **Impact :** M5, tests, confiance.
- **Décision :** *(à compléter)*

---

### #Q15 — Exemples protégés dans Git
- **Statut :** Résolu
- **Priorité :** P0
- **Décision :** `D8` — MP3/PNG réels **hors Git** (`.gitignore`), fixtures synthétiques dans `tests/fixtures/` pour la CI. Pas de Git LFS.
- **Impact :** dépôt, CI, licences.

---

### #Q16 — Emplacement de la description YouTube
- **Statut :** Résolu
- **Priorité :** P0
- **Décision :** `D9` — par défaut `output/description-youtube.txt` dans le dossier du projet ; l'utilisateur peut choisir un autre dossier de sortie. Contenu également copiable dans le presse-papiers.
- **Impact :** YouTube, I2, UI.

---

### #Q35 — Correspondance exacte entre `A^n` et les modificateurs `#`/`~`
- **Statut :** Résolu
- **Priorité :** P0
- **Contexte :** D10 autorise `A#`, `A##`, `A#~` et recommande `A^1`, `A^2`, `A^3` pour plusieurs variantes. La correspondance n'est pas fixée.
- **Décision :** `D15` — `A^n` est la forme canonique : `A^1` ≡ `A#`, `A^2` ≡ `A##`, `A^3` ≡ `A###`. `~` est un modificateur rythmique orthogonal ; `A~` et `A^2~` sont valides, mais `A~^2` est refusé (`warning` `GC-GRAM-009`) car l'exposant porte déjà le niveau de variante. En cas de doute, écrire `A^2` plutôt que `A##`.
- **Impact :** lexer, `motif_key`, golden, zones.
