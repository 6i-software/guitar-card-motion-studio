# Spécification — Pipeline image, audio et synchronisation

> **Contexte** : `core/image/`, `core/audio/`, `core/sync/`, `services/`  
> **Rôle** : Définir l'analyse de l'image et détecter la ROI de la Guitar Card, l'analyse de l'audio (dont MP3) et l'extraire de la guitare, puis aligner la séquence de motifs sur l'audio avec score de confiance et édition manuelle.

---

## 1. Import image et analyse ROI (`core/image/`)

- **Formats supportés** : `PNG`, `JPG`, `WebP` chargés via `Pillow`, avec normalisation de l'orientation EXIF et de l'espace colorimétrique (`RGB` / `RGBA`).
- **Détection automatique** :
    - Identifier la **ROI globale** (zone des motifs de la Guitar Card) 
    - Identifier la **couleur primaire** 
    - Produire une ROI globale + des `ZoneRegion` individuelles par motif (éditables manuellement dans l'UI).
- **Repli manuel** : si la détection de la ROI ou de la couleur primaire est incertaine, proposer une sélection manuelle dans l'UI sans échec silencieux.
- **Invariante d'intégrité** : toute opération d'animation (hors fondu global d'entrée/sortie lorsqu'il est activé) laisse les pixels hors ROI **strictement identiques** à l'image source.

---

## 2. Import audio, normalisation et analyse (`core/audio/`)

### 2.1 Normalisation audio
- Accepter `MP3`, `WAV`, `FLAC` (et formats gérés via `ffmpeg`/`ffprobe` / `soundfile`).
- Les fichiers MP3/VBR pouvant introduire des délais d'encodeur ou des décodages hétérogènes, inspecter l'audio avec `ffprobe` à l'import et le convertir une fois en WAV/PCM dans le dossier du projet via le binaire `ffmpeg` embarqué afin de figer la durée de référence.
- Gérer les cas atypiques : mono, 48 kHz, morceaux longs, métadonnées corrompues.
- Lors des appels à `librosa.load()`, garder la maîtrise de `(sr=None, mono=False)` lorsque la fréquence native ou les canaux séparés sont nécessaires (éviter le rééchantillonnage/mono implicite par défaut).

### 2.2 Passe 1 — Analyse audio complète (`librosa`)
- Extraire tempo (BPM), énergie RMS, enveloppe d'attaque (`onset`), chromagrammes, matrice d'auto-similarité et segmentation en sections (`librosa`, `numpy`, `scipy`)
- Mettre en cache sur disque (clé basée sur le hash du contenu audio normalisé + version de l'algorithme) avec des structures sérialisables.
- Rédiger un rapport d'analyse audio complet, avec des statistiques et des graphiques.

### 2.3 Passe 2 — Séparation de sources (`demucs`)
- Isoler la guitare du reste du mix (batterie, basse, voix, etc.).
- Exécuter dans un **processus séparé** (via la couche `services/`) avec `CancellationToken` et callbacks de progression (`progress(float, message)`), en CPU par défaut et avec utilisation du GPU si disponible + repli propre.
- Embarquer les poids dans le bundle nomade (aucun téléchargement à l'exécution).
- Produire un **rapport de séparation obligatoire** : ratio d'énergie par stem, détection de silence/clipping, corrélation avec le mix, durée, alertes (ex. stem guitare quasi vide) et verdict (`ok` / `douteux` / `echec`).
- Mettre les stems en cache sur disque et invalider si l'audio ou le modèle/paramètres changent.
- Doit fonctionner **CPU seul** ; utiliser le GPU s'il est détecté, avec repli propre.

*Remarques* : le modèle 4 stems standard classe souvent la guitare dans `other` ; `htdemucs_6s` expose un stem `guitar` dédié à qualité variable. À évaluer en spike et à garder configurable (`../DECISIONS.md`)

### 2.4 Passe 3 — Seconde analyse audio de la partie guitare isolé (`librosa`)
- Refaire le travail d'analyse audio de la passe 1 (Extraire tempo (BPM), énergie RMS, enveloppe d'attaque (`onset`), chromagrammes, matrice d'auto-similarité et segmentation en sections) pour la guiare isolé.
- Comparer les deux analyses audios (piste complete, et guitare seul) pour améliorer les scores de confiance, et rédiger un rapport d'analyse audio final.

---

## 3. Synchronisation, diagnostics et simulation (`core/sync/`)

### 3.1 Alignement assisté séquence et audio
- À partir de la séquence dépliée (`expand(ast)`), des onsets/caractéristiques du stem guitare (ou du mix) et de la similarité entre répétitions (clustering + alignement contraint par l'ordre, ex. programmation dynamique / DTW), proposer des timestamps `(start, end)` avec un **score de confiance** (`float`).
- L'alignement automatique est une **proposition éditable** : un événement `locked=True` n'est jamais écrasé par un recalcul automatique.

### 3.2 Pré-diagnostic et simulation temps réel
- **Pré-diagnostic** : détecter chevauchements, durées aberrantes, motifs sans `ZoneRegion`, écarts entre fin de timeline et durée audio, et conflits sur événements verrouillés (`info | warning | error`, avec navigation vers l'événement).
- **Tap-to-sync** : pose/ajustement de timestamps en temps réel (touche configurable, ex. `M`), déplacement direct sur la timeline et saisie numérique, avec compensation de latence audio/UI réglable.
- **Simulation temps réel & compte rendu** : prévisualisation instantanée de la surbrillance, de l'annonce du suivant et des compteurs sans encodage vidéo (mode simulation), suivie d'un **compte rendu de simulation** avant export.
- Résultat = *proposition éditable dans l'UI*, jamais définitive.

---

## 4. Points d'attention

- **Taille et licences** : PyTorch + poids Demucs sont lourds. Embarquer les poids dans le bundle (pas de téléchargement au premier lancement), torch CPU-only par défaut. Vérifier les licences (Demucs MIT, librosa ISC, PySide6 LGPL, FFmpeg LGPL/GPL selon le build) et les documenter dans `THIRD_PARTY_LICENSES.md`.
- Par défaut, `librosa.load()` rééchantillonne à 22050Hz et convertit en mono. Commence avec ce comportement par défaut pour analyse. Ne change pour garder la fréquence d’échantillonnage d’origine ou analyser des canaux séparés que si nécessaire `(sr=None, mono=False)`.
- Entrées MP3 : `soundfile` gère très bien le WAV, FLAC, OGG, mais pas le MP3 ni l'AAC/M4A. `librosa` s’appuie sur `soundfile` et, en secours, sur `audioread` qui délègue souvent à `ffmpeg`). Attention MP3 ajoute parfois des délais/padding d'encodeur qui peuvent créer de légers écarts de durée ou des décodages hétérogènes. Inspecter le fichier avec ffprobe et le convertir une seule fois en WAV/PCM dans le dossier du projet à l'import via le binaire ffmpeg embarqué (en figeant la durée de référence et en embarquant ffprobe à côté de ffmpeg dans le bundle).