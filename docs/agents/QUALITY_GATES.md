# Gates de qualité et Definition of Done

> **Statut :** adopté (2026-11-25, cadre complet)
> **Règle :** un rapport sans preuve de gate n'est pas un rapport `done`.

---

## 1. Vue d'ensemble

| Gate | Objet | Commande de référence | Bloquant pour |
|---|---|---|---|
| G0 | Spec prête | revue de task card | coder |
| G1 | Statique | `ruff check`, `ruff format --check`, `mypy`, message de commit conforme | commit / review |
| G2 | Unitaire | `pytest tests/unit` | review |
| G3 | Intégration | `pytest tests/integration` + golden + intégrité | merge |
| G4 | UI / démo | `pytest tests/ui` + checklist manuelle | clôture de vague |
| G5 | Release | suite complète + build + machine vierge + licences | release |

Les commandes seront centralisées dans `scripts/ci.py` (tâche T-0002). En attendant, utiliser les commandes directes ci-dessous.

---

## 2. G0 — Spec prête

**Critères :**
- [ ] Objectif et périmètre in/out.
- [ ] Critères d'acceptation testables.
- [ ] `files_owned` sans chevauchement.
- [ ] Dépendances satisfaites ou contrat gelé.
- [ ] Specs/contrats liés.
- [ ] Risques et questions bloquantes identifiés.
- [ ] Taille ≤ 1 jour.

**Preuve :** task card complète + validation de l'orchestrateur.

---

## 3. G1 — Statique

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src/gcstudio/core
```

**Critères :**
- Zéro erreur ruff.
- Formatage conforme.
- `mypy --strict` sur `core/` (config dans `pyproject.toml`).
- Pas de `# type: ignore` non justifié.
- Pas d'import Qt dans `core/` (test dédié).
- Commit conforme à `docs/agents/COMMITS.md` : gitmoji + Conventional Commits, anglais, `Refs: T-XXXX`.

**Périmètre :** pour un agent, lancer d'abord sur ses fichiers, puis la gate complète avant handoff. Ne jamais faire `ruff format .` (formatage global interdit).

---

## 4. G2 — Tests unitaires

```bash
uv run pytest tests/unit -q
uv run pytest tests/unit/grammar -q          # ciblé
```

**Critères :**
- Tous les tests unitaires passent.
- Les nouveaux comportements ont un test.
- Les cas limites identifiés dans la task card sont couverts.
- Pas de test skippé sans justification.
- Pas de réseau, pas de dépendance à un fichier local non versionné.
- Durée cible : < 60 s sur une machine de dev.

**Preuve :** sortie pytest (nombre de tests, durée) dans le rapport.

---

## 5. G3 — Intégration

```bash
uv run pytest tests/integration -q
uv run pytest -m "not slow" -q
uv run pytest -m slow -q          # si ffmpeg/demucs disponibles
```

**Critères :**
- Golden tests grammaire verts (4 cartes).
- Test d'intégrité image : N frames, pixels hors ROI identiques à la source (fondus désactivés).
- Round-trip projet : save/load, migration, projet corrompu.
- Export court : MP4 valide, durée et audio vérifiés via `ffprobe` (marqué `slow`).
- Diagnostics : un test par type de problème.
- Pas de flaky : un test instable est marqué `xfail`/quarantaine avec une tâche de fix.

**Preuve :** commandes + résultats + artefacts (hash, durée, ffprobe) dans le rapport.

---

## 6. G4 — UI et démo

```bash
uv run pytest tests/ui -q
uv run python -m gcstudio
```

**Checklist manuelle :**
- [ ] L'écran s'ouvre sans erreur.
- [ ] Le parcours principal est utilisable.
- [ ] L'UI ne bloque pas pendant une tâche longue (progression visible, annulation).
- [ ] Les messages d'erreur sont en français clair.
- [ ] Le redimensionnement/les chemins avec espaces/accents fonctionnent.
- [ ] La preview tient le budget de FPS défini (à calibrer).

**Preuve :** capture ou description dans le rapport de vague.

---

## 7. G5 — Release

```bash
uv run pytest -q
uv run python scripts/build_portable.py --target=PyInstaller
uv run python scripts/build_portable.py --target=Nuitka
```

