---
description: Prend en charge une task card et la dispatche au bon agent
agent: orchestrator
---

Charge `docs/plan/tasks/$1.md`.

Vérifie : statut `ready`, dépendances `done`, `files_owned` sans chevauchement, questions bloquantes résolues, contrat gelé si nécessaire.

Si la DoR est incomplète, explique ce qui manque et ne lance rien. Sinon, dispatche la tâche au rôle `owner_role` avec la task card, les specs/contrats liés et les gates à exécuter. Demande un rapport `docs/reports/tasks/R-$1-YYYYMMDD.md` et un handoff.

Après le rapport : review indépendante, puis l'intégrateur crée la branche `task/$1-<slug>`, commite avec gitmoji + Conventional Commits (anglais), pousse la branche, ouvre la PR et merge en merge commit après gates. Voir `docs/agents/COMMITS.md`.
