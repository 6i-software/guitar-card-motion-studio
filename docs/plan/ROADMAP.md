# Roadmap agentique — Guitar Card AI-Motion Studio

> **Statut :** adopté (2026-11-25, cadre complet)
> **Stratégie :** rolling wave planning. On détaille les 2 prochaines vagues ; le reste est indicatif.
> **Règle :** chaque milestone se termine par une démo reproductible, des gates vertes et un tag.

---

## 1. Vue d'ensemble

| # | Milestone | Objectif | Vagues | Sortie |
|---|---|---|---|---|
| M0 | Scaffold | Projet `uv`, fenêtre hello world, gates, docs | W0.1–W0.3 | `uv run python -m gcstudio` + CI verte |
| M1 | Grammaire | Lexer, parser, AST, expansion, diagnostics | W1.1–W1.3 | 4 golden verts + fuzz sans crash |
| M2 | Image | ROI, couleur primaire, zones, overlay | W2.1–W2.3 | ROI sur exemples + intégrité hors ROI |
| M3 | Audio passe 1 | Import/normalisation, features, cache, rapport | W3.1–W3.3 | Fixtures synthétiques + rapport The Wolf |
| M4 | Demucs | Séparation, worker, cache, rapport | W4.1–W4.3 | Séparation CPU + rapport + repli GPU |
| M5 | Sync | Alignement proposé, confiance, timeline, locked | W5.1–W5.3 | Ground truth The Wolf + édition manuelle |
| M6 | Timeline UI | Waveform, marqueurs, tap-to-sync, undo/redo | W6.1–W6.3 | Démo interactive |
| M7 | Animation + simulation | Moteur pur, preview, rapport de simulation | W7.1–W7.3 | Preview 1080p + intégrité |
| M8 | Export | Pipe ffmpeg, hwaccel, progression, annulation | W8.1–W8.3 | MP4 court valide + The Wolf complet |
| M9 | Projets + YouTube | Bibliothèque, migrations, chapitres, description | W9.1–W9.3 | Round-trip + projet corrompu + description |
| M10 | Packaging | PyInstaller, Nuitka, binaires, licences | W10.1–W10.3 | 3 OS testés sur machine vierge |

---

## 2. Dépendances entre milestones

```
M0 ──► M1 ──► M2 ──► M5 ──► M6 ──► M7 ──► M8 ──► M10
        │      │      ▲
        │      └► M3 ─┘
        │             │
        └────────────►M4
                       │
M0 ──► M9 ─────────────┘ (peut démarrer après M1/M2)
```

- M1 (grammaire) et M9 (persistance) peuvent avancer en parallèle après M0.
- M3 (audio) et M2 (image) sont indépendants.
- M4 (Demucs) dépend de M3.
- M5 (sync) dépend de M1, M2, M3, M4.
- M6 (UI) dépend de M5 (contrat timeline) et M2 (zones).
- M7 (animation) dépend de M2, M5, M6 (preview).
- M8 (export) dépend de M7.
- M10 dépend de M8 et M9.

---

## 3. Détail des milestones

### M0 — Scaffold

**Objectif :** un dépôt qui démarre, se teste et se lint, sans logique métier.

**Prérequis machine :** `uv` 0.13.10, Python 3.12.16 (installés le 2026-11-25), ffmpeg/ffprobe pour les tests slow. Remote GitHub : `origin` (`D13`).

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W0.1 | T-0001 scaffold uv + hello world | core-dev, qa-verifier | fenêtre + pytest |
| W0.2 | T-0002 gates/CI locale, T-0003 erreurs/logging | integrator, core-dev | `scripts/ci.py`, erreurs, logs |
| W0.3 | T-0009 README + docs de démarrage | spec-analyst | doc lisible |

**Critère de sortie :**
- `uv sync` OK sur Windows/macOS/Linux.
- `uv run python -m gcstudio` ouvre une fenêtre.
- `uv run pytest` vert.
- `uv run ruff check .`, `ruff format --check .`, `mypy src/gcstudio/core` verts.
- Aucun import Qt dans `core/`.
- Démo : capture de la fenêtre + sortie des gates.

### M1 — Grammaire