**Critères :**
- Suite complète verte (unit + integration + ui + slow si possible).
- Build PyInstaller et/ou Nuitka produit.
- Test sur machine vierge (ou VM) : lancement, import image/audio, preview, export court.
- `THIRD_PARTY_LICENSES.md` à jour (dont `matplotlib`, BSD).
- `CHANGELOG.md` à jour.
- Version bump + tag (validation humaine).
- Pas de binaire lourd dans Git.
- PR mergée en merge commit ; pas de squash/rebase.

**Preuve :** rapport de release `docs/releases/vX.Y.Z.md` + artefacts.

---

## 8. Definition of Done (rappel)

Une tâche est `done` si :
- [ ] G0 respectée.
- [ ] G1 et G2 vertes.
- [ ] G3 verte si la tâche touche une intégration.
- [ ] G4 si UI.
- [ ] Rapport écrit avec preuves.
- [ ] Review indépendante, blockers corrigés.
- [ ] Board à jour.
- [ ] Décisions/questions consignées.
- [ ] Changelog si visible utilisateur.
- [ ] Commit gitmoji + Conventional Commits, PR ouverte puis mergée.
- [ ] Handoff explicite.

---

## 9. Tests : stratégie par domaine

| Domaine | Tests obligatoires |
|---|---|
| Grammar | golden 4 cartes, property `hypothesis`, cas d'erreur, spans |
| Model | validation pydantic, sérialisation, migrations, immuabilité |
| Projects | round-trip, écriture atomique, corruption, duplication |
| Image | chargement EXIF/RGBA, ROI, couleur, intégrité hors ROI |
| Render | frame pure, conversion temps→frame, pipe, annulation, partial cleanup |
| Audio | fixtures synthétiques BPM/onset, normalisation, cache, rapport |
| Demucs | séparation courte, progression, annulation, rapport, CPU fallback |
| Sync | alignement ground truth, confiance, locked, diagnostics |
| UI | smoke pytest-qt, workers, i18n, raccourcis |
| YouTube | chapitres, timestamps, description, copie |

---

## 10. Politique de flakiness

- Un test qui échoue de façon non déterministe est **immédiatement** signalé.
- Il est marqué `@pytest.mark.flaky` (ou `xfail(strict=True)`) et une task card `fix` est ouverte.
- Il ne peut pas rester dans la suite par défaut.
- Les tests `slow` sont exclus par défaut et exécutés en G3/G5.
- Les tests réseau sont interdits.

---

## 11. Couverture et typage

```bash
uv run pytest --cov=gcstudio.core --cov-report=term-missing
```

- `pytest-cov` est la seule dépendance de couverture (groupe dev, décision `D7`).
- Modules purs (`grammar`, `model`, `sync`, `render`) : objectif pragmatique **80–85 %**, pas 100 %.
- `ui/` et `services/` : pas d'objectif de couverture ; smoke tests et scénarios.
- `mypy --strict` sur `core/`.
- `services/` : typage progressif, pas de `Any` non justifié.
- La couverture est une **aide**, pas une fin : les critères d'acceptation priment.

---

## 12. Performance (à calibrer)

| Métrique | Cible initiale | Mesure |
|---|---|---|
| Preview 1080p | ≥ 30 fps | `scripts/bench_preview.py` (à créer) |
| Export 1080p30 | ≥ 1× temps réel sur CPU | chrono + `ffprobe` |
| Analyse audio 4 min | < 60 s | chrono |
| Demucs 4 min CPU | < 10 min | chrono |
| Mémoire preview | < 500 Mo | profileur |
| Taille bundle | à définir | build |

Ces cibles sont des hypothèses à valider en M7/M8. Toute régression > 20 % doit être expliquée dans le rapport.

---

## 13. Preuves et logs

- Les commandes sont copiées dans le rapport avec leur résultat (pas seulement « tests OK »).
- Les logs longs vont dans `docs/reports/attachments/` ou un fichier temporaire, pas dans le rapport.
- Ne jamais inclure de secret, token, chemin personnel ou contenu protégé.
- Un échec connu et accepté doit être explicitement listé avec sa justification et sa task card de suivi.
