# Spécification — Modèle de données 

> **Contexte** : `core/model/`, `core/projects/`  
> **Rôle** : Définir les entités métier du cœur (Project, Timeline, Marker, Pattern, ZoneRegion…), les règles de précision temporelle, l'immuabilité / historique Undo-Redo, la persistance projet (`project.json`) et les migrations de schéma.

---

## 1. Principes généraux

- **Isolation UI** : aucune dépendance à `PySide6` / Qt dans les modèles, ni d'aucun code d'interface. Tests sans UI.
- **Validation stricte** : modèles structurés avec `pydantic` v2 (ou dataclasses/types strictement annotés validés aux frontières I/O).
- Tout modèle persistant porte un `schema_version` et passe par des migrations explicites.
- **Immuabilité et copies contrôlées** : les états du projet sont traités de façon immuable ou copiés lors des mutations afin de garantir un historique Undo/Redo fiable et prédictible.
- **Temps en secondes** : toutes les durées et positions temporelles (`start`, `end`, `duration`, `t`) sont stockées en **secondes (`float`) arrondies à la milliseconde** (`round(val, 3)`). La conversion en index de frame se fait uniquement au rendu via une règle d'arrondi unique, centralisée et testée.

---

## 2. Entités principales

### 2.1 `Project`
Racine d'un projet Guitar Card persisté sur disque.

- `id` : identifiant unique du projet (`str` / UUID).
- `schema_version` : version entière du schéma de données (ex. `1`), obligatoire pour les migrations.
- `metadata` : `ProjectMetadata`.
- `assets` : références relatives aux fichiers du dossier projet (image source, audio normalisé/original, éventuels stems ou fichiers annexes).
- `card_text` : texte brut de la Guitar Card saisi par l'utilisateur.
- `zones` : liste de `ZoneRegion` (Region Of Interest (ROI) globale et zones individuelles par motif).
- `timeline` : `Timeline` (événements synchronisés et marqueurs).
- `style` : `AnimationStyle` (paramètres visuels de surbrillance, anticipation, compteurs, fondus, halo).
- `export_prefs` : préférences d'export (résolution, FPS, codecs, dossier de sortie par défaut).

### 2.2 `ProjectMetadata`
- `title` : titre du projet / morceau.
- `description` : description libre (réutilisable notamment pour l'export YouTube).
- `author` : guitariste / interprète / créateur.
- `album` : album ou contexte éventuel.
- `created_at` / `updated_at` : horodatages ISO-8601.

### 2.3 `ZoneRegion`
Représente une zone rectangulaire sur l'image de la carte.

- `id` : identifiant unique de la zone.
- `motif_key` : clé de motif associée (ex. `A`, `A#`, `|4`, `Punk`, ou identifiant de ROI globale).
- `bbox` : coordonnées `(x, y, w, h)` en pixels dans l'espace normalisé de l'image source.
- `source` : `"auto"` (détection automatique) ou `"manual"` (ajustée/créée par l'utilisateur).

### 2.4 `Timeline` & `Event`
- `Timeline` :
  - `duration` : durée de référence en secondes (`float`, arrondie à la ms).
  - `events` : liste ordonnée d'`Event`.
  - `markers` : liste optionnelle de `Marker` (`pattern_change | section`, `t`, `label`).
- `Event` :
  - `id` : identifiant unique de l'événement.
  - `occurrence_ref` : référence vers l'`Occurrence` issue de l'expansion de la grammaire (index, motif, répétition).
  - `start` / `end` : bornes temporelles en secondes (`float`, arrondies à la ms), avec `end >= start`.
  - `zone_id` : identifiant de la `ZoneRegion` ciblée (ou `None` si non encore associée).
  - `locked` : `bool` (`True` = timestamp verrouillé manuellement, jamais écrasé par un recalcul automatique).
  - `confidence` : `float | None` (score de confiance de l'alignement automatique, `None` si manuel).

### 2.5 `AnimationStyle`
- `highlight_color` : couleur de surbrillance du motif actif.
- `next_color` : couleur d'annonce du motif suivant.
- `anticipation_s` : fenêtre d'anticipation en secondes (`0.2` à `1.2`).
- `counter_style` : `"pips" | "badge" | "off"`.
- `fade_in` : `bool` (fondu d'entrée global).
- `fade_out` : `bool` (fondu de sortie global).
- `halo_pulse` : activation et intensité (`bool` ou niveau d'intensité).

---

## 3. Historique Undo / Redo

Les modèles du cœur sont **immuables ou copiés à l'édition** (undo/redo simple côté UI). Ce qui permet que l'historique d'édition côté UI repose sur trois piles d'états :
- `past: list[object]`
- `present: object`
- `future: list[object]`

Règles :
- **Undo (`Ctrl+Z`)** : dépile le dernier élément de `past`, pousse `present` dans `future`, et définit cet élément comme nouveau `present`.
- **Redo (`Ctrl+Y` / `Ctrl+Shift+Z`)** : dépile le premier élément de `future`, pousse `present` dans `past`, et définit cet élément comme nouveau `present`.
- **Nouvelle modification** : vide `future` (`[]`) pour éviter les branches d'historique divergentes.

---

## 4. Persistance, migrations et résilience

- **Structure d'un projet** : un répertoire dédié contenant `project.json` et les assets copiés/normalisés (`assets/`), génération par défaut dans `output/`.
- **Écriture atomique** : toute sauvegarde écrit d'abord dans un fichier temporaire du même répertoire, *flush*/*fsync* si pertinent, puis remplace `project.json` par renommage atomique.
- **Migrations de schéma** : si `schema_version < CURRENT_SCHEMA_VERSION`, appliquer séquentiellement les fonctions de migration enregistrées (`v1 -> v2 -> ...`) avant validation.
- **Mode dégradé** : si un fichier de projet est partiellement corrompu ou incomplet, tenter une récupération partielle plutôt qu'un crash brutal, et retourner un rapport explicite des éléments récupérés ou ignorés.
