# Rapports d'exécution

> **Règle :** une tâche sans rapport n'est pas terminée. Un rapport sans preuve n'est pas un rapport.

---

## 1. Où écrire

| Type | Chemin | Auteur |
|---|---|---|
| Tâche | `docs/reports/tasks/R-T-XXXX-YYYYMMDD.md` | agent exécutant |
| Vague | `docs/reports/waves/W-YYYYMMDD-<slug>.md` | orchestrateur |
| Milestone | `docs/reports/milestones/M-<n>-<slug>.md` | orchestrateur + humain |
| Review | `docs/reports/reviews/RV-T-XXXX-YYYYMMDD.md` | code-reviewer |
| Release | `docs/releases/vX.Y.Z.md` | intégrateur |
| Incident | `docs/reports/incidents/I-YYYYMMDD-<slug>.md` | intégrateur |

---

## 2. Nommage

- `R-T-0005-20261126.md` : rapport de la tâche T-0005, le 26/11/2026.
- `W-20261128-grammar.md` : rapport de vague du 28/11/2026.
- `M-1-grammar.md` : rapport du milestone M1.
- `RV-T-0005-20261126.md` : review de T-0005.

Un rapport est **immuable**. Une correction se fait par addendum daté en fin de fichier.

---

## 3. Contenu minimal

- Résumé (3 puces).
- Fichiers changés.
- Commandes exécutées + résultats (pas « tests OK » sans preuve).
- Écarts par rapport à la task card.
- Décisions/questions.
- Risques et suites.
- Handoff (prochain agent, fichiers, points d'attention).

Template : `docs/templates/REPORT.md`.

---

## 4. Bonnes pratiques

- Écrire le rapport **avant** de rendre la main, pas après coup.
- Copier les commandes exactes.
- Distinguer exécuté / non exécuté (GPU, ffmpeg, OS absent).
- Ne jamais inclure de secret, token, chemin personnel ou contenu protégé.
- Un rapport `blocked` contient une question précise avec 2-3 options.
- Un rapport `partial` liste ce qui reste et propose les tasks de suite.

---

## 5. Index

Voir `docs/reports/INDEX.md` (mis à jour par l'orchestrateur en fin de vague).
