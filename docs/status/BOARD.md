# Board — Guitar Card AI-Motion Studio

> **Mis à jour :** 2026-11-26 (T-0001 mergé, W0.1 en cours)
> **WIP limit :** 3 implémenteurs + 1 QA + 1 reviewer
> **Règle :** seul l'orchestrateur modifie ce fichier.

---

## 1. En cours

| ID | Titre | Rôle | Branche | Depuis | Rapport |
|---|---|---|---|---|---|
| T-0002 | Gates locales + `scripts/ci.py` | integrator | `task/T-0002-quality-gates` | 2026-11-26 | — |
| T-0003 | Erreurs + logging | platform-dev | `task/T-0003-logging-errors` | 2026-11-26 | — |

## 2. En review / vérification

| ID | Titre | Rôle | Review | QA | Rapport |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 3. Prêt (ready)

| ID | Titre | Rôle | Dépend | Task card |
|---|---|---|---|---|
| T-0004 | Contrat grammar v0.2 | spec-analyst | T-0001 (Q3/Q8 tranchées) | `docs/plan/tasks/T-0004-grammar-contract.md` |
| T-0005 | Lexer | core-dev | T-0004 | `docs/plan/tasks/T-0005-lexer.md` |

## 4. Bloqué

| ID | Titre | Blocage | Question | Depuis |
|---|---|---|---|---|
| — | — | — | — | — |

## 5. Terminé (7 derniers jours)

| ID | Titre | Rôle | Merge | Rapport |
|---|---|---|---|---|
| T-0001 | Scaffold uv + hello world | platform-dev | `97d1439` (PR #1) | `docs/reports/tasks/R-T-0001-20261125.md` |

---

## 6. Décisions humaines

### En attente

| ID | Sujet | Impact | Recommandation |
|---|---|---|---|
| — | — | — | — |

### Résolues

| ID | Sujet | Décision | Date |
|---|---|---|---|
| H-0001 | Mode de travail | Mode **A — cadre complet** adopté | 2026-11-25 |
| H-0002 | Dépendances | `D7` + `D11` : `pytest-cov` en dev, `matplotlib` en runtime ; pas de `scikit-learn` | 2026-11-25 |
| H-0003 | Exemples protégés | `D8` : hors Git + fixtures synthétiques | 2026-11-25 |
| H-0004 | Python/OS | Python 3.12 ; Win10+/macOS12+/Ubuntu22.04+ | 2026-11-25 |
| H-0005 | Sortie YouTube | `D9` : `output/description-youtube.txt`, configurable | 2026-11-25 |
| H-0006 | Environnement | `uv` 0.13.10 + Python 3.12.16 installés | 2026-11-25 |
| H-0007 | Remote Git | GitHub : `6i-software/guitar-card-motion-studio` (`D13`) | 2026-11-25 |
| H-0008 | Q4/Q7/Q35 | `D12` + `D15` : `Punk2` = nom, `a` = motif distinct, `A^n` canonique | 2026-11-25 |
| H-0009 | Git workflow | `D6` + `D13` : branche `task/*`, PR, merge commit | 2026-11-25 |
| H-0010 | Langues/commits | `D14` : docs FR, code/commits EN, gitmoji obligatoire | 2026-11-25 |
| H-0011 | Force push | `D16` : `git push --force*` / `-f*` en `ask` (confirmation humaine), garde-fous tags/reset conservés | 2026-11-26 |
| H-0012 | Grammar Q3/Q8 | `D17` + `D18` : `¦`/`\|` = motif générique ; compteurs de groupe via `group_path` riche | 2026-11-26 |

---

## 7. Prochaine action

1. Implémenter T-0002 (integrator) et T-0003 (platform-dev) en parallèle ; review + PR + merge commit pour chacune.
2. Lancer T-0004 (spec-analyst) : contrat grammar v0.2 avec Q3 (`D17`) et Q8 (`D18`) tranchées, review `core-dev` + `qa-verifier`, validation humaine.
3. Détailer W1.1 après la démo M0.
