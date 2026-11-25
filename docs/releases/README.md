# Notes de release

> **Règle :** une release = un fichier `vX.Y.Z.md`, un tag, un changelog à jour, un test machine vierge si packaging.

---

## 1. Convention

- Fichier : `docs/releases/vX.Y.Z.md`.
- Version SemVer : `MAJOR.MINOR.PATCH`.
- Tag Git : `vX.Y.Z` (validation humaine).
- Changelog : `CHANGELOG.md`, sections Added/Changed/Fixed/Removed/Security.

## 2. Contenu

```markdown
# vX.Y.Z — YYYY-MM-DD

## Résumé
...

## Ajouté
- ...

## Modifié
- ...

## Corrigé
- ...

## Sécurité / licences
- ...

## Migration
- ...

## Vérifications
- [ ] G1-G5
- [ ] Build machine vierge
- [ ] Tests de fumée
```

## 3. Checklist

- [ ] Suite complète verte.
- [ ] Gates G1-G5.
- [ ] Changelog à jour.
- [ ] `THIRD_PARTY_LICENSES.md` à jour.
- [ ] Build testé sur machine vierge.
- [ ] Notes de release.
- [ ] Tag (validation humaine).
- [ ] Rapport de release.

## 4. Hotfix

- Branche `hotfix/<version>-<slug>`.
- Fix minimal + test de non-régression.
- Release patch immédiate.
- Rapport d'incident dans `docs/reports/incidents/`.
