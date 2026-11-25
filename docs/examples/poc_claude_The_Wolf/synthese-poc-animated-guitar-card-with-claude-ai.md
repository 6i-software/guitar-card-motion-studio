# Motivations

L'objectif de l'expérimentation était de transformer une "**Guitar Card"** statique au format PNG (`1920×1080`, RGBA) représentant la structure d'un morceau à la guitare (*Guitar card The Wolf*, notée `{ 5A BB } x 2`, `CC#`, `BBB`, `A`) en une vidéo synchronisée avec le MP3 de la chanson, mettant en surbrillance le motif actif, annonçant le motif suivant, affichant des indicateurs de progression (répétitions de `5A` et passes `x2`) et pulsant au tempo détecté du morceau.

Pour le processus, on a donc deux entrées :

* le MP3 du morceau
* l'image de la carte de guitare

Et on souhaite obtenir en sortie, une vidéo généré à partir de cette image qui anime la Guitar Card.

# Prompt IA pour la définition du contexte 

En préambule de la demande, voila les éléments techniques qui ont été passé à Claude pour contextualisé le travail demandé

## Evaluer les méthodes d'analyse audio

### Via partition ou notation symbolique (MIDI, MusicXML, ABC, tablature, grille d’accords en texte)

C’est l’analyse la plus précise avec du code (Python, music21, pretty_midi), je peux :

* détecter les motifs mélodiques et rythmiques qui se répètent, y compris transposés ou légèrement variés
* identifier les progressions d’accords récurrentes et la structure (couplet, refrain, pont)
* analyser la tonalité, les modulations, le rythme harmonique
* produire une matrice d’auto-similarité ou un schéma de la structure du morceau

### Via l'analyse du signal audio (mp3, wav, flac...)

#### Librosa, la référence Python

Librosa est la bibliothèque Python de référence pour l'analyse de signaux audio et le traitement de la musique (*Music Information Retrieval* - MIR) sur CPU. Elle permet de charger facilement des fichiers sonores sous forme de tableaux NumPy et d'en extraire des caractéristiques acoustiques essentielles :

* **Analyse spectrale :** spectrogrammes, transformée de Fourier (STFT), spectrogrammes Mel.
* **Extraction de caractéristiques :** coefficients MFCC, chromagrammes (notes/accords), centroïde spectral.
* **Analyse rythmique :** détection du tempo (BPM) et suivi des temps (*beat tracking*).

Idéale en combinaison avec des bibliothèques de Machine Learning (Scikit-learn, PyTorch) ou de visualisation (Matplotlib), elle constitue la boîte à outils standard pour la classification audio, la reconnaissance vocale ou l'analyse musicale automatisée.

#### Torchaudio, le passage au deep-learning GPU

La solution alternative ou complémentaire Torchaudio (combiné avec TorchCodec) permet une approche plus industrialisé et de deep learning pour entrainer et déployer des modèles PyTorch sur de gros volumes de données. 

