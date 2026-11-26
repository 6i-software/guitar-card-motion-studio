---
task_id: T-0003
title: Erreurs GCStudioException + logging rotatif
milestone: M0
wave: W0.1
status: ready
owner_role: platform-dev
depends_on: [T-0001]
blocks: [T-0004]
files_owned:
  - src/gcstudio/core/errors.py
  - src/gcstudio/core/logging.py
  - src/gcstudio/services/__init__.py
  - src/gcstudio/services/logging.py
  - src/gcstudio/services/paths.py
  - tests/unit/test_errors.py
  - tests/unit/test_logging.py
contracts: []
human_gate: false
estimated_hours: 4
created_at: 2026-11-25
updated_at: 2026-11-25
---

# T-0003 — Erreurs `GCStudioException` + logging rotatif

## 1. Contexte

Toutes les erreurs du cœur doivent hériter de `GCStudioException`. Les comptes rendus d'exécution exigent un log rotatif consultable, avec niveaux de verbosité, sans secret ni chemin personnel.

## 2. Objectif

Une hiérarchie d'erreurs claire, un format de message utilisateur + détail technique, et un logging rotatif dans le dossier de configuration de l'application.

## 3. Périmètre

**In :**
- `core/errors.py` : `GCStudioException` + sous-classes (`GrammarError`, `AudioError`, `ImageError`, `SyncError`, `RenderError`, `ProjectError`, `ExportError`, `ConfigError`).
- Chaque exception : `code`, `user_message` (FR), `technical_detail`, `cause`.
- `core/logging.py` : configuration pure (niveaux, format), sans Qt.
- `services/paths.py` : résolution des chemins via `QStandardPaths` (Qt autorisé ici).
- `services/logging.py` : handler rotatif, niveau configurable, pas de secret.
- Tests unitaires.

**Out :**
- UI de configuration du log.
- Télémétrie.
- Logs réseau.

## 4. Critères d'acceptation

- [ ] `GCStudioException` et ses sous-classes sont importables sans Qt.
- [ ] Chaque exception expose `code`, `user_message`, `technical_detail`.
- [ ] Un test vérifie qu'une exception non gérée produit un message utilisateur clair + un détail technique.
- [ ] Le log est écrit dans `QStandardPaths.AppLocalDataLocation`, avec rotation (taille max, backups).
- [ ] Le niveau est configurable (DEBUG/INFO/WARNING/ERROR).
- [ ] Aucun secret/token n'est loggé (test avec une valeur sentinelle).
- [ ] `core/` n'importe pas Qt (test existant).
- [ ] Tests verts sous Windows et Unix (chemins avec espaces).

## 5. Plan de test

| Type | Fichier | Cas |
|---|---|---|
| Unitaire | `tests/unit/test_errors.py` | hiérarchie, champs, cause |
| Unitaire | `tests/unit/test_logging.py` | rotation, niveau, sentinelle |
| Manuel | lancement + inspection du log | chemin, contenu |

## 6. Contrats

Aucun contrat inter-domaines à ce stade. Les erreurs seront utilisées par tous les modules.

## 7. Risques

- `QStandardPaths` nécessite une `QApplication` ; prévoir un fallback testable.
- Rotation Windows : fichier ouvert, ne pas verrouiller.
- Ne pas mettre de logique UI dans `core/logging.py`.

## 8. Notes de conception

- `core/errors.py` : dataclasses ou classes simples, pas de dépendance.
- `services/paths.py` : fonction `app_data_dir() -> Path`, injectable pour les tests.
- `services/logging.py` : `setup_logging(level, log_dir)` retourne un logger.
- Format : `%(asctime)s %(levelname)s %(name)s %(message)s`.
- Pas de singleton : le logger est passé/injecté.

## 9. Definition of Done

- [ ] Critères couverts.
- [ ] G1 + G2 vertes.
- [ ] Rapport `R-T-0003-YYYYMMDD.md`.
- [ ] Review indépendante.
- [ ] Branche `task/T-0003-logging-errors` poussée et PR ouverte.
- [ ] Handoff vers T-0004/T-0005.
