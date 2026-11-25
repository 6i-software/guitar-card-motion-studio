# AGENTS.md — Guitar Card AI-Motion Studio

> **Version :** 2.1 (adoptée, 2026-11-25) — cadre complet, GitHub et conventions de commit.
> **Remplace :** la v1 (non conservée dans ce dépôt ; voir `D3`).
> **Portée :** tout agent IA ou humain qui lit, modifie, teste ou livre ce dépôt.
> **Règle d'or :** une session = une tâche = un rapport. Pas de tâche, pas de code.

## 1. Mission

Application desktop nomade et cross-platform (Windows, macOS, Linux) qui transforme une **Guitar Card** (image + séquence de motifs) et une piste audio en **vidéo synchronisée** : surbrillance du motif actif, annonce du suivant, compteurs de répétition, sans altérer les pixels hors de la zone des motifs (ROI).

L'application est **hors ligne**, **portable**, **en français par défaut** (i18n anglais), et **pilotée par l'utilisateur** : les heuristiques proposent, l'humain décide.

## 2. Comment utiliser ce fichier

1. Lis ce fichier en entier.
2. Trouve ta tâche dans `docs/plan/tasks/` ou le board `docs/status/BOARD.md`.
3. Lis **uniquement** les specs, contrats et fichiers listés dans la task card.
4. Exécute les gates de `docs/agents/QUALITY_GATES.md`.
5. Écris ton rapport avec `docs/templates/REPORT.md` et mets à jour le board si tu es orchestrateur.
6. Arrête-toi. Ne commence pas une autre tâche dans la même session.

Si une information manque : ne devine pas. Consulte `docs/OPEN_QUESTIONS.md`, puis applique `docs/agents/PLAYBOOK.md` § Escalade.

## 3. Invariants non négociables

| ID | Invariant | Détail |
|---|---|---|
| I1 | **Intégrité de l'image** | Seule la ROI peut être modifiée. Hors ROI, les pixels sont strictement identiques à la source, sauf fondu global d'entrée/sortie explicitement activé. |
| I2 | **Nomade et hors ligne** | Aucun téléchargement à l'exécution. Écritures limitées au dossier de config (`QStandardPaths`), au dossier projet choisi et au dossier d'export choisi. |
| I3 | **UI jamais bloquée** | Analyse, Demucs, rendu : hors thread UI, avec progression, annulation propre et erreur explicite. |
| I4 | **Cœur pur** | `core/` n'importe jamais Qt/PySide6 ni `ui/`. Pas de singleton global. Les erreurs héritent de `GCStudioException`. |
| I5 | **Données utilisateur sacrées** | Jamais de suppression/écrasement sans confirmation UI et écriture atomique (temp + rename). |
| I6 | **La synchro manuelle prime** | Un événement `locked=True` n'est jamais écrasé par un recalcul automatique. |
| I7 | **Stack approuvée** | Toute nouvelle dépendance exige une décision dans `docs/DECISIONS.md` (licence, poids, maintenance). |
| I8 | **Rendu sans fichiers lourds** | Les frames partent en `rawvideo` sur `stdin` de ffmpeg. Pas de milliers de PNG intermédiaires. |
| I9 | **Pas d'invention** | Toute heuristique expose un score de confiance et un rapport. Aucune détection présentée comme certaine. |
| I10 | **Cross-platform** | `pathlib.Path`, `QStandardPaths`, aucun séparateur/casse/police supposé. Toute branche OS est isolée et testée. |
| I11 | **Discipline de périmètre** | On ne touche qu'aux fichiers de `files_owned`. Pas de refactor opportuniste, pas de renommage global, pas de formatage global. |
| I12 | **Specs product-owned** | Les specs et `AGENTS.md` sont arbitrés par l'humain. Un agent propose, il ne décide pas seul. |

## 4. Architecture

```
UI (PySide6) → services/ (workers, jobs, progression) → core/ (pur Python, testable sans GUI)
```

```
src/gcstudio/
├── core/
│   ├── grammar/   # lexer, parser, AST, expand, diagnostics
│   ├── model/     # Project, Timeline, Event, ZoneRegion, AnimationStyle
│   ├── image/     # ROI, couleur primaire, overlay
│   ├── audio/     # import/normalisation, features, stems, rapports
│   ├── sync/      # alignement, confiance, tap-to-sync, diagnostics
│   ├── render/    # moteur d'animation, pipe ffmpeg, profils
│   ├── projects/  # persistance, migrations, bibliothèque
│   └── youtube/   # chapitres, description
├── services/      # orchestration, workers, CancellationToken, progression
├── ui/            # fenêtres, timeline, preview, dialogues
└── resources/     # icônes, traductions
```

