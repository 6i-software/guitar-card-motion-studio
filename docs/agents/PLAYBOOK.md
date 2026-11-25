# Playbook — Développement piloté par agents IA

> **Statut :** adopté (2026-11-25) — cadre complet, GitHub/PR
> **Public :** orchestrateur, agents, développeur humain
> **Règle d'or :** une session = une tâche = un rapport. Le code n'est qu'une des sorties ; le rapport et la traçabilité en sont une autre.

---

## 1. Pourquoi ce cadre

Le projet a trois caractéristiques qui rendent le pilotage agentique à la fois prometteur et risqué :

1. **Fort invariant produit** : l'intégrité des pixels hors ROI, la synchro manuelle qui prime, la persistance des données utilisateur. Une erreur silencieuse est plus grave qu'un échec visible.
2. **Pipeline hétérogène** : grammaire, image, audio, ML (Demucs), rendu vidéo, UI Qt, packaging. Les compétences et les fichiers sont naturellement séparables.
3. **Specs encore jeunes** : plusieurs ambiguïtés (voir `docs/plan/SPEC_GAPS.md`). Un agent qui devine produira une implémentation plausible mais fausse.

Le cadre ci-dessous vise donc :
- **petites tâches** à périmètre fichier explicite ;
- **contrats gelés** avant le travail parallèle ;
- **vérification indépendante** (tests + review) ;
- **traçabilité** (task card → rapport → décision → changelog) ;
- **gates humaines** sur les décisions structurantes, pas sur chaque ligne.

---

## 2. Principes directeurs

| # | Principe | Conséquence pratique |
|---|---|---|
| P1 | **La spec est la source de vérité, pas le code** | Une ambiguïté se consigne dans `OPEN_QUESTIONS.md` ; elle ne se résout pas dans un commit. |
| P2 | **Contrat d'abord** | Une interface consommée par deux domaines est écrite dans `docs/contracts/` avant l'implémentation. |
| P3 | **Petit et fini** | Une tâche = un objectif, un périmètre, une branche, un rapport. Si > 1 jour, découper. |
| P4 | **Un seul écrivain par fichier** | La carte `OWNERSHIP.md` et le champ `files_owned` de la task card font foi. |
| P5 | **La vérité est exécutable** | Un critère d'acceptation sans test ou commande de vérification n'est pas un critère. |
| P6 | **Review indépendante** | L'auteur ne valide pas seul. Le reviewer est un agent séparé, read-only. |
| P7 | **Append-only** | Décisions, questions, rapports : on ajoute, on ne réécrit pas l'histoire. |
| P8 | **Contexte économe** | `AGENTS.md` court, task card autoportante, liens vers les specs plutôt que copier-coller. |
| P9 | **Humain aux portes** | Architecture, dépendances, schéma, grammaire, rendu, intégrité, licences, release : validation humaine. |
| P10 | **Zéro surprise** | Pas de refactor opportuniste, pas de renommage global, pas de formatage global, pas de push direct sur `main`. |

---

## 3. Organisation et rôles

### 3.1 RACI simplifié

| Activité | Humain | Orchestrateur | Spec Analyst | Devs | QA | Reviewer | Intégrateur |
|---|---|---|---|---|---|---|---|
| Prioriser le backlog | **A** | R | C | I | I | I | I |
| Rédiger/valider une spec | **A** | C | R | C | C | I | I |
| Découper une vague | C | **R/A** | C | I | C | I | C |
| Écrire une task card | I | **A** | R | C | C | I | I |
| Implémenter | I | I | I | **R** | I | I | I |
| Tester | I | I | I | C | **R** | C | I |
| Reviewer | I | A | I | C | C | **R** | I |
| Intégrer / merger | I | A | I | I | C | C | **R** |
| Décider d'une dépendance | **A** | R | C | C | I | I | I |
| Release | **A** | R | I | I | C | C | **R** |

`R` = réalise, `A` = approuve, `C` = consulté, `I` = informé.

### 3.2 Rôles en une phrase

