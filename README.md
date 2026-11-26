# Guitar Card AI-Motion Studio

**Une Guitar Card, une piste audio, une vidéo de pratique synchronisée.**

Guitar Card AI-Motion Studio est une application de bureau (Windows, macOS, Linux) qui transforme une **Guitar Card** — une partition simplifiée faite de motifs et de répétitions — et un enregistrement audio en une **vidéo animée** : le motif en cours est mis en évidence, le motif suivant est annoncé, et les répétitions sont comptées.

L'application fonctionne **hors ligne**, en **français par défaut**, et ne modifie que la zone des motifs : le reste de l'image reste strictement identique à l'original.

> **État du projet :** le socle technique est en place et la fenêtre de démarrage s'ouvre. L'import, l'analyse audio, la synchronisation et le rendu vidéo sont en cours de développement.

---

## Sommaire

- [Le problème](#le-problème)
- [Ce que fait l'application](#ce-que-fait-lapplication)
- [État du projet](#état-du-projet)
- [Démarrage](#démarrage)
- [Développement](#développement)
- [Documentation](#documentation)
- [Contribuer](#contribuer)

## Le problème

Une Guitar Card est une partition de poche : une image avec quelques motifs (riffs) et une séquence de répétitions, par exemple :

```text
AA BBBB       deux fois A, puis quatre fois B
2A 4B         la même chose, en version compacte
{5A BB}x2     cinq A puis deux B, répétés deux fois
```

Pour en faire une vidéo de pratique, il faut suivre l'audio, retrouver le début de chaque motif, l'annoncer, compter les répétitions… et recommencer à chaque prise. C'est long, répétitif et source d'erreurs.

## Ce que fait l'application

**Préparer la carte**

- Importer une image (PNG, JPG, WebP…) et un fichier audio (MP3, WAV, FLAC…).
- Détecter la zone des motifs (ROI) et la couleur primaire de la carte, puis ajuster le cadrage à la main.
- Saisir la séquence avec une grammaire tolérante : `A`, `A#`, `a`, `¦4`, `|4`, `{5A BB}x2`, `Punkx2`…

**Synchroniser**

- Analyser l'audio pour proposer un alignement entre les motifs et la musique.
- Séparer la guitare du reste du mix (optionnel, via Demucs) pour affiner l'analyse.
- Ajuster la timeline à la main : tap-to-sync, saisie numérique, verrouillage des points clés.
- Lire les rapports d'analyse et les scores de confiance avant de valider.

**Animer et vérifier**

- Prévisualiser en temps réel : surbrillance du motif actif, annonce du suivant, compteurs de répétition.
- Personnaliser les couleurs, le halo, les fondus et le délai d'anticipation.
- Contrôler les diagnostics et les avertissements avant l'export.

**Exporter**

- Générer la vidéo finale avec l'audio synchronisé.
- Exporter les chapitres horodatés et un bloc de description YouTube.
- Sauvegarder et réutiliser les projets.

## État du projet

| Disponible aujourd'hui | En cours de développement |
|---|---|
| Fenêtre de démarrage PySide6 | Import image et audio |
| Socle `core/` sans dépendance Qt | Analyse de la ROI et grammaire |
| Outillage de qualité (ruff, mypy, pytest) | Analyse audio, synchronisation, rendu vidéo |

Les fonctionnalités ci-dessus décrivent la cible du produit ; elles ne sont pas toutes disponibles dans la version actuelle.

## Démarrage

### Prérequis

- [`uv`](https://docs.astral.sh/uv/) pour gérer Python et les dépendances
- Python 3.12 (installé automatiquement par `uv` si besoin)
- `ffmpeg` / `ffprobe` pour le rendu vidéo (à venir)

### Lancer l'application

```bash
git clone https://github.com/6i-software/guitar-card-motion-studio.git
cd guitar-card-motion-studio
uv sync
uv run python -m gcstudio
```

Une fenêtre « Guitar Card AI-Motion Studio » s'ouvre.

Si `uv` n'est pas disponible dans votre terminal, le venv créé par `uv sync` suffit :

```powershell
.\.venv\Scripts\python.exe -m gcstudio   # Windows
.venv/bin/python -m gcstudio             # macOS / Linux
```

### Séparation de sources (optionnel)

Demucs et PyTorch ne sont pas installés par défaut (plusieurs centaines de Mo) :

```bash
uv sync --extra ml
```

## Développement

```bash
uv run pytest                 # tests unitaires (Qt en mode offscreen)
uv run ruff check .           # lint
uv run ruff format --check .  # formatage
uv run mypy src/gcstudio/core # typage strict du cœur
```

Pour mesurer la couverture du cœur :

```bash
uv run pytest --cov=gcstudio.core --cov-report=term-missing
```

### Organisation du code

```text
src/gcstudio/
├── core/       # logique pure : grammaire, modèle, audio, synchro, rendu
├── services/   # orchestration, workers, chemins, logging (à venir)
└── ui/         # fenêtres et composants PySide6
```

`core/` ne dépend ni de Qt ni de `ui/` : il se teste sans interface graphique.

## Documentation

| Sujet | Fichier |
|---|---|
| Vision produit | [`docs/SPEC.md`](docs/SPEC.md) |
| Grammaire Guitar Card | [`docs/specs/spec-grammar-guitar-card.md`](docs/specs/spec-grammar-guitar-card.md) |
| Modèle de données | [`docs/specs/spec-data-model.md`](docs/specs/spec-data-model.md) |
| Image, audio et synchronisation | [`docs/specs/spec-audio-sequence-alignement.md`](docs/specs/spec-audio-sequence-alignement.md) |
| Interface et projets | [`docs/specs/spec-ui-project.md`](docs/specs/spec-ui-project.md) |
| Rendu vidéo | [`docs/specs/spec-render-video.md`](docs/specs/spec-render-video.md) |
| YouTube | [`docs/specs/spec-youtube.md`](docs/specs/spec-youtube.md) |

## Contribuer

Les contributions sont bienvenues via les issues et les pull requests. Avant de proposer un changement, consultez la spec du domaine concerné et vérifiez que les tests et le lint passent :

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src/gcstudio/core
```

## Licence

La licence du projet n'est pas encore définie.

---

**Vos images et vos audios restent sur votre machine.** Aucun envoi vers un service externe n'est effectué par l'application.
