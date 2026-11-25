# Carte de propriété des fichiers

> **Statut :** adopté (2026-11-25)
> **Règle :** un fichier a **un seul écrivain** à un instant donné. Le champ `files_owned` d'une task card doit être un sous-ensemble de la zone de son rôle. L'orchestrateur vérifie l'absence de chevauchement avant dispatch.

---

## 1. Domaines et propriétaires

| Domaine | Propriétaire | Fichiers / globs | Notes |
|---|---|---|---|
| Grammaire | `core-dev` | `src/gcstudio/core/grammar/**`, `tests/unit/grammar/**` | TDD, golden, hypothesis |
| Modèle | `core-dev` | `src/gcstudio/core/model/**`, `tests/unit/model/**` | pydantic v2, pas de Qt |
| Projets / migrations | `core-dev` | `src/gcstudio/core/projects/**`, `tests/unit/projects/**` | écriture atomique |
| YouTube | `core-dev` | `src/gcstudio/core/youtube/**`, `tests/unit/youtube/**` | chapitres, description |
| Erreurs / logging cœur | `platform-dev` | `src/gcstudio/core/errors.py`, `src/gcstudio/core/logging.py` | pas de Qt dans `core/` |
| Scaffold / CI / chemins | `platform-dev` | `pyproject.toml`, `uv.lock`, `src/gcstudio/__main__.py`, `src/gcstudio/services/paths.py`, `src/gcstudio/services/logging.py`, `scripts/ci.py` | logique métier des domaines |
| Audio | `audio-dev` | `src/gcstudio/core/audio/**`, `tests/unit/audio/**` | librosa, ffmpeg, cache |
| Sync | `audio-dev` | `src/gcstudio/core/sync/**`, `tests/unit/sync/**` | alignement, confiance, locked |
| Image | `render-dev` | `src/gcstudio/core/image/**`, `tests/unit/image/**` | ROI, couleur, overlay |
| Rendu | `render-dev` | `src/gcstudio/core/render/**`, `tests/unit/render/**`, `tests/integration/render/**` | pipe ffmpeg, intégrité |
| Services | `ui-dev` | `src/gcstudio/services/**`, `tests/unit/services/**` | workers, jobs, progression |
| UI | `ui-dev` | `src/gcstudio/ui/**`, `tests/ui/**` | PySide6, i18n |
| Fixtures audio | `audio-dev` | `tests/fixtures/audio/**` | synthétiques, pas de morceaux protégés |
| Fixtures image | `render-dev` | `tests/fixtures/images/**` | synthétiques ou libres |
| Fixtures projet | `core-dev` | `tests/fixtures/projects/**` | versions de schéma |
| Intégration / E2E | `qa-verifier` | `tests/integration/**` (hors render), `tests/e2e/**`, `tests/ui/**` en co-écriture | ne corrige pas `src/` |
| Contrats | `spec-analyst` + owner | `docs/contracts/**` | validation humaine si breaking |
| Specs | `spec-analyst` | `docs/specs/**`, `docs/SPEC.md` | humain valide |
| Questions / décisions | `spec-analyst` | `docs/OPEN_QUESTIONS.md`, `docs/DECISIONS.md` | append-only |
| Task cards | `orchestrator` / `spec-analyst` | `docs/plan/tasks/**` | l'orchestrateur assigne |
| Roadmap / backlog | `orchestrator` | `docs/plan/ROADMAP.md`, `docs/plan/BACKLOG.md` | humain valide les priorités |
| Board / métriques | `orchestrator` | `docs/status/**` | un seul écrivain |
| Conventions Git | `integrator` + orchestrateur | `docs/agents/COMMITS.md` | validation humaine |
| Rapports de tâche | agent exécutant | `docs/reports/tasks/R-<ID>-*.md` | chaque agent n'écrit que le sien |
| Rapports de vague | `orchestrator` | `docs/reports/waves/**` | fin de vague |
| Rapports de milestone | `orchestrator` | `docs/reports/milestones/**` | fin de milestone |
| Reviews | `code-reviewer` | `docs/reports/reviews/**` | read-only sur le code |
| Changelog | `integrator` | `CHANGELOG.md` | release |
| Dépendances | `integrator` | `pyproject.toml`, `uv.lock`, `.python-version` | décision humaine obligatoire ; exception T-0001 : `platform-dev` crée le scaffold initial |
| CI / scripts | `integrator` | `scripts/ci.py`, `.github/workflows/**` | cross-platform |
| Build / packaging | `integrator` | `scripts/build_portable.py`, `scripts/fetch_*.py` | release |
| Binaires / modèles | `integrator` | `binaries/**`, `models/**` | hors Git, build-time |
| Config OpenCode | `orchestrator` | `.opencode/**`, `opencode.jsonc` | validation humaine |

