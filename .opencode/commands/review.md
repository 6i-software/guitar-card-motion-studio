---
description: Review indépendante d'une tâche
agent: code-reviewer
---

Review la tâche `$1` : lis la task card, le diff, les tests et les contrats concernés.

Vérifie dans l'ordre : correction, invariants I1-I12, tests, contrats, performance, sécurité/licences, périmètre.

Produis `docs/reports/reviews/RV-$1-YYYYMMDD.md` avec un verdict (`approved`, `approved_with_nits`, `changes_requested`, `blocked`) et des findings classés `blocker | major | minor | nit`, avec fichier:ligne.