**Objectif :** parser robuste, AST, expansion, diagnostics, 4 golden.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W1.1 | T-0004 contrat grammar, T-0005 lexer, T-0008 golden/property | spec-analyst, core-dev, qa-verifier | contrat + lexer + tests |
| W1.2 | T-0006 parser/AST, T-0010 diagnostics | core-dev | AST + erreurs localisées |
| W1.3 | T-0007 expand + compteurs de groupe | core-dev | occurrences plates |

**Critère de sortie :**
- 4 golden verts : The Wolf, Reckless Paradise, Rusted From The Rain, Try Honesty.
- `Punkx2` = 2 occurrences ; `{5A BB}x2` = 14 occurrences avant `CC#`.
- `hypothesis` : aucun crash sur entrées aléatoires.
- Diagnostics en français, spans corrects.
- Couverture grammar ≥ 90 %.

### M2 — Image

**Objectif :** charger une image, détecter la ROI et la couleur primaire, permettre l'ajustement manuel.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W2.1 | T-0011 load/normalize, T-0012 couleur primaire | render-dev | image normalisée + couleur |
| W2.2 | T-0013 ROI auto (spike + baseline), T-0014 zones manuelles | render-dev, ui-dev | ROI + éditeur |
| W2.3 | T-0015 overlay integrity harness | render-dev, qa-verifier | test pixels hors ROI |

**Critère de sortie :**
- Chargement PNG/JPG/WebP, EXIF, RGB/RGBA.
- ROI globale + couleur primaire sur les 5 cartes PNG fournies.
- Fallback manuel si confiance faible.
- Test d'intégrité : 100 frames, hors ROI identique.
- Démo : image + ROI affichée.

### M3 — Audio passe 1

**Objectif :** importer/normaliser l'audio, extraire les features, cacher, produire un rapport.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W3.1 | T-0016 import ffprobe/ffmpeg + WAV PCM | audio-dev | audio normalisé |
| W3.2 | T-0017 features librosa (BPM, RMS, onset, chroma, SSM, sections) | audio-dev | features + cache |
| W3.3 | T-0018 rapport audio + fixtures synthétiques | audio-dev, qa-verifier | rapport + tests |

**Critère de sortie :**
- Fixtures synthétiques : BPM/onset dans la tolérance.
- Cache invalidé par hash + version.
- Rapport The Wolf reproductible (BPM ~124, durée 227,7 s).
- Aucun test CI dépendant d'un MP3 protégé.

### M4 — Demucs

**Objectif :** séparer la guitare, en CPU par défaut, avec progression/annulation et rapport.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W4.1 | T-0019 worker séparé + CancellationToken | audio-dev, ui-dev | job annulable |
| W4.2 | T-0020 cache stems + rapport de séparation | audio-dev | rapport + cache |
| W4.3 | T-0021 spike modèle 4 stems vs 6 stems + GPU fallback | audio-dev | décision modèle |

**Critère de sortie :**
- Séparation CPU sur un extrait court.
- Progression et annulation testées.
- Rapport : ratio d'énergie, silence/clipping, corrélation, verdict.
- Décision documentée sur le modèle et les poids.
- Aucun téléchargement à l'exécution.

### M5 — Sync

**Objectif :** proposer un alignement avec confiance, éditable, en respectant `locked`.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W5.1 | T-0022 contrat timeline + modèle Event | spec-analyst, core-dev | contrat + modèle |
| W5.2 | T-0023 alignement v1 (onsets + DTW/clustering) | audio-dev | proposition + confiance |
| W5.3 | T-0024 diagnostics + ground truth The Wolf | audio-dev, qa-verifier | tests + rapport |

**Critère de sortie :**
- The Wolf : frontières A/B dans la tolérance définie (à calibrer, cible ±0,15 s sur les frontières solides).
- `locked=True` jamais écrasé.
- Diagnostics overlap/durée aberrante/motif sans zone/écart de durée.
- Édition manuelle possible (modèle, pas encore UI).

### M6 — Timeline UI

**Objectif :** timeline interactive, waveform, marqueurs, tap-to-sync, undo/redo.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W6.1 | T-0025 widget timeline + waveform | ui-dev | affichage + zoom |
| W6.2 | T-0026 marqueurs, drag, snapping, saisie numérique | ui-dev | édition |
| W6.3 | T-0027 tap-to-sync + latence, undo/redo | ui-dev, qa-verifier | démo |