Règles de dépendance :
- `core/` ne dépend d'aucune couche supérieure.
- `services/` orchestre `core/` et expose des jobs annulables.
- `ui/` ne contient pas de logique métier ; elle appelle `services/`.
- Les contrats entre domaines sont dans `docs/contracts/` et sont gelés par vague.

## 5. Stack et commandes

Stack approuvée : Python 3.12 (épinglé), `uv`, PySide6, librosa 1.x, numpy, scipy, soundfile, demucs, Pillow, opencv-python-headless, pydantic v2, matplotlib 3.x, pytest, pytest-qt, pytest-cov, hypothesis, ruff, mypy, ffmpeg/ffprobe embarqués.

> Python 3.12 est le minimum imposé par librosa 1.x et numpy/scipy récents. Ne pas monter de version sans vérifier PyTorch/Demucs.
> `matplotlib` est réservé aux **rapports audio statiques** (backend Agg, SVG/PNG, hors thread UI) — décision `D11`. Pas de `seaborn`, `plotnine`, `plotly`, `bokeh`, `altair` ni `scikit-learn` en v1.

### 5.1 Langues et conventions

- **Français** : tout `docs/**/*.md`, `README.md`, `CHANGELOG.md`.
- **Anglais** : code source, identifiants, noms de fichiers, commentaires, docstrings, noms de tests, branches et messages de commit.
- **UI** : chaînes visibles en français par défaut via l'i18n ; les clés et identifiants restent en anglais.
- **Commits** : gitmoji obligatoire + Conventional Commits, en anglais, avec `Refs: T-XXXX`. Voir `docs/agents/COMMITS.md`.

```bash
uv sync
uv run python -m gcstudio
uv run pytest -m "not slow"
uv run pytest -m slow
uv run pytest --cov=gcstudio.core --cov-report=term-missing
uv run ruff check .
uv run ruff format --check .
uv run mypy src/gcstudio/core
uv run python scripts/build_portable.py --target=PyInstaller
uv run python scripts/build_portable.py --target=Nuitka
```

Règles :
- Lance d'abord les tests ciblés, puis la gate complète avant le handoff.
- Ne modifie jamais `pyproject.toml` ou `uv.lock` sans tâche dédiée.
- N'ajoute aucune dépendance sans décision humaine.
- Les commandes exactes de chaque gate sont dans `docs/agents/QUALITY_GATES.md`.

## 6. Cycle de vie d'une tâche

```
ready → claimed → in_progress → review → verification → done
                                   ↘ blocked ↗
```

1. **Choisir** : une task card `ready`, dépendances satisfaites, pas de conflit de fichiers.
2. **Claim** : l'orchestrateur réserve la tâche ; l'intégrateur crée la branche `task/<ID>-<slug>` et la pousse sur `origin`.
3. **Comprendre** : lire la task card, les specs liées, les contrats, les rapports des dépendances.
4. **Planifier** : 5 lignes max dans le brouillon de rapport (fichiers, tests, risques).
5. **Implémenter** : uniquement `files_owned`. Tests d'abord pour le cœur (grammar, sync, diagnostics).
6. **Vérifier** : gates G1/G2 (et G3 si applicable). Corriger jusqu'au vert.
7. **Auto-review** : relire son diff, vérifier I1-I12, chercher les régressions.
8. **Rapporter** : `docs/reports/tasks/R-<ID>-<date>.md` avec le template.
9. **Commiter** : l'intégrateur commite avec gitmoji + Conventional Commits, pousse la branche et ouvre la pull request.
10. **Review + merge** : review indépendante approuvée, puis merge de la PR (merge commit, jamais squash/rebase).
11. **Handoff** : signaler l'état à l'orchestrateur (seul écrivain du board), indiquer le prochain agent et les points d'attention.
12. **Stop** : ne pas enchaîner une autre tâche.

Une tâche qui dépasse 1 jour doit être découpée. Une tâche bloquée produit un rapport `blocked` et une question précise.

## 7. Travail en parallèle

