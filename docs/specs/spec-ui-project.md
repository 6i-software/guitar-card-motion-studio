# Spécification — Interface utilisateur, projets

> **Contexte** : `ui/`, `core/projects/`, `services/`  
> **Rôle** : Définir l'architecture des écrans PySide6, la timeline interactive, l'internationalisation et la gestion de projets locaux 

---

## 1. Interface utilisateur (`ui/`)

- **Framework** : **PySide6** (Qt 6), strictement découplé de `core/` (aucun import Qt dans `core/`).
- **Écrans principaux** :
    - *Import* (image de la carte + fichier audio) ;
    - *Atelier de carte* (ROI globale, zones par motif, texte de la Guitar Card) ;
    - *Analyse* (rapports audio, séparation Demucs, diagnostics) ;
    - *Timeline / Sync* (édition fine et synchronisation manuelle) ;
    - *Personnalisation* (choix des couleurs, durée de l'anticipation, compteurs, fondus, halo) ;
    - *Export* (paramètres vidéo/audio, progression, temps restant, annulation, export YouTube) ;
    - *Bibliothèque* (liste, ouverture, duplication et recherche de projets).
- **Timeline interactive** : widget custom performant intégrant, marqueurs déplaçables, zoom, snapping optionnel, saisie numérique précise et *tap-to-sync* (touche `M` configurable avec calibration de latence audio/UI). Design similaire aux timelines des éditeurs vidéo.
- **Ergonomie, i18n et erreurs** :
    - Français par défaut + anglais dès le départ via le système de traduction Qt (`tr`), configurable dans *Paramètres > Langue*.
    - Raccourcis clavier configurables et accessibilité de base (contrastes, focus clavier, tailles de police).
    - Messages d'erreur en français clair avec action corrective proposée ; compte rendu d'éxécution et détails techniques consignés dans un fichier `.log` rotatif consultable.

---

## 2. Gestion des projets (`core/projects/`)

- **Structure locale** : un répertoire par projet contenant `project.json` + les assets copiés/normalisés (`image`, `audio`, texte de carte, MIDI éventuel) + métadonnées (`title`, `description`, `author`, `album`, `created_at`, `updated_at`).
- **Fonctions** : créer, ouvrir, dupliquer (variante), régénérer un rendu et rechercher dans la bibliothèque.
- **Intégrité et résilience** :
    - Écritures atomiques (fichier temporaire puis renommage) et confirmation UI avant suppression ou écrasement d'assets utilisateur.
    - Migrations explicites basées sur `schema_version`.
    - Ouverture en **mode dégradé** avec rapport explicite si un projet est partiellement corrompu.

---

## 3. Export chapitres et description YouTube (`core/youtube/`)

- **Référentiel** : lire `docs/specs/spec-youtube.md` avant toute implémentation.
- **Sortie** : liste de chapitres horodatés (ex. `0:00 Intro / 5A`, `0:39 BB`…) et bloc de description youtube complet prêt à copier-coller intégrant la Guitar Card et les timestamps.