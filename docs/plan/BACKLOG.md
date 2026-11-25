# Backlog — Guitar Card AI-Motion Studio

> **Statut :** adopté (2026-11-25, cadre complet)
> **Règle :** seules les tâches `ready` peuvent être claim. Les tâches `proposed` doivent d'abord passer la DoR (voir `docs/agents/PLAYBOOK.md` §5.2).

---

## 1. Légende

| Statut | Signification |
|---|---|
| `proposed` | Idée, pas encore découpée/validée |
| `ready` | DoR remplie, peut être claim |
| `claimed` | Assignée, branche créée |
| `in_progress` | En cours |
| `review` | En review |
| `verification` | QA en cours |
| `done` | Terminée, mergée |
| `blocked` | Bloquée par une question/décision |

---

## 2. Prochaines vagues (détaillées)

### W0.1 — Scaffold

| ID | Titre | Rôle | Dépend | Statut | Task card |
|---|---|---|---|---|---|
| T-0001 | Scaffold uv + fenêtre hello world | platform-dev | — | `ready` | `T-0001-scaffold.md` |
| T-0002 | Gates locales + `scripts/ci.py` | integrator | T-0001 | `ready` | `T-0002-quality-gates.md` |
| T-0003 | Erreurs `GCStudioException` + logging rotatif | platform-dev | T-0001 | `ready` | `T-0003-logging-errors.md` |
| T-0009 | README + guide de démarrage | spec-analyst | T-0001 | `proposed` | à créer |

### W1.1 — Contrat + lexer

| ID | Titre | Rôle | Dépend | Statut | Task card |
|---|---|---|---|---|---|
| T-0004 | Contrat `core/grammar` v0.2 | spec-analyst | T-0001 | `ready` | `T-0004-grammar-contract.md` |
| T-0005 | Lexer + spans + multiplicateurs | core-dev | T-0004 | `ready` | `T-0005-lexer.md` |
| T-0008 | Golden + property tests | qa-verifier | T-0004 | `proposed` | à créer |

---

## 3. Backlog complet (indicatif)

### M0 — Scaffold

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0001 | Scaffold uv + hello world | platform-dev | — | `ready` |
| T-0002 | Gates locales + CI script | integrator | T-0001 | `ready` |
| T-0003 | Erreurs + logging | platform-dev | T-0001 | `ready` |
| T-0009 | README + démarrage | spec-analyst | T-0001 | `proposed` |

### M1 — Grammaire

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0004 | Contrat grammar v0.2 | spec-analyst | T-0001 | `ready` |
| T-0005 | Lexer | core-dev | T-0004 | `ready` |
| T-0006 | Parser + AST | core-dev | T-0005 | `proposed` |
| T-0007 | Expand + compteurs de groupe | core-dev | T-0006 | `proposed` |
| T-0008 | Golden + property tests | qa-verifier | T-0004 | `proposed` |
| T-0010 | Diagnostics localisés | core-dev | T-0006 | `proposed` |

### M2 — Image

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0011 | Load/normalize image | render-dev | T-0001 | `proposed` |
| T-0012 | Couleur primaire | render-dev | T-0011 | `proposed` |
| T-0013 | ROI auto (spike + baseline) | render-dev | T-0011 | `proposed` |
| T-0014 | Éditeur de zones manuel | ui-dev | T-0013 | `proposed` |
| T-0015 | Intégrité overlay hors ROI | render-dev | T-0011 | `proposed` |

### M3 — Audio passe 1

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0016 | Import/normalisation ffmpeg | audio-dev | T-0001 | `proposed` |
| T-0017 | Features librosa + cache | audio-dev | T-0016 | `proposed` |
| T-0018 | Rapport audio + fixtures | audio-dev | T-0017 | `proposed` |

### M4 — Demucs

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0019 | Worker Demucs + annulation | audio-dev | T-0016 | `proposed` |
| T-0020 | Cache stems + rapport | audio-dev | T-0019 | `proposed` |
| T-0021 | Spike modèle 4/6 stems + GPU | audio-dev | T-0019 | `proposed` |

### M5 — Sync

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0022 | Contrat timeline + Event | spec-analyst | T-0004 | `proposed` |
| T-0023 | Alignement v1 + confiance | audio-dev | T-0017, T-0022 | `proposed` |
| T-0024 | Diagnostics + ground truth The Wolf | audio-dev | T-0023 | `proposed` |

### M6 — Timeline UI

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0025 | Widget timeline + waveform | ui-dev | T-0022 | `proposed` |
| T-0026 | Marqueurs, drag, snapping | ui-dev | T-0025 | `proposed` |
| T-0027 | Tap-to-sync + undo/redo | ui-dev | T-0026 | `proposed` |

### M7 — Animation

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0028 | Moteur d'animation pur | render-dev | T-0015, T-0022 | `proposed` |
| T-0029 | Preview + styles | ui-dev | T-0028 | `proposed` |
| T-0030 | Rapport de simulation | qa-verifier | T-0029 | `proposed` |

### M8 — Export

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0031 | Pipe ffmpeg + mux audio | render-dev | T-0028 | `proposed` |
| T-0032 | Hwaccel + fallback | render-dev | T-0031 | `proposed` |
| T-0033 | UI export + annulation | ui-dev | T-0031 | `proposed` |

### M9 — Projets + YouTube

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0034 | Project + schéma v1 + atomic write | core-dev | T-0001 | `proposed` |
| T-0035 | Migrations + mode dégradé + bibliothèque | core-dev | T-0034 | `proposed` |
| T-0036 | Chapitres + description YouTube | core-dev | T-0034, T-0022 | `proposed` |

### M10 — Packaging

| ID | Titre | Rôle | Dépend | Statut |
|---|---|---|---|---|
| T-0037 | PyInstaller + ffmpeg/ffprobe | integrator | T-0033 | `proposed` |
| T-0038 | Nuitka + poids Demucs + licences | integrator | T-0037 | `proposed` |
| T-0039 | Tests machine vierge 3 OS | qa-verifier | T-0038 | `proposed` |

---

## 4. Règles de priorisation

1. **Bloquant spec** : une question P0 bloque la task qui en dépend.
2. **Chemin critique** : M1 → M2/M3 → M5 → M6 → M7 → M8 → M10.
3. **Parallélisme** : M2 et M3 peuvent avancer ensemble ; M9 après M1.
4. **Dette** : une vague par milestone, jamais dans une feature.
5. **Pas de task sans critère d'acceptation** : sinon elle reste `proposed`.

---

## 5. Prochaine action

1. Valider le plan et `AGENTS.md` v2.
2. Arbitrer les questions P0 de `docs/plan/SPEC_GAPS.md`.
3. Lancer W0.1 : T-0001, T-0002, T-0003 en parallèle.
4. Détailer W1.1 après la démo M0.