- **Un seul écrivain par fichier.** La carte `docs/agents/OWNERSHIP.md` fait foi.
- **Fichiers partagés interdits** sans assignation explicite : `AGENTS.md`, `docs/DECISIONS.md`, `docs/OPEN_QUESTIONS.md`, `docs/status/BOARD.md`, `CHANGELOG.md`, `pyproject.toml`, `uv.lock`.
- **Contrats d'abord** : si ta tâche produit ou consomme une interface, le contrat doit être gelé avant de coder.
- **PR obligatoire, jamais de commit direct sur `main`.** Une tâche = une branche `task/<ID>-<slug>`, une review approuvée, une pull request, puis un **merge commit** (jamais squash/rebase). Seul l'intégrateur écrit dans Git ; les autres agents lisent `git status`/`git diff`.
- **Dépôt distant :** `origin` = `https://github.com/6i-software/guitar-card-motion-studio`. L'intégrateur pousse les branches `task/*` et ouvre les PR. Il ne pousse jamais `main`, ne force pas et ne tague pas sans validation humaine.
- **Bootstrap :** le commit initial sur `main` est l'unique exception ; ensuite la règle PR s'applique.
- **Pas de formatage global** (`ruff format .`), pas de renommage global, pas de mise à jour de dépendances.
- **WIP limit** : 3 implémenteurs + 1 QA + 1 reviewer en parallèle. Au-delà, le risque de conflit dépasse le gain.
- **Worktrees** : par défaut, fichiers disjoints dans le même arbre. Worktree isolé pour les tâches larges (refactor, packaging, migration) ou si >3 agents. Voir `docs/agents/PLAYBOOK.md` § Parallélisme.
- **Conflit détecté** : stop, rapport `blocked`, escalade. Ne pas résoudre un conflit de propriété en écrasant le travail d'un autre.

## 8. Qualité

| Gate | Contenu | Quand |
|---|---|---|
| G0 | Task card complète, critères d'acceptation, périmètre, tests, dépendances | Avant de coder |
| G1 | `ruff check`, `ruff format --check`, `mypy` sur le périmètre | À chaque commit |
| G2 | Tests unitaires ciblés + suite unitaire complète | Avant review |
| G3 | Tests d'intégration, golden, intégrité image, round-trip projet | Avant merge |
| G4 | Smoke UI `pytest-qt`, démo manuelle, perf preview | Avant clôture de vague |
| G5 | Suite complète, build, test machine vierge, licences, changelog | Avant release |

La definition of done complète est dans `docs/agents/QUALITY_GATES.md`. Un rapport sans gates vertes n'est pas un rapport `done`.

## 9. Documentation et comptes rendus

- **Task card** : `docs/plan/tasks/T-XXXX-*.md`, créée par l'orchestrateur ou le spec-analyst.
- **Rapport de tâche** : `docs/reports/tasks/R-T-XXXX-YYYYMMDD.md`, écrit par l'agent qui exécute.
- **Rapport de vague** : `docs/reports/waves/W-*.md`, écrit par l'orchestrateur.
- **Board** : `docs/status/BOARD.md`, mis à jour par l'orchestrateur uniquement.
- **Décisions** : `docs/DECISIONS.md`, append-only, IDs `D*`. Un agent propose via son rapport ; l'orchestrateur ou le spec-analyst rédige.
- **Questions** : `docs/OPEN_QUESTIONS.md`, IDs `Q*`, statut `Ouvert | Bloquant | Résolu`. Ne jamais inventer une réponse.
- **Changelog** : `CHANGELOG.md`, Keep a Changelog, mis à jour par l'intégrateur.
- **Commits** : `docs/agents/COMMITS.md` — gitmoji + Conventional Commits, en anglais, `Refs: T-XXXX`.

Un compte rendu contient toujours : résumé, fichiers changés, commandes exécutées + résultats, écarts, décisions/questions, risques, handoff. Voir `docs/agents/REPORTING.md`.

## 10. Quand s'arrêter et demander

Stop et escalade si :
- une ambiguïté bloque un critère d'acceptation ;
- il faut changer un contrat, un schéma, la grammaire, l'algorithme de rendu ou l'invariante I1 ;
- il faut ajouter/modifier une dépendance, un binaire ou un modèle ;
- un gate échoue deux fois de suite sans cause identifiée ;
- la tâche exige de toucher des fichiers hors `files_owned` ;
- une question de licence, sécurité, données personnelles ou copyrighted content se pose ;
- le scope dépasse la task card.

Format d'escalade : problème, options (2-3), recommandation, impact, ce qui est bloqué. Voir `docs/agents/PLAYBOOK.md` § Escalade.