**Critère de sortie :**
- Timeline fluide sur The Wolf.
- Tap-to-sync avec compensation de latence réglable.
- Undo/redo fiable.
- Pré-diagnostic affiché et navigable.
- Smoke tests `pytest-qt`.

### M7 — Animation + simulation

**Objectif :** moteur d'animation pur, preview temps réel, rapport de simulation.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W7.1 | T-0028 moteur `(state, t) -> overlay RGBA` | render-dev | moteur pur |
| W7.2 | T-0029 preview + styles (couleurs, anticipation, compteurs, halo) | ui-dev, render-dev | preview |
| W7.3 | T-0030 rapport de simulation + intégrité | qa-verifier | démo |

**Critère de sortie :**
- Preview 1080p ≥ 30 fps (cible).
- Intégrité hors ROI sur N frames.
- Anticipation 0,2–1,2 s, compteurs pips/badge/off.
- Rapport de simulation avant export.

### M8 — Export

**Objectif :** export MP4 via pipe rawvideo, hwaccel + repli, progression, annulation.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W8.1 | T-0031 pipe ffmpeg + audio mux | render-dev | MP4 court |
| W8.2 | T-0032 hwaccel detection + test frame + fallback | render-dev | encodeurs |
| W8.3 | T-0033 UI export + progression + annulation + cleanup | ui-dev, qa-verifier | démo |

**Critère de sortie :**
- MP4 2 s valide (durée + audio via ffprobe).
- The Wolf complet exporté.
- Annulation : process tué, fichier partiel supprimé.
- Pas de deadlock stderr/progress.
- Durée vidéo = durée audio dans la tolérance documentée.

### M9 — Projets + YouTube

**Objectif :** bibliothèque, persistance, migrations, chapitres et description.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W9.1 | T-0034 modèle Project + schéma v1 + atomic write | core-dev | save/load |
| W9.2 | T-0035 migrations + mode dégradé + bibliothèque UI | core-dev, ui-dev | round-trip |
| W9.3 | T-0036 chapitres + description YouTube | core-dev, ui-dev | export texte |

**Critère de sortie :**
- Round-trip projet complet.
- Migration v1→v2 testée (fixture).
- Projet corrompu : récupération partielle + rapport.
- Chapitres et description copiables.
- Écriture dans le dossier projet/export, pas `./build`.

### M10 — Packaging

**Objectif :** bundles nomades Windows/macOS/Linux, binaires et poids inclus, licences.

| Vague | Tasks | Rôles | Sortie |
|---|---|---|---|
| W10.1 | T-0037 PyInstaller onedir + ffmpeg/ffprobe | integrator | bundle Windows |
| W10.2 | T-0038 Nuitka + poids Demucs + licences | integrator | bundle prod |
| W10.3 | T-0039 tests machine vierge 3 OS | integrator, qa-verifier | matrice |

**Critère de sortie :**
- Bundle lance sans Python installé.
- Import image/audio, preview, export court.
- Aucun téléchargement au premier lancement.
- `THIRD_PARTY_LICENSES.md` complet.
- Taille et temps de build documentés.

---

## 4. Post-MVP : itérations

Après M10, le rythme passe en **flux continu** :

- **Feature** : brief → impact → décision → tasks → vague → release.
- **Bugfix** : reproduction → test rouge → fix → régression → patch.
- **Dette** : une vague par milestone, jamais mélangée à une feature.
- **Release** : SemVer, changelog, tag, notes, test machine vierge.
- **Rétro** : après chaque milestone, mettre à jour le playbook et les gates.

Détail : `docs/plan/ITERATIONS.md`.

---

## 5. Règles de planification

1. Ne détailler que les 2 prochaines vagues.
2. Une vague = 1 objectif démontrable, 2-5 tasks, fichiers disjoints.
3. Une task > 1 jour est découpée.
4. Un milestone sans démo n'est pas terminé.
5. Un milestone qui dérape > 30 % déclenche une rétro de périmètre.
6. Les dépendances externes (GPU, ffmpeg, OS) sont des risques explicites, pas des surprises.
