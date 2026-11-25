---
task_id: T-0004
title: Contrat core/grammar v0.2
milestone: M1
wave: W1.1
status: ready
owner_role: spec-analyst
depends_on: [T-0001]
blocks: [T-0005, T-0008]
files_owned:
  - docs/contracts/core-grammar.md
  - docs/specs/spec-grammar-guitar-card.md
  - docs/plan/tasks/T-0005-lexer.md
contracts: [core-grammar]
human_gate: true
estimated_hours: 3
created_at: 2026-11-25
updated_at: 2026-11-25
---

# T-0004 — Contrat `core/grammar` v0.2

## 1. Contexte

Le lexer, le parser, l'expansion et les consommateurs (sync, UI, YouTube) doivent partager les mêmes types et invariants. La spec grammar est précise mais comporte encore des cas ouverts (Q3, Q8). Q4-Q7 et Q35 sont résolues par `D10`, `D12` et `D15`.

## 2. Objectif

Un contrat `docs/contracts/core-grammar.md` **gelé v0.2** pour W1.1 : API, types, invariants, diagnostics, cas de test, points ouverts.

## 3. Périmètre

**In :**
- Relire `docs/specs/spec-grammar-guitar-card.md`.
- Aligner l'EBNF et les exemples sur `D10`/`D12`/`D15` (noms, `^INT`, préfixe de groupe, ordre des modificateurs).
- Formaliser `tokenize`, `parse`, `expand`, `Span`, `Diagnostic`, `Token`, `Occurrence`, `GroupRef`.
- Lister les invariants et les codes de diagnostic.
- Lister les tests de conformité (golden, property, cas d'erreur).
- Trancher Q3 et Q8 avec l'humain.
- Mettre à jour `T-0005-lexer.md` si le contrat change son périmètre.

**Out :**
- Implémentation.
- Choix définitif sur Q3/Q8 sans validation humaine.

## 4. Critères d'acceptation

- [ ] Le contrat contient l'API, les types, les invariants, les codes de diagnostic.
- [ ] Les 4 golden et les cas `Punkx2`, `Punk2`, `{5A BB}x2`, `AAA`, `AA#`, `bbbb#` sont listés.
- [ ] Les cas d'erreur (groupe non fermé, multiplicateur incomplet, caractère inconnu, `A2`) sont listés.
- [ ] Les points ouverts Q3 et Q8 sont explicitement marqués comme bloquants ou non.
- [ ] Le contrat est reviewé par `core-dev` et `qa-verifier`.
- [ ] Validation humaine obtenue (`human_gate: true`).

## 5. Plan de test

Pas de test code. Vérification : relecture croisée spec ↔ contrat ↔ task cards.

## 6. Contrats

C'est la tâche de contrat. Elle produit `core-grammar.md` v0.2.

## 7. Risques

- Le contrat fige une interprétation erronée de Q3/Q8 → le lexer devra être refait.
- Un contrat trop détaillé devient une implémentation déguisée.

## 8. Notes de conception

- Rester au niveau interface : pas de pseudocode exhaustif.
- Distinguer `draft` et `frozen` ; ne geler que ce qui est certain.
- Les points ouverts doivent avoir une option par défaut **provisoire** clairement marquée, pour ne pas bloquer W1.1 si l'humain tarde.

## 9. Definition of Done

- [ ] Contrat complet et reviewé.
- [ ] Q3/Q8 documentées avec recommandation ; Q4-Q7/Q35 pointent vers D10/D12/D15.
- [ ] Validation humaine.
- [ ] Rapport `R-T-0004-YYYYMMDD.md`.
- [ ] Handoff vers T-0005 et T-0008.