* **Accélération GPU native et** ***batching*** **:** avec cette architecture par GPU (ex. CUDA) et traitement par lots (*batches*)  il est possible de traiter des centaines ou milliers d'extraits audio en *batch* au lieu d'une boucle itérative par fichier sur CPU, le débit peut bondir d'un facteur de 10× à 50×+ (voire plus sur des transformées répétées pendant l'entraînement d'un modèle, où l'on évite de recalculer ou de transférer depuis le CPU à chaque époque). Techniquement les transformées (`Spectrogram`, `MelSpectrogram`, `MFCC`, `Resample`, augmentations type *SpecAugment*) tournent directement sur tenseurs GPU par lots (*batches*). Sur des dizaines ou centaines de milliers de fichiers, le gain de débit est massif par rapport à une boucle Python/NumPy sur CPU avec `librosa`. Par contre, notons que le gain est presque nul, sur CPU (i.e. sans GPU), dans ce cas les gains sont modestes (souvent **1,5× à 3×** selon la taille des signaux et le *batching*), car `librosa` s'appuie déjà sur NumPy/SciPy/Numba.
* **Richesse** ***Music Information Retrieval*** **(MIR) moindre :** `librosa` reste bien plus fourni et intuitif pour l'analyse musicale de haut niveau (détection de *beats*/tempo, *chroma* avancés, décomposition harmonique/percussive *HPSS*, *onset* musicaux, outils de visualisation dédiés). Avec `torchaudio`, il faut assembler soi-même les briques ou garder `librosa` pour l'exploration.
* **Coût de développement et de déploiement :** \
**Avec** `librosa` **:** quelques minutes pour charger, tracer un spectrogramme ou tester une idée.\
**Avec** `TorchCodec` **+** `torchaudio` **:** un peu plus de mise au point au départ (calage des paramètres de fenêtre/Mel si tu compares avec `librosa`, gestion de l'environnement et de la compatibilité `torch` / `torchaudio` / `torchcodec` / FFmpeg).

### Essentia : Environnement MIR / extraction de descripteurs

Boîte à outils très riche pour l'analyse musicale et acoustique (tempo, rythme, tonalité/accords, énergie, *loudness*, descripteurs spectraux, *extractors* tout prêts et modèles pré-entraînés).

* **Pros vs Librosa :**
  * **Beaucoup plus rapide sur l'extraction massive de descripteurs** : le cœur est en C++ (avec FFTW / Eigen), sans l'overhead Python/Numba typique de `librosa` sur de gros volumes de morceaux.
  * **Algorithmes MIR prêts à l'emploi** : propose des chaînes d'extraction complètes (*MusicExtractor*, *FreesoundExtractor*, estimation de tonalité/rythme) là où `librosa` demande souvent d'assembler soi-même plusieurs fonctions.
* **Cons vs Librosa :**
  * **Moins facile d'accès / plus « bas niveau » ou orienté graphes d'algorithmes** : sa logique (algorithmes, *pool* de résultats, conventions de paramètres) déroute davantage quand on vient de la simplicité NumPy/Python de `librosa`.
  * **Installation et packaging parfois plus exigeants** : selon l'OS, l'environnement Python et les dépendances natives, c'est moins plug-and-play qu'un petit script `librosa` + `soundfile`.
  * **Licence AGPLv3** : contraignante si tu intègres le code dans un produit fermé ou un service exposé sans ouvrir les sources correspondantes.

### AudioFlux : intéressant sur le papier, plus jeune / plus niche

Bibliothèque en C et Python axée sur le calcul temps-fréquence, l'extraction de *features* et l'analyse audio, avec une licence MIT permissive.

* **Pros vs Librosa :**
  * **Licence MIT** : très souple pour réutiliser, adapter ou intégrer sans les contraintes *copyleft* d'une AGPL.
  * **Cœur C orienté calcul de transformées /** ***features*** : conçu pour aller vite sur certaines décompositions et extractions de caractéristiques numériques.
* **Cons vs Librosa :**
  * **Moins « facile » et moins standard dans l'écosystème** : communauté, exemples, tutoriels, recettes prêtes à l'emploi et intégrations tierces sont nettement moindres que pour `librosa`.
  * **Écosystème plus récent / plus étroit** : si tu cherches la fiabilité éprouvée, la documentation abondante ou la compatibilité large avec d'autres outils Python audio, `librosa` reste plus rassurant pour démarrer.

### En résumé

* Le gain de vitesse éventuel d'un entrainement/inférence avec Pytorch sur GPU ne vaut pas la complexité supplémentaire.
* Essentia : moins intuitif au début que `librosa` ; il prend tout son sens quand tu veux extraire massivement des descripteurs musicaux/acoustiques en C++ et que le modèle de licence AGPLv3 ne pose pas de problème.
* AudioFlux : moins mature à considérer si tu veux du **MIT** et du calcul C pour des *features* spécifiques, mais **moins évident à prendre en main** au quotidien qu'un `librosa` bien document

Pour l'analyse et l'exploration musicale d'une dizaine, voir d'une centaine de fichiers, l'option librosa exclusivement est largement suffisant. 

## Spécifications

Pour décrire le travail

### C'est quoi une guitare card ?

Le principe est simple, une lettre désigne un riff à jouer. « *Pour l'introduction, tu joues deux fois le motif A, puis quatre fois le motif B* » — soit 2A 4B. Concis, visuel, et redoutablement efficace. Puis pour ajouter du relief et des variations, on ajoute aussi des symboles clés.

Quelques exemples :

* Une lettre (A, B, C...) = pour un motif précis
* Avec un symbole (A#, A~) = pour une variante mélodique et/ou rythmique du motif
* En minuscule (aA) = pour une variante d'intensité (*pianissimo pour la lettre minuscule*) du motif
* Le symbole ¦4 pour un arpège et |4 pour un barré sur la 4ième frète, qui peut ou non être un power chord exclusif ou accompagné d'une mélodie sur les doigts libres.
* Et plein d'autres ! C'est ultra-flexible pour (essayer honnêtement) de capturer l'intention exacte du morceau.

### Exemple d'une guitare card

Pour le morceau The Wolf de Billy Talent, voila sa guitar card associé.

```javascript
{ 5A BB } x 2
CC#
BBB
A
```

Exemple d'illustration

![preview.webp](../exemples/Guitar-card_The-Wolf/guitar_card_The_Wolf.webp)

### Résultat attendu

Transformé l'image de la guitar card donné en une vidéo où l'on peut apprécier visuellement la progression du morceau. L'idée est de recolorer uniquement les lettres du motifs en cours et de prevoir une transition (fondu ou pulsation) quelques instants avant le changement effectif de motif, pour annoncer la transition au guitariste. 

ATTENTION ! Il ne faut pas traiter le reste de l'image, seul la partie de la guitar card doit être impacté.

# Déroulement chronologique des étapes et logs

### Étape 1 — Réponse Claude prompt IA

Je génère les images avec Python et je les assemble avec ffmpeg, mais deux limites sont à régler avant.

**Comment je comprends ta carte**

* `5A` = le motif A joué 5 fois.
* La séquence complète donne : 5A, BB, 5A, BB, C, C#, B, B, B, A, soit 20 riffs au total.
* Les `x2` de l’accolade répètent le bloc `{5A BB}` en entier.

**Comment je fabrique la vidéo**

* Je reprends ton image telle quelle (loup, titre, police d’origine). Je recolore uniquement les lettres du motif en cours.
* Je prévois une transition (fondu ou pulsation) un peu avant le changement, pour annoncer le prochain motif.
* J’exporte en 1920×1080 pour les 3 min 51 du morceau.

**Pour la synchro, deux options**

1. **Tu m’envoies le fichier audio** (mp3 ou wav) du morceau. J’analyse les temps et les sections avec librosa, je te propose un découpage riff par riff, tu corriges les erreurs, et je recolle le son dans la vidéo finale. C’est plus rapide pour toi, mais la détection de A, B ou C reste approximative sur un morceau avec batterie et voix, donc ta validation sera nécessaire.
2. **Tu me donnes les timestamps** relevés à la main, par exemple `0:00 → 5A`, `0:48 → BB`… C’est plus fiable, et je produis une vidéo sans le son, que tu pourras superposer à l’audio dans ton éditeur.

Tu peux m’envoyer le fichier audio du morceau ?\
*=> dépôt du fichier mp3*

### Étape 2 — Inspection de l'environnement et des fichiers d'entrée

* **Actions & commandes** : vérification de la présence des fichiers d'entrée (`018 - The_Wolf.mp3` de ~9,2 Mo et `Billy_NO_Talent - Guitar_card_v2__juillet_2026___018 - The_Wolf.png` de ~1,67 Mo), des binaires `ffmpeg` / `ffprobe` et des bibliothèques Python (`PIL` 13.0.0, `cv2` 5.0.0, `numpy`, `scipy`, `librosa`).
* **Résultats clés** :
  * `librosa` était absent au premier test puis installé (`1.0.1`) via `pip install librosa --break-system-packages`.
  * Analyse de l'image est en `1920×1080` (`RGBA`, alpha constant à `255`), et le bleu présent sur la carte (`x2`) a été relevé autour de `RGB(96, 130, 169)`.
  * La durée réelle du MP3 (`44100 Hz`, stéréo, `320 kb/s`) mesurée par `ffprobe` est de **227,709 s** (3 min 47,7 s) et non 3 min 51 s, et `librosa.load` à `sr=22050` a donné `227,660 s`.

### Étape 3 — Analyse du tempo, des beats et de l'énergie (`analyze.py`)

test

* **Méthode** : chargement mono à `22050 Hz`, `hop_length=512`, détection des temps via `librosa.beat.beat_track(..., start_bpm=100)`, calcul de l'enveloppe d'attaque (`onset_strength`) et du niveau quadratique moyen (`RMS`) par fenêtres de 4 secondes ; sauvegarde de `beats.npy`.
* **Résultats clés** : 
  * tempo estimé à `123.05 BPM` (`455` beats détectés, premier beat à `0,77 s`)
  * montée nette d'énergie vers `0:08` (`RMS` passant d'environ `0,05–0,07` à `> 0,21`) 
  * et fin/extinction vers `3:40–3:44`.test

### Étape 4 — Recherche de périodicité et matrice d'auto-similarité (`seg_analysis.py` et `ssm.py`)

* **Actions & commandes** :

Un premier script (`struct.py`, renommé `seg_analysis.py` après une erreur d'import circulaire `numpy`/`scipy` résolue par nettoyage de `__pycache__`) a calculé un chromagramme CQT (`12 × 456`) et des MFCC (`13 × 456`) synchronisés aux beats, puis une autocorrélation sur les lags de 2 à 80 beats : les meilleurs lags ressortent à **32 beats** (`2,593`) et **16 beats** (`2,549`).

```shellscript
python3 seg_analysis.py

Output
(12, 456) (13, 456)
best lags (beats): [(32, np.float32(2.593)), (16, np.float32(2.549)), (2, np.float32(2.494)), (31, np.float32(2.49)), (4, np.float32(2.441)), (33, np.float32(2.434)), (30, np.float32(2.429)), (28, np.float32(2.414)), (15, np.float32(2.409)), (34, np.float32(2.401)), (17, np.float32(2.4)), (48, np.float32(2.397))]
G G G G G G F F D# D# D# G G G G G G G G G G G F F D# D# D# D# C C C G G G G G G G F F D# D# D# D# C C D D G G G G G F F D# D# D# D# C C C C G G G G G G F F G D# D# D# D C C C A#
```

**Génération de la matrice d'auto-similarity (ssm.png)**

Le script `ssm.py` a construit une matrice d'auto-similarité (`SSM`) empilant `ctx=4` beats sur les chromagrammes (poids `1.0`), MFCC (`0.6`) et `RMS` en dB (`1.5`), puis appliqué un noyau damier (*checkerboard kernel* de taille `L=8` et `L=16` fenêtré par Hann) pour détecter les pics de nouveauté (`nov8.npy`, `nov16.npy`).

![image.png](matrix-self-similarity_ssm.png)

### Étape 5 — Segmentation en blocs de 16 beats et matching par gabarits (`chunks.py` et `match.py`)

* **Découpage par blocs (**`chunks.py`**)** : à partir du beat `14` (`7,5 s`), découpage en 27 blocs de `16` beats en concaténant les chromagrammes moyens sur 4 quarts de bloc (`Q` normalisé, similarité cosinus / produit scalaire `Sim = Q @ Q.T`). Cela a permis d'identifier des séquences récurrentes (blocs proches de `G-F-D#-C` pour `A` et `A#-A#-F-F` / `D#-D#-D-C` pour `B`), ainsi qu'une zone finale (à partir du bloc 19, `~155,1 s`) présentant des motifs de 24 et 32 beats.
* **Corrélation par gabarits (**`match.py`**)** : extraction de deux gabarits chromiques sur des zones jugées propres — **A** sur `16` beats (`beats 158:174`, `~77,7 s`) et **B** sur `32` beats (`beats 110:142`, `~54,5 s`) — puis calcul de la corrélation moyenne par beat (`cA.npy`, `cB.npy`). Les pics ont permis de localiser les occurrences de `A` (`16` beats) et `B` (`32` beats) et d'inspecter les classes de hauteur dominantes par groupe de 4 beats sur la fin du morceau (`beats 278` à `456`).\


### Étape 6 — Affinage des frontières et ajustement d'une grille temporelle linéaire (`snap.py`, `snap2.py`, `grid.py`)

* **Tentative d'alignement sur les attaques (**`snap.py`**)** : recherche du maximum d'enveloppe d'attaque (`hop=256`, `sr=44100`, `fmax=8000`) dans une fenêtre de `±0,45 s` autour des temps du tracker sur 8 frontières clés (`snapped.json`).
* **Affinage par nouveauté chromatique (**`snap2.py`**)** : sur `20` points de transition (`idx` de `15` à `454`, couvrant `A2..A5`, `B1..B2`, `A1..A5`, `B1..B2`, `C`, `C#`, `B1..B3`, `A`, `END`), calcul de la distance euclidienne entre le chromagramme moyen précédent et suivant (`w = 0,45 s`, rayon de recherche `±0,6 s`, lissage moyen sur 5 trames) pour produire `refined.json`.
* **Modélisation de grille (**`grid.py`**)** : régression linéaire itérative (`np.polyfit` degré 1, rejet des résidus `>= 0,25 s` sur 4 passes) reliant les indices de beats théoriques `b` aux instants affinés `t`. Deux points (`beat 96` et `beat 128`) ont été exclus ; sur les points conservés, le modèle donne :
* **Période** : `0,48354 s/beat` soit **124,09 BPM** (`t0 = 8,166 s` au beat `0` de référence).
* **Écart-type résiduel** : **0,042 s** (début théorique de l'intro `A` au beat `-16` : `0,43 s` ; fin du `A` final au beat `440` : `220,92 s`).\


### Étape 7 — Détection des boîtes englobantes de glyphes et rendu (`locate.py`, `locate2.py`, `render.py`)

* **Localisation visuelle** : analyse des pixels lumineux (`max(RGB) > 120` puis `> 70`) dans la zone droite (`x: 1440..1780`, `y: 430..730`) et génération d'un agrandissement (`crop_right.png`) pour définir manuellement les 9 zones (`GL`) correspondant aux motifs animés (`5A`, `B1a`, `B1b`, `C`, `Cs`, `B3a`, `B3b`, `B3c`, `A`).\
\
**Enregistrement du fichier** `crop_right.png`

![image.png](3-9bebe055-8c86-4e29-b307-c34d6e42178c.png)



* **Moteur de rendu (**`render.py`**)** :
  * Calcul d'un masque de couverture `cov` (`0..1`) et d'un halo gaussien `glow` (`sigma=5` pondéré `1.6` + `sigma=2` pondéré `0.5`) sur le crop `340×300`.
  * Coloration en **ambre** `RGB(255, 176, 56)` avec une pulsation exponentielle calée sur la phase du beat (`pulse = exp(-4.5 * ph)`).
  * Fenêtre d'anticipation de `1,0 s` (`ANN = 1.0`) allumant le motif suivant jusqu'à `0,55` avec une courbe *smoothstep* `ease(x) = x²(3 - 2x)`, relâchement sur `0,35 s` après transition, et fondu de sortie global entre `END_HOLD = tb(440) + 2.6` et `+ 1.6 s`.
  * Dessin anti-aliasé de **5 pips** sous `5A` (centre `(1525, 512)`, écart `11 px`, rayon `3 px`) et de **2 pips** sous `x2` (centre `(1713, 512)`), plus un correctif prolongeant `seq[-1]['t1']` jusqu'à `END_HOLD` afin que le dernier `A` ne s'éteigne pas prématurément.
  * **Génération de planches de contrôle (**`contact.png` **à partir de** `still_*.png`**).**

![image.png](4-4350c6a1-13cc-40a2-b182-6a6efef662c4.png)



### Étape 8 — Encodage vidéo contraint par timeout et livraison (`encode.py`, `region.py`, `seg.sh`)

* 6 831 images de texte sont prêtes. Assemblage final : image du loup + zone animée + audio MP3.
* **Problème rencontré** : un encodage direct en une passe (`encode.py`, `6831` images à `30 fps`, `libx264 -crf 17 -preset veryfast`, `aac 256k`) a dépassé la limite d'exécution de `300 s` (1 seul cœur CPU disponible, `~25 ms` par appel à `frame()`).
* **Stratégie de contournement**
  1. Génération des frames brutes (`rgb24`, `340×300`, `306 000` octets/frame) en deux tranches (`0..3500` -> `reg_a.rgb` et `3500..6831` -> `reg_b.rgb`), puis concaténation en `reg_all.rgb` (~2,09 Go).
  2. Encodage vidéo par segments via `seg.sh` (`dd` + `ffmpeg` overlay sur l'image `1920×1080` en `yuv420p`) : 4 blocs de `1500` frames (`seg_00.mp4` à `seg_03.mp4`) et 1 bloc de `831` frames (`seg_04.mp4`).
  3. Concaténation (`-c:v copy`) et muxage audio (`aac 256k`, `-movflags +faststart`) vers `the_wolf_guitar_card.mp4`, puis copie vers `/mnt/user-data/outputs/The_Wolf_guitar_card_animee.mp4` (`38 427 947` octets, `1920×1080`, `30 fps`, `6831` frames vidéo, `227,70 s`).
  4. Extraction de 9 images clés (`chk_*.png` -> `final_check.png`) pour vérification visuelle finale.

![image.png](5-9087bf01-eb1d-4497-b52b-493e3b04ca74.png)



### Étape 9 — Compte rendu d'éxecution

La vidéo "*The_Wolf_guitar_card_animee.mp4*" est prête : 1920×1080, 30 i/s, avec le son du MP3. Je n’ai pas pu l’écouter, je l’ai calée à partir de l’analyse du signal et de contrôles sur des images extraites, donc vérifie-la à l’oreille.

**Durée**. Le MP3 dure 3 min 47,7 s et non 3 min 51, donc la vidéo fait 3 min 47,7 s.

**Ce que montre la vidéo**

* Le motif en cours passe en ambre avec un léger halo qui pulse sur le tempo.
* Environ 1 s avant un changement, le motif suivant s’allume à moitié pour l’annoncer. Il prend ensuite le relais et le précédent s’éteint.
* Sous « 5A », cinq petits points comptent les répétitions du riff.
* Sous « x2 », deux points indiquent le tour (1/2 ou 2/2).
* Le loup, le titre et la police restent tels quels. À la fin, tout redevient blanc.

**Découpage détecté**. Le morceau tient un tempo stable d’environ 124 BPM. A dure 16 temps (≈ 7,7 s) et B en dure 32 (≈ 15,5 s).

| Motif      | Début → fin | Détail                                                         |
| ---------- | ----------- | -------------------------------------------------------------- |
| 5A         | 0:00 → 0:39 | l’intro douce (0 → 0:08) compte pour le 1er A, puis 4 A pleins |
| BB         | 0:39 → 1:10 | 2 × 15,5 s                                                     |
| 5A         | 1:10 → 1:49 | 5 × 7,7 s                                                      |
| BB         | 1:49 → 2:20 |                                                                |
| C          | 2:20 → 2:31 | 24 temps                                                       |
| C#         | 2:31 → 2:47 | 32 temps                                                       |
| BBB        | 2:47 → 3:33 | 3 × 15,5 s                                                     |
| A          | 3:33 → 3:41 | puis résonance et silence                                      |

Le comptage colle à ta carte : on retrouve bien 5 A, 2 B, 5 A, 2 B, C, C#, 3 B et A.

**Ce qui est moins sûr**. Les positions des A et des B sont solides, avec un écart de 0,04 s sur la grille. C et C# le sont moins : les 24 premiers temps de C# reproduisent C, puis 8 temps supplémentaires s’y ajoutent. J’en ai déduit que c’est la variante, mais je peux me tromper sur l’endroit exact de la frontière à 2:31. Le C# est aussi le seul passage où mon repérage manque de confirmation sonore.

Si une transition te paraît décalée, donne-moi le bon timestamp et je régénère la vidéo, attention cela prend du temps > dizaine de minutes. Je peux aussi changer la couleur (l’ambre est un choix de ma part, le bleu de ta carte étant déjà pris par « x2 »), retirer les petits points ou ajuster la durée de l’annonce.

### Annexe : code python exécuté par Claude dans son containeur Docker

````javascript
cd /mnt/user-data/uploads && ls -la && which ffmpeg ffprobe
ffprobe -hide_banner 018*-*The_Wolf.mp3 2>&1 | tail -8
python3 -c "import librosa, numpy, scipy; print('librosa', librosa.__version__)" 2>&1
python3 -c "import PIL; print('PIL', PIL.__version__)" 2>&1
python3 -c "import cv2; print('cv2', cv2.__version__)" 2>&1
python3 -c "from PIL import Image; im=Image.open('Billy_NO_Talent*-*Guitar_card_v2__juillet_2026___018*-*The_Wolf.png'); print(im.size, im.mode)"
```[cite: 1]

```bash
pip install librosa --break-system-packages -q 2>&1 | tail -3
python3 -c "import librosa; print(librosa.__version__)"
ffprobe -v error -show_entries format=duration -of csv=p=0 /mnt/user-data/uploads/018*-*The_Wolf.mp3
```[cite: 1]

### 2. Analyse du tempo, des beats, de l'attaque et du RMS (`analyze.py`)

```bash
mkdir -p /home/claude/work && cd /home/claude/work && cat > analyze.py <<'EOF'
import librosa, numpy as np, json
y, sr = librosa.load('/mnt/user-data/uploads/018*-*The_Wolf.mp3', sr=22050, mono=True)
dur = len(y)/sr
print("dur", dur)
hop=512
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop, start_bpm=100)
bt = librosa.frames_to_time(beats, sr=sr, hop_length=hop)
print("tempo", tempo, "nbeats", len(bt))
print("first beats", bt[:12].round(2))

# onset strength envelope
oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)

# RMS
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
t = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)

# print rms per 2 seconds
for s in range(0, int(dur), 4):
    m = (t>=s)&(t<s+4)
    print(f"{s//60}:{s%60:02d} rms={rms[m].mean():.3f} onset={oenv[:len(t)][m].mean():.2f}")
np.save('beats.npy', bt)
EOF
python3 analyze.py
```[cite: 1]

### 3. Autocorrélation chromatique (`struct.py` -> `seg_analysis.py`)

```bash
cd /home/claude/work && cat > struct.py <<'EOF'
import librosa, numpy as np
y, sr = librosa.load('/mnt/user-data/uploads/018*-*The_Wolf.mp3', sr=22050, mono=True)
hop=512
bt = np.load('beats.npy')
chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop)
bf = librosa.time_to_frames(bt, sr=sr, hop_length=hop)
cs = librosa.util.sync(chroma, bf, aggregate=np.median)
cs = librosa.util.normalize(cs, axis=0)
mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop, n_mfcc=13)
ms = librosa.util.sync(mfcc, bf, aggregate=np.mean)
print(cs.shape, ms.shape)

# self-similarity on chroma (beat-sync)
S = cs.T @ cs

# lag autocorrelation: mean similarity at each lag in beats
n = S.shape[0]
lags = range(2, 80)
ac = []
for L in lags:
    ac.append(np.mean(np.diag(S, L)))
ac = np.array(ac)
order = np.argsort(-ac)[:12]
print("best lags (beats):", [(list(lags)[i], round(ac[i],3)) for i in order])
np.save('cs.npy', cs)

# chord-ish dominant pitch class per bar-ish of 8 beats
names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
dom = [names[i] for i in cs.argmax(axis=0)]
print(' '.join(dom[:80]))
EOF
python3 struct.py
```[cite: 1]

```bash
cd /home/claude/work && mv struct.py seg_analysis.py && rm -rf __pycache__ && python3 seg_analysis.py
```[cite: 1]

### 4. Matrice d'auto-similarité et nouveauté (`ssm.py`)

```bash
cd /home/claude/work && cat > ssm.py <<'EOF'
import librosa, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
y, sr = librosa.load('/mnt/user-data/uploads/018*-*The_Wolf.mp3', sr=22050, mono=True)
hop=512
bt = np.load('beats.npy')
bf = librosa.time_to_frames(bt, sr=sr, hop_length=hop)
chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop)
mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop, n_mfcc=20)[1:]
rms = librosa.feature.rms(y=y, hop_length=hop)
def sync(X): 
    Z = librosa.util.sync(X, bf, aggregate=np.mean)
    Z = (Z - Z.mean(axis=1,keepdims=True))/(Z.std(axis=1,keepdims=True)+1e-6)
    return Z
F = np.vstack([sync(chroma)*1.0, sync(mfcc)*0.6, sync(librosa.amplitude_to_db(rms))*1.5])

# stack 4 beats of context
ctx=4
n=F.shape[1]
Fs = np.vstack([np.roll(F, -k, axis=1) for k in range(ctx)])
D = np.linalg.norm(Fs[:,:,None]-Fs[:,None,:],axis=0)
S = np.exp(-D/np.median(D))

# novelty with checkerboard kernel
def checker(L):
    g = np.outer(np.hanning(2*L), np.hanning(2*L))
    k = np.ones((2*L,2*L)); k[:L,L:]=-1; k[L:,:L]=-1
    return k*g

nov = {}
for L in (8,16):
    K = checker(L)
    N = np.zeros(n)
    Sp = np.pad(S, L, mode='edge')
    for i in range(n):
        N[i] = np.sum(Sp[i:i+2*L, i:i+2*L]*K)
    nov[L]=N
np.save('S.npy', S); np.save('nov8.npy', nov[8]); np.save('nov16.npy', nov[16])
fig,ax=plt.subplots(1,2,figsize=(18,8))
ax[0].imshow(S, origin='lower', cmap='magma', extent=[0,bt[-1],0,bt[-1]] if False else None)
ax[0].set_title('SSM (beats)')
ax[1].plot(nov[16]); ax[1].set_title('novelty L=16'); ax[1].plot(nov[8]*0.6,alpha=.5)
for x in range(0,n,16): ax[1].axvline(x,color='k',alpha=.1)
plt.savefig('ssm.png',dpi=80)

# peaks
from scipy.signal import find_peaks
for L in (8,16):
    pk,_ = find_peaks(nov[L], distance=8, prominence=np.std(nov[L])*0.6)
    print(L, [(int(p), round(float(bt[min(p,n-1)]),1)) for p in pk])
EOF
python3 ssm.py
```[cite: 1]

### 5. Segmentation en blocs de 16 beats et matching par gabarits (`chunks.py` et `match.py`)

```bash
cd /home/claude/work && cat > chunks.py <<'EOF'
import librosa, numpy as np
y, sr = librosa.load('/mnt/user-data/uploads/018*-*The_Wolf.mp3', sr=22050, mono=True)
hop=512
bt = np.load('beats.npy')
nb=len(bt)
chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop)
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
cent = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop)[0]
oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
bf = librosa.time_to_frames(bt, sr=sr, hop_length=hop)
def seg(X, a, b):
    fa, fb = bf[a], bf[min(b, nb-1)]
    return X[..., fa:fb]
names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
start=14; L=16
rows=[]
i=start
while i+L <= nb+2:
    a,b=i,i+L
    ch = seg(chroma,a,b)
    # chroma in 4 quarters (chord progression shape) 
    q = np.concatenate([ch[:, k*ch.shape[1]//4:(k+1)*ch.shape[1]//4].mean(axis=1) for k in range(4)])
    rows.append(dict(a=a,t=bt[a],q=q/np.linalg.norm(q),rms=seg(rms,a,b).mean(),cent=seg(cent,a,b).mean(),on=seg(oenv,a,b).mean(),
                     chord=[names[int(np.argmax(ch[:, k*ch.shape[1]//4:(k+1)*ch.shape[1]//4].mean(axis=1)))] for k in range(4)]))
    i+=L
Q = np.array([r['q'] for r in rows])
Sim = Q@Q.T
n=len(rows)
print("chunks:",n)
for k,r in enumerate(rows):
    # most similar earlier chunk
    best = max(range(k), key=lambda j: Sim[k,j]) if k>0 else -1
    print(f"{k:2d} t={r['t']:6.1f}s chords={'-'.join(r['chord']):<14} rms={r['rms']:.2f} cent={r['cent']:.0f} on={r['on']:.2f} nearest={best:2d} ({Sim[k,best]:.2f})" if k>0 else f"{k:2d} t={r['t']:6.1f}s chords={'-'.join(r['chord'])} rms={r['rms']:.2f}")
EOF
python3 chunks.py
```[cite: 1]

```bash
cd /home/claude/work && cat > match.py <<'EOF'
import librosa, numpy as np
from scipy.signal import find_peaks
y, sr = librosa.load('/mnt/user-data/uploads/018*-*The_Wolf.mp3', sr=22050, mono=True)
hop=512
bt = np.load('beats.npy'); nb=len(bt)
chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop)
bf = librosa.time_to_frames(bt, sr=sr, hop_length=hop)
C = librosa.util.sync(chroma, bf, aggregate=np.mean) # 12 x nb (beat i -> i..i+1)
C = C/ (np.linalg.norm(C,axis=0,keepdims=True)+1e-9)
names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def corr(template):
    T = template.shape[1]
    out=np.full(nb, np.nan)
    for i in range(nb-T+1):
        out[i] = np.mean(np.sum(C[:,i:i+T]*template,axis=0))
    return out

# templates from clean zones: A = chunk 9 (beats 14+9*16=158 .. 174) ; B = chunks 6-7 (110..142)
A = C[:,158:174]; B = C[:,110:142]
cA = corr(A); cB = corr(B)
def show(c, T, name, thr):
    pk,_ = find_peaks(np.nan_to_num(c,nan=0), height=thr, distance=T//2)
    print(name, [(int(p), round(float(bt[p]),1), round(float(c[p]),2)) for p in pk])
show(cA,16,'A (16b)',0.80)
show(cB,32,'B (32b)',0.80)
np.save('cA.npy',cA); np.save('cB.npy',cB)

# print beat-level dominant chord for last section for inspection
dom = [names[i] for i in C.argmax(axis=0)]
print("\nlast section beats 280-456 dominant pitch per 4 beats:")
for b in range(278, nb, 4):
    print(b, round(float(bt[b]),1), dom[b:b+4])
EOF
python3 match.py
```[cite: 1]

### 6. Vérification des sections, calage sur attaques et chromagramme (`refine.py`, `snap.py`, `snap2.py`)

```bash
cd /home/claude/work && cat > refine.py <<'EOF'
import librosa, numpy as np
y, sr = librosa.load('/mnt/user-data/uploads/018*-*The_Wolf.mp3', sr=22050, mono=True)
hop=512
bt = np.load('beats.npy'); nb=len(bt)
k = np.arange(nb)
p = np.polyfit(k, bt, 1)
res = bt - np.polyval(p,k)
print("period %.4f s => %.2f BPM, t0=%.3f ; residual std %.3f s, max %.3f s"%(p[0],60/p[0],p[1],res.std(),np.abs(res).max()))

# residual by sections
for a in range(0,nb,50): print(a, round(float(res[a:a+50].mean()),3), end=' | ')
print()
chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop)
bf = librosa.time_to_frames(bt, sr=sr, hop_length=hop)
C = librosa.util.sync(chroma, bf, aggregate=np.mean)
C = C/(np.linalg.norm(C,axis=0,keepdims=True)+1e-9)

# per-beat similarity between 286..310 and 310..334 (candidate C vs C#)
sim = np.sum(C[:,286:334-24]*C[:,310:334],axis=0)
print("C vs next 24 beats sim per beat:", sim.round(2))

# diverge check: beats 334..342 vs beats ~ 286+24..: compare with C first 8 beats..
for off in range(0,32):
    pass

# Intro: compare beats 0..14 to A template (beats 158..174 tail 14 beats)
A = C[:,158:174]
print("intro vs A tail:", np.sum(C[:,0:15]*A[:,1:16],axis=0).round(2))

# fine energy: rms per beat around 0..16 and end
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
t = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
for a,b in [(0,2),(2,4),(4,6),(6,8),(8,10)]:
    print(a,b, rms[(t>=a)&(t<b)].mean().round(3))
EOF
python3 refine.py
```[cite: 1]

```bash
cd /home/claude/work && cat > snap.py <<'EOF'
import librosa, numpy as np, json
y, sr = librosa.load('/mnt/user-data/uploads/018*-*The_Wolf.mp3', sr=44100, mono=True)
hop=256
bt = np.load('beats.npy')
oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop, aggregate=np.median, fmax=8000)
t = librosa.frames_to_time(np.arange(len(oenv)), sr=sr, hop_length=hop)

# candidate boundaries in beat-index (from template matching), then refine
cands = {
    'A2_loud_start': 15, 'BB1': 79, 'A5_2': 143, 'BB2': 223, 'C': 287, 'C#': 311, 'BBB': 343, 'A_end': 439,
}

# individual riff repetitions inside (16 or 32 beats) will be interpolated between snapped boundaries.
out={}
for name,b in cands.items():
    c = bt[b] if b < len(bt) else bt[-1]
    # use mean of tracker time at b-1..b+1 region as center
    win = (t>=c-0.45)&(t<=c+0.45)
    i = np.argmax(oenv[win]); tt = t[win][i]
    out[name]=(float(c), float(tt), float(oenv[win][i]), float(np.median(oenv[(t>=c-3)&(t<=c+3)])))
    print(f"{name:14s} tracker={c:7.2f} snapped={tt:7.2f} strength={oenv[win][i]:.1f} (local median {out[name][3]:.1f})")
json.dump(out, open('snapped.json','w'))
EOF
python3 snap.py
```[cite: 1]

```bash
cd /home/claude/work && cat > snap2.py <<'EOF'
import librosa, numpy as np, json
y, sr = librosa.load('/mnt/user-data/uploads/018*-*The_Wolf.mp3', sr=22050, mono=True)
hop=256
bt = np.load('beats.npy')
chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop, n_chroma=12)
fr = sr/hop
def nov_at(tc, w=0.45):
    a = int((tc-w)*fr); m=int(tc*fr); b=int((tc+w)*fr)
    p = chroma[:,a:m].mean(axis=1); n = chroma[:,m:b].mean(axis=1)
    return np.linalg.norm(p-n)
def refine(tc, rad=0.6):
    ts = np.arange(tc-rad, tc+rad, 1/fr)
    v = np.array([nov_at(x) for x in ts])
    v = np.convolve(v, np.ones(5)/5, mode='same')
    return float(ts[v.argmax()]), float(v.max()), float(np.median(v))

# boundary beat indices from template matching (start of each riff repetition)
idx = [15,31,47,63,78.5,110,142,158,174,190,206,222,254,286,310,342,374,406,438,454]
names = ['A2','A3','A4','A5','B1','B2','A1','A2','A3','A4','A5','B1','B2','C','C#','B1','B2','B3','A','END']
res=[]
for i,n in zip(idx,names):
    lo=int(np.floor(i)); tc = bt[lo]+ (i-lo)*(bt[min(lo+1,len(bt)-1)]-bt[lo])
    tr, v, med = refine(tc)
    res.append(tr)
    print(f"beat {i:6.1f} {n:3s} tracker={tc:7.2f} refined={tr:7.2f} delta={tr-tc:+.2f} nov={v:.2f} (med {med:.2f})")
res=np.array(res)
print("\ndurations:", np.diff(res).round(2))
json.dump(dict(idx=idx,names=names,refined=res.tolist()), open('refined.json','w'))
EOF
python3 snap2.py
```[cite: 1]

### 7. Détection des zones de glyphes et ajustement de la grille (`locate.py`, `locate2.py`, `grid.py`)

```bash
cd /home/claude/work && cat > locate.py <<'EOF'
from PIL import Image
import numpy as np
im = Image.open('/mnt/user-data/uploads/Billy_NO_Talent*-*Guitar_card_v2__juillet_2026___018*-*The_Wolf.png').convert('RGBA')
a = np.array(im)
print(a.shape, "alpha min/max", a[...,3].min(), a[...,3].max())
rgb = a[...,:3].astype(int)

# right panel region
x0,x1,y0,y1 = 1440,1780,430,740
reg = rgb[y0:y1, x0:x1]
bright = reg.max(axis=2)
mask = bright>120
rows = np.where(mask.any(axis=1))[0]

# group rows into lines
lines=[]; start=rows[0]; prev=rows[0]
for r in rows[1:]:
    if r-prev>6: lines.append((start,prev)); start=r
    prev=r
lines.append((start,prev))
for (s,e) in lines:
    sub = mask[s:e+1]
    cols = np.where(sub.any(axis=0))[0]
    # group cols into glyph clusters (gap>10)
    groups=[]; cs=cols[0]; cp=cols[0]
    for c in cols[1:]:
        if c-cp>9: groups.append((cs,cp)); cs=c
        cp=c
    groups.append((cs,cp))
    print("line y", y0+s, y0+e, "glyph x-ranges:", [(x0+g[0], x0+g[1]) for g in groups])

# colour of x2
sub = rgb[470:500, 1690:1745]
m = (sub.max(axis=2)>90)
cols = sub[m]

# find bluish
blue = cols[(cols[:,2]>cols[:,0]+25)]
print("blue median", np.median(blue,axis=0) if len(blue) else None)
white = rgb[y0:y1, x0:x1][mask]
print("white p95", np.percentile(white,95,axis=0))
EOF
python3 locate.py
```[cite: 1]

```bash
cd /home/claude/work && cat > locate2.py <<'EOF'
from PIL import Image
import numpy as np
im = Image.open('/mnt/user-data/uploads/Billy_NO_Talent*-*Guitar_card_v2__juillet_2026___018*-*The_Wolf.png').convert('RGB')
a = np.array(im).astype(int)
def glyphs(y0,y1,x0,x1,thr=70,gap=2):
    reg=a[y0:y1+1,x0:x1+1].max(axis=2)>thr
    cols=np.where(reg.any(axis=0))[0]
    g=[];s=cols[0];p=cols[0]
    for c in cols[1:]:
        if c-p>gap: g.append((x0+s,x0+p)); s=c
        p=c
    g.append((x0+s,x0+p))
    return g
print("L1", glyphs(450,505,1460,1745))
print("L2", glyphs(520,570,1640,1745))
print("L3", glyphs(600,640,1640,1745))
print("L4", glyphs(670,712,1690,1745))

# crop for viewing
crop = im.crop((1440,430,1780,730)).resize((1020,900), Image.LANCZOS)
crop.save('crop_right.png')
EOF
python3 locate2.py
```[cite: 1]

```bash
cd /home/claude/work && cat > grid.py <<'EOF'
import json, numpy as np
R = json.load(open('refined.json'))
t = np.array(R['refined'])

# beat positions relative to the loud A start (A2 in first pass = beat 0)
b = np.array([0,16,32,48,64,96,128,144,160,176,192,208,240,272,296,328,360,392,424,440], float)
keep = np.ones(len(b), bool)
for _ in range(4):
    p = np.polyfit(b[keep], t[keep], 1)
    res = t - np.polyval(p, b)
    keep = np.abs(res) < 0.25
    print("iter: period %.5f s/beat (%.2f BPM) t0=%.3f excluded:"%(p[0],60/p[0],p[1]), [(int(b[i]),round(float(res[i]),2)) for i in np.where(~keep)[0]])
print("residual std on kept: %.3f s"%res[keep].std())
json.dump(dict(period=float(p[0]), t0=float(p[1])), open('grid.json','w'))
print("start of intro A (beat -16): %.2f s ; end of final A (beat 440): %.2f s"%(p[1]-16*p[0], p[1]+440*p[0]))
EOF
python3 grid.py
```[cite: 1]

### 8. Moteur de rendu, planches de test et encodage (`render.py`, `encode.py`, `region.py`, `seg.sh`)

```bash
cd /home/claude/work && cat > render.py <<'EOF'
import json, sys, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

G = json.load(open('grid.json')); P, T0 = G['period'], G['t0']
def tb(b): return T0 + P*b # beat index -> seconds
DUR = 227.709
AMBER = np.array([255, 176, 56], np.float32)

img = Image.open('/mnt/user-data/uploads/Billy_NO_Talent*-*Guitar_card_v2__juillet_2026___018*-*The_Wolf.png').convert('RGB')
base_full = np.array(img)
X0, Y0, X1, Y1 = 1440, 430, 1780, 730
base = base_full[Y0:Y1, X0:X1].astype(np.float32)

# glyph groups: name -> bbox (x0,x1,y0,y1) in full-image coords
GL = {
    '5A': (1497,1554,452,503),
    'B1a': (1596,1622,452,503), 'B1b': (1625,1652,452,503),
    'C': (1666,1695,524,570), 'Cs': (1695,1742,524,570),
    'B3a': (1655,1682,598,642), 'B3b': (1685,1711,598,642), 'B3c': (1714,1741,598,642),
    'A': (1710,1741,670,714),
}
cov, glow = {}, {}
for k,(x0,x1,y0,y1) in GL.items():
    m = np.zeros(base.shape[:2], np.float32)
    sub = base[y0-Y0:y1-Y0, x0-X0:x1-X0].max(axis=2)
    m[y0-Y0:y1-Y0, x0-X0:x1-X0] = np.clip((sub-25)/230, 0, 1)
    cov[k] = m
    glow[k] = gaussian_filter(m, 5)*1.6 + gaussian_filter(m, 2)*0.5

# timeline: (glyph, start_beat, end_beat, pip or None) -- beat 0 = start of the loud A
seq = []
def add(g, a, n, pip=None, group=None): seq.append(dict(g=g, a=a, b=a+n, pip=pip, grp=group))

# pass 1
for i in range(5): add('5A', -16+16*i, 16, pip=i, group=('pass',0))
add('B1a', 64, 32, group=('pass',0)); add('B1b', 96, 32, group=('pass',0))

# pass 2
for i in range(5): add('5A', 128+16*i, 16, pip=i, group=('pass',1))
add('B1a', 208, 32, group=('pass',1)); add('B1b', 240, 32, group=('pass',1))
add('C', 272, 24); add('Cs', 296, 32)
add('B3a', 328, 32); add('B3b', 360, 32); add('B3c', 392, 32)
add('A', 424, 16)
for s in seq: s['t0'], s['t1'] = tb(s['a']), tb(s['b'])
seq[0]['t0'] = 0.0
END_HOLD, END_FADE = tb(440)+2.6, 1.6

ANN = 1.0 # announcement window before a glyph change (s)
def ease(x): x = min(max(x,0),1); return x*x*(3-2*x)

def weights(t):
    w = {k:0.0 for k in GL}
    for i,s in enumerate(seq):
        g = s['g']
        if s['t0'] <= t < s['t1']:
            w[g] = max(w[g], 1.0)
        # fade-in at very start
        if i == 0: w[g] = min(w[g], ease(t/0.6))
        # glyph-change handling
        nxt = seq[i+1] if i+1 < len(seq) else None
        if nxt and nxt['g'] != g:
            tc = s['t1']
            if tc - ANN <= t < tc: # announce next glyph
                x = (t-(tc-ANN))/ANN
                w[nxt['g']] = max(w[nxt['g']], 0.55*ease(x))
            if tc <= t < tc+0.35: # old glyph releases
                w[g] = max(w[g], 1-ease((t-tc)/0.35))
    # end fade
    if t > END_HOLD:
        f = 1-ease((t-END_HOLD)/END_FADE)
        w = {k:v*f for k,v in w.items()}
    return w

def state(t):
    """pass index (0/1) and current/ finished pip of 5A"""
    cur = None
    for s in seq:
        if s['t0'] <= t < s['t1']: cur = s
    return cur

def draw_pips(reg, cx, cy, n, lit, cur, pulse, active):
    r = 3
    gap = 11
    x_start = cx - gap*(n-1)/2
    yy, xx = np.mgrid[0:reg.shape[0], 0:reg.shape[1]]
    for i in range(n):
        px, py = x_start+gap*i - X0, cy - Y0
        d = np.sqrt((xx-px)**2 + (yy-py)**2)
        a = np.clip(r+0.7-d, 0, 1)[...,None]
        if i < lit: col, lv = AMBER*0.55, 1.0 # already played
        elif i == cur: col, lv = AMBER, 0.55+0.45*pulse # playing
        else: col, lv = np.array([95,95,100],np.float32), 1.0
        if not active and i >= lit and i != cur:
            col = np.array([95,95,100],np.float32)
        reg[:] = reg*(1-a*lv) + col*a*lv

def frame(t):
    reg = base.copy()
    ph = ((t - T0)/P) % 1.0
    pulse = float(np.exp(-4.5*ph))
    w = weights(t)
    for k,v in w.items():
        if v <= 0.002: continue
        reg += v*cov[k][...,None]*(AMBER-255.0)
        reg += (v*(0.55+0.45*pulse))*glow[k][...,None]*AMBER*0.55
    # pips under 5A (5 repetitions) and under x2 (2 passes)
    s = state(t)
    fin = 1.0
    if t > END_HOLD: fin = 1-ease((t-END_HOLD)/END_FADE)
    if s is not None:
        if s['g'] == '5A' or True:
            # 5A pips: show current progress of the active/last 5A block
            pas = s['grp'][1] if s['grp'] else None
            # determine pass and 5A progress
            pas, a5 = None, -1
            for sg in seq:
                if sg['grp'] and sg['t0'] <= t: pas = sg['grp'][1]
                if sg['g']=='5A' and sg['t0'] <= t < sg['t1']: a5 = sg['pip']
            lit5 = 0; cur5 = None
            if s is not None and s['g'] == '5A':
                cur5 = s['pip']; lit5 = s['pip']
            elif pas is not None and t < tb(424):
                lit5 = 5 if (s is None or s['g']!='5A') else lit5
            if t < tb(424) and s is not None and s['g'] == '5A':
                draw_pips(reg, 1525, 512, 5, lit5, cur5, pulse, True)
            elif t < tb(424) and pas is not None:
                draw_pips(reg, 1525, 512, 5, 5, None, pulse, True)
        # x2 pips: pass 1 / pass 2 (pass 2 lit from the second 5A on)
        if pas is not None and t < tb(272):
            draw_pips(reg, 1713, 512, 2, pas, pas, pulse, True)
        elif t >= tb(272) and t < END_HOLD:
            draw_pips(reg, 1713, 512, 2, 2, None, pulse, True)
    return np.clip(reg, 0, 255).astype(np.uint8)

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        times = [float(x) for x in sys.argv[2:]]
        for tt in times:
            f = base_full.copy(); f[Y0:Y1, X0:X1] = frame(tt)
            Image.fromarray(f).crop((1380,420,1800,740)).resize((840,640)).save(f'still_{tt:06.1f}.png')
        print('ok')
EOF
python3 render.py stills 4 38.3 39.5 70.3 139 151 223
python3 -c "
from PIL import Image
ts=['004.0','038.3','039.5','070.3','139.0','151.0','223.0']
ims=[Image.open(f'/home/claude/work/still_{t}.png').resize((420,320)) for t in ts]
W=Image.new('RGB',(420*4,320*2))
for i,im in enumerate(ims): W.paste(im,((i%4)*420,(i//4)*320))
W.save('/home/claude/work/contact.png')
"
```[cite: 1]

```bash
cd /home/claude/work && ls still* && python3 -c "
from PIL import Image, ImageDraw
import glob
fs=sorted(glob.glob('still_*.png'))
ims=[Image.open(f).resize((420,320)) for f in fs]
W=Image.new('RGB',(420*4,320*2))
d=ImageDraw.Draw(W)
for i,(f,im) in enumerate(zip(fs,ims)):
    W.paste(im,((i%4)*420,(i//4)*320)); d.text(((i%4)*420+6,(i//4)*320+4),f[6:-4]+'s',fill=(120,200,255))
W.save('contact.png')
"
```[cite: 1]

```bash
cd /home/claude/work && python3 - <<'EOF'
s = open('render.py').read()
s = s.replace("END_HOLD, END_FADE = tb(440)+2.6, 1.6", "END_HOLD, END_FADE = tb(440)+2.6, 1.6\nseq[-1]['t1'] = END_HOLD")
open('render.py','w').write(s)
EOF

cat > encode.py <<'EOF'
import subprocess, sys, numpy as np, time
import render as R
FPS = 30
N = int(round(R.DUR*FPS))
cmd = ['ffmpeg','-y','-hide_banner','-loglevel','error',
       '-loop','1','-framerate',str(FPS),'-i','/mnt/user-data/uploads/Billy_NO_Talent*-*Guitar_card_v2__juillet_2026___018*-*The_Wolf.png',
       '-f','rawvideo','-pix_fmt','rgb24','-s',f'{R.X1-R.X0}x{R.Y1-R.Y0}','-framerate',str(FPS),'-i','-',
       '-i','/mnt/user-data/uploads/018*-*The_Wolf.mp3',
       '-filter_complex',f'[0:v][1:v]overlay={R.X0}:{R.Y0}:eof_action=pass,format=yuv420p[v]',
       '-map','[v]','-map','2:a:0','-t',f'{R.DUR:.3f}',
       '-c:v','libx264','-preset','veryfast','-crf','17','-tune','stillimage','-r',str(FPS),
       '-c:a','aac','-b:a','256k','-movflags','+faststart','/home/claude/work/the_wolf_guitar_card.mp4']
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
t0=time.time()
try:
    for i in range(N):
        p.stdin.write(R.frame(i/FPS).tobytes())
        if i%300==0: print(f'{i}/{N} {time.time()-t0:.0f}s', flush=True)
    p.stdin.close()
except BrokenPipeError:
    pass
p.wait()
print('done', p.returncode, f'{time.time()-t0:.0f}s', flush=True)
EOF
nohup python3 encode.py > encode.log 2>&1 &
sleep 45; cat encode.log
```[cite: 1]

```bash
cd /home/claude/work && rm -f the_wolf_guitar_card.mp4 && nproc && df -h /home/claude | tail -1 && python3 - <<'EOF'
import time, render as R
t=time.time()
for i in range(60): R.frame(100+i/30)
print("frame() ms:", (time.time()-t)/60*1000)
EOF
```[cite: 1]

```bash
cd /home/claude/work && cat > region.py <<'EOF'
import sys, render as R
FPS=30; N=int(round(R.DUR*FPS))
a,b = int(sys.argv[1]), int(sys.argv[2]); out=sys.argv[3]
with open(out,'wb') as f:
    for i in range(a, min(b,N)):
        f.write(R.frame(i/FPS).tobytes())
print(out, 'frames', a, min(b,N))
EOF
python3 region.py 0 3500 reg_a.rgb && ls -la reg_a.rgb
python3 region.py 3500 7000 reg_b.rgb && ls -la reg_*.rgb
```[cite: 1]

```bash
cd /home/claude/work && cat reg_a.rgb reg_b.rgb > reg_all.rgb && rm reg_a.rgb reg_b.rgb && ls -la reg_all.rgb && cat > seg.sh <<'EOF'
#!/bin/bash
# usage: seg.sh index start_frame count
cd /home/claude/work
i=$1; s=$2; c=$3
dd if=reg_all.rgb bs=306000 skip=$s count=$c status=none | ffmpeg -y -hide_banner -loglevel error \
  -loop 1 -framerate 30 -i "/mnt/user-data/uploads/Billy_NO_Talent*-*Guitar_card_v2__juillet_2026___018*-*The_Wolf.png" \
  -f rawvideo -pix_fmt rgb24 -s 340x300 -framerate 30 -i - \
  -filter_complex "[0:v]format=yuv420p[bg];[1:v]format=yuv420p[fg];[bg][fg]overlay=1440:430:eof_action=endall:format=yuv420" \
  -frames:v $c -c:v libx264 -preset veryfast -crf 17 -tune stillimage -r 30 -g 60 -pix_fmt yuv420p seg_$(printf %02d $i).mp4
EOF
chmod +x seg.sh && s=$(date +%s) && ./seg.sh 0 0 600 && echo "took $(( $(date +%s)-s ))s" && ls -la seg_00.mp4
```[cite: 1]

```bash
cd /home/claude/work && rm -f seg*.mp4 && ./seg.sh 0 0 1500 && ./seg.sh 1 1500 1500 && ./seg.sh 2 3000 1500 && ls -la seg*.mp4
cd /home/claude/work && ./seg.sh 3 4500 1500 && ./seg.sh 4 6000 831 && ls -la seg*.mp4 && for f in seg*0*.mp4; do echo "file '$PWD/$f'"; done > list.txt && ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i list.txt -i /mnt/user-data/uploads/018*-*The_Wolf.mp3 -map 0:v -map 1:a:0 -c:v copy -c:a aac -b:a 256k -t 227.709 -movflags +faststart the_wolf_guitar_card.mp4 && ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,nb_frames -of default=nw=1 the_wolf_guitar_card.mp4
```[cite: 1]

```bash
cd /home/claude/work && rm -f chk*.png && for t in 38.7 39.5 70.5 139.9 152.0 167.0 213.6 222.5 226.5; do ffmpeg -y -hide_banner -loglevel error -ss $t -i the_wolf_guitar_card.mp4 -frames:v 1 chk_$t.png; done && python3 -c "
from PIL import Image, ImageDraw
import glob
fs=sorted(glob.glob('chk_*.png'), key=lambda f: float(f[4:-4]))
W=Image.new('RGB',(380*5,300*2))
d=ImageDraw.Draw(W)
for i,f in enumerate(fs):
    im=Image.open(f).crop((1440,430,1780,730)).resize((380,335)).crop((0,0,380,300))
    W.paste(im,((i%5)*380,(i//5)*300)); d.text(((i%5)*380+6,(i//5)*300+4),f[4:-4]+' s',fill=(120,200,255))
W.save('final_check.png')
"
```[cite: 1]

```bash
mkdir -p /mnt/user-data/outputs && cp /home/claude/work/the_wolf_guitar_card.mp4 /mnt/user-data/outputs/The_Wolf_guitar_card_animee.mp4 && ls -la /mnt/user-data/outputs/
```[cite: 1]
````



***

# Analyse critique et pistes d'amélioration

L'approche de Claude a abouti à un résultat fonctionnel et visuellement soigné, mais elle présente plusieurs fragilités méthodologiques, techniques et de performance, pour passer ce processus en tant qu'application desktop cross-platform.

## Exactitude musicale et méthodologie d'analyse

* **Hypothèse de tempo constant vs réalité musicale** : la régression linéaire sur l'ensemble du morceau suppose une pulsation rigoureusement constante (`124,09 BPM`) et a dû exclure deux points (`beats 96` et `128`) avec des écarts de `-0,35 s` et `+0,46 s`. Sur des morceaux enregistrés en groupe (batterie acoustique, variations de *groove* ou *ritardando* de fin), un modèle global peut dériver légèrement.

*Piste d'amélioration* : utiliser un suivi de tempo local / *beat tracking* adaptatif ou une grille ancrée sur des **marqueurs/timestamps validés par l'utilisateur** (interpolation linéaire par sections entre points d'ancrage).

* **Dépendance aux chromagrammes bruts sur un mix polyphonique** : voix, basse, cymbales et guitares saturées polluent `chroma_cqt`, ce qui explique l'incertitude explicite de Claude sur la frontière `C` / `C#` (`24` premiers temps identiques + `8` temps ajoutés) et la nécessité de choisir manuellement des gabarits `A` et `B`.

*Piste d'amélioration* : intégrer une séparation de sources (*source separation* via Demucs / HTDemucs en local ou optionnel) pour isoler la guitare ou les harmoniques avant l'analyse, et combiner similarité chromatique, enveloppe énergétique et reconnaissance de motifs par **DTW (*****Dynamic Time Warping*****)** ou **matrice de récurrence / clustering de segments** plutôt qu'une corrélation glissante rigide.

* **Prise en compte incomplète de la grammaire des Guitar Cards** : dans l'exemple traité, Claude a codé en dur la structure de *The Wolf* (`5A`, `BB`, `C`, `C#`, `BBB`, `A` et les positions des pips `5A` / `x2`). Or, la notation Guitar Card comporte une syntaxe riche (variantes `A#`, `A~`, minuscules d'intensité `aA`, arpèges `¦4`, barrés `|4`, répétitions `{ ... } x N`, ou répétitions de riffs variables selon les morceaux).

*Piste d'amélioration* : concevoir un **parseur structuré de Guitar Card** (JSON/YAML ou DSL léger) qui décompose la partition en *événements temporels* (motif, répétition `k/N`, passe `p/M`, variante/annotation) et génère dynamiquement la timeline et les compteurs visuels.

## Qualité visuelle et maintenabilité du rendu

* **Détection des zones de texte heuristique et coordonnées codées en dur** : `locate.py` / `locate2.py` ont servi à repérer des plages de pixels puis `GL` a été renseigné manuellement avec des rectangles fixes (`1440..1780`, `430..730`) et des positions de pips figées (`(1525, 512)` et `(1713, 512)`). Sur une autre Guitar Card (autre police, autre mise en page, autre nombre de lignes ou présence de `¦4` / `|4`), ces coordonnées échoueront.

*Piste d'amélioration* : proposer un **éditeur visuel interactif** dans l'application (cliquer/tracer les zones de chaque motif et des compteurs directement sur l'image de la carte, avec aperçu instantané de la couleur, du halo et des pips) complété par une détection automatique de composantes connexes comme point de départ.

* **Rendu pixel-by-pixel en Python pur** : dans `render.py`, `draw_pips` recalcule `np.mgrid` à chaque appel et `frame()` tourne en ~25 ms/image sur un seul cœur, sans parallélisation.

*Piste d'amélioration* : précalculer les masques, gradients et courbes d'animation (ou utiliser des opérations vectorisées / shaders / OpenCV / Pillow optimisé + multiprocessing ou encodage GPU NVENC quand disponible).

## Performance et fiabilité de l'encodage

* **Découpage manuel en fichiers RGB bruts de 2 Go** : l'écriture de `reg_all.rgb` (~2,09 Go) sur disque et le découpage par `dd` + `seg.sh` puis concaténation ont été imposés par le timeout de 300 s et le monocœur de l'environnement sandbox.

*Amélioration* : dans une application desktop locale, utiliser un **pipeline streaming direct** (`subprocess` pipe vers `ffmpeg` avec gestion propre de la progression, annulation et reprise) ou un rendu par segments en mémoire/temp géré proprement, avec détection automatique des encodeurs matériels (`h264_nvenc`, `h264_videotoolbox` sur macOS) et repli sur `libx264`.