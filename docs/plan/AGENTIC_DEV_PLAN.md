# Plan de conception et d'organisation — développement piloté par agents IA

> **Statut :** adopté (2026-11-25) — mode A, cadre complet.
> **But :** donner une vue d'ensemble du cadre avant d'entrer dans les documents détaillés.
> **Décision :** `D2` (cadre agentique), `D3` (`AGENTS.md` v2), `D4` (un écrivain par fichier), `D5` (questions), `D13` (GitHub/PR), `D14` (langues/commits).

---

## 1. Ce que je propose

Un développement en **vagues courtes**, avec :

- un **orchestrateur** qui découpe, dispatche et intègre ;
- des **agents spécialisés** par domaine (spec, platform, core, audio, render, UI, QA, review, intégration) ;
- des **task cards** autoportantes avec `files_owned`, dépendances et critères d'acceptation ;
- des **contrats gelés** avant le travail parallèle ;
- des **gates G0–G5** exécutables ;
- un **rapport par tâche** et un **rapport de vague** ;
- un **board** et des **métriques** légères ;
- des **portes humaines** sur les décisions structurantes.

Le principe central : **le code est une sortie, pas la seule**. Une tâche sans rapport, sans test et sans review n'est pas terminée.

---

## 2. Pourquoi ce cadre

Le projet combine :
- un invariant fort (pixels hors ROI, données utilisateur, synchro verrouillée) ;
- un pipeline hétérogène (grammaire, image, audio, ML, rendu, UI, packaging) ;
- des specs jeunes avec des ambiguïtés.

Un agent qui travaille seul sur une spec ambiguë produit du code plausible mais faux. Le cadre réduit ce risque par :
- des **questions explicites** au lieu de devinettes ;
- des **contrats** au lieu de suppositions ;
- des **tests** au lieu de déclarations ;
- une **review indépendante** au lieu d'un agent juge et partie ;
- des **petites tâches** au lieu de branches géantes.

---

## 3. Organisation

```
Humain (Product Owner)
   │  arbitre les décisions, valide les démos
   ▼
Orchestrateur (Tech Lead)
   │  découpe, dispatche, tient le board, intègre
   ├── Spec Analyst      → specs, questions, décisions, task cards, contrats
   ├── Platform Dev      → scaffold, CI, chemins, logging, packaging
   ├── Core Dev          → grammar, model, projects, youtube
   ├── Audio Dev         → audio, sync, Demucs
   ├── Render Dev        → image, ROI, overlay, ffmpeg
   ├── UI Dev            → écrans, timeline, preview, workers
   ├── QA Verifier       → tests d'intégration/E2E, vérification
   ├── Code Reviewer     → review read-only
   └── Intégrateur       → merge, gates, changelog, board
```

Détail : `docs/agents/ROLES.md`.

---

## 4. Flux d'une tâche

```
ready
 → claim (branche task/T-XXXX)
 → lire task card + specs + contrat
 → plan 5 lignes
 → implémenter + tests
 → G1/G2 (+G3)
 → rapport
 → review indépendante
 → QA
 → merge (intégrateur)
 → done + board + changelog
```

Une tâche > 1 jour est découpée. Une tâche bloquée produit un rapport `blocked` et une question.

Détail : `docs/agents/PLAYBOOK.md` §5–6.

---

## 5. Parallélisme

- **WIP limit** : 3 implémenteurs + 1 QA + 1 reviewer.
- **Un seul écrivain par fichier** : `docs/agents/OWNERSHIP.md`.
- **Vagues** : tâches disjointes, objectif démontrable, 1–3 jours.
- **Contrats d'abord** : `docs/contracts/`.
- **Worktrees** : optionnels, pour les tâches larges ou >3 agents.
- **Intégration quotidienne** : l'intégrateur merge les tâches `done`, lance G1–G3.
- **Pas de git write** pour les devs : seul l'intégrateur commit/merge.

Exemple de vague M1 :

```
W1.1
├── T-0004 contrat grammar   (spec-analyst)
├── T-0005 lexer             (core-dev)
└── T-0008 golden/property   (qa-verifier, en parallèle)
```

---

## 6. Qualité

| Gate | Objet | Preuve |
|---|---|---|
| G0 | Spec/DoR | Task card complète |
| G1 | Statique | ruff + mypy |
| G2 | Unitaire | pytest unit |
| G3 | Intégration | golden + intégrité + round-trip |
| G4 | UI/perf | pytest-qt + démo |
| G5 | Release | suite + build + machine vierge |

Revue indépendante : correction → invariants → tests → contrats → perf → sécurité/licences → périmètre.

Détail : `docs/agents/QUALITY_GATES.md`.