---

## 2. Fichiers partagés (un seul écrivain)

Ces fichiers sont **interdits en écriture** pour un agent qui n'est pas explicitement assigné :

- `AGENTS.md` — orchestrateur + humain.
- `docs/DECISIONS.md` — spec-analyst + humain (append-only).
- `docs/OPEN_QUESTIONS.md` — spec-analyst (append-only).
- `docs/status/BOARD.md` — orchestrateur.
- `docs/status/METRICS.md` — orchestrateur.
- `CHANGELOG.md` — intégrateur.
- `pyproject.toml`, `uv.lock`, `.python-version` — intégrateur, sur décision.
- `docs/plan/ROADMAP.md`, `docs/plan/BACKLOG.md` — orchestrateur.
- `docs/agents/*.md` — orchestrateur + humain.
- `opencode.jsonc`, `.opencode/**` — orchestrateur + humain.
- `README.md` — spec-analyst ou orchestrateur.

Un agent qui a besoin d'une modification dans un fichier partagé l'écrit dans son **rapport** (section « propositions »). L'orchestrateur ou le spec-analyst l'applique.

---

## 3. Comment déclarer `files_owned`

Dans une task card :

```yaml
files_owned:
  - src/gcstudio/core/grammar/**
  - tests/unit/grammar/**
  - docs/contracts/core-grammar.md   # seulement si la task card inclut le contrat
```

Règles :
- Les globs sont relatifs à la racine du dépôt.
- Un glob large (`src/**`) est refusé : découper.
- Un fichier partagé ne peut être dans `files_owned` que si la task card est explicitement une tâche de contrat/documentation.
- L'orchestrateur vérifie l'intersection avec les tâches `claimed`/`in_progress`.
- En cas de chevauchement : sérialiser, réassigner, ou découper la tâche. Jamais « on verra au merge ».

---

## 4. Conflits de propriété

| Situation | Décision |
|---|---|
| Deux tâches veulent le même fichier | L'orchestrateur sérialise ; la seconde attend |
| Un bug est dans le périmètre d'un autre | Ouvrir une task card `fix`, ne pas corriger |
| Un contrat doit changer | Spec-analyst + owner + humain ; mise à jour des consommateurs |
| Un fichier partagé doit changer | Rapport de proposition ; l'écrivain désigné applique |
| Un agent a déjà modifié un fichier hors scope | Stop, rapport `blocked`, ne pas continuer ; l'intégrateur décide de garder/revertir |
| Un worktree et l'arbre principal divergent | L'intégrateur merge ; pas de copie manuelle |

---

## 5. Worktrees et branches

- Branche par tâche : `task/T-XXXX-<slug>`.
- Worktree optionnel : `.worktrees/T-XXXX` (gitignored).
- Un worktree = une tâche = un agent.
- Pas de partage de worktree entre agents.
- Après merge : supprimer la branche et le worktree.
- Ne jamais travailler directement sur `main`.

---

## 6. Exceptions

Une exception à la carte de propriété doit être :
1. explicitement listée dans `files_owned` de la task card ;
2. justifiée dans le rapport (pourquoi ce fichier, quel impact) ;
3. reviewée par le propriétaire du domaine ou l'orchestrateur.

Une exception non documentée est un `blocker` de review.
