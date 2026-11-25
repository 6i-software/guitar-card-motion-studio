---
description: Planifie et dispatche une vague
agent: orchestrator
---

Planifie la vague `$1` à partir de `docs/plan/ROADMAP.md` et `docs/plan/BACKLOG.md`.

Produis :
1. l'objectif démontrable de la vague ;
2. la liste des tasks avec rôle, dépendances et `files_owned` ;
3. la vérification d'absence de chevauchement ;
4. l'ordre de dispatch et le WIP limit ;
5. les gates de sortie et la démo ;
6. le flux Git : une branche `task/T-XXXX-slug` et une PR par tâche, merge commit après review.

Si une task n'est pas `ready`, garde-la `proposed` et explique ce qui manque. Ne détaille que cette vague ; ne planifie pas les suivantes.
