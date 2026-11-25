# Conventions de commit, branches et pull requests

> **Statut :** adopté (2026-11-25, `D13` et `D14`)
> **Portée :** tout agent ou humain qui écrit dans Git.
> **Règle d'or :** un commit = un changement logique, en anglais, avec un gitmoji et une référence de tâche.

---

## 1. Format obligatoire

```text
<gitmoji> <type>(<scope>): <subject>

<body>

<footer>
```

### Règles

- **Gitmoji obligatoire** en premier caractère, suivi d'une espace.
- **Type** : `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`, `security`, `merge`.
- **Scope** : court, en anglais, en minuscules (`grammar`, `model`, `audio`, `sync`, `render`, `ui`, `services`, `deps`, `repo`, `agents`).
- **Subject** : anglais, impératif, minuscule, sans point final, ≤ 72 caractères.
- **Body** : anglais, explique le *pourquoi*, pas le *comment*. Lignes ≤ 72 caractères.
- **Footer** : `Refs: T-XXXX` obligatoire pour une tâche. `BREAKING CHANGE: ...` si rupture de contrat/schéma.
- Un commit ne doit pas mélanger feature, refactor et formatage.
- Pas de `wip`, `update`, `fix again`, `final`.
- Ne jamais committer de secret, de média protégé, de build ou de cache.
- **Encodage** : écrire le message dans un fichier UTF-8 puis `git commit -F <fichier>`. Les here-strings PowerShell peuvent remplacer les emojis par `??`.

### Exemples

```text
✨ feat(grammar): parse variant exponents as motif keys

Normalize A# to A^1 and A## to A^2 so the model has one
canonical key per variant.

Refs: T-0005
```

```text
🐛 fix(sync): preserve locked events on recompute

Refs: T-0021
```

```text
📝 docs(agents): adopt the full agentic framework

Refs: T-0001
```

```text
🎉 chore(repo): bootstrap repository and agentic framework
```

```text
🔀 chore(merge): integrate T-0001 scaffold

Refs: T-0001
```

---

## 2. Gitmoji de référence

| Gitmoji | Type | Usage |
|---|---|---|
| 🎉 | `chore` | Premier commit / bootstrap |
| ✨ | `feat` | Nouvelle fonctionnalité |
| 🐛 | `fix` | Correction de bug |
| 🩹 | `fix` | Correctif mineur |
| 🚑️ | `fix` | Correctif critique / hotfix |
| 📝 | `docs` | Documentation |
| ✅ | `test` | Tests ajoutés ou corrigés |
| ♻️ | `refactor` | Refactor sans changement de comportement |
| 🎨 | `style` | Formatage, structure, pas de logique |
| ⚡️ | `perf` | Performance |
| 🔧 | `chore` | Configuration, outillage |
| 🚀 | `ci` | CI/CD, déploiement |
| 📦️ | `build` | Dépendances, packaging |
| 🔒️ | `security` | Sécurité |
| 🔥 | `chore` | Suppression de code/fichiers |
| 🏗️ | `refactor` | Architecture |
| 💚 | `ci` | Réparation de la CI |
| ⏪️ | `revert` | Annulation |
| 🔀 | `merge` | Merge de branche/PR |
| 📌 | `chore` | Épinglage de version |
| 🗑️ | `chore` | Dépréciation |

> En cas de doute, choisir le gitmoji qui décrit **l'intention** du commit, pas le fichier touché.

---

## 3. Branches

| Type | Convention | Exemple |
|---|---|---|
| Tâche | `task/<ID>-<slug>` | `task/T-0001-scaffold` |
| Feature | `feat/<slug>` | `feat/roi-manual-editor` |
| Fix | `fix/<ID>-<slug>` | `fix/T-0042-locked-event` |
| Hotfix | `hotfix/<version>-<slug>` | `hotfix/0.3.1-export-crash` |
| Vague | `wave/<n>-<slug>` | `wave/W1.1-grammar` |

- Une branche part de `main` à jour.
- Le slug est en anglais, en minuscules, avec des tirets.
- Une branche = une tâche = une PR.
- Après merge, la branche est supprimée.

---

## 4. Pull requests

### Création

1. L'intégrateur pousse la branche : `git push -u origin task/<ID>-<slug>`.
2. Il ouvre une PR vers `main` (GitHub CLI `gh pr create`, ou l'URL de comparaison fournie par GitHub).
3. Titre de PR : même format que le commit principal, gitmoji inclus.
4. Description :

```markdown
## Summary
- ...

## Tests
- `uv run pytest ...`
- `uv run ruff check .`
- `uv run mypy ...`

## Risks
- ...

## Checklist
- [ ] Task card respectée (`files_owned`)
- [ ] Rapport `docs/reports/tasks/R-T-XXXX-YYYYMMDD.md`
- [ ] Review approuvée
- [ ] Gates G1/G2 (G3 si intégration)
- [ ] Aucun secret, média protégé ou fichier généré

Refs: T-XXXX
```

### Merge

- **Merge commit obligatoire** (« Create a merge commit »). Jamais squash, jamais rebase.
- La PR doit avoir une review approuvée et les gates vertes.
- L'intégrateur merge, supprime la branche distante et locale, puis met à jour le board.
- `main` reste protégée : aucun commit direct, aucun force push, aucun tag sans validation humaine.

### Exception bootstrap

Le tout premier commit sur `main` (création du dépôt) est la seule exception. Il doit être poussé une fois par l'humain ou par l'intégrateur avec validation humaine, puis la règle PR s'applique sans exception.

---

## 5. Langues

| Élément | Langue |
|---|---|
| `docs/**/*.md`, `README.md`, `CHANGELOG.md` | Français |
| Code, identifiants, noms de fichiers, commentaires, docstrings | Anglais |
| Noms de tests, branches, commits, PR | Anglais |
| Chaînes UI visibles | Français par défaut via i18n |

Un message de commit en français est refusé. Une documentation produit en anglais est refusée sans décision explicite.

---

## 6. Checklist avant commit

- [ ] Le changement est unique et cohérent.
- [ ] Le message respecte `<gitmoji> <type>(<scope>): <subject>`.
- [ ] Le message est en anglais, à l'impératif.
- [ ] `Refs: T-XXXX` est présent.
- [ ] Les fichiers générés/caches/médias sont ignorés.
- [ ] Les gates G1/G2 sont vertes (ou le rapport explique pourquoi).
- [ ] Aucun fichier hors `files_owned` n'est modifié sans justification.
