# Guitar Card AI-Motion Studio

Application desktop nomade (Windows, macOS, Linux) qui transforme une **Guitar Card** et une piste audio en **vidéo synchronisée** : surbrillance du motif actif, annonce du motif suivant, compteurs de répétition, sans altérer les pixels hors de la zone des motifs (ROI).

> **État :** cadre de développement adopté (2026-11-25) ; scaffold M0 en place (T-0001).
> **Dépôt :** [github.com/6i-software/guitar-card-motion-studio](https://github.com/6i-software/guitar-card-motion-studio)

---

## 1. Documentation

| Sujet | Fichier |
|---|---|
| Vision produit | `docs/SPEC.md` |
| Grammaire Guitar Card | `docs/specs/spec-grammar-guitar-card.md` |
| Modèle de données | `docs/specs/spec-data-model.md` |
| Image, audio, sync | `docs/specs/spec-audio-sequence-alignement.md` |
| UI et projets | `docs/specs/spec-ui-project.md` |
| Rendu vidéo | `docs/specs/spec-render-video.md` |
| YouTube | `docs/specs/spec-youtube.md` |
| Questions ouvertes | `docs/OPEN_QUESTIONS.md` |
| Décisions | `docs/DECISIONS.md` |
| Lacunes spec | `docs/plan/SPEC_GAPS.md` |

## 2. Développement piloté par agents

| Sujet | Fichier |
|---|---|
| Constitution agents | `AGENTS.md` |
| Playbook | `docs/agents/PLAYBOOK.md` |
| Rôles | `docs/agents/ROLES.md` |
| Propriété des fichiers | `docs/agents/OWNERSHIP.md` |
| Gates | `docs/agents/QUALITY_GATES.md` |
| Comptes rendus | `docs/agents/REPORTING.md` |
| Commits et PR | `docs/agents/COMMITS.md` |
| Roadmap | `docs/plan/ROADMAP.md` |
| Backlog | `docs/plan/BACKLOG.md` |
| Itérations | `docs/plan/ITERATIONS.md` |
| Board | `docs/status/BOARD.md` |

## 3. Démarrage

Prérequis : [`uv`](https://docs.astral.sh/uv/) et Python 3.12 (épinglé par `.python-version`).

```bash
uv sync                       # crée .venv, installe runtime + outils dev
uv run python -m gcstudio     # ouvre la fenêtre « Guitar Card AI-Motion Studio »
uv run pytest                 # tests unitaires (Qt en mode offscreen)
uv run ruff check .           # lint
uv run ruff format --check .  # formatage
uv run mypy src/gcstudio/core # typage strict du cœur pur
```

Options :

```bash
uv sync --extra ml            # ajoute Demucs (PyTorch), non installé par défaut
uv run pytest -m "not slow"   # exclut les tests lents (ffmpeg, Demucs)
uv run pytest --cov=gcstudio.core --cov-report=term-missing
```

La fenêtre n'est qu'un point de départ : la logique métier arrive avec les vagues suivantes.

## 4. Workflow Git

- Une tâche = une branche `task/T-XXXX-slug`, une PR vers `main`, une review approuvée, un **merge commit**.
- Aucun commit direct sur `main` (exception : bootstrap initial).
- Commits en anglais avec **gitmoji** + Conventional Commits et `Refs: T-XXXX` : voir `docs/agents/COMMITS.md`.
- Seul l'intégrateur écrit dans Git ; il pousse les branches `task/*` et ouvre les PR, jamais `main`.

## 5. Prérequis de développement

- **`uv`** 0.13.10 ou plus récent (gestion des dépendances et de Python).
- **Python 3.12** géré par `uv` (3.12.16 installé le 2026-11-25). C'est le minimum imposé par `librosa` 1.x, `numpy` et `scipy` récents ; ne pas utiliser Python 3.14 (compatibilité PyTorch/Demucs non garantie).
- **ffmpeg/ffprobe** disponibles pour les tests d'intégration (ou binaires embarqués plus tard).
- Espace disque suffisant pour PyTorch + poids Demucs (plusieurs centaines de Mo à quelques Go).

> Environnement au 2026-11-25 : `uv` 0.13.10 et Python 3.12.16 installés. Le projet n'est pas encore scaffoldé (T-0001).

## 6. Principes

- **Hors ligne et portable** : aucun téléchargement à l'exécution.
- **Intégrité de l'image** : seule la ROI est modifiée.
- **L'humain décide** : les heuristiques proposent, l'utilisateur verrouille.
- **Cœur pur** : `core/` sans Qt, testable sans GUI.
- **UI jamais bloquée** : workers, progression, annulation.
- **Rapports graphiques** : `matplotlib` (backend Agg, hors thread UI) pour les rapports audio SVG/PNG.

## 7. Licence et données

Le dépôt ne doit pas contenir de secrets, de musique ou d'artwork protégé. Les exemples locaux sont hors Git (voir `docs/plan/SPEC_GAPS.md` Q15). Les licences tierces seront documentées dans `THIRD_PARTY_LICENSES.md`.
