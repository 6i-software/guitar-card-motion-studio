---
task_id: T-0001
title: Scaffold uv + fenêtre hello world
milestone: M0
wave: W0.1
status: ready
owner_role: platform-dev
depends_on: []
blocks: [T-0002, T-0003, T-0004]
files_owned:
  - pyproject.toml
  - uv.lock
  - .python-version
  - .gitignore
  - README.md
  - src/gcstudio/__init__.py
  - src/gcstudio/__main__.py
  - src/gcstudio/core/__init__.py
  - src/gcstudio/ui/__init__.py
  - src/gcstudio/ui/app.py
  - tests/unit/test_smoke.py
  - tests/unit/test_core_purity.py
  - tests/conftest.py
  - docs/reports/tasks/R-T-0001-*.md
contracts: []
human_gate: false
estimated_hours: 4
created_at: 2026-11-25
updated_at: 2026-11-25
---

# T-0001 — Scaffold uv + fenêtre hello world

## 1. Contexte

Le dépôt ne contient que des specs et des exemples. Il faut un projet Python installable, une fenêtre PySide6 minimale, et les outils de qualité (ruff, mypy, pytest) avant toute logique métier.

## 2. Objectif

`uv sync` puis `uv run python -m gcstudio` ouvre une fenêtre « Guitar Card AI-Motion Studio » ; `uv run pytest`, `ruff` et `mypy` passent.

## 3. Périmètre

**In :**
- `pyproject.toml` avec `requires-python = ">=3.12,<3.13"`, dépendances approuvées (dont `matplotlib>=3.11,<4` en runtime), extras dev (dont `pytest-cov`).
- Layout `src/gcstudio/`.
- `__main__.py` + fenêtre Qt minimale.
- `core/` vide mais importable, sans Qt.
- Config ruff, mypy strict sur `core/`, pytest.
- `.gitignore` (caches, builds, `.worktrees/`, binaires, exemples protégés à valider).
- README de démarrage (en français).
- Un test smoke + un test de pureté de `core/`.

**Out :**
- Toute logique métier (grammaire, audio, image, rendu).
- ffmpeg/Demucs.
- Packaging.
- CI distante.

## 4. Critères d'acceptation

- [ ] `uv sync` réussit sur Windows (et le lockfile est produit).
- [ ] `uv run python --version` affiche 3.12.x (Python épinglé par `.python-version`).
- [ ] `uv run python -m gcstudio` ouvre une fenêtre avec le titre attendu et se ferme proprement.
- [ ] `uv run pytest` passe (au moins 1 test).
- [ ] `uv run ruff check .` passe.
- [ ] `uv run ruff format --check .` passe.
- [ ] `uv run mypy src/gcstudio/core` passe.
- [ ] Un test vérifie qu'aucun module de `core/` n'importe `PySide6`.
- [ ] `README.md` contient les commandes de démarrage.

## 5. Plan de test

| Type | Fichier / commande | Cas |
|---|---|---|
| Smoke | `tests/unit/test_smoke.py` | import package, version |
| UI | `tests/unit/test_core_purity.py` | pas de Qt dans core |
| Manuel | `uv run python -m gcstudio` | fenêtre visible, fermeture |

## 6. Contrats

Aucun. Les contrats arrivent en T-0004.

## 7. Risques

- PySide6 est lourd ; vérifier le temps d'installation.
- `mypy --strict` sur un package vide peut nécessiter `py.typed` et une config minimale.
- Dépendances approuvées : `pytest-cov` en dev (`D7`), `matplotlib` en runtime pour les rapports (`D11`) ; pas de `scikit-learn`, `seaborn`, `plotnine`, `plotly`, `bokeh` ni `altair`.
- `librosa` 1.x exige Python ≥3.12 ; épingler `librosa>=1.0,<2` et smoke-tester l'API utilisée dès M3.
- Code, identifiants, commentaires, docstrings et noms de tests en **anglais** ; README et docs en **français** (`D14`).

## 8. Notes de conception

- Point d'entrée : `src/gcstudio/__main__.py` → `ui/app.py:main()`.
- `core/` ne contient qu'un `__init__.py` et éventuellement `errors.py` (T-0003).
- Pas de singleton global : la fenêtre est créée dans `main()`.
- Le titre de fenêtre peut être provisoire.

## 9. Definition of Done

- [ ] Critères d'acceptation couverts.
- [ ] G1 + G2 vertes.
- [ ] Rapport `docs/reports/tasks/R-T-0001-YYYYMMDD.md`.
- [ ] Review indépendante.
- [ ] Branche `task/T-0001-scaffold` poussée et PR ouverte (`D13`).
- [ ] Board mis à jour.
- [ ] README à jour.
- [ ] Handoff vers T-0002/T-0003.
