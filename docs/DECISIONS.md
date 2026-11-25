# Décisions — Guitar Card AI-Motion Studio

> **Règle :** append-only. Une décision adoptée ne se réécrit pas ; elle se supersède par une nouvelle décision.
> **Statuts :** `Proposé` | `Adopté` | `Superseded`.

---

## #D1 — Lecture de `aA` comme deux tokens distincts (2026-11-23 13:11)
- **Statut :** Adopté (clôt `#Q1`)
- **Contexte :** SPEC.md 6. Grammaire Guitar Card
- **Description :** Des séquences mêlant minuscules et majuscules sur une même lettre ou un même motif (ex. `aA`, `bB`, `cC`, `DDdD`, `eeEeE`) pourraient prêter à confusion entre des tokens successifs (variantes d'intensité / répétitions) et d'éventuels tokens composés ou noms de motifs.
- **Décision :** Toujours découper ces séquences en tokens indépendants selon les règles standards de la grammaire (lettre/variante d'intensité, modificateurs, multiplicateurs), sans règle spéciale de casse croisée ni regroupement implicite. Exemple toujours découper `aA` en deux tokens indépendants (`a` puis `A`), sans règle spéciale de casse croisée.
- **Conséquences :** Règle uniforme et prévisible dans le lexer et les tests `hypothesis` ; si un passage progressif d'intensité est souhaité plus tard, il s'écrira explicitement ou fera l'objet d'une nouvelle décision.
- **Alternatives écartées :** Token composé `aA` (ajoute une exception de grammaire et un sens musical non encore stabilisé).

---

## #D2 — Cadre de développement agentique (2026-11-25)
- **Statut :** Proposé
- **Contexte :** Le projet doit être développé par plusieurs agents IA en parallèle, avec des itérations de features et de correctifs, et des comptes rendus d'exécution traçables.
- **Décision proposée :**
  1. Adopter un modèle **orchestrateur + subagents spécialisés** (spec, core, audio, render, UI, QA, reviewer, intégrateur).
  2. Utiliser des **task cards** (`docs/plan/tasks/`) avec `files_owned`, dépendances, critères d'acceptation et Definition of Done.
  3. Appliquer un **WIP limit** de 3 implémenteurs + 1 QA + 1 reviewer.
  4. Exiger un **rapport d'exécution** par tâche et un **rapport de vague** (`docs/reports/`).
  5. Geler les **contrats** entre domaines avant le travail parallèle (`docs/contracts/`).
  6. Appliquer les **gates G0–G5** (`docs/agents/QUALITY_GATES.md`).
  7. Réserver les écritures Git à l'intégrateur ; pas de push/tag sans validation humaine.
- **Conséquences :** Plus de discipline documentaire, mais moins de conflits, plus de traçabilité et des revues indépendantes. Coût : task cards et rapports à maintenir.
- **Alternatives écartées :**
  - Agents qui travaillent directement sur `main` : conflits et perte de traçabilité.
  - Un seul agent séquentiel : plus simple, mais ne exploite pas le parallélisme.
  - Specs lues intégralement à chaque session : coût de contexte et dérive.

---

## #D3 — `AGENTS.md` v2 : constitution courte + playbook (2026-11-25)
- **Statut :** Proposé
- **Contexte :** La v1 de `AGENTS.md` (13,6 Ko) mélange vision, architecture, roadmap, conventions et workflow. Elle est longue à charger et contient des points devenus obsolètes.
- **Décision proposée :**
  - `AGENTS.md` devient une **constitution courte** (~200 lignes) : mission, invariants, architecture, commandes, cycle de tâche, parallélisme, gates, escalade, rôles, routage documentaire.
  - Le détail opératoire est déplacé dans `docs/agents/PLAYBOOK.md`, `ROLES.md`, `OWNERSHIP.md`, `QUALITY_GATES.md`, `REPORTING.md`.
  - La v1 est supersédée ; elle n'a pas été conservée dans ce dépôt (aucun historique antérieur au bootstrap).
- **Conséquences :** Contexte plus léger, règles plus faciles à faire respecter, mais une lecture supplémentaire pour les détails.
- **Alternatives écartées :** Conserver un fichier unique géant (coût de contexte, duplication, dérive).

---

## #D4 — Un seul écrivain par fichier et rapports immuables (2026-11-25)
- **Statut :** Proposé
- **Contexte :** Les agents parallèles partagent le même arbre de travail ; les fichiers partagés (`BOARD.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`, `CHANGELOG.md`) sont des points de conflit.
- **Décision proposée :**
  - Chaque fichier a un propriétaire unique (`docs/agents/OWNERSHIP.md`).
  - Les fichiers partagés sont écrits par un seul rôle (orchestrateur, spec-analyst, intégrateur).
  - Les rapports et décisions sont **append-only** ; une correction se fait par addendum daté.
  - Les agents qui veulent modifier un fichier partagé formulent une proposition dans leur rapport.
- **Conséquences :** Moins de conflits, historique auditable ; les agents doivent accepter de ne pas tout écrire eux-mêmes.
- **Alternatives écartées :** Merge concurrent des mêmes fichiers (conflits fréquents, historique illisible).

---

## #D5 — Questions ouvertes : statuts, priorités et escalade (2026-11-25)
- **Statut :** Proposé
- **Contexte :** `OPEN_QUESTIONS.md` ne définit ni priorité, ni propriétaire, ni critère de blocage.
- **Décision proposée :**
  - Chaque question a un ID `Q*`, un statut (`Ouvert | Bloquant | Résolu`), une priorité (`P0 | P1 | P2`), un contexte, des options, une recommandation et un impact.
  - Une question `P0` bloque la tâche qui en dépend ; une `P1` bloque le milestone ; une `P2` est traitée plus tard.
  - Un agent ne devine jamais : il consigne la question et escalade.
- **Conséquences :** Les blocages sont visibles et arbitrables ; le coût est un peu de rédaction.
- **Alternatives écartées :** Questions en vrac dans les rapports (perte de trace, doublons).

---

## #D6 — Git local, MR obligatoire, push différé (2026-11-25)
- **Statut :** Adopté (partie « local / push différé » supersédée par `D13`)
- **Contexte :** Le dépôt n'a pas encore de remote ; GitHub ou GitLab n'est pas tranché. L'utilisateur veut des commits, mais refuse les commits directs sur `main` et veut pousser uniquement du code testé.
- **Décision :**
  1. Travail **100 % local** pour l'instant ; aucun `push`, aucun `tag`.
  2. **Une tâche = une branche `task/<ID>-<slug>`** ; jamais de commit direct sur `main` (exception : commit bootstrap initial).
  3. **MR obligatoire** : la branche est mergée seulement après review approuvée, avec `git merge --no-ff`.
  4. Sans remote, la MR est matérialisée par la branche + le rapport `docs/reports/reviews/RV-*.md` + le commit de merge.
  5. Quand un remote existera, la même branche sera poussée et une MR/PR sera ouverte avec le rapport comme description.
  6. Seul l'intégrateur écrit dans Git ; l'humain autorise push, tag et réécriture d'historique.
- **Conséquences :** Historique propre, review traçable, publication différée sans rework.
- **Alternatives écartées :** Commits directs sur `main` (perte de traçabilité) ; travail sans branche (impossible à reviewer).

---

## #D7 — Dépendances v1 : `pytest-cov` uniquement (2026-11-25)
- **Statut :** Adopté (clause 2 « pas de matplotlib » supersédée par `D11`)
- **Contexte :** `matplotlib` (graphes de rapport audio) et `scikit-learn` (clustering sync) étaient envisagés ; `pytest-cov` manquait pour mesurer la couverture.
- **Décision :**
  1. Ajouter **`pytest-cov`** dans le groupe dev (`uv add --dev pytest-cov`).
  2. **Ne pas ajouter `matplotlib`** en v1 : rapports audio en JSON/Markdown, graphiques éventuellement en SVG/Pillow ou dans une itération ultérieure.
  3. **Ne pas ajouter `scikit-learn`** : le clustering utilise `scipy`/`numpy`.
  4. Seuil de couverture pragmatique sur les modules purs (`grammar`, `model`, `sync`, `render`), pas d'objectif sur `ui/` ni sur le code d'orchestration.
- **Conséquences :** Arbre de dépendances plus léger, build plus rapide ; pas de visualisation graphique en v1.
- **Alternatives écartées :** `matplotlib` immédiatement (poids et dépendances GUI) ; `scikit-learn` (dépendance lourde pour un besoin couvert par scipy).

---

## #D8 — Exemples protégés hors Git, fixtures synthétiques (2026-11-25)
- **Statut :** Adopté
- **Contexte :** `docs/examples` contient 24 MP3 et des PNG d'artwork protégés ; le dépôt n'a aucun commit.
- **Décision :** Les MP3/PNG réels restent **hors Git** (`.gitignore`). La CI et les tests utilisent des **fixtures synthétiques** dans `tests/fixtures/`. Git LFS n'est pas utilisé.
- **Conséquences :** Dépôt léger et légal ; les tests ne dépendent pas des œuvres ; les démos locales utilisent les fichiers présents sur la machine.
- **Alternatives écartées :** Git LFS (autorisation et licence à gérer) ; commit des œuvres (risque juridique).

---

## #D9 — Description YouTube (2026-11-25)
- **Statut :** Adopté
- **Contexte :** `spec-youtube.md` prévoyait `./build/youtube-description.txt`, ce qui viole I2 (écritures limitées à config/projet/export).
- **Décision :** Par défaut, écrire `output/description-youtube.txt` dans le dossier du projet. L'utilisateur peut choisir un autre dossier de sortie. Le contenu reste aussi copiable dans le presse-papiers.
- **Conséquences :** Conforme à I2, prévisible, testable.
- **Alternatives écartées :** `./build` (hors périmètre) ; presse-papiers uniquement (pas de trace).

---

## #D10 — Multiplicateurs et variantes (2026-11-25)
- **Statut :** Adopté
- **Contexte :** La grammaire autorisait `NA`, `AxN` et `A#`/`A~`, mais ne tranchait ni les doublons de modificateurs ni la priorité des formes.
- **Décision :**
  1. **`x<INT>` est toujours un multiplicateur** : `Punkx2` = `Punk x2` = `Punk` joué 2 fois.
  2. **Le compteur préfixe est un multiplicateur** : `2Punk` = `Punkx2` ; `3A` = `AAA`.
  3. **Les accolades servent aux séquences** : `{CACA 2B}x2` est la forme préférée. `2{AA}` est accepté mais **déconseillé** (diagnostic `info`) : préférer `4A` ou `{AA}x2`.
  4. **Les modificateurs se cumulent** : `A#` = variante de `A`, `A##` = variante de la variante. `A#~` combine variante mélodique et rythmique.
  5. **Pour plusieurs variantes, préférer l'exposant** : `A^1`, `A^2`, `A^3` plutôt que `A#`, `A##`, `A###`.
- **Points à préciser :** `Punk2` sans `x` (nom ou répétition ?) → `Q4` ; correspondance exacte `A^n` ↔ `#`/`~` → `Q35`.
- **Conséquences :** Règles simples et prévisibles ; le lexer doit produire un token multiplicateur unique et le parser appliquer la priorité.
- **Alternatives écartées :** Réserver `x<INT>` aux motifs nommés (ambigu) ; interdire les doublons de modificateurs (limite la notation).

---

## #D11 — Rapports graphiques : `matplotlib` (2026-11-25)
- **Statut :** Adopté
- **Supersède :** la clause 2 de `D7` (pas de `matplotlib` en v1).
- **Contexte :** `D7` avait écarté `matplotlib` pour alléger les dépendances. L'utilisateur veut finalement des rapports audio avec graphiques (forme d'onde, onsets, chroma, SSM, confiance). Comparaison demandée : matplotlib, seaborn, plotnine, plotly, bokeh, altair, pyqtgraph.
- **Comparaison :**

| Solution | Force | Coût | Verdict |
|---|---|---|---|
| `matplotlib` 3.11.2 | Standard, statique PNG/SVG, offline, numpy, backend Agg | ~9,3 Mo + 8 dépendances légères | **Retenu** |
| `seaborn` 0.13.2 | Statistiques, jolis défauts | Ajoute `pandas` | Non |
| `plotnine` 0.15.9 | Grammar of graphics | Ajoute `pandas`, `statsmodels`, `mizani` | Non |
| `plotly` 7.2.0 | Interactif HTML | Runtime JS, `kaleido` pour le statique | Non |
| `bokeh` 3.10.2 | Interactif | `tornado`, `pandas`, serveur | Non |
| `altair` 6.3.0 | Déclaratif | `vl-convert` (binaire) pour le statique | Non |
| `pyqtgraph` 0.14.0 | Temps réel Qt, léger | Pas adapté aux rapports statiques | Complément possible plus tard |
| `Pillow` | Déjà présent | Dessin manuel, limité | Insuffisant seul |

- **Décision :** ajouter **`matplotlib`** aux dépendances runtime. Utiliser le backend **Agg** dans un worker (jamais le thread UI), générer **SVG + PNG** dans le dossier de rapport du projet. Pas de `seaborn`, `plotnine`, `plotly`, `bokeh`, `altair` en v1. `pyqtgraph` reste une option pour la timeline interactive, à décider séparément.
- **Conséquences :** Rapports lisibles et reproductibles, hors ligne. Poids supplémentaire acceptable dans un bundle qui embarque déjà PySide6 et PyTorch.
- **Alternatives écartées :** `seaborn`/`plotnine` (pandas + statsmodels pour des courbes audio), `plotly`/`bokeh` (JS/serveur), `altair` (binaire vl-convert).

---

## #D12 — Motifs, variantes et zones : clés distinctes + famille (2026-11-25)
- **Statut :** Adopté
- **Contexte :** La spec traite `a` comme une « variante d'intensité » de `A`. L'utilisateur précise que `a` est un **riff distinct** (joué moins fort, parfois une mesure en moins), presque similaire à `A`. Exemple : `aaAA` = `a` deux fois puis `A` deux fois.
- **Décision :**
  1. `a` est un **motif à part entière** : `motif_key = "a"`, avec `family_key = "A"`.
  2. Les variantes `A#`, `A^2`, `A^3` ont leur **propre `motif_key`** et leur **propre zone**, avec `family_key = "A"`.
  3. `ZoneRegion` est indexé par `motif_key`. Si la carte dessine `a` dans la même case que `A`, l'utilisateur peut mapper les deux clés sur le même rectangle (override manuel).
  4. La famille permet de regrouper visuellement `a`, `A`, `A#`, `A^2` et de calculer des transitions, sans les confondre.
  5. L'animation peut différer par clé (intensité, durée, style) tout en partageant la famille.
- **Conséquences :** Modèle plus riche (`family_key`), zones par graphie, UI de regroupement. Évite de perdre la distinction `a`/`A` et permet `aaAA`.
- **Alternatives écartées :** Fusionner `a` dans `A` (perte de la distinction rythmique) ; clés indépendantes sans famille (impossible de les rapprocher).

---

## #D13 — GitHub, branches et pull requests (2026-11-25)
- **Statut :** Adopté (supersède la partie « local only » de `D6`)
- **Contexte :** Le dépôt distant vide existe : `https://github.com/6i-software/guitar-card-motion-studio`. L'utilisateur veut des merge requests dès maintenant.
- **Décision :**
  1. `origin` pointe sur le dépôt GitHub.
  2. `main` est protégée par convention : **aucun commit direct**.
  3. Chaque tâche = branche `task/T-XXXX-slug`, poussée sur `origin`, puis **pull request** vers `main`.
  4. Review obligatoire (`docs/reports/reviews/RV-*.md`) avant merge. Le merge se fait via la PR (humain ou intégrateur autorisé).
  5. L'intégrateur peut pousser les branches de tâche et créer les PR ; il ne pousse jamais `main` directement, ne force pas, ne tague pas.
  6. Les tags et releases restent soumis à validation humaine.
  7. Le commit bootstrap initial sur `main` reste l'unique exception.
- **Conséquences :** Historique linéaire et reviewable, CI GitHub possible plus tard.
- **Alternatives écartées :** Continuer en local (pas de MR) ; commits directs sur `main` (perte de review).

---

## #D14 — Langue et conventions de commit (2026-11-25)
- **Statut :** Adopté
- **Contexte :** Le projet est francophone, mais le code et l'historique Git doivent rester lisibles par tous les agents et outils.
- **Décision :**
  1. **Français** : tout `docs/**/*.md`, ainsi que `README.md` et `CHANGELOG.md`.
  2. **Anglais** : code source, identifiants, noms de fichiers, commentaires, docstrings, noms de tests, messages de commit.
  3. **UI** : chaînes visibles en français par défaut via l'i18n ; les clés et identifiants de code restent en anglais.
  4. **Commits** : gitmoji obligatoire + Conventional Commits, message en anglais, impératif, scope court, footer `Refs: T-XXXX`. Référence : `docs/agents/COMMITS.md`.
- **Conséquences :** Historique homogène, code standard, documentation produit en français.
- **Alternatives écartées :** Tout en français (moins lisible pour les outils) ; tout en anglais (perte de la documentation produit francophone).

---

## #D15 — Noms de motifs, variantes et exposants (2026-11-25)
- **Statut :** Adopté
- **Contexte :** `Q4`, `Q6` et `Q35` restaient ouverts après `D10`. L'utilisateur a précisé que `Punk2` est un nom de motif joué une seule fois, et que `A^2` désigne la deuxième variation de `A`.
- **Décision :**
  1. **Sans `x`, une suite de chiffres collée à un motif nommé fait partie du nom.** `Punk2`, `Solo1`, `Solo2` sont des noms ; chaque occurrence est jouée une fois. Exemple : `A Solo1 AA Solo2` = `A` une fois, `Solo1` une fois, `A` deux fois, `Solo2` une fois.
  2. **Une répétition s'écrit explicitement** : `2Punk`, `Punkx2`, `Punk x2`, `AA`, `3A`.
  3. **Un chiffre collé à un motif d'une seule lettre (`A2`) est ambigu** : diagnostic `error` `GC-GRAM-008`, aucune occurrence pour le `2` ; suggestion `2A` ou `Ax2`.
  4. **`A^n` est la forme canonique des variantes** : `A^1` = première variante (équivalent à `A#`), `A^2` = deuxième variante (préféré à `A##`), `A^3` (préféré à `A###`). L'AST normalise `#` en exposant.
  5. **`~` est un modificateur rythmique orthogonal** : `A~` et `A^2~` sont valides ; `A~^2` est refusé (`warning` `GC-GRAM-009`) car l'exposant porte déjà le niveau de variante.
  6. **Clés** : `motif_key` = graphie canonique (`A`, `a`, `A^1`, `A^2`, `A^2~`, `Punk2`, `|4`) ; `family_key` = motif de base (`A` pour `a`, `A^1`, `A^2` ; `Punk2` pour lui-même).
- **Conséquences :** Le lexer distingue nom, multiplicateur et exposant ; le parser normalise `#`/`##` ; le modèle peut regrouper les variantes sans les confondre.
- **Alternatives écartées :** Traiter `Punk2` comme `Punk` × 2 (ambigu avec `Solo1`) ; fusionner `a` dans `A` (perte de la distinction de riff) ; combiner `~` et `^n` (notation trop complexe).
