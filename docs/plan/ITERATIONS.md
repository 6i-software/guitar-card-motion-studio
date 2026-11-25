# Itérations, features, correctifs et releases

> **Statut :** adopté (2026-11-25, cadre complet)
> **But :** organiser les itérations après le MVP (M0–M10) sans casser le cadre agentique.

---

## 1. Trois boucles

| Boucle | Durée | Objectif | Sortie |
|---|---|---|---|
| Milestone | 1–3 semaines | Construire une capacité du MVP | Démo + tag `v0.x.0-mN` |
| Feature | 1–5 jours | Ajouter/modifier une capacité | Spec delta + tasks + release |
| Correctif | heures–2 jours | Réparer un comportement | Test de régression + patch |

Le flux est **continu** : pas de sprint cérémoniel. Une release est décidée quand un ensemble cohérent est prêt, pas à date fixe.

---

## 2. Feature : du besoin à la release

```
Demande
  → triage (valeur, urgence, alignement)
  → feature brief (F-XXX)
  → impact analysis
  → décision (D*) si structurant
  → task cards (T-XXXX)
  → vague
  → démo
  → release
  → rétro
```

### 2.1 Triage

Critères :
- **Valeur utilisateur** : quel problème, pour qui ?
- **Alignement** : specs, vision, invariants.
- **Coût** : tâches, risques, dépendances.
- **Urgence** : bloquant, important, nice-to-have.
- **Décision** : `now`, `next`, `later`, `rejected`.

Une demande sans problème utilisateur clair est rejetée ou mise en attente.

### 2.2 Feature brief

Template : `docs/templates/FEATURE.md`. Contient :
- problème, comportement attendu, hors scope ;
- critères d'acceptation ;
- impact architecture/modèle/grammaire/UI/audio/rendu/perf/tests/docs/licences ;
- décisions nécessaires ;
- découpage proposé ;
- démo.

### 2.3 Impact analysis

Checklist obligatoire :

| Domaine | Questions |
|---|---|
| Architecture | Nouveau module ? Nouvelle dépendance ? Contrat modifié ? |
| Modèle | Nouveau champ ? Migration ? Compatibilité ? |
| Grammaire | Nouveau token ? Nouvelle priorité ? Golden impactés ? |
| UI | Nouvel écran ? Navigation ? i18n ? Accessibilité ? |
| Audio/sync | Nouvel algorithme ? Confiance ? Locked ? |
| Rendu/export | Nouvel overlay ? Perf ? Intégrité ? Codec ? |
| Tests | Quels tests, fixtures, ground truth ? |
| Docs | Specs, README, changelog, aide ? |
| Licences | Nouveau binaire/modèle/donnée ? |

### 2.4 Décision

Une décision (`D*`) est requise si :
- changement de schéma projet ;
- changement de grammaire ;
- changement d'algorithme de rendu ou de l'invariant I1 ;
- nouvelle dépendance/binaire/modèle ;
- changement d'architecture (frontière, threading, stockage) ;
- changement de contrat breaking.

La décision est rédigée dans `DECISIONS.md` avec contexte, options, conséquences, alternatives.

### 2.5 Découpage

- Une feature = 1 à 5 tasks.
- Chaque task a un `files_owned` disjoint.
- La première task est souvent un **contrat** ou un **spike**.
- Un spike a une durée limitée et un critère de sortie : décision, pas code de production.

### 2.6 Démo et release

- Démo reproductible : scénario, données, commande, résultat attendu.
- Release : SemVer, changelog, tag, notes, test machine vierge si packaging.
- Une feature non démontrée n'est pas releasée.

---

## 3. Correctifs

```
Signalement (B-XXX)
  → reproduction
  → test rouge
  → cause racine
  → fix minimal
  → test vert + régression
  → review
  → patch release
```

### 3.1 Règles

