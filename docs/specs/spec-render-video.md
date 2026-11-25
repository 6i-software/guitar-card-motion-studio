# Spécification — Rendu vidéo et animation

> **Contexte** : `core/image/`, `core/render/`, `services/`
> **Rôle** : Définir le moteur d'animation pur et le rendu export vidéo 

---

## 1. Moteur d'animation

- Fonction pure : `(état, t) -> overlay RGBA` partagée entre la prévisualisation temps réel et l'export vidéo.
- Conversion temps (`float` en secondes à la ms) → index de frame via une règle d'arrondi unique et centralisée.

---

## Personnalisation de l'animation

- Choix de la couleur de surbrillance du motif et de la couleur d'annonce (*next motif*)
- Définition de la durée d'anticipation du next motif (ex. `0,2 s` à `1,2 s`), du style des compteurs (pips, badge texte `2/5`, ou désactivés)
- Activation (ou non) du fondu d'entrée et de fin de la vidéo
- Activation (ou non) de l'intensité du halo/pulsation

---

## 2. Rendu et export
- Fenêtre d'export : codec vidéo, codec audio, résolution, FPS, barre de progression, **temps restant estimé**, annulation propre.
- Détection automatique de l'accélération matérielle (`nvenc`, `qsv`, `videotoolbox`, `vaapi`, `amf`) : lister les encodeurs via `ffmpeg -encoders`, **valider par un encodage test d'une frame**, puis **repli** sur logiciel (`libx264`).
- Pipeline : frame de base calculée **une fois** ; par frame, seule la ROI est recomposée (alpha blending numpy) ; cache des états visuels identiques ; écriture sur `stdin` de ffmpeg via file bornée.
- Robustesse du pipe : lire `stderr`/`-progress pipe:` dans un thread dédié (sinon deadlock), gérer `BrokenPipeError`, fermer stdin proprement, tuer le process à l'annulation et **supprimer le fichier partiel**.
- **Robustesse du processus** :
  - Lire `stderr` / `-progress pipe:` dans un thread dédié pour éviter tout deadlock.
  - Gérer `BrokenPipeError`, fermer `stdin` proprement, et en cas d'annulation ou d'erreur, arrêter le processus et **supprimer le fichier partiel**.
  - Muxer l'audio et contrôler la cohérence de durée vidéo/audio selon la tolérance définie. garantir durée vidéo = durée audio (tolérance documentée).

---