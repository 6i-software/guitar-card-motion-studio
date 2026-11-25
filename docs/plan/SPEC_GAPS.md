# Analyse des lacunes et ambiguïtés des specs

> **Statut :** adopté (2026-11-25, cadre complet)
> **But :** lister ce qui manque ou se contredit avant de lancer les agents, avec une priorité et une recommandation.
> **Règle :** une lacune P0 bloque une tâche ; une lacune P1 bloque un milestone ; une lacune P2 est à traiter plus tard.

---

## 1. Synthèse

Les specs couvrent bien la vision, la grammaire, le modèle de données, l'audio, le rendu et YouTube. Les manques les plus structurants sont :

1. **Grammaire** : `D10` + `D15` tranchent les multiplicateurs, les noms (`Punk2`), les variantes (`A^n`) et le cumul de modificateurs ; `D12` tranche la zone des variantes. Reste `Q8` (compteurs de groupe).
2. **Modèle de données** : les compteurs de groupe (`x2`) ne sont pas représentables dans `Occurrence` tel que spécifié ; `bbox` n'a pas d'espace de coordonnées défini.
3. **Temps/rendu** : la règle de conversion seconde → frame n'est pas fixée ; la tolérance durée vidéo/audio n'est pas chiffrée.
4. **Audio** : la cible de normalisation (fréquence, canaux, profondeur) n'est pas fixée ; le choix du modèle Demucs est un spike.
5. **Image** : la détection ROI/zones n'a pas d'algorithme ni de critère d'acceptation ; le fallback manuel est la seule certitude.
6. **Dépendances** : résolu par `D7` + `D11` — `pytest-cov` en dev, `matplotlib` en runtime pour les rapports ; pas de `scikit-learn`.
7. **Licences** : ffmpeg/libx264 et poids Demucs restent à documenter ; exemples protégés hors Git (`D8`).
8. **Écriture** : résolu par `D9` — `output/description-youtube.txt` dans le projet, dossier configurable.

---

## 2. Questions P0 — bloquantes pour M0/M1

| ID | Sujet | Question | Recommandation | Impact |
|---|---|---|---|---|
| Q4 | `Punk2` vs `Punkx2` | `Punk2` (sans `x`) est-il un nom, ou une répétition ? | Résolu `D15` : `Punk2` est un **nom** joué une fois ; `A Solo1 AA Solo2` = A, Solo1, A, A, Solo2. `A2` est ambigu → `error` `GC-GRAM-008`. | Lexer, parser, golden, zones |
| Q5 | Compteur préfixe sur groupe | `2{AA}` est-il valide ? | Résolu `D10` : accepté mais déconseillé (`info`) ; préférer `4A` ou `{AA}x2`. | Parser, diagnostics |
| Q6 | Modificateurs répétés | `A##`, `A~~`, `A#~` sont-ils valides ? | Résolu `D10` : cumul autorisé (`A##` = variante de variante), `A^n` recommandé ; mapping exact en Q35. | Lexer, motif_key |
| Q7 | Zone des variantes | `a`/`A#` partagent-ils la case de `A` ? | Résolu `D12` : `a` est un motif distinct (`motif_key="a"`, `family_key="A"`) avec sa propre zone ; `A^2`/`A#` aussi, famille `A`. Override manuel possible si même case. | Modèle, zones, animation |
| Q8 | Compteurs de groupe | Comment représenter `{5A BB}x2` : 5 pips sous `5A`, 2 pips sous `x2` ? | Ajouter `group_path: list[GroupRef]` avec `repetition_index/total` par groupe ; l'UI affiche le compteur du groupe le plus interne. | Occurrence, UI, YouTube |
| Q9 | Conversion temps → frame | `round`, `floor` ou `ceil` ? | `floor(t * fps + 1e-9)` pour le début, `ceil(end * fps - 1e-9)` pour la fin, avec clamp ; documenter et tester. | Rendu, export, sync |
| Q10 | Normalisation audio | Fréquence, canaux, profondeur ? | WAV PCM 44,1 kHz, stéréo conservé, 16 bits (ou float32 interne) ; documenter. | Import, cache, sync |
| Q35 | `A^n` vs `#`/`~` | `A^2` ≡ `A##` ? Comment combiner `~` ? | Résolu `D15` : `A^1` ≡ `A#`, `A^2` ≡ `A##` ; `~` est orthogonal (`A^2~`) ; `A~^2` refusé (`GC-GRAM-009`). | Lexer, modèle, golden |
| Q15 | Exemples protégés | Les MP3/PNG de `docs/examples` doivent-ils être dans Git ? | Résolu `D8` : hors Git ; fixtures synthétiques pour la CI. | Dépôt, CI, licences |
| Q16 | Sortie YouTube | `./build/youtube-description.txt` viole I2. Où écrire ? | Résolu `D9` : `output/description-youtube.txt`, dossier configurable. | YouTube, I2 |