---

## 7. Comptes rendus

| Niveau | Fichier | Auteur | Fréquence |
|---|---|---|---|
| Tâche | `docs/reports/tasks/R-T-XXXX-YYYYMMDD.md` | agent exécutant | chaque tâche |
| Vague | `docs/reports/waves/W-*.md` | orchestrateur | fin de vague |
| Milestone | `docs/reports/milestones/M-*.md` | orchestrateur + humain | fin de milestone |
| Release | `docs/releases/vX.Y.Z.md` | intégrateur | release |
| Board | `docs/status/BOARD.md` | orchestrateur | à chaque transition |

Chaque rapport contient : résumé, fichiers, commandes/résultats, écarts, décisions/questions, risques, handoff.

**Option :** un digest quotidien de 10 lignes peut être généré par l'orchestrateur à partir du board et des rapports. Aucune automatisation n'est créée sans validation.

Détail : `docs/agents/REPORTING.md`.

---

## 8. Itérations

- **Milestones M0–M10** : construction du MVP, démo + tag à chaque fin.
- **Features** : brief → impact → décision → tasks → vague → release.
- **Bugs** : reproduction → test rouge → fix → régression → patch.
- **Refactors** : task dédiée, zéro changement de comportement.
- **Hotfix** : fix minimal, test de non-régression, release patch.
- **Release** : SemVer, changelog, tag, machine vierge.

Détail : `docs/plan/ITERATIONS.md`.

---

## 9. Roadmap

| Milestone | Objectif | Sortie |
|---|---|---|
| M0 | Scaffold | fenêtre + gates |
| M1 | Grammaire | 4 golden + fuzz |
| M2 | Image | ROI + intégrité |
| M3 | Audio passe 1 | features + rapport |
| M4 | Demucs | séparation + rapport |
| M5 | Sync | alignement + confiance |
| M6 | Timeline UI | démo interactive |
| M7 | Animation | preview + intégrité |
| M8 | Export | MP4 + annulation |
| M9 | Projets + YouTube | round-trip + description |
| M10 | Packaging | 3 OS |

Détail : `docs/plan/ROADMAP.md`, `docs/plan/BACKLOG.md`.

---

## 10. Ce qui est à valider

### Décisions structurantes — adoptées

1. **Cadre complet** (`D2`, mode A) : orchestrateur + subagents, task cards, rapports, gates, WIP limit.
2. **`AGENTS.md` v2.1** (`D3`) : constitution courte + playbook.
3. **Un écrivain par fichier** (`D4`) et rapports append-only.
4. **Statuts/priorités de questions** (`D5`).
5. **GitHub + PR** (`D13`) et **langues/commits** (`D14`).

### Questions P0 (détail dans `docs/plan/SPEC_GAPS.md`)

- **Q4** : résolu `D15` — `Punk2` est un nom joué une fois.
- **Q5** : résolu `D10` — `2{AA}` accepté mais déconseillé.
- **Q6** : résolu `D10` + `D15` — `A##` ≡ `A^2`.
- **Q7** : résolu `D12` — `a` est un motif distinct, famille `A`.
- **Q8** : compteurs de groupe `{5A BB}x2` — encore ouvert.
- **Q9** : conversion temps → frame — encore ouvert.
- **Q10** : normalisation audio — encore ouvert.
- **Q11** : résolu `D7` + `D11` — `pytest-cov` en dev, `matplotlib` en runtime ; pas de `scikit-learn`.
- **Q15** : résolu `D8` — exemples protégés hors Git.
- **Q16** : résolu `D9` — description YouTube dans `output/`.
- **Q27** : Python **3.12** (imposé par librosa 1.x), Win10+/macOS12+/Ubuntu22.04+.
- **Q35** : résolu `D15` — `A^1` ≡ `A#`, `A^2` ≡ `A##`, `A~^2` refusé.

### Environnement

- **Résolu** : `uv` 0.13.10 et Python 3.12.16 installés le 2026-11-25. M0 peut démarrer.
- **Remote** : `origin` = `https://github.com/6i-software/guitar-card-motion-studio` (`D13`). Travail par branches + PR, merge commit.

---

## 11. Prochaine étape

1. Pousser le commit bootstrap sur `main` (unique exception).
2. Lancer **W0.1** : T-0001 (platform-dev) sur `task/T-0001-scaffold`, puis T-0002 (integrator) et T-0003 (platform-dev).
3. Démo M0 : fenêtre hello world + `uv run pytest` + gates vertes + PR mergée.
4. Détailer W1.1 (grammaire) après la démo M0.

Le board est dans `docs/status/BOARD.md`.
