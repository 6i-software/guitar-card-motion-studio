# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Cadre de développement agentique : `AGENTS.md` v2, playbook, rôles, carte de propriété, gates, reporting, roadmap, backlog, itérations.
- Templates de task card, rapport, review, feature, bug et rapport de vague.
- Board et métriques initiales.
- Contrat `core/grammar` v0.1 (draft).
- Configuration OpenCode : agents, commandes, permissions.
- Matrice de tests par milestone (`docs/plan/TEST_MATRIX.md`).
- Environnement de développement : `uv` 0.13.10 et Python 3.12.16.
- Conventions de commit, branches et PR (`docs/agents/COMMITS.md`).
- Dépôt GitHub `6i-software/guitar-card-motion-studio`.

### Changed

- `AGENTS.md` scindé en constitution courte + documents de playbook ; v1 remplacée (archive non conservée).
- Cible Python portée à **3.12** (exigence de librosa 1.x et numpy/scipy récents).
- Workflow Git : branche par tâche, PR obligatoire, merge commit, push de `main` réservé au bootstrap (`D6` + `D13`).
- Dépendances v1 : `pytest-cov` en dev, `matplotlib` en runtime pour les rapports (`D7` + `D11`) ; pas de `scikit-learn`.
- Exemples protégés exclus de Git ; fixtures synthétiques pour la CI (`D8`).
- Description YouTube écrite dans `output/description-youtube.txt` par défaut (`D9`).
- Grammaire : multiplicateurs `x<INT>`/préfixes, noms (`Punk2`), variantes `A^n` et cumul de modificateurs (`D10` + `D15`).
- Motifs : `a` est un riff distinct rattaché à la famille `A` (`D12`).
- Langues : documentation produit en français ; code, identifiants, commentaires et commits en anglais (`D14`).
- Commits : gitmoji obligatoire + Conventional Commits (`D14`).

### Fixed

- `docs/OPEN_QUESTIONS.md` : Q1/Q2 documentées, Q4/Q5/Q6/Q7/Q11/Q15/Q16/Q35 résolues.
- `docs/DECISIONS.md` : D1–D15 cohérentes.
- `docs/contracts/core-grammar.md` : révision après D10/D12/D15 (noms, variantes, familles, diagnostics 008–011).

### Notes

- Aucun code applicatif n'est encore présent ; le scaffold est planifié en M0 (T-0001).