---

## 3. Questions P1 — bloquantes pour M2–M5

| ID | Sujet | Question | Recommandation | Impact |
|---|---|---|---|---|
| Q11 | Dépendances manquantes | Peut-on ajouter `matplotlib` (rapports), `pytest-cov` (couverture) ? `scikit-learn` pour le clustering ? | Résolu `D7` + `D11` : `pytest-cov` en dev, `matplotlib` en runtime ; pas de `scikit-learn`. | Stack, licences, build |
| Q12 | ROI auto | Quel algorithme et quel critère d'acceptation ? | Baseline : détection de la zone de texte contrastée + projection ; confiance + fallback manuel. Spike avant engagement. | M2, UI |
| Q13 | Zones par motif | OCR, template matching ou manuel ? | v1 : auto best-effort + éditeur manuel obligatoire ; pas d'OCR fiable promis. | M2, UI |
| Q14 | Précision sync | Quelle tolérance sur les frontières ? | Cible ±0,15 s sur les frontières à forte attaque ; ±0,3 s ailleurs ; score de confiance calibré sur The Wolf. | M5, tests |
| Q17 | `bbox` | « espace normalisé » = pixels source ou 0..1 ? | Pixels dans l'image source, origine top-left, `w/h > 0` ; conversion au rendu. | Modèle, UI, rendu |
| Q18 | `Timeline.duration` | Est-ce la durée audio, la fin du dernier event, ou les deux ? | `duration` = durée audio de référence ; `end` du dernier event peut être ≤ duration ; diagnostic si écart. | Modèle, sync, export |
| Q19 | Fade/halo | `fade_in/out` bool sans durée ; `halo_pulse` bool ou intensité ? | Ajouter `fade_duration_s` (0,2–2 s) et `halo_intensity` (0–1) ; valeurs par défaut documentées. | Style, rendu |
| Q20 | Chapitres | Granularité : occurrence, groupe, section ? | Un chapitre par « run » de groupe ou par changement de motif majeur ; configurable. | YouTube |

---

## 4. Questions P2 — M6–M10

