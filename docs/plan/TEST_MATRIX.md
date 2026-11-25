# Matrice de tests par milestone

> **Statut :** adopté (2026-11-25, cadre complet)
> **Règle :** un critère d'acceptation sans test est une intention, pas une preuve.

---

## 1. Niveaux

| Niveau | Emplacement | Marqueur | Quand |
|---|---|---|---|
| Unitaire | `tests/unit/**` | — | G2, chaque tâche |
| Intégration | `tests/integration/**` | — | G3, avant merge |
| Slow | `tests/integration/**` ou `tests/e2e/**` | `@pytest.mark.slow` | G3/G5, si ffmpeg/GPU dispo |
| UI | `tests/ui/**` | `@pytest.mark.ui` | G4 |
| Property | `tests/unit/**` | `@pytest.mark.property` | G2 |

Configuration pytest (à créer en T-0001) : `slow` et `ui` exclus par défaut, `-m "not slow"` pour la suite rapide.

---

## 2. Matrice

| Milestone | Unitaire | Intégration | Slow / manuel | Preuve attendue |
|---|---|---|---|---|
| M0 Scaffold | import, core purity, erreurs, logging | — | lancement manuel | gates vertes + capture |
| M1 Grammaire | lexer, parser, expand, diagnostics, property | 4 golden | fuzz long (optionnel) | golden 4/4, aucun crash |
| M2 Image | load, ROI, couleur, zones | intégrité hors ROI (100 frames) | 5 cartes réelles | hash pixels hors ROI |
| M3 Audio | import, features, cache, rapport | fixture synthétique bout en bout | The Wolf (local) | BPM/durée dans la tolérance |
| M4 Demucs | cache, rapport, annulation | séparation extrait court | séparation complète CPU | rapport d'énergie + verdict |
| M5 Sync | alignement, confiance, locked, diagnostics | ground truth The Wolf | écoute manuelle | frontières dans la tolérance |
| M6 Timeline UI | modèles de vue, undo/redo | smoke `pytest-qt` | démo interactive | capture + scénario |
| M7 Animation | moteur pur, styles | intégrité N frames + preview | perf 1080p | fps mesurés + hash |
| M8 Export | conversion temps→frame, args ffmpeg | MP4 2 s + ffprobe | The Wolf complet | durée/audio/annulation |
| M9 Projets/YouTube | schéma, migrations, chapitres | round-trip + projet corrompu | — | fixtures v1→v2 |
| M10 Packaging | — | smoke bundle | 3 OS machine vierge | matrice + licences |

---

## 3. Fixtures

| Fixture | Contenu | Versionnée | Propriétaire |
|---|---|---|---|
| `tests/fixtures/audio/` | WAV synthétiques (clics, motifs, BPM connus) | oui | audio-dev |
| `tests/fixtures/images/` | PNG synthétiques + cartes libres | oui | render-dev |
| `tests/fixtures/projects/` | projets v1, v2, corrompu | oui | core-dev |
| `tests/fixtures/sync/` | ground truth JSON (timings) | oui | audio-dev / qa-verifier |
| `docs/examples/**` | MP3/PNG réels | **non** (Q15) | humain |

Règles :
- Aucune fixture ne dépend du réseau.
- Aucune fixture ne contient de musique/artwork protégé.
- Une fixture lourde (> 1 Mo) doit être justifiée ; préférer la génération déterministe.
- Toute fixture a un test qui la valide (durée, hash, schéma).

---

## 4. Ground truth

| Donnée | Source | Usage |
|---|---|---|
| The Wolf : BPM ≈ 123–124, durée ≈ 227,709 s | PoC + ffprobe | audio, sync |
| The Wolf : structure `5A BB 5A BB C C# BBB A` | PoC | grammaire, sync |
| The Wolf : frontières A/B | à extraire et valider humainement | sync |

Le ground truth est un fichier JSON versionné, avec une note de confiance par timestamp. Il ne remplace pas une validation humaine.

---

## 5. Règles

1. Un bug corrigé ⇒ un test de reproduction (sauf incident critique documenté).
2. Un golden qui change ⇒ analyse, pas mise à jour automatique.
3. Un test flaky ⇒ quarantaine + task card, jamais `skip` silencieux.
4. Un test `slow` non exécutable localement doit être signalé dans le rapport.
5. La couverture est mesurée avec `pytest-cov` (Q11) et seuil sur `core/` uniquement.
