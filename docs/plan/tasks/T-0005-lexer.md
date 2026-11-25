---
task_id: T-0005
title: Lexer + spans + multiplicateurs
milestone: M1
wave: W1.1
status: ready
owner_role: core-dev
depends_on: [T-0004]
blocks: [T-0006, T-0008]
files_owned:
  - src/gcstudio/core/grammar/**
  - tests/unit/grammar/test_lexer.py
  - tests/unit/grammar/test_spans.py
contracts: [core-grammar]
human_gate: false
estimated_hours: 6
created_at: 2026-11-25
updated_at: 2026-11-25
---

# T-0005 — Lexer + spans + multiplicateurs

## 1. Contexte

Le lexer est la première brique de la grammaire. Il doit être tolérant, préserver les spans, et appliquer la priorité du multiplicateur `x<INT>`.

## 2. Objectif

`tokenize(source)` produit une liste de tokens typés avec spans, sans jamais lever d'exception sur une entrée utilisateur.

## 3. Périmètre

**In :**
- Tokens : lettres, modificateurs `#`/`~`, exposant `^`, symboles `¦`/`|`, chiffres, accolades, `x`, espaces/newlines.
- Priorité `x<INT>` : `Punkx2` = `Punk` + `x2`, jamais `Punkx` + `2`.
- Noms : `Punk2` est un token `NAMED_MOTIF` (le chiffre sans `x` fait partie du nom) ; `A2` produit `A` + `2` + diagnostic `GC-GRAM-008`.
- Variantes : `A^2` produit `A` + `^2` ; `A#` reste un token modificateur normalisé plus tard.
- Spans corrects (code points), y compris accents/Unicode.
- Tokens inconnus + diagnostic.
- Tests unitaires ciblés.

**Out :**
- Parser/AST (T-0006).
- Expansion (T-0007).
- Golden complets (T-0008).

## 4. Critères d'acceptation

- [ ] `tokenize("AAA")` → 3 tokens `A`.
- [ ] `tokenize("AA#")` → `A`, `A#`.
- [ ] `tokenize("bbbb#")` → `b`, `b`, `b`, `b#`.
- [ ] `tokenize("Punkx2")` → `Punk`, `x2` (ou token multiplicateur équivalent).
- [ ] `tokenize("Punk x2")` → même sortie sémantique que `Punkx2`.
- [ ] `tokenize("Punk2")` → un seul token `NAMED_MOTIF("Punk2")`.
- [ ] `tokenize("A2")` → `A`, `2` + diagnostic `GC-GRAM-008`.
- [ ] `tokenize("A^2~")` → `A`, `^2`, `~`.
- [ ] `tokenize("¦4|4")` → `¦4`, `|4`.
- [ ] Les spans sont corrects pour une chaîne avec accents/emoji.
- [ ] `tokenize("@")` → token inconnu + diagnostic `GC-GRAM-001`, pas d'exception.
- [ ] Aucun import Qt.
- [ ] Tests verts.

## 5. Plan de test

| Type | Fichier | Cas |
|---|---|---|
| Unitaire | `test_lexer.py` | lettres, modificateurs, symboles, multiplicateurs, inconnus |
| Unitaire | `test_spans.py` | offsets, Unicode, espaces |
| Property | `test_lexer_property.py` (si T-0008 prêt) | pas de crash |

## 6. Contrats

`core-grammar.md` v0.2. Ne pas modifier le contrat sans passer par T-0004.

## 7. Risques

- Q4/Q6 sont tranchées (`D15`) : `Punk2` est un nom, `A##` ≡ `A^2`. Le lexer doit isoler la logique de suffixe/exposant.
- `A2` doit rester une erreur locale, pas une répétition silencieuse.
- Unicode : utiliser les indices Python, pas les bytes.

## 8. Notes de conception

- Un token par élément lexical, avec `Span`.
- Le lexer ne décide pas de la sémantique du multiplicateur ; il produit un token `MULTIPLIER` avec la valeur.
- Les espaces sont des tokens `SPACE`/`NEWLINE` ou ignorés mais les spans restent dans les tokens utiles.
- Diagnostic localisé, message en français.
- Pas de dépendance externe.

## 9. Definition of Done

- [ ] Critères couverts.
- [ ] G1 + G2 vertes.
- [ ] Rapport `R-T-0005-YYYYMMDD.md`.
- [ ] Review indépendante.
- [ ] Branche `task/T-0005-lexer` poussée et PR ouverte.
- [ ] Handoff vers T-0006/T-0008.