| ID | Sujet | Question | Recommandation |
|---|---|---|---|
| Q21 | Architecture UI | Navigation, état, injection de dépendances ? | `QMainWindow` + écrans, `AppState` injecté, pas de singleton ; services via constructeurs. |
| Q22 | i18n | Workflow Qt `.ts`/`.qm`, chaînes source ? | Sources françaises dans `tr()`, `.ts` par langue, build `.qm` au packaging. |
| Q23 | Logging | Format, niveaux, rotation, localisation ? | Log texte rotatif dans `QStandardPaths.AppLocalDataLocation`, niveau configurable, pas de secret. |
| Q24 | Undo/redo | Portée : projet entier ou écran ? | Projet entier, snapshots immuables ; limite mémoire à définir. |
| Q25 | Autosave | Fréquence, recovery ? | Autosave toutes les 2 min dans le projet, recovery au lancement. |
| Q26 | CI | GitHub Actions ou local seulement ? | Local `scripts/ci.py` d'abord ; GitHub Actions quand le remote existe. |
| Q27 | OS/Python | Versions minimales ? | **Python 3.12** (librosa 1.x et numpy/scipy récents l'exigent), Windows 10+, macOS 12+, Ubuntu 22.04+. |
| Q28 | ffmpeg | Build LGPL ou GPL ? | LGPL si possible ; `libx264` est GPL → documenter l'obligation et la distribution. |
| Q29 | Poids Demucs | Modèle et licence ? | Spike 4 stems vs 6 stems ; vérifier licence des poids ; bundle build-time. |
| Q30 | Taille bundle | Budget ? | À mesurer après M10 ; documenter, pas de promesse avant. |
| Q31 | Perf preview | Cible FPS/résolution ? | 1080p ≥ 30 fps sur machine de dev moyenne ; à calibrer. |
| Q32 | Export | Tolérance durée vidéo/audio ? | ±1 frame ou ±50 ms, au plus strict ; documenter. |
| Q33 | Accessibilité | Contraste, focus, raccourcis ? | Base : focus clavier visible, contraste AA, raccourcis configurables. |
| Q34 | Sécurité | Télémétrie, réseau ? | Aucune télémétrie, aucun réseau à l'exécution. |

---

> **Note de numérotation :** les questions Q1–Q16 et Q35 sont dans `OPEN_QUESTIONS.md`. Les IDs Q17–Q34 ci-dessous sont des IDs de travail pour la planification ; ils seront migrés vers `OPEN_QUESTIONS.md` lorsqu'ils deviennent bloquants, sans réutiliser un ID existant.

## 5. Incohérences et dettes documentaires

| # | Fichier | Constat | Recommandation |
|---|---|---|---|
| I-01 | `docs/OPEN_QUESTIONS.md` | `Q1` est absente alors que `D1` la clôt. | Ajouter une section « Résolues » avec Q1 → D1. |
| I-02 | `docs/OPEN_QUESTIONS.md` Q2 | La spec 4.1.2 répond déjà à Q2. | Marquer Q2 « Résolue par spec 4.1.2 », à archiver en décision. |
| I-03 | `docs/SPEC.md` | Référence « SPEC.md 6. Grammaire » qui n'existe pas dans ce fichier. | Pointer vers `docs/specs/spec-grammar-guitar-card.md`. |
| I-04 | `docs/specs/spec-youtube.md` | Écrit dans `./build/youtube-description.txt` → viole I2. | Écrire dans `output/` du projet ou dossier d'export. |
| I-05 | `docs/specs/spec-render-video.md` | Les puces « Robustesse du pipe » et « Robustesse du processus » se répètent. | Fusionner. |
| I-06 | `docs/specs/spec-render-video.md` | Tolérance durée vidéo/audio non chiffrée. | Fixer ±1 frame / ±50 ms. |
| I-07 | `docs/specs/spec-data-model.md` | `Event.occurrence_ref` n'a pas de type précis. | Définir `OccurrenceRef(index, motif_key)` ou un ID stable. |
| I-08 | `docs/specs/spec-data-model.md` | `ZoneRegion.bbox` « espace normalisé » ambigu. | Définir pixels source top-left. |
| I-09 | `docs/specs/spec-data-model.md` | Modèles « immuables ou copiés » sans règle. | `pydantic` `frozen=True` ou copy-on-write explicite. |
| I-10 | `docs/specs/spec-audio-sequence-alignement.md` | `librosa.load` : default vs `sr=None, mono=False` contradictoire. | Une règle par usage : analyse = 22,05 kHz mono ; inspection = natif. |
| I-11 | `docs/specs/spec-audio-sequence-alignement.md` | Passe 3 décrite mais pas de spec de comparaison/rapport final. | Ajouter une section « comparaison des analyses ». |
| I-12 | `AGENTS.md` v1 | Stack sans `pytest-cov` alors que la couverture est demandée. | Résolu `D7` + `D11` : `pytest-cov` en dev, `matplotlib` en runtime. |
| I-13 | `AGENTS.md` v1 | « Aucune écriture hors config/projet/export » vs `./build` YouTube. | Voir I-04. |
| I-14 | `AGENTS.md` v1 | « Pas de fichiers intermédiaires lourds » vs stems/caches Demucs. | Préciser : la règle vise les frames de rendu, pas les caches audio. |
| I-15 | `AGENTS.md` v1 | `[À VALIDER]` annoncé mais aucun point marqué. | Supprimé dans la v2 ; utiliser `OPEN_QUESTIONS.md`. |
| I-16 | `docs/examples` | MP3/PNG protégés, aucun `.gitignore`, aucun commit initial. | Décider avant le premier commit (Q15). |
| I-17 | `AGENTS.md` v1 | « mypy strict sur core » sans config ni plugin pydantic. | Ajouter config `pyproject.toml` en T-0001/T-0002. |
| I-18 | `AGENTS.md` v1 | « couverture ≥ 85 % » sans `pytest-cov`. | Résolu `D7` : `pytest-cov`, objectif pragmatique 80–85 % sur les modules purs. |
| I-19 | `docs/specs/spec-grammar-guitar-card.md` | EBNF `named := [A-Z][a-z]+ INT?` contredit la priorité `x<INT>` et ne définit pas `Punk2`. | Résolu `D15` : le chiffre sans `x` fait partie du nom ; mettre à jour l'EBNF. |
| I-20 | `docs/specs/spec-grammar-guitar-card.md` | `modifier*` autorise les doublons sans sémantique. | Résolu `D10` + `D15` : `A##` ≡ `A^2`, `A~^2` refusé ; mettre à jour l'EBNF. |
| I-21 | Environnement | `uv` absent, `python` = 3.14.0 ; la stack cible 3.11+ avec PyTorch/Demucs. | **Résolu** : `uv` 0.13.10 + Python 3.12.16 installés le 2026-11-25. |
| I-22 | `spec-audio` | La spec suppose l'API librosa 0.x ; la version courante est 1.0.1 (Python ≥3.12). | Épingler `librosa>=1.0,<2` et smoke-tester `load`, `beat_track`, `onset_detect`, `chroma_*`, `segment` dès M3 ; repli 0.11 si rupture. |
| I-23 | `spec-grammar` | L'EBNF ne couvre ni `^INT`, ni le compteur préfixe, ni la priorité `x<INT>`. | T-0004 aligne l'EBNF sur `D10`/`D15` ; le contrat `core-grammar` v0.1-r2 fait foi en attendant. |

---

## 6. Ce qui manque complètement

| Sujet | Pourquoi c'est nécessaire | Où l'ajouter |
|---|---|---|
| Spec d'architecture | Frontières, DI, threading, erreurs, logging | `docs/specs/spec-architecture.md` |
| NFR / budgets | Perf preview/export, mémoire, taille bundle, temps Demucs | `docs/specs/spec-nfr.md` |
| Spec i18n | Workflow Qt, langues, formats | `docs/specs/spec-i18n.md` |
| Spec packaging | PyInstaller/Nuitka, binaires, poids, licences, OS | `docs/specs/spec-packaging.md` |
| `THIRD_PARTY_LICENSES.md` | Obligation légale, ffmpeg/Demucs/PySide6 | racine |
| Matrice de tests | Quels tests par milestone, fixtures, ground truth | `docs/plan/TEST_MATRIX.md` |
| Ground truth The Wolf | Timestamps de référence pour la sync | `tests/fixtures/sync/the_wolf_ground_truth.json` |
| Catalogue d'erreurs | Codes, messages FR, actions correctives | `docs/specs/spec-errors.md` |
| Stratégie de cache | Audio, stems, features, invalidation | `docs/specs/spec-cache.md` |
| Politique de données | Aucune télémétrie, logs, chemins | `docs/specs/spec-privacy.md` |

---

## 7. Ordre de résolution recommandé

1. **Avant M0** : Q11 (dépendances), Q15 (exemples/Git), Q27 (Python/OS), Q16 (sortie YouTube). — *résolu*
2. **Avant M1** : Q4, Q5, Q6, Q7, Q35 (résolues) ; restent Q8 (groupes), Q9 (temps→frame), Q10 (audio).
3. **Avant M2** : Q12, Q13, Q17.
4. **Avant M5** : Q14, Q18, Q19, Q20.
5. **Avant M6** : Q21–Q26.
6. **Avant M8** : Q28, Q32.
7. **Avant M10** : Q29, Q30, Q31, Q33, Q34.

---

## 8. Format d'une question

Dans `docs/OPEN_QUESTIONS.md` :

```markdown
## #Q4 — Suffixe numérique d'un motif nommé
- **Statut :** Ouvert | Bloquant | Résolu
- **Priorité :** P0 | P1 | P2
- **Contexte :** spec §...
- **Question :** ...
- **Options :**
  1. ...
  2. ...
- **Recommandation :** ...
- **Impact :** ...
- **Décision :** *(à compléter / D*)*
```
