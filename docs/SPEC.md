# Spécification — Produit et vision globale

## 1. Finalité du produit

Offrir aux guitaristes et créateurs de contenu YouTube une application de bureau nomade cross-platform (Windows, macOS, Linux) capable de transformer une **Guitar Card** (image de partition simplifiée avec une séquence de motifs dans la ROI=region of interest) et une piste audio en une **vidéo animée synchronisée** mettant en valeur le motif actif, annonçant le motif suivant, affichant les compteurs de répétition, et sans altérer le reste de l'image.

L'application est nomade, elle fonctionne hors ligne et sans prérequis système (moteurs audio/analyse et encodeur vidéo (`ffmpeg`/`ffprobe`) inclus).

L'UI est en **français par défaut** avec support i18n.

## 2. Input/Output

Entrées : 
 - une image de Guitar Card (`PNG`, `JPG`, `WebP`, ...) avec le titre et le texte de la séquence de motifs (riffs)
 - et un fichier audio (`MP3`, `WAV`, `FLAC`, ...), normalisé à l'import pour garantir une référence temporelle fiable.

**Sorties** :
 - Vidéo synchronisée (prévisualisation temps réel et export final encodé avec audio) ;
 - Chapitres horodatés (`0:00`) des motifs de la guitar card ; 
 - Bloc de description YouTube ;
 - Projets GuitarCard Motion Studio locaux sauvegardés et réutilisables.

## 3. Parcours utilisateur

1. **Créer / ouvrir un projet GuitarCard Motion Studio** : importer l'image et l'audio (ou ouvrir/dupliquer un projet existant).
2. Une fois l'image chargée, analyse pour détecter la zone des riffs de la guitar card et pour identifier la couleur primaire de la carte.
3. **Préparer la carte** : vérifier/ajuster la zone globale des riffs (ROI), les zones individuelles par motif et le texte de la séquence. 
4. **Analyser et synchroniser** : lancer l'analyse audio (et la séparation guitare si utile), obtenir une proposition d'alignement avec score de confiance, puis affiner manuellement (timeline, *tap-to-sync*, saisie numérique, verrouillage des points clés). Lire les rapports d'analyse audio et de synchronisation, et évauler le score de confiance de la guitar card par rapport à la piste audio. 
5. **Contrôler et styliser** : vérifier les diagnostics, personnaliser couleurs, délai anticipation d'annonce du prochain motif, compteurs, halo et fondus, puis simuler en temps réel la lecture de la guitar card. 
6. **Exporter** : générer la vidéo finale et copier/exporter les chapitres et la description YouTube.

## 4. Exigences transverses

- **Respect de l'image** : l'animation se concentre sur la zone des motifs sans dénaturer le reste de l'image.
- **Maîtrise utilisateur** : l'outil assiste et accélère la synchronisation, mais l'utilisateur garde le dernier mot sur les timestamps.
- **Fiabilité et simplicité** : interface claire en français par défaut (avec anglais démarche i18n), messages compréhensibles, journal technique (log) des comptes rendus d'éxécution (avec différents niveaux de verbosité)