- **Humain (Product Owner)** : arbitre les questions, valide les décisions structurantes, juge les démos.
- **Orchestrateur / Tech Lead** : seul agent primaire ; découpe, dispatche, tient le board, arbitre les conflits de périmètre, produit les rapports de vague. Il ne code pas les features.
- **Spec Analyst** : transforme une demande en spec/acceptance criteria, maintient questions/décisions/contrats, écrit les task cards. Il ne touche pas au code.
- **Core Dev / Audio Dev / Render Dev / UI Dev** : implémentent dans leur périmètre, avec tests unitaires.
- **QA Verifier** : conçoit et exécute les tests d'intégration/E2E, vérifie les critères d'acceptation, reproduit les bugs. Il ne corrige pas `src/`.
- **Code Reviewer** : lit le diff, cherche les régressions, les violations d'invariants, les problèmes de test/perf/sécurité. Read-only.
- **Intégrateur** : crée et pousse les branches `task/*`, ouvre les PR, merge après review, résout les conflits, lance les gates complètes, met à jour le changelog et signale les transitions à l'orchestrateur (seul écrivain du board). Seul agent autorisé aux écritures Git, mais jamais de push direct sur `main`.

Détail : `docs/agents/ROLES.md`.

---

## 4. Artefacts et sources de vérité

| Artefact | Fichier | Propriétaire | Rôle |
|---|---|---|---|
| Constitution | `AGENTS.md` | Humain + orchestrateur | Règles lues par tous, invariants, routage |
| Playbook | `docs/agents/PLAYBOOK.md` | Orchestrateur | Modèle opératoire détaillé |
| Rôles | `docs/agents/ROLES.md` | Orchestrateur | Périmètres, permissions, prompts |
| Propriété | `docs/agents/OWNERSHIP.md` | Orchestrateur | Qui écrit quoi |
| Gates | `docs/agents/QUALITY_GATES.md` | QA + orchestrateur | Commandes et critères de passage |
| Reporting | `docs/agents/REPORTING.md` | Orchestrateur | Formats et cadence |
| Commits / PR | `docs/agents/COMMITS.md` | Intégrateur | Gitmoji, Conventional Commits, branches, PR |
| Specs produit | `docs/specs/**` | Humain (via spec-analyst) | Comportement attendu |
| Contrats | `docs/contracts/**` | Domaine + spec-analyst | Interfaces entre domaines |
| Task cards | `docs/plan/tasks/T-*.md` | Orchestrateur | Unité de travail |
| Backlog | `docs/plan/BACKLOG.md` | Orchestrateur | File ordonnée |
| Roadmap | `docs/plan/ROADMAP.md` | Humain + orchestrateur | Milestones, vagues, sorties |
| Questions | `docs/OPEN_QUESTIONS.md` | Spec Analyst | Ambiguïtés, options, blocages |
| Décisions | `docs/DECISIONS.md` | Spec Analyst + humain | Arbitrages adoptés |
| Board | `docs/status/BOARD.md` | Orchestrateur | État temps réel |
| Rapports | `docs/reports/**` | Chaque agent (son fichier) | Preuve d'exécution |
| Changelog | `CHANGELOG.md` | Intégrateur | Historique user-facing |

**Règle de concurrence :** tout fichier listé comme « partagé » dans `OWNERSHIP.md` n'a qu'un seul écrivain. Les autres agents proposent via leur rapport.

---

## 5. Cycle de vie d'une tâche

### 5.1 États

```
proposed → ready → claimed → in_progress → review → verification → done
                                      ↘ blocked ↗
```

| État | Signification | Critère d'entrée | Critère de sortie |
|---|---|---|---|
| `proposed` | Idée, pas prête | — | Spec/acceptance criteria identifiés |
| `ready` | Prête à être prise | DoR remplie | Agent assigné |
| `claimed` | Assignée | Branche/worktree créé | Premier commit ou rapport de plan |
| `in_progress` | En cours | Plan 5 lignes | Code + tests + gates locales |
| `review` | En review | Rapport + diff | Review sans bloquant |
| `verification` | Vérification indépendante | Review OK | QA OK |
| `done` | Terminée | DoD complète | Merge + board + changelog |
| `blocked` | Bloquée | Question/décision | Déblocage documenté |

