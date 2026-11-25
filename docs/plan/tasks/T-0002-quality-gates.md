---
task_id: T-0002
title: Gates locales + scripts/ci.py
milestone: M0
wave: W0.1
status: ready
owner_role: integrator
depends_on: [T-0001]
blocks: [T-0004]
files_owned:
  - scripts/ci.py
  - tests/unit/test_ci.py
  - docs/agents/QUALITY_GATES.md
contracts: []
human_gate: false
estimated_hours: 4
created_at: 2026-11-25
updated_at: 2026-11-25
---

# T-0002 — Gates locales + `scripts/ci.py`

## 1. Contexte

Les gates sont définies dans `docs/agents/QUALITY_GATES.md`, mais les commandes sont dispersées. Il faut un runner unique, cross-platform, pour que les agents exécutent les mêmes vérifications.

## 2. Objectif

`uv run python scripts/ci.py --gate G1` (puis G2, G3, all) exécute les commandes de la gate, retourne un code de sortie fiable et un résumé lisible.

## 3. Périmètre

**In :**
- `scripts/ci.py` avec `--gate G1|G2|G3|all`, `--verbose`, `--dry-run`.
- Exécution via `subprocess` avec `sys.executable`/`uv run`.
- Agrégation des résultats, code de sortie non nul si échec.
- Mise à jour de `docs/agents/QUALITY_GATES.md` avec les commandes exactes.
- Tests unitaires du runner (mock de subprocess).

**Out :**
- CI GitHub Actions (le remote existe, mais le workflow sera ajouté dans une tâche dédiée).
- Build/packaging.
- Installation de dépendances.

## 4. Critères d'acceptation

- [ ] `--gate G1` exécute ruff check, ruff format --check, mypy core.
- [ ] `--gate G2` exécute pytest unit.
- [ ] `--gate G3` exécute pytest integration (skip propre si absent).
- [ ] `--gate all` enchaîne G1→G2→G3 et s'arrête au premier échec.
- [ ] Code de sortie 0 si tout passe, 1 sinon.
- [ ] Fonctionne sous Windows PowerShell et macOS/Linux (pas de `&&`, pas de chemin codé en dur).
- [ ] `--dry-run` affiche les commandes sans les exécuter.
- [ ] Tests du runner verts.

## 5. Plan de test

| Type | Fichier | Cas |
|---|---|---|
| Unitaire | `tests/unit/test_ci.py` | parse args, dry-run, échec, succès |
| Manuel | `uv run python scripts/ci.py --gate G1` | sur le dépôt |

## 6. Contrats

Aucun. Le script est un outil interne.

## 7. Risques

- Différences de shell Windows/Unix.
- `uv` absent de l'environnement : message clair, pas de stack trace.
- Ne pas masquer un échec par un `try/except` silencieux.

## 8. Notes de conception

- Utiliser `subprocess.run([...], check=False)` avec une liste d'arguments.
- Afficher la commande, la durée, le code de sortie.
- Résumé final : gate, statut, durée.
- Pas de dépendance externe (stdlib uniquement).

## 9. Definition of Done

- [ ] Critères couverts.
- [ ] G1 + G2 vertes.
- [ ] Rapport `R-T-0002-YYYYMMDD.md`.
- [ ] Review indépendante.
- [ ] Branche `task/T-0002-quality-gates` poussée et PR ouverte.
- [ ] `QUALITY_GATES.md` à jour.
- [ ] Handoff vers T-0004.