- **Toujours** un test de reproduction, sauf incident critique documenté.
- **Jamais** de fix + refactor dans la même branche.
- **Jamais** modifier la spec pour masquer le bug ; on corrige le code ou on décide d'un changement de comportement.
- **Toujours** vérifier les invariants I1-I12.
- **Toujours** un rapport de tâche et une entrée changelog.

### 3.2 Sévérités

| Sévérité | Définition | Délai cible |
|---|---|---|
| `critical` | Perte de données, crash au lancement, export corrompu, violation I1 | hotfix immédiate |
| `major` | Fonctionnalité cassée sans contournement | prochaine vague |
| `minor` | Contournement possible, gêne | backlog |

### 3.3 Hotfix

- Branche `hotfix/<version>-<slug>`.
- Fix minimal + test de non-régression.
- G1-G3 + test manuel du scénario.
- Release patch, notes, rapport d'incident.
- Action préventive : test/gate/checklist ajouté.

---

## 4. Refactor et dette

- Task card dédiée, aucun changement de comportement.
- Tests de caractérisation avant/après.
- Pas de refactor dans une feature ou un fix.
- Budget : une vague de dette par milestone, si le besoin est démontré.
- Un refactor qui change un contrat est une feature/décision, pas un refactor.

---

## 5. Dépendances et upgrades

- Toute dépendance nouvelle : décision (`D*`), licence, poids, maintenance, alternative.
- Upgrade : task dédiée, lockfile, suite complète, changelog.
- Ne jamais mettre à jour les dépendances « au passage ».
- Les binaires (ffmpeg, poids Demucs) sont des dépendances de build : version, source, hash, licence.
- Un upgrade qui casse un golden est un signal, pas un test à mettre à jour sans analyse.

---

## 6. Versioning et releases

### 6.1 SemVer

- `MAJOR` : rupture de compatibilité (projet, API, format).
- `MINOR` : nouvelle fonctionnalité compatible.
- `PATCH` : correctif compatible.

### 6.2 Schéma projet

- `schema_version` entier, indépendant de la version app.
- Migrations forward-only, testées sur fixtures.
- Une migration ne supprime jamais de données sans backup.
- Un projet plus récent que l'app est refusé avec un message clair.

### 6.3 Release checklist

- [ ] Suite complète verte.
- [ ] Gates G1-G5.
- [ ] Changelog à jour.
- [ ] Version bump.
- [ ] `THIRD_PARTY_LICENSES.md` à jour.
- [ ] Build testé sur machine vierge.
- [ ] Notes de release.
- [ ] Tag (validation humaine).
- [ ] Rapport de release.

### 6.4 Notes de release

Format :
```markdown
# vX.Y.Z — YYYY-MM-DD

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
```

---

## 7. Cadence et WIP

- **WIP** : 3 implémenteurs + 1 QA + 1 reviewer.
- **Intégration** : quotidienne.
- **Release** : à la fin d'un milestone ou d'un ensemble de features cohérent.
- **Rétro** : après chaque milestone et chaque incident majeur.
- **Revue de backlog** : hebdomadaire, 30 min, humain + orchestrateur.

---

## 8. Rétrospective

Questions :
1. Qu'est-ce qui a bien marché ?
2. Où avons-nous perdu du temps ?
3. Quelles questions ont bloqué, et pourquoi ?
4. Quels gates ont échoué, et pourquoi ?
5. Quelle règle du playbook faut-il ajuster ?
6. Quelle dette doit être payée ?

Sortie : 1 à 3 actions concrètes, assignées, avec task cards. Pas de roman.

---

## 9. Métriques de flux

| Métrique | Définition | Cible initiale |
|---|---|---|
| Lead time | `done` - `claimed` | < 1 jour |
| First-pass gate rate | tâches sans rework / total | > 70 % |
| Rework | tâches rouvertes / total | < 20 % |
| Questions bloquantes | nombre et âge | 0 avant vague |
| Conflits de merge | par vague | < 2 |
| Tests flaky | par suite | 0 |
| Couverture core | lignes/branches | ≥ 85 % |

À suivre dans `docs/status/METRICS.md`.
