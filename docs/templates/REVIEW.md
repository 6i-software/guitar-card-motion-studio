---
review_id: RV-T-XXXX-YYYYMMDD
task_id: T-XXXX
reviewer: code-reviewer
date: 2026-11-25
verdict: changes_requested   # approved | approved_with_nits | changes_requested | blocked
---

# Review — T-XXXX Titre

## 1. Périmètre reviewé

- Branche :
- Commit :
- Fichiers :
- Task card :

## 2. Verdict

`approved` | `approved_with_nits` | `changes_requested` | `blocked`

## 3. Findings

| # | Sévérité | Fichier:ligne | Finding | Suggestion |
|---|---|---|---|---|
| 1 | blocker | `...` | ... | ... |
| 2 | major | `...` | ... | ... |
| 3 | minor | `...` | ... | ... |
| 4 | nit | `...` | ... | ... |

Sévérités :
- **blocker** : correctness, invariant, sécurité, données, test manquant critique.
- **major** : risque de régression, contrat non respecté, perf significative.
- **minor** : lisibilité, test limite, documentation.
- **nit** : préférence, ne bloque pas.

## 4. Checklist

- [ ] Le code fait ce que la task card demande.
- [ ] I1-I12 respectés (intégrité, core pur, locked, etc.).
- [ ] Les critères d'acceptation sont réellement testés.
- [ ] Cas limites couverts.
- [ ] Pas de fichier hors `files_owned`.
- [ ] Pas de dépendance/secret/contenu protégé ajouté.
- [ ] Pas de régression de perf évidente.
- [ ] Tests déterministes, pas de réseau.

## 5. Points positifs

- ...

## 6. Tests suggérés

- ...
