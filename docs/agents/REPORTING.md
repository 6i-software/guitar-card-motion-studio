# Comptes rendus d'exécution

> **Statut :** adopté (2026-11-25)
> **Règle :** une tâche sans rapport n'est pas terminée. Un rapport sans preuve n'est pas un rapport.

---

## 1. Pourquoi des rapports

Les rapports servent à :
- **prouver** ce qui a été fait et testé (pas seulement déclaré) ;
- **transmettre** le contexte au prochain agent sans rejouer la session ;
- **tracer** les écarts, décisions et questions ;
- **alimenter** le board, les métriques et le changelog ;
- **auditer** une régression ou une décision.

Un rapport est **court** (1 page), **daté**, **immuable**. Une correction se fait par addendum daté, jamais en réécrivant.

---

## 2. Types et emplacements

| Type | Fichier | Auteur | Fréquence |
|---|---|---|---|
| Tâche | `docs/reports/tasks/R-T-XXXX-YYYYMMDD.md` | agent exécutant | à chaque tâche |
| Vague | `docs/reports/waves/W-YYYYMMDD-<slug>.md` | orchestrateur | fin de vague |
| Milestone | `docs/reports/milestones/M-<n>-<slug>.md` | orchestrateur + humain | fin de milestone |
| Review | `docs/reports/reviews/RV-T-XXXX-YYYYMMDD.md` | code-reviewer | à chaque review |
| Release | `docs/releases/vX.Y.Z.md` | intégrateur | à chaque release |
| Incident | `docs/reports/incidents/I-YYYYMMDD-<slug>.md` | intégrateur | si incident |

---

## 3. Format d'un rapport de tâche

Le template complet est `docs/templates/REPORT.md`. Structure minimale :

```markdown
---
report_id: R-T-0005-20261126
task_id: T-0005
agent: core-dev
role: core-dev
started_at: 2026-11-26T09:00:00+01:00
finished_at: 2026-11-26T12:30:00+01:00
status: done            # done | partial | blocked | failed
branch: task/T-0005-lexer
commit: abc1234          # gitmoji + Conventional Commits, anglais
pr: 12                   # pull request GitHub
gates:
  G1: pass
  G2: pass
  G3: n/a
files_changed:
  - src/gcstudio/core/grammar/lexer.py
  - tests/unit/grammar/test_lexer.py
tests_added: 12
coverage_core: 87.4
open_questions: []
decisions_requested: []
---

# Rapport — T-0005 Lexer

## 1. Résumé
- ...

## 2. Ce qui a changé
...

## 3. Vérifications
| Commande | Résultat | Preuve |
|---|---|---|
| `uv run pytest tests/unit/grammar -q` | 12 passed | ... |
| `uv run ruff check ...` | OK | ... |

## 4. Écarts par rapport au plan
...

## 5. Décisions / questions
...

## 6. Risques et suites
...

## 7. Handoff
- Prochain agent :
- Fichiers à lire :
- Points d'attention :
```

---

## 4. Règles de contenu

### 4.1 Résumé
3 puces maximum : résultat, preuve principale, point d'attention.

### 4.2 Vérifications
- Copier les commandes exactes.
- Indiquer le résultat (nombre de tests, durée, code de sortie).
- Ne pas écrire « tests OK » sans commande.
- Distinguer **exécuté** et **non exécuté** (ex. GPU absent, ffmpeg absent).

### 4.3 Écarts
Tout écart par rapport à la task card : fichier non prévu, test non fait, comportement différent, dépendance ajoutée. Un écart non documenté est un `blocker` de review.

### 4.4 Décisions / questions
- Une décision structurante ne se prend pas dans le rapport : elle se **propose**.
- Une question bloquante reçoit un ID `Q*` et un statut `Bloquant`.
- Ne jamais inventer une réponse pour « avancer ».

### 4.5 Handoff
5 lignes max : état, fichiers, points d'attention, prochaine action, personne/agent cible.

---

## 5. Statuts

| Statut | Signification | Suite |
|---|---|---|
| `done` | Tous les critères + gates | Review/merge |
| `partial` | Une partie faite, le reste est une nouvelle tâche | Découper, ne pas merger en l'état |
| `blocked` | Impossible de continuer sans décision | Escalade, board `blocked` |
| `failed` | Tentative abandonnée | Rapport + cause + nouvelle approche |

Un rapport `partial` doit lister précisément ce qui reste et créer les task cards de suite (ou les proposer).

---

## 6. Board et index

- `docs/status/BOARD.md` : état temps réel, mis à jour par l'orchestrateur à chaque transition.
- `docs/reports/INDEX.md` : index des rapports, mis à jour par l'orchestrateur en fin de vague.
- `docs/status/METRICS.md` : métriques agrégées, mises à jour par l'orchestrateur.

Le board contient au minimum : ID, titre, milestone, vague, rôle, statut, branche, rapport, dernière mise à jour.

---

## 7. Cadence de communication

| Moment | Message | Destinataire |
|---|---|---|
| Début de tâche | « T-XXXX claimed, branche ..., plan en 5 lignes » | board |
| Blocage | Rapport `blocked` + question | orchestrateur + humain |
| Fin de tâche | Rapport + handoff | orchestrateur |
| Fin de vague | Rapport de vague + démo | humain |
| Fin de milestone | Rapport de milestone + métriques | humain |
| Release | Notes de release + changelog | humain |

**Digest quotidien (optionnel) :** l'orchestrateur peut générer un résumé de 10 lignes à partir du board et des rapports du jour. Aucune automatisation n'est créée sans validation.

---

## 8. Exemple de rapport de vague

```markdown
# Vague W1.1 — Grammaire

## Objectif
Contrat grammar gelé + lexer + tests golden.

## Résultat
- T-0004 done (contrat v0.1)
- T-0005 done (lexer, 42 tests)
- T-0008 partial (golden 3/4, cas `Punkx2` bloqué par Q4)

## Gates
- G1 OK
- G2 OK (128 tests)
- G3 partiel (golden manquant)

## Décisions / questions
- Q4 `Punk2` toujours ouverte, bloque le 4e golden.

## Risques
- Le lexer devra être rouvert si Q4 change la priorité des suffixes.

## Prochaine vague
W1.2 parser/AST, dépend de Q4.
```

---

## 9. Anti-patterns

- Rapport rédigé après coup, sans commandes.
- « Tout est vert » sans preuve.
- Rapport qui réécrit l'histoire ou masque un échec.
- Rapport de 10 pages : ce n'est pas un rapport, c'est un journal.
- Handoff « à suivre » sans fichier ni point d'attention.
- Board mis à jour par tout le monde : conflits garantis.
