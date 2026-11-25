# Métriques — Guitar Card AI-Motion Studio

> **Statut :** initialisation (2026-11-25)
> **Règle :** métriques légères, mises à jour par l'orchestrateur en fin de vague.

---

## 1. Flux

| Métrique | Définition | Cible | Dernière valeur |
|---|---|---|---|
| Lead time | `done` - `claimed` | < 1 jour | — |
| First-pass gate rate | tâches sans rework / total | > 70 % | — |
| Rework | tâches rouvertes / total | < 20 % | — |
| Questions bloquantes | nombre / âge max | 0 avant vague | — |
| Conflits de merge | par vague | < 2 | — |
| Tests flaky | par suite | 0 | — |

## 2. Qualité

| Métrique | Cible | Dernière valeur |
|---|---|---|
| Couverture `core/` | ≥ 85 % | — |
| `mypy --strict` core | 0 erreur | — |
| Tests unitaires | tous verts | — |
| Tests d'intégration | tous verts | — |
| Golden grammar | 4/4 | — |

## 3. Performance (à calibrer)

| Métrique | Cible initiale | Dernière valeur |
|---|---|---|
| Preview 1080p | ≥ 30 fps | — |
| Export 1080p30 | ≥ 1× temps réel CPU | — |
| Analyse audio 4 min | < 60 s | — |
| Demucs 4 min CPU | < 10 min | — |
| Mémoire preview | < 500 Mo | — |
| Taille bundle | à définir | — |

## 4. Coût / contexte

| Métrique | Cible | Dernière valeur |
|---|---|---|
| Fichiers lus par tâche | ≤ 5 | — |
| Taille task card | ≤ 1 page | — |
| Taille rapport | ≤ 1 page | — |
| Agents parallèles | ≤ 3 implémenteurs | — |

## 5. Historique

| Date | Vague | Lead time moyen | Gates 1er coup | Questions ouvertes | Notes |
|---|---|---|---|---|---|
| 2026-11-25 | — | — | — | 9 P0/P1 | Initialisation |
