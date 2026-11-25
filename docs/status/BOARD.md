# Board — Guitar Card AI-Motion Studio

> **Mis à jour :** 2026-11-25 (cadre complet adopté, GitHub connecté, W0.1 prêt à démarrer)
> **WIP limit :** 3 implémenteurs + 1 QA + 1 reviewer
> **Règle :** seul l'orchestrateur modifie ce fichier.

---

## 1. En cours

| ID | Titre | Rôle | Branche | Depuis | Rapport |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 2. En review / vérification

| ID | Titre | Rôle | Review | QA | Rapport |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 3. Prêt (ready)

| ID | Titre | Rôle | Dépend | Task card |
|---|---|---|---|---|
| T-0001 | Scaffold uv + hello world | platform-dev | — | `docs/plan/tasks/T-0001-scaffold.md` |
| T-0002 | Gates locales + `scripts/ci.py` | integrator | T-0001 | `docs/plan/tasks/T-0002-quality-gates.md` |
| T-0003 | Erreurs + logging | platform-dev | T-0001 | `docs/plan/tasks/T-0003-logging-errors.md` |
| T-0004 | Contrat grammar v0.2 | spec-analyst | T-0001 | `docs/plan/tasks/T-0004-grammar-contract.md` |
| T-0005 | Lexer | core-dev | T-0004 | `docs/plan/tasks/T-0005-lexer.md` |

## 4. Bloqué

| ID | Titre | Blocage | Question | Depuis |
|---|---|---|---|---|
| — | — | — | — | — |

## 5. Terminé (7 derniers jours)

| ID | Titre | Rôle | Merge | Rapport |
|---|---|---|---|---|
| — | — | — | — | — |

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

---

## 7. Prochaine action

1. Finaliser le commit bootstrap et pousser `main` sur GitHub.
2. Lancer W0.1 : T-0001 (platform-dev) sur `task/T-0001-scaffold`, puis T-0002 (integrator) et T-0003 (platform-dev).
3. Review + PR pour chaque tâche ; merge commit après gates.
4. Détailer W1.1 après la démo M0.
