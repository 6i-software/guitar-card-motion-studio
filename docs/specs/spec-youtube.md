# Spécification — Fonctionnalités YouTube

> **Contexte** : `core/youtube/`, `ui/` (écran *Export*)
> **Rôle** : Générer le bloc de description YouTube prêts à copier-coller d'un projet Guitar Card synchronisé.

---

## 1. Sources de données d'entrée

La génération s'appuie sur les données du projet (`Project`) et de sa timeline :
- **Métadonnées** : titre, description existante, auteur/chaîne, album ou contexte éventuel.
- **Séquence & occurrences** : texte brut de la Guitar Card (`card_text`), structure des groupes/répétitions et liste des occurrences/événements horodatés (`start`, `end`, `motif_key`, `repetition_index`, `repetition_total`).
- **Durée totale** : durée de référence du morceau/projet en secondes (`float` à la milliseconde).

---

## 2. Générateur de description vidéo Youtube

**Bloc de description prêt à copier-coller** :
  - Texte assemblant présentation du morceau/projet, Guitar Card (version lisible/réduite ou développée selon la spec) et éventuels liens/crédits.
  - Copie en un clic dans le presse-papiers et sauvegarde en fichier texte dans ./build/youtube-description.txt.

Exemple de template de description de vidéo Youtube

```text
🎸 Want to memorize a [AUTHOR] song on guitar? Try this Guitar card!🎸

You know the feeling: you practice song after song, memorize dozens of guitar tabs, but the moment you play with a band or in front of friends... total blank. Your mind goes completely empty when trying to remember the exact structure. Because we’ve all been there, and let’s be honest, we’re all a little lazy sometimes 😉, we’ve created the ultimate method to lock any song into your brain with minimal effort: guitar card!

The concept is simple: each letter represents a specific riff. « For the intro, play pattern A twice, then pattern B four times », written simply as 2A 4B. It’s concise, visual, and incredibly effective. To add dynamics and variations, we also include key symbols.

In short:
A capital letter (A, B, C...) = A specific riff
A symbol attached (A#, A~) = A melodic and/or rhythmic variation of that riff
In lowercase (aA) = A dynamic/intensity variation (*pianissimo*) of the pattern
The ¦4 symbol = An arpeggio on the 4th fret
The |4 symbol = A bar chord on the 4th fret
...and many more! It’s ultra-flexible, designed to capture the exact feel and intent of any song.

━━━

🎸Ca te dit mémoriser un morceau de [AUHTOR] à la guitare ?🎸

Vous connaissez ce problème ? Vous enchaînez les morceaux, vous apprenez des dizaines de lignes de tablatures, et au moment de jouer en groupe ou devant des amis... trou noir. Impossible de se souvenir de la structure exacte du morceau. Parce qu'on est tous passés par là, et qu'on est aussi un poil fainéants 😉, on a créé une méthode ultime pour graver n'importe quel morceau dans sa mémoire avec peu d'effort : guitar card !

Le principe est simple, une lettre désigne un riff à jouer. « Pour l'introduction, tu joues deux fois le motif A, puis quatre fois le motif B » — soit 2A 4B. Concis, visuel, et redoutablement efficace. Puis pour ajouter du relief et des variations, on ajoute aussi des symboles clés.

En bref :
Une lettre (A, B, C...) = pour un motif précis
Avec un symbole (A#, A~) = pour une variante mélodique et/ou rythmique du motif
En minuscule (aA) = pour une variante d'intensité (*pianissimo*) du motif
Le symbole ¦4 pour un arpège et |4 pour un barré sur la 4ième frète
Et plein d'autres ! C'est ultra-flexible pour (essayer honnêtement) de capturer l'intention exacte du morceau.

━━━

[AUTHOR] - [TITLE] Guitar card
[GUITAR_CARD_TEXT]

In startiflette, we trust ^^..
```