## 11. Rôles (résumé)

| Rôle | Mode | Périmètre | Interdits |
|---|---|---|---|
| Orchestrateur / Tech Lead | primary | plan, board, dispatch, intégration, rapports de vague | coder les features à la place des devs |
| Spec Analyst | subagent | specs, questions, décisions, task cards, contrats | modifier `src/`, `tests/` |
| Platform Dev | subagent | scaffold, CI, chemins, logging, packaging | logique métier des domaines |
| Core Dev | subagent | `core/grammar`, `core/model`, `core/projects`, `core/youtube` | `ui/`, `pyproject.toml` |
| Audio Dev | subagent | `core/audio`, `core/sync`, fixtures audio | `ui/`, render |
| Render Dev | subagent | `core/image`, `core/render`, intégrité | `ui/`, audio |
| UI Dev | subagent | `ui/`, `services/`, tests UI | `core/` hors contrat |
| QA Verifier | subagent | tests d'intégration, E2E, fixtures, rapports de vérification | corriger `src/` |
| Code Reviewer | subagent | review read-only, findings | éditer le code |
| Intégrateur | subagent | branches `task/*`, PR, merge, conflits, gates complètes, changelog, board | push `main`, tag, release sans humain |

Détail des prompts et permissions : `docs/agents/ROLES.md`.

## 12. Contexte : quoi lire selon la tâche

| Type de tâche | À lire |
|---|---|
| Grammar / parser | `docs/specs/spec-grammar-guitar-card.md`, `docs/contracts/core-grammar.md`, golden tests |
| Modèle / persistance | `docs/specs/spec-data-model.md`, `docs/specs/spec-ui-project.md` §2 |
| Image / ROI / overlay | `docs/specs/spec-audio-sequence-alignement.md` §1, `docs/specs/spec-render-video.md` |
| Audio / Demucs | `docs/specs/spec-audio-sequence-alignement.md` §2, rapport PoC |
| Sync / timeline | `docs/specs/spec-audio-sequence-alignement.md` §3, `docs/specs/spec-data-model.md` |
| UI | `docs/specs/spec-ui-project.md`, contrats services |
| Export | `docs/specs/spec-render-video.md` §2 |
| YouTube | `docs/specs/spec-youtube.md` |
| Packaging | `docs/specs/spec-render-video.md`, `THIRD_PARTY_LICENSES.md` (à créer) |

Ne lis pas tout le dépôt « pour comprendre ». Le contexte est un budget.

## 13. Sécurité, données, licences

- Aucun secret, clé, token ou chemin personnel dans le dépôt.
- Aucun téléchargement à l'exécution : binaires et poids sont préparés au build.
- Pas de musique/artwork protégé dans Git : exemples locaux hors dépôt, fixtures synthétiques pour la CI (`D8`). Pas de Git LFS en v1.
- Toute dépendance/binaire doit figurer dans `THIRD_PARTY_LICENSES.md` (à créer) avec licence, version, source, obligations.
- Les logs ne doivent contenir ni secrets ni données personnelles.

## 14. Change control

- `AGENTS.md` : orchestrateur + validation humaine uniquement.
- `docs/specs/**` : spec-analyst propose, humain valide.
- `docs/DECISIONS.md` : append-only ; une décision adoptée ne se réécrit pas, elle se supersède par une nouvelle décision.
- `docs/OPEN_QUESTIONS.md` : append-only ; une question résolue garde son historique et pointe vers la décision.
- `docs/contracts/**` : propriétaire du domaine + spec-analyst + validation humaine pour tout changement breaking.
- `docs/plan/**`, `docs/status/**` : orchestrateur.
- `CHANGELOG.md`, `pyproject.toml`, `uv.lock`, `scripts/build*` : intégrateur.

## 15. Références

- Playbook complet : `docs/agents/PLAYBOOK.md`
- Rôles et permissions : `docs/agents/ROLES.md`
- Propriété des fichiers : `docs/agents/OWNERSHIP.md`
- Gates et DoD : `docs/agents/QUALITY_GATES.md`
- Comptes rendus : `docs/agents/REPORTING.md`
- Commits et PR : `docs/agents/COMMITS.md`
- Roadmap : `docs/plan/ROADMAP.md`
- Backlog : `docs/plan/BACKLOG.md`
- Lacunes et questions : `docs/plan/SPEC_GAPS.md`
- Itérations et releases : `docs/plan/ITERATIONS.md`
