# Contrats entre domaines

> **But :** permettre à plusieurs agents de travailler en parallèle sur des modules différents sans se lire mutuellement le code.
> **Règle :** un contrat est gelé avant l'implémentation d'une vague. Un changement breaking exige une décision.

---

## 1. Qu'est-ce qu'un contrat ?

Un contrat décrit :
- les **types** échangés (dataclasses/pydantic, pas d'implémentation) ;
- les **fonctions** publiques (signature, entrées, sorties, erreurs) ;
- les **invariants** (ce qui est toujours vrai) ;
- les **cas d'erreur** et diagnostics ;
- la **version** et les consommateurs.

Il ne décrit pas l'implémentation interne.

---

## 2. Cycle de vie

```
draft → review → frozen → deprecated → removed
```

- `draft` : en cours de rédaction, pas d'implémentation parallèle.
- `review` : les consommateurs relisent.
- `frozen` : implémentation autorisée ; changement = nouvelle version.
- `deprecated` : encore supporté, à migrer.
- `removed` : supprimé après migration.

---

## 3. Règles

1. Un contrat a un **propriétaire** (domaine) et des **consommateurs** listés.
2. Un contrat `frozen` ne change pas silencieusement : nouvelle version + décision + mise à jour des consommateurs.
3. Les agents codent contre le contrat, pas contre l'implémentation d'un autre agent.
4. Les mocks/stubs sont autorisés pour tester un consommateur avant que le producteur soit prêt.
5. Un contrat sans test de conformité est incomplet.
6. Les types doivent être importables sans Qt.

---

## 4. Contrats prévus

| Contrat | Domaine | Consommateurs | Statut |
|---|---|---|---|
| `core-grammar.md` | grammar | model, sync, ui, youtube | draft |
| `core-model.md` | model | projects, sync, render, ui | à créer |
| `services-jobs.md` | services | ui | à créer |
| `render-pipeline.md` | render | ui, services | à créer |
| `projects-store.md` | projects | ui, services | à créer |

---

## 5. Template

Voir `docs/templates/` et le contrat `core-grammar.md` comme exemple.