### 5.2 Definition of Ready (DoR)

Une task card n'est `ready` que si :
- [ ] objectif et périmètre in/out explicites ;
- [ ] critères d'acceptation testables (au moins un test ou une commande) ;
- [ ] `files_owned` renseigné et sans chevauchement avec une tâche en cours ;
- [ ] dépendances identifiées et satisfaites, ou contrat gelé ;
- [ ] specs/contrats liés ;
- [ ] risques et questions bloquantes identifiés ;
- [ ] taille estimée ≤ 1 jour d'agent.

### 5.3 Definition of Done (DoD)

Une tâche est `done` seulement si :
- [ ] tous les critères d'acceptation sont couverts par un test ou une vérification manuelle tracée ;
- [ ] G1 et G2 vertes ; G3 si la tâche touche une intégration ;
- [ ] pas de fichier hors `files_owned` modifié (sauf justification dans le rapport) ;
- [ ] rapport écrit avec le template, gates et commandes incluses ;
- [ ] review indépendante effectuée, findings bloquants corrigés ;
- [ ] board mis à jour ;
- [ ] décisions/questions consignées ;
- [ ] changelog si changement visible utilisateur ;
- [ ] handoff explicite (prochain agent, points d'attention).

Détail des gates : `docs/agents/QUALITY_GATES.md`.

---

## 6. Parallélisme et vagues

### 6.1 Vague

Une **vague** est un lot de tâches sans dépendance entre elles, avec des périmètres fichiers disjoints, et un objectif démontrable. Une vague dure 1 à 3 jours.

```
Milestone M1 (grammaire)
└── Vague W1.1 (contrat + lexer + tests)
    ├── T-0004 contrat grammar      (spec-analyst)
    ├── T-0005 lexer                (core-dev)
    └── T-0008 golden/property      (qa-verifier, en parallèle du lexer)
```

### 6.2 Règles de dispatch

1. **DAG** : une tâche ne démarre que si `depends_on` est `done` ou si le contrat est gelé.
2. **Pas de chevauchement** : l'orchestrateur vérifie `files_owned` avant de lancer deux agents.
3. **WIP limit** : 3 implémenteurs + 1 QA + 1 reviewer. Au-delà, le coût de coordination dépasse le gain.
4. **Contrat d'abord** : si deux tâches partagent une interface, la tâche de contrat est prioritaire.
5. **Intégration quotidienne** : l'intégrateur merge les tâches `done` en fin de journée, lance G1-G3, met à jour le board.
6. **Pas de branche longue** : une tâche > 1 jour est découpée ; une branche > 3 jours est un signal d'alerte.

### 6.3 Worktrees

Deux modes :

- **Mode A (par défaut)** : même arbre de travail, fichiers disjoints. Simple, rapide, adapté à 2-3 agents.
- **Mode B (isolation)** : un worktree par tâche, pour les refactors, migrations, packaging, ou si >3 agents. L'intégrateur merge ensuite.

Convention worktree :
```bash
git worktree add .worktrees/T-0005 -b task/T-0005-lexer
```
`.worktrees/` est gitignored. Le worktree est supprimé après merge.

### 6.4 Résolution de conflit

- Conflit de **fichier** : l'orchestrateur réassigne ou sérialise. On n'écrase jamais.
- Conflit de **contrat** : stop, décision, mise à jour du contrat et des consommateurs.
- Conflit de **spec** : question ouverte, arbitrage humain.
- Conflit **Git** : seul l'intégrateur résout ; il documente la résolution dans le rapport de vague.

---

## 7. Qualité et vérification

### 7.1 Gates

Voir `docs/agents/QUALITY_GATES.md` pour les commandes exactes. Résumé :

| Gate | Objet | Preuve |
|---|---|---|
| G0 | Spec/DoR | Task card complète |
| G1 | Statique | ruff + mypy |
| G2 | Unitaire | pytest unit |
| G3 | Intégration | pytest integration + golden + integrity |
| G4 | UI/perf | pytest-qt + démo manuelle |
| G5 | Release | suite complète + build + machine vierge |

### 7.2 Review indépendante

Le reviewer vérifie dans cet ordre :
1. **Correction** : le code fait-il ce que la task card demande ?
2. **Invariants** : I1-I12, en particulier intégrité image, core pur, synchro verrouillée.
3. **Tests** : les critères sont-ils réellement testés ? Cas limites ? Flakiness ?
4. **Contrats** : les interfaces sont-elles respectées ? Pas de couplage caché ?
5. **Performance** : pas de boucle chaude évitable, pas de chargement inutile.
6. **Sécurité/licences** : pas de secret, pas de dépendance non validée, pas de contenu protégé.
7. **Périmètre** : pas de changement hors sujet.

Findings classés `blocker`, `major`, `minor`, `nit`. Un `blocker` empêche le merge.

### 7.3 Tests

- **Unitaires** : `core/` sans Qt, rapides, déterministes.
- **Propriété** : grammar (`hypothesis`), sérialisation, normalisation.
- **Golden** : 4 cartes de référence + cas d'erreur.
- **Intégrité image** : N frames, pixels hors ROI identiques à la source, fondus désactivés.
- **Intégration** : ffmpeg court (2 s, petite résolution), projet round-trip, migration.
- **UI** : smoke `pytest-qt`, pas de logique métier dans les tests UI.
- **Slow** : marqués `@pytest.mark.slow`, exclus par défaut, exécutés en G3/G5.
- **Fixtures** : synthétiques pour la CI ; les exemples locaux protégés ne sont pas dans Git.

### 7.4 Métriques légères

Suivre dans `docs/status/METRICS.md` :
- lead time par tâche ;
- taux de gates vertes du premier coup ;
- taux de rework ;
- nombre de questions bloquantes et leur âge ;
- nombre de conflits de merge ;
- couverture `core/` ;
- tests flaky ;
- perf preview/export (quand disponible).

Pas de dashboard lourd : le board et le rapport de vague suffisent.

---

## 8. Comptes rendus

### 8.1 Cadence

| Niveau | Auteur | Fréquence | Fichier |
|---|---|---|---|
| Tâche | agent exécutant | à chaque tâche | `docs/reports/tasks/R-T-XXXX-YYYYMMDD.md` |
| Vague | orchestrateur | fin de vague | `docs/reports/waves/W-YYYY-MM-DD-*.md` |
| Milestone | orchestrateur + humain | fin de milestone | `docs/reports/milestones/M-*.md` |
| Release | intégrateur | à chaque release | `docs/releases/vX.Y.Z.md` |
| Board | orchestrateur | à chaque transition | `docs/status/BOARD.md` |

### 8.2 Règles

- Un rapport est **obligatoire** : sans rapport, la tâche n'est pas `done`.
- Un rapport est **daté** et **immuable** ; une correction se fait par addendum daté.
- Un rapport contient toujours : résumé, fichiers, commandes/résultats, écarts, décisions/questions, risques, handoff.
- Les rapports sont **courts** : 1 page suffit. Les logs complets vont dans un fichier annexe si besoin.
- Le board est mis à jour par l'orchestrateur uniquement, pour éviter les conflits.

Détail et template : `docs/agents/REPORTING.md` et `docs/templates/REPORT.md`.

---

## 9. Itérations de développement

### 9.1 Trois boucles

1. **Boucle milestone** (M0 → M10) : construit le MVP. Chaque milestone a une démo et un tag.
2. **Boucle feature** (post-MVP) : nouvelle fonctionnalité, spec delta, ADR si structurant, tasks, release.
3. **Boucle correctif** : bug → test rouge → fix → test vert → régression → patch release.

### 9.2 Feature

```
Demande → triage → feature brief → impact analysis → décision (si structurant)
       → task cards → vague → démo → release → rétro
```

- **Feature brief** : problème utilisateur, comportement attendu, hors scope, critères d'acceptation, impact specs.
- **Impact analysis** : architecture, modèle de données, schéma projet, UI, perf, tests, docs, licences.
- **ADR/décision** : si changement de schéma, de grammaire, de rendu, d'invariant, de dépendance ou d'architecture.
- **Release** : SemVer, changelog, tag, notes.

### 9.3 Bugfix

```
Reproduction → test qui échoue → cause racine → fix minimal → test vert
            → régression → rapport → patch release
```

Interdit : corriger sans test de reproduction (sauf incident critique documenté), mélanger fix et refactor, modifier la spec pour masquer le bug.

### 9.4 Refactor / dette

- Task card dédiée, aucun changement de comportement.
- Golden tests et tests de caractérisation avant/après.
- Pas de refactor opportuniste dans une feature.
- Budget : une vague de dette par milestone, si nécessaire.

### 9.5 Hotfix

- Branche `hotfix/<version>-<slug>`, fix minimal, G1-G3 + test de non-régression.
- Release patch immédiate, rapport d'incident, action préventive.

### 9.6 Versioning

- **App** : SemVer `MAJOR.MINOR.PATCH`.
- **Schéma projet** : `schema_version` entier, migrations forward-only, fixtures de chaque version.
- **Contrats** : `v0.x`, breaking = nouvelle version + décision + mise à jour des consommateurs.
- **Changelog** : Keep a Changelog, sections Added/Changed/Fixed/Removed/Security.

Détail : `docs/plan/ITERATIONS.md`.

---

## 10. Git et branches

| Type | Convention | Exemple |
|---|---|---|
| Tâche | `task/<ID>-<slug>` | `task/T-0005-lexer` |
| Feature | `feat/<slug>` | `feat/roi-manual-editor` |
| Fix | `fix/<ID>-<slug>` | `fix/T-0042-locked-event` |
| Hotfix | `hotfix/<version>-<slug>` | `hotfix/0.3.1-export-crash` |
| Vague | `wave/<n>-<slug>` (optionnel) | `wave/W1.1-grammar` |

Règles :
- `main` toujours verte et protégée par convention.
- Commits **gitmoji + Conventional Commits**, en anglais, un changement logique, `Refs: T-XXXX`. Détail : `docs/agents/COMMITS.md`.
- **PR obligatoire** : aucune tâche n'est commitée directement sur `main`. Une branche `task/<ID>-<slug>` est poussée, une PR est ouverte, une review approuvée est exigée, puis merge.
- **Merge commit obligatoire** : jamais squash, jamais rebase. Le merge `--no-ff` préserve l'historique de la tâche.
- **Remote** : `origin` = `https://github.com/6i-software/guitar-card-motion-studio`.
- Agents : pas de `git push` direct sur `main`, pas de `tag`, pas de `rebase` de branche partagée, pas de `reset --hard`, pas de `clean`.
- Intégrateur : crée et pousse la branche `task/*`, ouvre la PR, merge après gates et review, supprime la branche, signale l'état à l'orchestrateur.
- Humain : seul à approuver un tag de release ou une réécriture d'historique.
- **Exception bootstrap** : le tout premier commit peut être poussé sur `main` pour créer la base ; ensuite la règle PR s'applique sans exception.
- Si `gh` n'est pas disponible, l'intégrateur pousse la branche et fournit l'URL de comparaison GitHub ; l'humain ouvre la PR.

---

## 11. Contexte et prompts

- **`AGENTS.md`** : contrat court, lu par tous. Il ne contient pas le détail des specs.
- **Task card** : autoportante ; elle liste les fichiers à lire, pas tout le dépôt.
- **Rapport de dépendance** : le prochain agent lit le rapport, pas la session précédente.
- **Budget contexte** : si un agent doit lire > 5 fichiers pour commencer, la task card est trop vague.
- **Pas de copier-coller de spec** : lien vers la section précise.
- **Pas de « lis tout le repo »** : routing explicite dans `AGENTS.md` §12.
- **Handoff** : 5 lignes max : état, fichiers, points d'attention, prochaine action.

---

## 12. Risques et mitigations

| Risque | Mitigation |
|---|---|
| Spec ambiguë → implémentation plausible mais fausse | Questions ouvertes, G0, human gate, tests d'acceptation |
| Hallucination d'API | Contrats + mypy + tests + review |
| Conflits de merge | Ownership, petites tâches, intégration quotidienne |
| Dérive de scope | `files_owned`, I11, review de périmètre |
| Tests flaky | Fixtures déterministes, pas de réseau, marqueur `slow`, quarantaine |
| Perte de données | Écriture atomique, backups, mode dégradé, tests de corruption |
| Licence/ffmpeg/Demucs | `THIRD_PARTY_LICENSES.md`, décision, build contrôlé |
| Contenu protégé dans Git | Exemples hors Git, fixtures synthétiques, Git LFS si autorisé |
| Perf preview/export | Budgets, benchmarks, profilage, cache d'états |
| Coût/tokens | WIP limit, modèles adaptés, contexte économe, pas de relecture globale |
| Agents qui se marchent dessus | Un écrivain par fichier, board, locks de tâche |
| Review complaisante | Reviewer séparé, checklist, findings sévérité |

---

## 13. Plan d'adoption

### Semaine 0 — Cadrage (cette proposition)
- [x] Adopter `AGENTS.md` v2.1 et le playbook (cadre complet, mode A).
- [x] Arbitrer les questions P0 de `docs/plan/SPEC_GAPS.md` (Q4, Q7, Q35).
- [x] Valider la politique exemples/licences (`D8`).
- [x] Stack validée : `pytest-cov` en dev, `matplotlib` en runtime pour les rapports (`D7` + `D11`) ; pas de `scikit-learn`.
- [x] GitHub + PR (`D13`) et conventions de commit (`D14`).

### Semaine 1 — M0 Scaffold
- [ ] T-0001 scaffold uv + hello world.
- [ ] T-0002 gates/CI locale.
- [ ] T-0003 erreurs + logging.
- [ ] Démo : fenêtre vide, `uv run pytest` vert, gates vertes.

### Semaine 2 — M1 Grammaire
- [ ] T-0004 contrat grammar.
- [ ] T-0005 lexer + T-0008 golden/property en parallèle.
- [ ] T-0006 parser/AST.
- [ ] T-0007 expand/diagnostics.
- [ ] Démo : 4 golden verts, fuzz sans crash.

### Ensuite
Dérouler `docs/plan/ROADMAP.md` vague par vague. Ne détailler que les 2 prochaines vagues ; le reste est indicatif (rolling wave planning).

---

## 14. Escalade

Un agent **doit s'arrêter** et produire un rapport `blocked` si :
- une décision structurante est nécessaire (schéma, grammaire, rendu, invariant, dépendance) ;
- deux options techniques ont un impact produit différent et la spec ne tranche pas ;
- un gate échoue deux fois sans cause identifiée ;
- le périmètre déborde de `files_owned` ;
- une question de licence, sécurité, données ou contenu protégé apparaît.

Format :
```markdown
## Blocage
- **Problème :** ...
- **Options :** 1) ... 2) ... 3) ...
- **Recommandation :** ...
- **Impact si option 1/2/3 :** ...
- **Ce qui est bloqué :** ...
- **Question précise :** ...
```

L'orchestrateur consigne la question dans `OPEN_QUESTIONS.md` avec un ID, notifie l'humain, et met la tâche `blocked`. Aucun agent ne « choisit en silence ».

---

## 15. Annexes

- Rôles et prompts : `docs/agents/ROLES.md`
- Propriété : `docs/agents/OWNERSHIP.md`
- Gates : `docs/agents/QUALITY_GATES.md`
- Reporting : `docs/agents/REPORTING.md`
- Roadmap : `docs/plan/ROADMAP.md`
- Backlog : `docs/plan/BACKLOG.md`
- Itérations : `docs/plan/ITERATIONS.md`
- Lacunes spec : `docs/plan/SPEC_GAPS.md`
- Templates : `docs/templates/`
